import { useState, FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Trophy, Mail, Lock, Loader2 } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'

export default function Login() {
  const navigate = useNavigate()
  const { signIn } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      await signIn(email.trim(), password)
      navigate('/', { replace: true })
    } catch (err: any) {
      setError(err?.message || 'Erro ao entrar')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#009739]/10 via-[#FEDD00]/10 to-[#012169]/10 dark:from-[#0F172A] dark:via-[#012169]/30 dark:to-[#0F172A] p-4 relative overflow-hidden">
      {/* Elementos decorativos da bandeira brasileira */}
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
          <CardTitle className="text-2xl">Bem-vindo de volta!</CardTitle>
          <CardDescription>Entre na sua conta de colecionador</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium">E-mail</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
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
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  minLength={6}
                  placeholder="••••••••"
                  autoComplete="current-password"
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
                <><Loader2 className="h-4 w-4 animate-spin" /> Entrando...</>
              ) : (
                'Entrar'
              )}
            </Button>
          </form>

          <div className="mt-6 text-center space-y-2 text-sm">
            <Link to="/forgot-password" className="text-primary hover:underline block">
              Esqueceu a senha?
            </Link>
            <div className="border-t pt-4 mt-4">
              <p className="text-muted-foreground">
                Não tem conta?{' '}
                <Link to="/register" className="text-primary hover:underline font-semibold">
                  Cadastre-se grátis
                </Link>
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
