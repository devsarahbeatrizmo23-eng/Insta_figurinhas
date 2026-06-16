import { useState, useEffect, useRef, FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload, Loader2, Save, Trash2, Edit3, Plus, ImagePlus } from 'lucide-react'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'
import { Sticker, TEAMS, POSITIONS } from '../lib/types'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Textarea } from '../components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card'
import { Badge } from '../components/ui/badge'

interface FormData {
  athlete_name: string
  team: string
  position: string
  number: string
  description: string
  image_url: string
}

const INITIAL_FORM: FormData = {
  athlete_name: '',
  team: '',
  position: '',
  number: '',
  description: '',
  image_url: '',
}

export default function CreateSticker() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [formData, setFormData] = useState<FormData>(INITIAL_FORM)
  const [imageFile, setImageFile] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [myStickers, setMyStickers] = useState<Sticker[]>([])
  const [editingId, setEditingId] = useState<string | null>(null)
  const [loadingMine, setLoadingMine] = useState(true)

  useEffect(() => {
    if (user) void fetchMyStickers()
  }, [user])

  const fetchMyStickers = async () => {
    setLoadingMine(true)
    try {
      const { data, error } = await supabase
        .from('stickers')
        .select('*')
        .eq('creator_id', user!.id)
        .order('created_at', { ascending: false })

      if (error) throw error
      setMyStickers(data || [])
    } catch (err) {
      console.error('Erro ao buscar figurinhas:', err)
    } finally {
      setLoadingMine(false)
    }
  }

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    if (file.size > 5 * 1024 * 1024) {
      setError('A imagem deve ter no máximo 5MB')
      return
    }
    setImageFile(file)
    setImagePreview(URL.createObjectURL(file))
  }

  const uploadImage = async (): Promise<string | null> => {
    if (!imageFile || !user) return null
    const fileExt = imageFile.name.split('.').pop()
    const fileName = `${Date.now()}-${Math.random().toString(36).slice(2)}.${fileExt}`
    const filePath = `${user.id}/${fileName}`

    const { error } = await supabase.storage
      .from('stickers')
      .upload(filePath, imageFile, { contentType: imageFile.type })

    if (error) {
      console.error('Erro no upload:', error)
      return null
    }

    const { data } = supabase.storage.from('stickers').getPublicUrl(filePath)
    return data.publicUrl
  }

  const resetForm = () => {
    setFormData(INITIAL_FORM)
    setImageFile(null)
    setImagePreview(null)
    setEditingId(null)
    setError(null)
    setSuccess(null)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!user) return
    setError(null)
    setSuccess(null)

    if (!formData.athlete_name.trim()) {
      setError('Nome do atleta é obrigatório')
      return
    }
    if (!formData.team) {
      setError('Seleção é obrigatória')
      return
    }
    if (!editingId && !imageFile && !formData.image_url) {
      setError('Forneça uma imagem (upload ou URL)')
      return
    }

    setLoading(true)
    try {
      let image_url = formData.image_url
      if (imageFile) {
        const uploaded = await uploadImage()
        if (uploaded) image_url = uploaded
        else if (!formData.image_url) throw new Error('Falha no upload da imagem')
      }

      const payload = {
        creator_id: user.id,
        athlete_name: formData.athlete_name.trim(),
        team: formData.team,
        position: formData.position || null,
        number: formData.number ? parseInt(formData.number, 10) : null,
        description: formData.description.trim() || null,
        image_url,
      }

      if (editingId) {
        const { error } = await supabase.from('stickers').update(payload).eq('id', editingId)
        if (error) throw error
        setSuccess('Figurinha atualizada!')
      } else {
        const { error } = await supabase.from('stickers').insert(payload)
        if (error) throw error
        setSuccess('Figurinha criada!')
      }

      resetForm()
      void fetchMyStickers()
    } catch (err: any) {
      setError(err?.message || 'Erro ao salvar figurinha')
    } finally {
      setLoading(false)
    }
  }

  const handleEdit = (sticker: Sticker) => {
    setFormData({
      athlete_name: sticker.athlete_name,
      team: sticker.team,
      position: sticker.position || '',
      number: sticker.number?.toString() || '',
      description: sticker.description || '',
      image_url: sticker.image_url,
    })
    setImagePreview(sticker.image_url)
    setImageFile(null)
    setEditingId(sticker.id)
    setError(null)
    setSuccess(null)
    if (fileInputRef.current) fileInputRef.current.value = ''
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Tem certeza que deseja excluir esta figurinha?')) return
    try {
      const { error } = await supabase.from('stickers').delete().eq('id', id)
      if (error) throw error
      void fetchMyStickers()
      if (editingId === id) resetForm()
    } catch (err) {
      console.error('Erro ao excluir:', err)
      alert('Não foi possível excluir a figurinha.')
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            {editingId ? <Edit3 className="h-5 w-5" /> : <Plus className="h-5 w-5" />}
            {editingId ? 'Editar figurinha' : 'Criar nova figurinha'}
          </CardTitle>
          <CardDescription>
            {editingId ? 'Atualize os dados da figurinha' : 'Adicione uma nova figurinha à sua coleção'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid md:grid-cols-[200px_1fr] gap-6">
              {/* Upload de imagem */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Imagem</label>
                <div className="aspect-square rounded-lg border-2 border-dashed flex items-center justify-center overflow-hidden bg-muted">
                  {imagePreview ? (
                    <img src={imagePreview} alt="Preview" className="w-full h-full object-cover" />
                  ) : (
                    <ImagePlus className="h-12 w-12 text-muted-foreground" />
                  )}
                </div>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  className="hidden"
                />
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => fileInputRef.current?.click()}
                  className="w-full"
                  size="sm"
                >
                  <Upload className="h-4 w-4 mr-2" />
                  {imagePreview ? 'Trocar' : 'Escolher'}
                </Button>
                <p className="text-xs text-muted-foreground text-center">ou cole uma URL:</p>
                <Input
                  name="image_url"
                  value={formData.image_url}
                  onChange={handleChange}
                  placeholder="https://..."
                  className="text-xs"
                />
              </div>

              {/* Campos */}
              <div className="space-y-3">
                <div className="space-y-2">
                  <label htmlFor="athlete_name" className="text-sm font-medium">Nome do atleta *</label>
                  <Input
                    id="athlete_name"
                    name="athlete_name"
                    value={formData.athlete_name}
                    onChange={handleChange}
                    required
                    placeholder="Ex: Neymar Jr."
                    maxLength={80}
                  />
                </div>

                <div className="space-y-2">
                  <label htmlFor="team" className="text-sm font-medium">Seleção *</label>
                  <select
                    id="team"
                    name="team"
                    value={formData.team}
                    onChange={handleChange}
                    required
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  >
                    <option value="">Selecione...</option>
                    {TEAMS.map((t) => <option key={t} value={t}>{t}</option>)}
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="space-y-2">
                    <label htmlFor="position" className="text-sm font-medium">Posição</label>
                    <select
                      id="position"
                      name="position"
                      value={formData.position}
                      onChange={handleChange}
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                    >
                      <option value="">Selecione...</option>
                      {POSITIONS.map((p) => <option key={p} value={p}>{p}</option>)}
                    </select>
                  </div>
                  <div className="space-y-2">
                    <label htmlFor="number" className="text-sm font-medium">Número</label>
                    <Input
                      id="number"
                      name="number"
                      type="number"
                      min={1}
                      max={99}
                      value={formData.number}
                      onChange={handleChange}
                      placeholder="10"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <label htmlFor="description" className="text-sm font-medium">Descrição</label>
                  <Textarea
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    placeholder="Detalhes sobre o atleta..."
                    rows={3}
                    maxLength={200}
                  />
                  <p className="text-xs text-muted-foreground text-right">{formData.description.length}/200</p>
                </div>
              </div>
            </div>

            {error && (
              <div className="text-sm text-destructive bg-destructive/10 border border-destructive/20 p-3 rounded-md">
                {error}
              </div>
            )}
            {success && (
              <div className="text-sm text-green-700 bg-green-100 border border-green-300 dark:bg-green-900/30 dark:text-green-300 p-3 rounded-md">
                {success}
              </div>
            )}

            <div className="flex flex-col-reverse sm:flex-row gap-2">
              {editingId && (
                <Button type="button" variant="outline" onClick={resetForm}>
                  Cancelar
                </Button>
              )}
              <Button type="submit" disabled={loading} className="sm:flex-1">
                {loading ? (
                  <><Loader2 className="h-4 w-4 animate-spin" /> Salvando...</>
                ) : (
                  <><Save className="h-4 w-4" /> {editingId ? 'Atualizar figurinha' : 'Criar figurinha'}</>
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Minhas figurinhas ({myStickers.length})</CardTitle>
          <CardDescription>Gerencie as figurinhas que você criou</CardDescription>
        </CardHeader>
        <CardContent>
          {loadingMine ? (
            <div className="flex justify-center py-8"><Loader2 className="h-6 w-6 animate-spin" /></div>
          ) : myStickers.length === 0 ? (
            <p className="text-sm text-muted-foreground text-center py-6">
              Você ainda não criou nenhuma figurinha. Use o formulário acima!
            </p>
          ) : (
            <div className="grid gap-3 sm:grid-cols-2 md:grid-cols-3">
              {myStickers.map((sticker) => (
                <Card key={sticker.id} className="overflow-hidden">
                  <div className="aspect-square bg-gradient-to-br from-[#009739]/15 via-[#FEDD00]/10 to-[#012169]/15 dark:from-[#009739]/25 dark:via-[#FEDD00]/15 dark:to-[#012169]/25 relative">
                    <img
                      src={sticker.image_url}
                      alt={sticker.athlete_name}
                      className="absolute inset-0 w-full h-full object-cover"
                      loading="lazy"
                    />
                  </div>
                  <CardContent className="p-3 space-y-2">
                    <div>
                      <h4 className="font-semibold text-sm truncate">{sticker.athlete_name}</h4>
                      <div className="flex items-center gap-2 mt-1">
                        <Badge variant="secondary" className="text-xs">{sticker.team}</Badge>
                        {sticker.number !== null && (
                          <span className="text-xs text-muted-foreground">#{sticker.number}</span>
                        )}
                      </div>
                    </div>
                    <div className="flex gap-1">
                      <Button size="sm" variant="outline" onClick={() => handleEdit(sticker)} className="flex-1">
                        <Edit3 className="h-3 w-3" /> Editar
                      </Button>
                      <Button size="sm" variant="destructive" onClick={() => handleDelete(sticker.id)} className="flex-1">
                        <Trash2 className="h-3 w-3" /> Excluir
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
