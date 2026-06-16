import { useEffect, useState, useRef, FormEvent } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Send, Loader2, MessageSquare, ArrowLeft } from 'lucide-react'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'
import { Message, Profile } from '../lib/types'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Card } from '../components/ui/card'
import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar'
import { cn, getInitials, formatRelativeTime } from '../lib/utils'

interface Conversation {
  other: Profile
  last_message: Message
  unread_count: number
}

export default function Messages() {
  const { userId } = useParams<{ userId?: string }>()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeConversation, setActiveConversation] = useState<Profile | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [newMessage, setNewMessage] = useState('')
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => { void fetchConversations() }, [user])

  useEffect(() => {
    if (userId) {
      void loadConversation(userId)
    }
  }, [userId])

  useEffect(() => {
    if (!activeConversation || !user) return

    void fetchMessages(activeConversation.id)

    // Marcar mensagens recebidas como lidas
    void supabase
      .from('messages')
      .update({ is_read: true })
      .eq('sender_id', activeConversation.id)
      .eq('receiver_id', user.id)
      .eq('is_read', false)

    const channel = supabase
      .channel(`messages:${user.id}:${activeConversation.id}`)
      .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'messages',
        filter: `or(and(sender_id.eq.${user.id},receiver_id.eq.${activeConversation.id}),and(sender_id.eq.${activeConversation.id},receiver_id.eq.${user.id}))`,
      }, (payload) => {
        const msg = payload.new as Message
        setMessages((prev) => {
          if (prev.find((m) => m.id === msg.id)) return prev
          return [...prev, msg]
        })
      })
      .subscribe()

    return () => { void supabase.removeChannel(channel) }
  }, [activeConversation])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const fetchConversations = async () => {
    setLoading(true)
    try {
      const { data, error } = await supabase
        .from('messages')
        .select('*')
        .or(`sender_id.eq.${user!.id},receiver_id.eq.${user!.id}`)
        .order('created_at', { ascending: false })

      if (error) throw error

      // Agrupar por outro usuário
      const grouped = new Map<string, Message>()
      ;((data as Message[]) || []).forEach((msg) => {
        const otherId = msg.sender_id === user!.id ? msg.receiver_id : msg.sender_id
        if (!grouped.has(otherId)) grouped.set(otherId, msg)
      })

      const otherIds = Array.from(grouped.keys())
      if (otherIds.length === 0) {
        setConversations([])
        return
      }

      const { data: profilesData } = await supabase
        .from('profiles')
        .select('*')
        .in('id', otherIds)

      const convs: Conversation[] = (profilesData || []).map((p) => ({
        other: p,
        last_message: grouped.get(p.id)!,
        unread_count: 0,
      }))

      // Contar não lidas
      for (const conv of convs) {
        const { count } = await supabase
          .from('messages')
          .select('*', { count: 'exact', head: true })
          .eq('sender_id', conv.other.id)
          .eq('receiver_id', user!.id)
          .eq('is_read', false)
        conv.unread_count = count || 0
      }

      convs.sort((a, b) =>
        new Date(b.last_message.created_at).getTime() -
        new Date(a.last_message.created_at).getTime()
      )
      setConversations(convs)
    } catch (err) {
      console.error('Erro ao buscar conversas:', err)
    } finally {
      setLoading(false)
    }
  }

  const loadConversation = async (otherUserId: string) => {
    try {
      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', otherUserId)
        .maybeSingle()

      if (error) throw error
      if (data) setActiveConversation(data)
    } catch (err) {
      console.error('Erro ao carregar conversa:', err)
    }
  }

  const fetchMessages = async (otherUserId: string) => {
    try {
      const { data, error } = await supabase
        .from('messages')
        .select('*')
        .or(`and(sender_id.eq.${user!.id},receiver_id.eq.${otherUserId}),and(sender_id.eq.${otherUserId},receiver_id.eq.${user!.id})`)
        .order('created_at', { ascending: true })

      if (error) throw error
      setMessages(data || [])
    } catch (err) {
      console.error('Erro ao buscar mensagens:', err)
    }
  }

  const sendMessage = async (e: FormEvent) => {
    e.preventDefault()
    const text = newMessage.trim()
    if (!text || !activeConversation || sending) return
    setSending(true)
    try {
      const { error } = await supabase.from('messages').insert({
        sender_id: user!.id,
        receiver_id: activeConversation.id,
        content: text,
        is_read: false,
      })
      if (error) throw error
      setNewMessage('')
      // Atualiza lista de conversas após enviar
      void fetchConversations()
    } catch (err) {
      console.error('Erro ao enviar mensagem:', err)
      alert('Não foi possível enviar a mensagem.')
    } finally {
      setSending(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    )
  }

  return (
    <Card className="overflow-hidden h-[calc(100vh-10rem)]">
      <div className="grid h-full md:grid-cols-[280px_1fr]">
        {/* Lista de conversas */}
        <div className={cn(
          "border-r overflow-y-auto bg-muted/20",
          activeConversation && "hidden md:block"
        )}>
          <div className="p-4 border-b font-semibold bg-background sticky top-0 z-10">
            Mensagens
          </div>
          {conversations.length === 0 ? (
            <div className="p-8 text-center text-sm text-muted-foreground space-y-2">
              <MessageSquare className="h-10 w-10 mx-auto opacity-40" />
              <p>Nenhuma conversa ainda</p>
              <p className="text-xs">
                Visite o perfil de alguém e clique em "Mensagem" para começar.
              </p>
            </div>
          ) : (
            <ul>
              {conversations.map((conv) => (
                <li key={conv.other.id}>
                  <button
                    onClick={() => {
                      setActiveConversation(conv.other)
                      navigate(`/messages/${conv.other.id}`, { replace: true })
                    }}
                    className={cn(
                      "w-full p-3 flex items-center gap-3 hover:bg-muted transition-colors text-left border-b",
                      activeConversation?.id === conv.other.id && "bg-muted"
                    )}
                  >
                    <Avatar className="h-10 w-10 flex-shrink-0">
                      <AvatarImage src={conv.other.avatar_url || undefined} />
                      <AvatarFallback className="text-xs">
                        {getInitials(conv.other.full_name || conv.other.username)}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-2">
                        <p className="font-medium text-sm truncate">
                          {conv.other.full_name || conv.other.username}
                        </p>
                        <span className="text-xs text-muted-foreground flex-shrink-0">
                          {formatRelativeTime(conv.last_message.created_at)}
                        </span>
                      </div>
                      <p className={cn(
                        "text-xs truncate",
                        conv.unread_count > 0 ? "text-foreground font-semibold" : "text-muted-foreground"
                      )}>
                        {conv.last_message.sender_id === user!.id && "Você: "}
                        {conv.last_message.content}
                      </p>
                    </div>
                    {conv.unread_count > 0 && (
                      <span className="bg-primary text-primary-foreground text-xs font-bold rounded-full h-5 min-w-[20px] px-1.5 flex items-center justify-center">
                        {conv.unread_count}
                      </span>
                    )}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Janela de chat */}
        <div className={cn(
          "flex flex-col h-full",
          !activeConversation && "hidden md:flex"
        )}>
          {activeConversation ? (
            <>
              <div className="p-3 border-b flex items-center gap-3 bg-background">
                <Button
                  variant="ghost"
                  size="icon"
                  className="md:hidden"
                  onClick={() => {
                    setActiveConversation(null)
                    navigate('/messages', { replace: true })
                  }}
                >
                  <ArrowLeft className="h-4 w-4" />
                </Button>
                <Avatar className="h-9 w-9">
                  <AvatarImage src={activeConversation.avatar_url || undefined} />
                  <AvatarFallback className="text-xs">
                    {getInitials(activeConversation.full_name || activeConversation.username)}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-sm truncate">
                    {activeConversation.full_name || activeConversation.username}
                  </p>
                  <p className="text-xs text-muted-foreground truncate">@{activeConversation.username}</p>
                </div>
              </div>

              <div className="flex-1 overflow-y-auto p-4 space-y-2 bg-muted/10">
                {messages.length === 0 ? (
                  <div className="text-center text-sm text-muted-foreground py-12">
                    <MessageSquare className="h-10 w-10 mx-auto opacity-40 mb-2" />
                    <p>Envie uma mensagem para iniciar a conversa!</p>
                  </div>
                ) : (
                  messages.map((msg, idx) => {
                    const isMine = msg.sender_id === user!.id
                    const prevMine = idx > 0 ? messages[idx - 1].sender_id === user!.id : false
                    const showAvatar = !isMine && !prevMine
                    return (
                      <div
                        key={msg.id}
                        className={cn("flex gap-2 items-end", isMine ? "justify-end" : "justify-start")}
                      >
                        {!isMine && (
                          <Avatar className={cn("h-7 w-7 flex-shrink-0", !showAvatar && "invisible")}>
                            <AvatarImage src={activeConversation.avatar_url || undefined} />
                            <AvatarFallback className="text-xs">
                              {getInitials(activeConversation.full_name || activeConversation.username)}
                            </AvatarFallback>
                          </Avatar>
                        )}
                        <div
                          className={cn(
                            "max-w-[75%] rounded-2xl px-3 py-2 text-sm shadow-sm",
                            isMine
                              ? "bg-primary text-primary-foreground rounded-br-sm"
                              : "bg-background border rounded-bl-sm"
                          )}
                        >
                          <p className="break-words whitespace-pre-wrap">{msg.content}</p>
                          <p className={cn(
                            "text-[10px] mt-1",
                            isMine ? "text-primary-foreground/70" : "text-muted-foreground"
                          )}>
                            {new Date(msg.created_at).toLocaleTimeString('pt-BR', {
                              hour: '2-digit', minute: '2-digit'
                            })}
                          </p>
                        </div>
                      </div>
                    )
                  })
                )}
                <div ref={messagesEndRef} />
              </div>

              <form onSubmit={sendMessage} className="p-3 border-t bg-background flex gap-2">
                <Input
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Digite uma mensagem..."
                  disabled={sending}
                  maxLength={1000}
                  autoFocus
                />
                <Button type="submit" disabled={!newMessage.trim() || sending} size="icon">
                  {sending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                </Button>
              </form>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center text-muted-foreground">
              <div className="text-center space-y-2">
                <MessageSquare className="h-16 w-16 mx-auto opacity-30" />
                <p>Selecione uma conversa para começar</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </Card>
  )
}
