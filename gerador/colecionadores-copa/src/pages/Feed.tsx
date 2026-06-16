import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { UserPlus, Loader2, Sparkles, Users } from 'lucide-react'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'
import { Sticker, Profile } from '../lib/types'
import StickerCard from '../components/StickerCard'
import { Button } from '../components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs'
import { getInitials } from '../lib/utils'

type StickerWithCreator = Sticker & { creator: Profile | null }

export default function Feed() {
  const { user } = useAuth()
  const [feedStickers, setFeedStickers] = useState<StickerWithCreator[]>([])
  const [suggestedUsers, setSuggestedUsers] = useState<Profile[]>([])
  const [loading, setLoading] = useState(true)
  const [tab, setTab] = useState('feed')

  useEffect(() => {
    if (user) {
      void fetchFeed()
      void fetchSuggestions()
    }
  }, [user])

  useEffect(() => {
    if (tab === 'all') void fetchAllStickers()
    else void fetchFeed()
  }, [tab])

  const fetchFeed = async () => {
    setLoading(true)
    try {
      const { data: followingData } = await supabase
        .from('follows')
        .select('following_id')
        .eq('follower_id', user!.id)

      const followingIds = followingData?.map((f) => f.following_id) || []
      followingIds.push(user!.id) // inclui o próprio usuário

      const { data, error } = await supabase
        .from('stickers')
        .select('*, creator:profiles(*)')
        .in('creator_id', followingIds)
        .order('created_at', { ascending: false })
        .limit(50)

      if (error) throw error
      setFeedStickers((data as StickerWithCreator[]) || [])
    } catch (err) {
      console.error('Erro ao buscar feed:', err)
    } finally {
      setLoading(false)
    }
  }

  const fetchAllStickers = async () => {
    setLoading(true)
    try {
      const { data, error } = await supabase
        .from('stickers')
        .select('*, creator:profiles(*)')
        .order('created_at', { ascending: false })
        .limit(100)

      if (error) throw error
      setFeedStickers((data as StickerWithCreator[]) || [])
    } catch (err) {
      console.error('Erro ao buscar todas figurinhas:', err)
    } finally {
      setLoading(false)
    }
  }

  const fetchSuggestions = async () => {
    try {
      const { data: followingData } = await supabase
        .from('follows')
        .select('following_id')
        .eq('follower_id', user!.id)

      const excludeIds = new Set<string>([user!.id])
      followingData?.forEach((f) => excludeIds.add(f.following_id))

      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .neq('id', user!.id)
        .limit(20)

      if (error) throw error
      const filtered = (data || []).filter((p: Profile) => !excludeIds.has(p.id))
      setSuggestedUsers(filtered.slice(0, 5))
    } catch (err) {
      console.error('Erro ao buscar sugestões:', err)
    }
  }

  const handleFollow = async (profileId: string) => {
    try {
      const { error } = await supabase.from('follows').insert({
        follower_id: user!.id,
        following_id: profileId,
      })
      if (error) throw error
      setSuggestedUsers((prev) => prev.filter((p) => p.id !== profileId))
    } catch (err) {
      console.error('Erro ao seguir:', err)
    }
  }

  const handleDeleteSticker = async (id: string) => {
    try {
      await supabase.from('stickers').delete().eq('id', id)
      setFeedStickers((prev) => prev.filter((s) => s.id !== id))
    } catch (err) {
      console.error('Erro ao excluir figurinha:', err)
      alert('Não foi possível excluir a figurinha.')
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-3">
      <div className="lg:col-span-2 space-y-4">
        <Tabs value={tab} onValueChange={setTab}>
          <TabsList className="w-full sm:w-auto">
            <TabsTrigger value="feed" className="flex-1 sm:flex-none">
              <Users className="h-4 w-4 mr-2" /> Meu Feed
            </TabsTrigger>
            <TabsTrigger value="all" className="flex-1 sm:flex-none">
              <Sparkles className="h-4 w-4 mr-2" /> Explorar
            </TabsTrigger>
          </TabsList>

          <TabsContent value="feed" className="space-y-4">
            {loading ? (
              <div className="flex justify-center py-12"><Loader2 className="h-8 w-8 animate-spin" /></div>
            ) : feedStickers.length === 0 ? (
              <EmptyFeed />
            ) : (
              feedStickers.map((sticker) => (
                <StickerCard
                  key={sticker.id}
                  sticker={sticker}
                  onDelete={handleDeleteSticker}
                />
              ))
            )}
          </TabsContent>

          <TabsContent value="all" className="space-y-4">
            {loading ? (
              <div className="flex justify-center py-12"><Loader2 className="h-8 w-8 animate-spin" /></div>
            ) : feedStickers.length === 0 ? (
              <Card>
                <CardContent className="text-center py-12 text-muted-foreground">
                  Nenhuma figurinha criada ainda
                </CardContent>
              </Card>
            ) : (
              feedStickers.map((sticker) => (
                <StickerCard
                  key={sticker.id}
                  sticker={sticker}
                  onDelete={handleDeleteSticker}
                />
              ))
            )}
          </TabsContent>
        </Tabs>
      </div>

      <aside className="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <UserPlus className="h-4 w-4" /> Sugestões para seguir
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {suggestedUsers.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-2">
                Você já segue todo mundo! ⚽
              </p>
            ) : (
              suggestedUsers.map((p) => (
                <div key={p.id} className="flex items-center gap-3">
                  <Avatar className="h-10 w-10">
                    <AvatarImage src={p.avatar_url || undefined} />
                    <AvatarFallback className="text-xs">{getInitials(p.full_name || p.username)}</AvatarFallback>
                  </Avatar>
                  <div className="flex-1 min-w-0">
                    <Link to={`/profile/${p.username}`} className="font-medium text-sm hover:underline block truncate">
                      {p.full_name || p.username}
                    </Link>
                    <p className="text-xs text-muted-foreground truncate">@{p.username}</p>
                  </div>
                  <Button size="sm" variant="outline" onClick={() => handleFollow(p.id)}>
                    Seguir
                  </Button>
                </div>
              ))
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">⚽ Atalhos</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Button asChild variant="outline" className="w-full justify-start">
              <Link to="/collection">📚 Minha coleção</Link>
            </Button>
            <Button asChild variant="outline" className="w-full justify-start">
              <Link to="/create-sticker">➕ Criar figurinha</Link>
            </Button>
            <Button asChild variant="outline" className="w-full justify-start">
              <Link to="/messages">💬 Mensagens</Link>
            </Button>
          </CardContent>
        </Card>
      </aside>
    </div>
  )
}

function EmptyFeed() {
  return (
    <Card>
      <CardContent className="text-center py-12 space-y-4">
        <div className="mx-auto h-16 w-16 rounded-full bg-muted flex items-center justify-center">
          <Sparkles className="h-8 w-8 text-muted-foreground" />
        </div>
        <div>
          <h3 className="font-semibold text-lg">Seu feed está vazio</h3>
          <p className="text-sm text-muted-foreground mt-1">
            Siga outros colecionadores ou crie sua primeira figurinha!
          </p>
        </div>
        <div className="flex gap-2 justify-center">
          <Button asChild><Link to="/create-sticker">Criar figurinha</Link></Button>
          <Button asChild variant="outline"><Link to="/collection">Ver coleção</Link></Button>
        </div>
      </CardContent>
    </Card>
  )
}
