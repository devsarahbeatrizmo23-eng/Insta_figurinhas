import { useEffect, useState, useCallback } from 'react'
import { useParams, Link } from 'react-router-dom'
import {
  UserPlus, UserMinus, MessageCircle, Edit, Settings,
  Loader2, Trophy, Users, Image as ImageIcon
} from 'lucide-react'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'
import { Profile as ProfileType, Sticker } from '../lib/types'
import { Button } from '../components/ui/button'
import { Card, CardContent } from '../components/ui/card'
import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar'
import { Badge } from '../components/ui/badge'
import { getInitials } from '../lib/utils'
import StickerCard from '../components/StickerCard'

type StickerWithCreator = Sticker & { creator: ProfileType | null }

export default function ProfilePage() {
  const { username } = useParams<{ username: string }>()
  const { user, profile: currentProfile } = useAuth()
  const [profile, setProfile] = useState<ProfileType | null>(null)
  const [stickers, setStickers] = useState<StickerWithCreator[]>([])
  const [loading, setLoading] = useState(true)
  const [notFound, setNotFound] = useState(false)
  const [isFollowing, setIsFollowing] = useState(false)
  const [followerCount, setFollowerCount] = useState(0)
  const [followingCount, setFollowingCount] = useState(0)
  const [followBusy, setFollowBusy] = useState(false)

  const isOwnProfile = user?.id === profile?.id

  const fetchProfile = useCallback(async () => {
    if (!username) return
    setLoading(true)
    setNotFound(false)
    try {
      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('username', username)
        .maybeSingle()

      if (error) throw error
      if (!data) {
        setNotFound(true)
        setProfile(null)
      } else {
        setProfile(data)
      }
    } catch (err) {
      console.error('Erro ao buscar perfil:', err)
    } finally {
      setLoading(false)
    }
  }, [username])

  useEffect(() => { void fetchProfile() }, [fetchProfile])

  useEffect(() => {
    if (!profile) return
    void fetchStickers()
    void checkFollowStatus()
    void fetchFollowCounts()
  }, [profile])

  const fetchStickers = async () => {
    const { data, error } = await supabase
      .from('stickers')
      .select('*, creator:profiles(*)')
      .eq('creator_id', profile!.id)
      .order('created_at', { ascending: false })

    if (!error) setStickers((data as StickerWithCreator[]) || [])
  }

  const checkFollowStatus = async () => {
    if (!user || isOwnProfile) return
    const { data } = await supabase
      .from('follows')
      .select('follower_id')
      .eq('follower_id', user.id)
      .eq('following_id', profile!.id)
      .maybeSingle()
    setIsFollowing(!!data)
  }

  const fetchFollowCounts = async () => {
    const { count: fc } = await supabase
      .from('follows')
      .select('*', { count: 'exact', head: true })
      .eq('following_id', profile!.id)
    const { count: fg } = await supabase
      .from('follows')
      .select('*', { count: 'exact', head: true })
      .eq('follower_id', profile!.id)
    setFollowerCount(fc || 0)
    setFollowingCount(fg || 0)
  }

  const toggleFollow = async () => {
    if (!user || followBusy) return
    setFollowBusy(true)
    try {
      if (isFollowing) {
        await supabase
          .from('follows')
          .delete()
          .eq('follower_id', user.id)
          .eq('following_id', profile!.id)
        setIsFollowing(false)
        setFollowerCount((c) => Math.max(0, c - 1))
      } else {
        await supabase.from('follows').insert({
          follower_id: user.id,
          following_id: profile!.id,
        })
        setIsFollowing(true)
        setFollowerCount((c) => c + 1)
      }
    } catch (err) {
      console.error('Erro ao seguir/deixar de seguir:', err)
    } finally {
      setFollowBusy(false)
    }
  }

  const handleDeleteSticker = async (id: string) => {
    try {
      await supabase.from('stickers').delete().eq('id', id)
      setStickers((prev) => prev.filter((s) => s.id !== id))
    } catch (err) {
      console.error('Erro ao excluir figurinha:', err)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    )
  }

  if (notFound || !profile) {
    return (
      <Card>
        <CardContent className="text-center py-12 space-y-4">
          <p className="text-lg">Usuário não encontrado</p>
          <Button asChild><Link to="/">Voltar ao feed</Link></Button>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      <Card>
        <div className="h-32 sm:h-40 bg-gradient-to-br from-[#009739] via-[#FEDD00] to-[#012169] rounded-t-lg relative overflow-hidden">
          {/* Estrelas decorativas */}
          <div className="absolute inset-0 opacity-30" aria-hidden>
            <div className="absolute top-4 left-8 text-white text-xl">★</div>
            <div className="absolute top-8 right-12 text-white text-lg">★</div>
            <div className="absolute bottom-6 left-1/3 text-white text-sm">★</div>
            <div className="absolute top-1/2 right-1/4 text-white text-base">★</div>
          </div>
        </div>
        <CardContent className="pt-0 -mt-12">
          <div className="flex flex-col sm:flex-row items-start sm:items-end gap-4">
            <Avatar className="h-24 w-24 border-4 border-background shadow-lg">
              <AvatarImage src={profile.avatar_url || undefined} />
              <AvatarFallback className="text-2xl">{getInitials(profile.full_name || profile.username)}</AvatarFallback>
            </Avatar>
            <div className="flex-1 sm:pb-2 space-y-2">
              <div>
                <h1 className="text-2xl font-bold">{profile.full_name || profile.username}</h1>
                <p className="text-muted-foreground">@{profile.username}</p>
              </div>
              {profile.bio && (
                <p className="text-sm whitespace-pre-wrap">{profile.bio}</p>
              )}
            </div>
            <div className="flex flex-wrap gap-2 sm:pb-2">
              {isOwnProfile ? (
                <>
                  <Button asChild variant="outline" size="sm">
                    <Link to="/edit-profile"><Edit className="h-4 w-4 mr-2" /> Editar perfil</Link>
                  </Button>
                  <Button asChild variant="outline" size="sm">
                    <Link to="/collection"><Settings className="h-4 w-4 mr-2" /> Minha coleção</Link>
                  </Button>
                </>
              ) : (
                <>
                  <Button
                    onClick={toggleFollow}
                    variant={isFollowing ? 'outline' : 'default'}
                    size="sm"
                    disabled={followBusy}
                  >
                    {isFollowing ? (
                      <><UserMinus className="h-4 w-4 mr-2" /> Deixar de seguir</>
                    ) : (
                      <><UserPlus className="h-4 w-4 mr-2" /> Seguir</>
                    )}
                  </Button>
                  <Button asChild variant="outline" size="sm">
                    <Link to={`/messages/${profile.id}`}>
                      <MessageCircle className="h-4 w-4 mr-2" /> Mensagem
                    </Link>
                  </Button>
                </>
              )}
            </div>
          </div>

          <div className="flex flex-wrap gap-3 items-center mt-6 pt-4 border-t">
            {profile.favorite_team && (
              <Badge variant="secondary" className="gap-1">
                <Trophy className="h-3 w-3" /> {profile.favorite_team}
              </Badge>
            )}
            <div className="flex gap-4 text-sm">
              <span><strong>{followerCount}</strong> <span className="text-muted-foreground">seguidores</span></span>
              <span><strong>{followingCount}</strong> <span className="text-muted-foreground">seguindo</span></span>
              <span><strong>{stickers.length}</strong> <span className="text-muted-foreground">figurinhas</span></span>
            </div>
          </div>
        </CardContent>
      </Card>

      <div>
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
          <ImageIcon className="h-5 w-5" />
          Coleção de figurinhas
        </h2>
        {stickers.length === 0 ? (
          <Card>
            <CardContent className="text-center py-12 text-muted-foreground">
              {isOwnProfile ? 'Você ainda não criou nenhuma figurinha' : 'Este usuário ainda não criou figurinhas'}
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2">
            {stickers.map((s) => (
              <StickerCard
                key={s.id}
                sticker={s}
                onDelete={isOwnProfile ? handleDeleteSticker : undefined}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
