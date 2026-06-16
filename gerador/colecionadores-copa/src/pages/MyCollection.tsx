import { useEffect, useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { Check, Plus, Search, Loader2, BookmarkPlus } from 'lucide-react'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'
import { Sticker, UserCollection, CollectionStatus } from '../lib/types'
import { TEAMS } from '../lib/types'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Card, CardContent } from '../components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs'
import { Badge } from '../components/ui/badge'
import { cn } from '../lib/utils'

const STATUS_META: Record<CollectionStatus, { label: string; color: string; bg: string }> = {
  TENHO: { label: 'TENHO', color: 'text-green-700', bg: 'bg-green-500' },
  QUERO: { label: 'QUERO', color: 'text-blue-700', bg: 'bg-blue-500' },
  REPETIDA: { label: 'REPETIDA', color: 'text-orange-700', bg: 'bg-orange-500' },
}

export default function MyCollection() {
  const { user } = useAuth()
  const [allStickers, setAllStickers] = useState<Sticker[]>([])
  const [myCollection, setMyCollection] = useState<Map<string, CollectionStatus>>(new Map())
  const [search, setSearch] = useState('')
  const [filterTeam, setFilterTeam] = useState('')
  const [loading, setLoading] = useState(true)
  const [tab, setTab] = useState<'all' | CollectionStatus>('all')

  useEffect(() => { void fetchData() }, [user])

  const fetchData = async () => {
    setLoading(true)
    try {
      const [stickersRes, collectionRes] = await Promise.all([
        supabase.from('stickers').select('*').order('athlete_name'),
        supabase.from('user_collections').select('*').eq('user_id', user!.id),
      ])

      if (stickersRes.error) throw stickersRes.error
      if (collectionRes.error) throw collectionRes.error

      setAllStickers(stickersRes.data || [])
      const map = new Map<string, CollectionStatus>()
      ;((collectionRes.data as UserCollection[]) || []).forEach((c) => {
        map.set(c.sticker_id, c.status)
      })
      setMyCollection(map)
    } catch (err) {
      console.error('Erro ao carregar coleção:', err)
    } finally {
      setLoading(false)
    }
  }

  const setStatus = async (stickerId: string, status: CollectionStatus) => {
    try {
      const current = myCollection.get(stickerId)

      if (current === status) {
        // Toggle off
        await supabase
          .from('user_collections')
          .delete()
          .eq('user_id', user!.id)
          .eq('sticker_id', stickerId)
        const newMap = new Map(myCollection)
        newMap.delete(stickerId)
        setMyCollection(newMap)
      } else {
        await supabase.from('user_collections').upsert(
          {
            user_id: user!.id,
            sticker_id: stickerId,
            status,
            updated_at: new Date().toISOString(),
          },
          { onConflict: 'user_id,sticker_id' }
        )
        const newMap = new Map(myCollection)
        newMap.set(stickerId, status)
        setMyCollection(newMap)
      }
    } catch (err) {
      console.error('Erro ao atualizar status:', err)
    }
  }

  const filteredStickers = useMemo(() => {
    return allStickers.filter((s) => {
      const matchSearch =
        !search ||
        s.athlete_name.toLowerCase().includes(search.toLowerCase()) ||
        s.team.toLowerCase().includes(search.toLowerCase())
      const matchTeam = !filterTeam || s.team === filterTeam
      return matchSearch && matchTeam
    })
  }, [allStickers, search, filterTeam])

  const counts = useMemo(() => {
    const c = { TENHO: 0, QUERO: 0, REPETIDA: 0 }
    myCollection.forEach((s) => { c[s]++ })
    return c
  }, [myCollection])

  const visibleStickers = useMemo(() => {
    if (tab === 'all') return filteredStickers
    return filteredStickers.filter((s) => myCollection.get(s.id) === tab)
  }, [filteredStickers, tab, myCollection])

  return (
    <div className="space-y-6">
      <Card>
        <CardContent className="pt-6 space-y-4">
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Buscar por atleta ou seleção..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-10"
              />
            </div>
            <select
              value={filterTeam}
              onChange={(e) => setFilterTeam(e.target.value)}
              className="flex h-10 rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              <option value="">Todas as seleções</option>
              {TEAMS.map((team) => (
                <option key={team} value={team}>{team}</option>
              ))}
            </select>
          </div>

          <div className="flex flex-wrap gap-3 text-sm">
            <span className="inline-flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-green-500" />
              Tenho: <strong className="text-green-700 dark:text-green-400">{counts.TENHO}</strong>
            </span>
            <span className="inline-flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-blue-500" />
              Quero: <strong className="text-blue-700 dark:text-blue-400">{counts.QUERO}</strong>
            </span>
            <span className="inline-flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-orange-500" />
              Repetida: <strong className="text-orange-700 dark:text-orange-400">{counts.REPETIDA}</strong>
            </span>
          </div>
        </CardContent>
      </Card>

      {loading ? (
        <div className="flex justify-center py-12"><Loader2 className="h-8 w-8 animate-spin" /></div>
      ) : allStickers.length === 0 ? (
        <Card>
          <CardContent className="text-center py-12 space-y-4">
            <BookmarkPlus className="h-12 w-12 text-muted-foreground mx-auto" />
            <div>
              <h3 className="font-semibold text-lg">Nenhuma figurinha disponível</h3>
              <p className="text-sm text-muted-foreground mt-1">
                Ainda não existem figurinhas cadastradas no sistema.
              </p>
            </div>
            <Button asChild><Link to="/create-sticker">Criar a primeira</Link></Button>
          </CardContent>
        </Card>
      ) : (
        <Tabs value={tab} onValueChange={(v) => setTab(v as any)}>
          <TabsList className="flex-wrap h-auto">
            <TabsTrigger value="all">Todas ({filteredStickers.length})</TabsTrigger>
            <TabsTrigger value="TENHO">Tenho ({counts.TENHO})</TabsTrigger>
            <TabsTrigger value="QUERO">Quero ({counts.QUERO})</TabsTrigger>
            <TabsTrigger value="REPETIDA">Repetidas ({counts.REPETIDA})</TabsTrigger>
          </TabsList>

          <TabsContent value={tab}>
            {visibleStickers.length === 0 ? (
              <Card>
                <CardContent className="text-center py-12 text-muted-foreground">
                  {tab === 'all' ? 'Nenhuma figurinha corresponde ao filtro.' : `Nenhuma figurinha marcada como ${STATUS_META[tab as CollectionStatus].label}.`}
                </CardContent>
              </Card>
            ) : (
              <div className="grid gap-3 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
                {visibleStickers.map((sticker) => (
                  <StickerCollectionItem
                    key={sticker.id}
                    sticker={sticker}
                    status={myCollection.get(sticker.id)}
                    onSetStatus={(s) => setStatus(sticker.id, s)}
                  />
                ))}
              </div>
            )}
          </TabsContent>
        </Tabs>
      )}
    </div>
  )
}

