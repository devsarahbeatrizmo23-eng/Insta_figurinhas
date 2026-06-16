import { useState, useEffect, useRef, FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload, Loader2, Save } from 'lucide-react'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Textarea } from '../components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card'
import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar'
import { TEAMS } from '../lib/types'
import { getInitials } from '../lib/utils'

export default function EditProfile() {
  const { user, profile, refreshProfile } = useAuth()
  const navigate = useNavigate()
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [formData, setFormData] = useState({
    username: '',
    full_name: '',
    bio: '',
    favorite_team: '',
  })
  const [avatarFile, setAvatarFile] = useState<File | null>(null)
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)

  useEffect(() => {
    if (profile) {
      setFormData({
        username: profile.username || '',
        full_name: profile.full_name || '',
        bio: profile.bio || '',
        favorite_team: profile.favorite_team || '',
      })
      setAvatarPreview(profile.avatar_url)
    }
  }, [profile])

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    if (file.size > 5 * 1024 * 1024) {
      setMessage({ type: 'error', text: 'A imagem deve ter no máximo 5MB' })
      return
    }
    setAvatarFile(file)
    setAvatarPreview(URL.createObjectURL(file))
  }

  const uploadAvatar = async (): Promise<string | null> => {
    if (!avatarFile || !user) return null
    const fileExt = avatarFile.name.split('.').pop()
    const filePath = `${user.id}/avatar.${fileExt}`

    const { error } = await supabase.storage
      .from('avatars')
      .upload(filePath, avatarFile, { upsert: true, contentType: avatarFile.type })

    if (error) {
      console.error('Erro no upload:', error)
      return null
    }

    const { data } = supabase.storage.from('avatars').getPublicUrl(filePath)
    return `${data.publicUrl}?t=${Date.now()}`
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!user) return
    setMessage(null)

    if (!/^[a-zA-Z0-9_]{3,20}$/.test(formData.username)) {
      setMessage({ type: 'error', text: 'Nome de usuário inválido (3-20 caracteres: letras, números, _)' })
      return
    }

    setLoading(true)
    try {
      let avatar_url = profile?.avatar_url || null
      if (avatarFile) {
        const uploaded = await uploadAvatar()
        if (uploaded) avatar_url = uploaded
      }

      const { error } = await supabase
        .from('profiles')
        .update({
          username: formData.username,
          full_name: formData.full_name || null,
          bio: formData.bio || null,
          favorite_team: formData.favorite_team || null,
          avatar_url,
        })
        .eq('id', user.id)

      if (error) throw error

      await refreshProfile()
      setMessage({ type: 'success', text: 'Perfil atualizado com sucesso!' })

      setTimeout(() => {
        navigate(`/profile/${formData.username}`, { replace: true })
      }, 800)
    } catch (err: any) {
      setMessage({ type: 'error', text: err?.message || 'Erro ao atualizar perfil' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <Card>
        <CardHeader>
          <CardTitle>Editar perfil</CardTitle>
          <CardDescription>Atualize suas informações pessoais</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="flex flex-col items-center gap-4">
              <Avatar className="h-24 w-24 border-4 border-muted">
                <AvatarImage src={avatarPreview || undefined} />
                <AvatarFallback className="text-2xl">
                  {getInitials(formData.full_name || formData.username)}
                </AvatarFallback>
              </Avatar>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleAvatarChange}
                className="hidden"
              />
              <Button
                type="button"
                variant="outline"
                onClick={() => fileInputRef.current?.click()}
                size="sm"
              >
                <Upload className="h-4 w-4 mr-2" /> Trocar avatar
              </Button>
              <p className="text-xs text-muted-foreground">JPG, PNG ou WEBP. Máximo 5MB.</p>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <label htmlFor="full_name" className="text-sm font-medium">Nome completo</label>
                <Input
                  id="full_name"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleChange}
                  placeholder="Seu nome"
                  maxLength={60}
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="username" className="text-sm font-medium">Nome de usuário</label>
                <Input
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  required
                  pattern="[a-zA-Z0-9_]+"
                  minLength={3}
                  maxLength={20}
                />
              </div>
            </div>

            <div className="space-y-2">
              <label htmlFor="bio" className="text-sm font-medium">Biografia</label>
              <Textarea
                id="bio"
                name="bio"
                value={formData.bio}
                onChange={handleChange}
                placeholder="Conte um pouco sobre você..."
                rows={3}
                maxLength={300}
              />
              <p className="text-xs text-muted-foreground text-right">{formData.bio.length}/300</p>
            </div>

            <div className="space-y-2">
              <label htmlFor="favorite_team" className="text-sm font-medium">Seleção favorita</label>
              <select
                id="favorite_team"
                name="favorite_team"
                value={formData.favorite_team}
                onChange={handleChange}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              >
                <option value="">Selecione uma seleção</option>
                {TEAMS.map((team) => (
                  <option key={team} value={team}>{team}</option>
                ))}
              </select>
            </div>

            {message && (
              <div className={`text-sm p-3 rounded-md border ${
                message.type === 'success'
                  ? 'text-green-700 bg-green-100 border-green-300 dark:bg-green-900/30 dark:text-green-300'
                  : 'text-destructive bg-destructive/10 border-destructive/20'
              }`}>
                {message.text}
              </div>
            )}

            <div className="flex flex-col-reverse sm:flex-row gap-2">
              <Button type="button" variant="outline" onClick={() => navigate(-1)} className="sm:w-auto">
                Cancelar
              </Button>
              <Button type="submit" disabled={loading} className="sm:flex-1">
                {loading ? (
                  <><Loader2 className="h-4 w-4 animate-spin" /> Salvando...</>
                ) : (
                  <><Save className="h-4 w-4" /> Salvar alterações</>
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
