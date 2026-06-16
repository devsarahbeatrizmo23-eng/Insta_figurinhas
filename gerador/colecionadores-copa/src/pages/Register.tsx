import { useState, FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Trophy, Mail, Lock, User, Loader2 } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'

export default function Register() {
  const navigate = useNavigate()
  const { signUp } = useAuth()
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    username: '',
    fullName: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)

    if (formData.password !== formData.confirmPassword) {
      setError('As senhas não coincidem')
      return
    }
    if (formData.password.length < 6) {
      setError('A senha deve ter pelo menos 6 caracteres')
      return
    }
    if (!/^[a-zA-Z0-9_]{3,20}$/.test(formData.username)) {
      setError('Nome de usuário deve ter 3-20 caracteres (letras, números e _)')
      return
    }

    setLoading(true)
    try {
      await signUp(
        formData.email.trim(),
        formData.password,
        formData.username.trim(),
        formData.fullName.trim()
      )
      navigate('/', { replace: true })
    } catch (err: any) {
      if (err?.message?.includes('already registered')) {
        setError('Este e-mail já está cadastrado')
      } else if (err?.message?.includes('username')) {
        setError('Este nome de usuário já existe')
      } else {
        setError(err?.message || 'Erro ao criar conta')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#009739]/10 via-[#FEDD00]/10 to-[#012169]/10 dark:from-[#0F172A] dark:via-[#012169]/30 dark:to-[#0F172A] p-4 py-8 relative overflow-hidden">
      <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden>
        <div className="absolute -top-32 -left-32 h-64 w-64 rounded-full bg-[#009739]/20 blur-3xl" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-96 w-96 rounded-full bg-[#FEDD00]/20 blur-3xl" />
        <div className="absolute -bottom-32 -right-32 h-64 w-64 rounded-full bg-[#012169]/20 dark:bg-[#012169]/40 blur-3xl" />
      </div>
      <Card className="w-full max-w-md shadow-xl relative z-10 border-2 border-primary/20">
        <CardHeader className="text-center space-y-2">
          <div className="mx-auto h-16 w-16 rounded-full bg-gradient-to-br from-[#009739] via-[#FEDD00] to-[#012169] flex items-center justify-center shadow-lg ring-4 ring-background">
            <Trophy className="h-8 w-8 text-white drop-shadow" />
          </div>
          <CardTitle className="text-2xl">Crie sua conta</CardTitle>
          <CardDescription>Junte-se à comunidade de colecionadores</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="fullName" className="text-sm font-medium">Nome completo</label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  id="fullName"
                  name="fullName"
                  value={formData.fullName}
                  onChange={handleChange}
                  required
                  placeholder="João Silva"
                  className="pl-10"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label htmlFor="username" className="text-sm font-medium">Nome de usuário</label>
              <div className="relative">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-sm text-muted-foreground">@</span>
                <Input
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  required
                  placeholder="joaosilva"
                  pattern="[a-zA-Z0-9_]+"
                  minLength={3}
                  maxLength={20}
                  className="pl-10"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium">E-mail</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  placeholder="seu@email.com"
                  autoComplete="email"
                  className="pl-10"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium">Senha</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  id="password"
                  name="password"
                  type="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  placeholder="Mínimo 6 caracteres"
                  minLength={6}
                  autoComplete="new-password"
                  className="pl-10"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label htmlFor="confirmPassword" className="text-sm font-medium">Confirmar senha</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                  placeholder="••••••••"
                  autoComplete="new-password"
                  className="pl-10"
                />
              </div>
            </div>

            {error && (
              <p className="text-sm text-destructive bg-destructive/10 border border-destructive/20 p-3 rounded-md">
                {error}
              </p>
            )}

            <Button type="submit" className="w-full" size="lg" disabled={loading}>
              {loading ? (
                <><Loader2 className="h-4 w-4 animate-spin" /> Criando conta...</>
              ) : (
                'Criar conta'
              )}
            </Button>
          </form>

          <p className="mt-6 text-center text-sm text-muted-foreground">
            Já tem conta?{' '}
            <Link to="/login" className="text-primary hover:underline font-semibold">
              Entrar
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
