import { useState, FormEvent } from 'react'
import { Link } from 'react-router-dom'
import { Mail, Loader2, ArrowLeft, CheckCircle2 } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'

export default function ForgotPassword() {
  const { resetPassword } = useAuth()
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    setMessage(null)
    setLoading(true)
    try {
      await resetPassword(email.trim())
      setMessage('Enviamos um link de recuperação para o seu e-mail. Verifique a caixa de entrada.')
    } catch (err: any) {
      setError(err?.message || 'Erro ao enviar e-mail de recuperação')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#009739]/10 via-[#FEDD00]/10 to-[#012169]/10 dark:from-[#0F172A] dark:via-[#012169]/30 dark:to-[#0F172A] p-4 relative overflow-hidden">
      <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden>
        <div className="absolute -top-32 -left-32 h-64 w-64 rounded-full bg-[#009739]/20 blur-3xl" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-96 w-96 rounded-full bg-[#FEDD00]/20 blur-3xl" />
        <div className="absolute -bottom-32 -right-32 h-64 w-64 rounded-full bg-[#012169]/20 dark:bg-[#012169]/40 blur-3xl" />
      </div>
      <Card className="w-full max-w-md shadow-xl relative z-10 border-2 border-primary/20">
        <CardHeader className="text-center space-y-2">
          <CardTitle className="text-2xl">Recuperar senha</CardTitle>
          <CardDescription>Enviaremos um link para o seu e-mail</CardDescription>
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
                  className="pl-10"
                />
              </div>
            </div>

            {error && (
              <p className="text-sm text-destructive bg-destructive/10 border border-destructive/20 p-3 rounded-md">
                {error}
              </p>
            )}
            {message && (
              <div className="text-sm text-green-700 bg-green-100 border border-green-300 dark:bg-green-900/30 dark:text-green-300 dark:border-green-700 p-3 rounded-md flex gap-2 items-start">
                <CheckCircle2 className="h-4 w-4 mt-0.5 flex-shrink-0" />
                <span>{message}</span>
              </div>
            )}

            <Button type="submit" className="w-full" size="lg" disabled={loading}>
              {loading ? (
                <><Loader2 className="h-4 w-4 animate-spin" /> Enviando...</>
              ) : (
                'Enviar link de recuperação'
              )}
            </Button>
          </form>

          <Link to="/login" className="mt-6 inline-flex items-center gap-2 text-sm text-primary hover:underline">
            <ArrowLeft className="h-4 w-4" /> Voltar para o login
          </Link>
        </CardContent>
      </Card>
    </div>
  )
}
