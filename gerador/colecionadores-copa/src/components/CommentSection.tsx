import { useState, useEffect, useRef } from 'react'
import { Send, Loader2 } from 'lucide-react'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'
import { Comment, Profile } from '../lib/types'
import { formatRelativeTime, getInitials } from '../lib/utils'

type CommentWithUser = Comment & { user: Profile | undefined }

interface CommentSectionProps {
  stickerId: string
  onCommentAdded?: () => void
}

export default function CommentSection({ stickerId, onCommentAdded }: CommentSectionProps) {
  const { user, profile: me } = useAuth()
  const [comments, setComments] = useState<CommentWithUser[]>([])
  const [newComment, setNewComment] = useState('')
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    void fetchComments()

    const channel = supabase
      .channel(`comments:${stickerId}`)
      .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'comments',
        filter: `sticker_id=eq.${stickerId}`,
      }, (payload) => {
        // Insere o novo comentário na lista sem refazer fetch
        const newRow = payload.new as Comment
        setComments((prev) => {
          if (prev.find((c) => c.id === newRow.id)) return prev
          return [
            ...prev,
            { ...newRow, user: me || undefined }
          ]
        })
      })
      .subscribe()

    return () => {
      void supabase.removeChannel(channel)
    }
  }, [stickerId])

  const fetchComments = async () => {
    setLoading(true)
    try {
      const { data, error } = await supabase
        .from('comments')
        .select('*, user:profiles(*)')
        .eq('sticker_id', stickerId)
        .order('created_at', { ascending: true })

      if (error) throw error
      setComments((data as CommentWithUser[]) || [])
    } catch (err) {
      console.error('Erro ao buscar comentários:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const text = newComment.trim()
    if (!text || !user || submitting) return
    setSubmitting(true)
    try {
      const { data, error } = await supabase
        .from('comments')
        .insert({
          sticker_id: stickerId,
          user_id: user.id,
          content: text,
        })
        .select('*, user:profiles(*)')
        .single()

      if (error) throw error
      setComments((prev) => [...prev, data as CommentWithUser])
      setNewComment('')
      onCommentAdded?.()
      inputRef.current?.focus()
    } catch (err) {
      console.error('Erro ao comentar:', err)
      alert('Não foi possível enviar o comentário.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="space-y-3">
      <form onSubmit={handleSubmit} className="flex gap-2 items-center">
        <Avatar className="h-8 w-8 flex-shrink-0">
          <AvatarImage src={me?.avatar_url || undefined} />
          <AvatarFallback className="text-xs">
            {getInitials(me?.full_name || me?.username)}
          </AvatarFallback>
        </Avatar>
        <Input
          ref={inputRef}
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          placeholder="Comente algo..."
          disabled={submitting}
          className="flex-1"
          maxLength={500}
        />
        <Button
          type="submit"
          size="icon"
          disabled={!newComment.trim() || submitting}
          aria-label="Enviar comentário"
        >
          {submitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
        </Button>
      </form>

      {loading ? (
        <div className="flex justify-center py-2">
          <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
        </div>
      ) : comments.length === 0 ? (
        <p className="text-xs text-muted-foreground text-center py-3">
          Nenhum comentário ainda. Seja o primeiro!
        </p>
      ) : (
        <ul className="space-y-2 max-h-72 overflow-y-auto">
          {comments.map((c) => (
            <li key={c.id} className="flex gap-2 text-sm">
              <Avatar className="h-7 w-7 flex-shrink-0">
                <AvatarImage src={c.user?.avatar_url || undefined} />
                <AvatarFallback className="text-xs">
                  {getInitials(c.user?.full_name || c.user?.username)}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 bg-background rounded-lg px-3 py-2 border">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-xs">
                    {c.user?.full_name || c.user?.username || 'Usuário'}
                  </span>
                  <span className="text-xs text-muted-foreground">
                    {formatRelativeTime(c.created_at)}
                  </span>
                </div>
                <p className="break-words">{c.content}</p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
