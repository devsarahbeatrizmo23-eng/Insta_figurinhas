import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Heart, MessageCircle, Trash2 } from 'lucide-react'
import { Card, CardContent, CardHeader } from './ui/card'
import { Button } from './ui/button'
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar'
import { Badge } from './ui/badge'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'
import { Sticker } from '../lib/types'
import { getInitials } from '../lib/utils'
import CommentSection from './CommentSection'

interface StickerCardProps {
  sticker: Sticker & { creator?: { username?: string; full_name?: string | null; avatar_url?: string | null } }
  onDelete?: (id: string) => void
}

export default function StickerCard({ sticker, onDelete }: StickerCardProps) {
  const { user } = useAuth()
  const [liked, setLiked] = useState(false)
  const [likeCount, setLikeCount] = useState(0)
  const [commentCount, setCommentCount] = useState(0)
  const [showComments, setShowComments] = useState(false)
  const [busy, setBusy] = useState(false)
  const [imgSrc, setImgSrc] = useState(sticker.image_url)

  useEffect(() => {
    if (!user) return
    void checkLike()
    void fetchLikeCount()
    void fetchCommentCount()
  }, [user, sticker.id])

  const checkLike = async () => {
    const { data } = await supabase
      .from('likes')
      .select('user_id')
      .eq('user_id', user!.id)
      .eq('sticker_id', sticker.id)
      .maybeSingle()
    setLiked(!!data)
  }

  const fetchLikeCount = async () => {
    const { count } = await supabase
      .from('likes')
      .select('*', { count: 'exact', head: true })
      .eq('sticker_id', sticker.id)
    setLikeCount(count || 0)
  }

  const fetchCommentCount = async () => {
    const { count } = await supabase
      .from('comments')
      .select('*', { count: 'exact', head: true })
      .eq('sticker_id', sticker.id)
    setCommentCount(count || 0)
  }

  const toggleLike = async () => {
    if (!user || busy) return
    setBusy(true)
    try {
      if (liked) {
        await supabase
          .from('likes')
          .delete()
          .eq('user_id', user.id)
          .eq('sticker_id', sticker.id)
        setLiked(false)
        setLikeCount((c) => Math.max(0, c - 1))
      } else {
        await supabase
          .from('likes')
          .insert({ user_id: user.id, sticker_id: sticker.id })
        setLiked(true)
        setLikeCount((c) => c + 1)
      }
    } catch (err) {
      console.error('Erro ao curtir:', err)
    } finally {
      setBusy(false)
    }
  }

  const handleDelete = () => {
    if (confirm('Tem certeza que deseja excluir esta figurinha?')) {
      onDelete?.(sticker.id)
    }
  }

  const isOwner = user?.id === sticker.creator_id
  const fallbackImg = `https://ui-avatars.com/api/?name=${encodeURIComponent(sticker.athlete_name)}&background=009739&color=fff&size=400&bold=true`

  return (
    <Card className="overflow-hidden">
      <CardHeader className="flex flex-row items-center gap-3 space-y-0 pb-3">
        <Avatar className="h-10 w-10">
          <AvatarImage src={sticker.creator?.avatar_url || undefined} />
          <AvatarFallback>
            {getInitials(sticker.creator?.full_name || sticker.creator?.username)}
          </AvatarFallback>
        </Avatar>
        <div className="flex-1 min-w-0">
          <Link
            to={`/profile/${sticker.creator?.username || ''}`}
            className="font-semibold hover:underline block truncate"
          >
            {sticker.creator?.full_name || sticker.creator?.username || 'Colecionador'}
          </Link>
          <p className="text-xs text-muted-foreground truncate">
            @{sticker.creator?.username}
          </p>
        </div>
        {isOwner && (
          <Button
            variant="ghost"
            size="icon"
            onClick={handleDelete}
            title="Excluir figurinha"
          >
            <Trash2 className="h-4 w-4 text-destructive" />
          </Button>
        )}
      </CardHeader>

      <div className="relative aspect-square bg-gradient-to-br from-[#009739]/15 via-[#FEDD00]/10 to-[#012169]/15 dark:from-[#009739]/25 dark:via-[#FEDD00]/15 dark:to-[#012169]/25 overflow-hidden">
        <img
          src={imgSrc}
          alt={sticker.athlete_name}
          className="absolute inset-0 w-full h-full object-cover"
          onError={() => setImgSrc(fallbackImg)}
          loading="lazy"
        />
        <div className="absolute top-3 left-3 bg-background/90 backdrop-blur px-2 py-1 rounded-full text-xs font-bold shadow">
          #{sticker.number ?? '?'}
        </div>
      </div>

      <CardContent className="pt-4 space-y-3">
        <div>
          <h3 className="font-bold text-lg leading-tight">{sticker.athlete_name}</h3>
          <div className="flex flex-wrap items-center gap-2 mt-2">
            <Badge variant="secondary">{sticker.team}</Badge>
            {sticker.position && <Badge variant="outline">{sticker.position}</Badge>}
          </div>
        </div>
        {sticker.description && (
          <p className="text-sm text-muted-foreground line-clamp-3">
            {sticker.description}
          </p>
        )}
      </CardContent>

      <div className="px-6 pb-4 flex gap-1 border-t pt-3">
        <Button
          variant="ghost"
          size="sm"
          onClick={toggleLike}
          disabled={busy}
          className="gap-2"
        >
          <Heart
            className={`h-5 w-5 transition-all ${
              liked ? 'fill-red-500 text-red-500 scale-110' : ''
            }`}
          />
          <span className="text-sm">{likeCount}</span>
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setShowComments((s) => !s)}
          className="gap-2"
        >
          <MessageCircle className="h-5 w-5" />
          <span className="text-sm">{commentCount}</span>
        </Button>
      </div>

      {showComments && (
        <div className="border-t bg-muted/30 px-6 py-4">
          <CommentSection
            stickerId={sticker.id}
            onCommentAdded={fetchCommentCount}
          />
        </div>
      )}
    </Card>
  )
}
