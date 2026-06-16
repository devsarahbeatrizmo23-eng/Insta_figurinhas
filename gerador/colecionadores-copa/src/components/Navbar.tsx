import { Link, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import {
  Home, Bookmark, MessageCircle, PlusCircle,
  LogOut, Trophy, Sun, Moon
} from 'lucide-react'
import { Button } from './ui/button'
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar'
import { useAuth } from '../context/AuthContext'
import { getInitials } from '../lib/utils'

type Theme = 'light' | 'dark'

export default function Navbar() {
  const { profile, signOut } = useAuth()
  const navigate = useNavigate()
  const [theme, setTheme] = useState<Theme>(() => {
    if (typeof document === 'undefined') return 'light'
    return document.documentElement.classList.contains('dark') ? 'dark' : 'light'
  })

  // Sincroniza estado se o tema mudar em outra aba
  useEffect(() => {
    const onStorage = () => {
      const t = (localStorage.getItem('theme') as Theme) || 'light'
      setTheme(t)
    }
    window.addEventListener('storage', onStorage)
    return () => window.removeEventListener('storage', onStorage)
  }, [])

  const toggleTheme = () => {
    const next: Theme = theme === 'light' ? 'dark' : 'light'
    setTheme(next)
    if (next === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
    try {
      localStorage.setItem('theme', next)
    } catch {}
  }

  const handleSignOut = async () => {
    try {
      await signOut()
      navigate('/login', { replace: true })
    } catch (err) {
      console.error('Erro ao sair:', err)
    }
  }

  return (
    <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80">
      <div className="container mx-auto max-w-5xl flex h-16 items-center justify-between px-4">
        <Link to="/" className="flex items-center gap-2 group">
          {/* Logo com gradiente tricolor da bandeira do Brasil */}
          <div className="h-9 w-9 rounded-full bg-gradient-to-br from-[#009739] via-[#FEDD00] to-[#012169] flex items-center justify-center shadow-sm group-hover:scale-105 transition-transform ring-2 ring-background">
            <Trophy className="h-5 w-5 text-white drop-shadow" />
          </div>
          <span className="font-bold text-base sm:text-lg hidden sm:inline bg-gradient-to-r from-[#009739] via-[#012169] to-[#FEDD00] bg-clip-text text-transparent">
            Colecionadores da Copa
          </span>
        </Link>

        <nav className="flex items-center gap-1">
          <Button variant="ghost" size="icon" asChild>
            <Link to="/" title="Feed"><Home className="h-5 w-5" /></Link>
          </Button>
          <Button variant="ghost" size="icon" asChild>
            <Link to="/collection" title="Minha coleção">
              <Bookmark className="h-5 w-5" />
            </Link>
          </Button>
          <Button variant="ghost" size="icon" asChild>
            <Link to="/messages" title="Mensagens">
              <MessageCircle className="h-5 w-5" />
            </Link>
          </Button>
          <Button variant="ghost" size="icon" asChild>
            <Link to="/create-sticker" title="Criar figurinha">
              <PlusCircle className="h-5 w-5" />
            </Link>
          </Button>

          {profile?.username && (
            <Button variant="ghost" size="icon" asChild>
              <Link to={`/profile/${profile.username}`} title="Meu perfil">
                <Avatar className="h-8 w-8">
                  <AvatarImage src={profile.avatar_url || undefined} alt={profile.username} />
                  <AvatarFallback className="text-xs">
                    {getInitials(profile.full_name || profile.username)}
                  </AvatarFallback>
                </Avatar>
              </Link>
            </Button>
          )}

          {/* Toggle de tema claro/escuro */}
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleTheme}
            title={theme === 'light' ? 'Ativar modo escuro' : 'Ativar modo claro'}
            aria-label="Alternar tema"
          >
            {theme === 'light' ? (
              <Moon className="h-5 w-5" />
            ) : (
              <Sun className="h-5 w-5 text-[#FEDD00]" />
            )}
          </Button>

          <Button variant="ghost" size="icon" onClick={handleSignOut} title="Sair">
            <LogOut className="h-5 w-5" />
          </Button>
        </nav>
      </div>
    </header>
  )
}