function StickerCollectionItem({
  sticker,
  status,
  onSetStatus,
}: {
  sticker: Sticker
  status: CollectionStatus | undefined
  onSetStatus: (status: CollectionStatus) => void
}) {
  const [imgSrc, setImgSrc] = useState(sticker.image_url)
  const fallback = `https://ui-avatars.com/api/?name=${encodeURIComponent(sticker.athlete_name)}&background=009739&color=fff&size=300&bold=true`

  return (
    <Card className="overflow-hidden hover:shadow-md transition-shadow">
      <div className="relative aspect-square bg-gradient-to-br from-[#009739]/15 via-[#FEDD00]/10 to-[#012169]/15 dark:from-[#009739]/25 dark:via-[#FEDD00]/15 dark:to-[#012169]/25">
        <img
          src={imgSrc}
          alt={sticker.athlete_name}
          className="absolute inset-0 w-full h-full object-cover"
          onError={() => setImgSrc(fallback)}
          loading="lazy"
        />
        {sticker.number !== null && (
          <div className="absolute top-2 left-2 bg-background/90 backdrop-blur px-2 py-0.5 rounded text-xs font-bold">
            #{sticker.number}
          </div>
        )}
        {status && (
          <div className={cn(
            "absolute top-2 right-2 text-white text-xs px-2 py-1 rounded-full font-bold shadow",
            STATUS_META[status].bg
          )}>
            {STATUS_META[status].label}
          </div>
        )}
      </div>
      <CardContent className="p-3 space-y-2">
        <div>
          <h4 className="font-semibold text-sm truncate" title={sticker.athlete_name}>{sticker.athlete_name}</h4>
          <Badge variant="secondary" className="text-xs mt-1">{sticker.team}</Badge>
        </div>
        <div className="grid grid-cols-3 gap-1">
          {(['TENHO', 'QUERO', 'REPETIDA'] as CollectionStatus[]).map((s) => (
            <Button
              key={s}
              size="sm"
              variant={status === s ? 'default' : 'outline'}
              onClick={() => onSetStatus(s)}
              className={cn(
                "text-xs h-8 px-1",
                status === s && s === 'TENHO' && 'bg-green-600 hover:bg-green-700',
                status === s && s === 'QUERO' && 'bg-blue-600 hover:bg-blue-700',
                status === s && s === 'REPETIDA' && 'bg-orange-600 hover:bg-orange-700',
              )}
              title={s === status ? 'Clique para remover' : `Marcar como ${s}`}
            >
              {status === s ? <Check className="h-3 w-3" /> : <Plus className="h-3 w-3" />}
            </Button>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
