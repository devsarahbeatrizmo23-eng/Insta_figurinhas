#!/usr/bin/env python3
"""
Colecionadores da Copa - Project Generator
Gera toda a estrutura do projeto Vite + React + Supabase e cria um ZIP.
Uso: python3 generate_project.py
"""

import os
import zipfile
from pathlib import Path

PROJECT_NAME = "colecionadores-copa"
OUTPUT_ZIP = f"{PROJECT_NAME}.zip"
BASE_DIR = Path(PROJECT_NAME)

PROJECT_FILES = {}

def add(path, content):
    PROJECT_FILES[path] = content


# ============================================================
# CONFIGURAÇÕES DO PROJETO
# ============================================================

add("package.json", '''{
  "name": "colecionadores-copa",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "tsc --noEmit"
  },
  "dependencies": {
    "@radix-ui/react-avatar": "^1.0.4",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-slot": "^1.0.2",
    "@radix-ui/react-tabs": "^1.0.4",
    "@supabase/supabase-js": "^2.39.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "lucide-react": "^0.344.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.0",
    "tailwind-merge": "^2.2.1"
  },
  "devDependencies": {
    "@types/node": "^20.11.0",
    "@types/react": "^18.2.56",
    "@types/react-dom": "^18.2.19",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.17",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.2.2",
    "vite": "^5.1.4"
  }
}
''')

add("vite.config.ts", '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173,
  },
})
''')

add("tsconfig.json", '''{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
''')

add("tsconfig.node.json", '''{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true,
    "strict": true
  },
  "include": ["vite.config.ts"]
}
''')

add("tailwind.config.js", '''/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx,js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [],
}
''')

add("postcss.config.js", '''export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
''')

add("index.html", '''<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="Rede social para colecionadores de figurinhas digitais da Copa do Mundo" />
    <title>Colecionadores da Copa</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
''')

add("index.html", '''<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="Rede social para colecionadores de figurinhas digitais da Copa do Mundo" />
    <meta name="theme-color" content="#009739" />
    <title>Colecionadores da Copa</title>
    <script>
      // Inicializa o tema antes do React carregar (evita flash)
      (function () {
        try {
          var t = localStorage.getItem('theme');
          if (!t) t = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
          if (t === 'dark') document.documentElement.classList.add('dark');
        } catch (e) {}
      })();
    </script>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
''')

add(".env.example", '''VITE_SUPABASE_URL=
VITE_SUPABASE_ANON_KEY=
''')

add(".gitignore", '''# Logs
logs
*.log
npm-debug.log*

# Dependencies
node_modules
dist
dist-ssr
*.local

# Editor
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

# Env
.env
.env.local
.env.*.local

# Build
build
out
''')

# ============================================================
# ENTRY POINT - main.tsx, App.tsx, index.css
# ============================================================

add("src/main.tsx", '''import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.tsx'
import './index.css'
import { AuthProvider } from './context/AuthContext.tsx'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
''')

add("src/App.tsx", '''import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Login from './pages/Login'
import Register from './pages/Register'
import ForgotPassword from './pages/ForgotPassword'
import Feed from './pages/Feed'
import Profile from './pages/Profile'
import EditProfile from './pages/EditProfile'
import MyCollection from './pages/MyCollection'
import Messages from './pages/Messages'
import CreateSticker from './pages/CreateSticker'
import Layout from './components/Layout'

function App() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="text-center space-y-4">
          <div className="mx-auto h-16 w-16 rounded-full bg-gradient-to-br from-[#009739] via-[#FEDD00] to-[#012169] flex items-center justify-center animate-pulse shadow-lg">
            <span className="text-white font-bold text-2xl">⚽</span>
          </div>
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto" />
          <p className="text-muted-foreground text-sm">Carregando...</p>
        </div>
      </div>
    )
  }

  return (
    <Routes>
      <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
      <Route path="/register" element={!user ? <Register /> : <Navigate to="/" />} />
      <Route path="/forgot-password" element={!user ? <ForgotPassword /> : <Navigate to="/" />} />

      <Route element={<Layout />}>
        <Route path="/" element={user ? <Feed /> : <Navigate to="/login" />} />
        <Route path="/profile/:username" element={user ? <Profile /> : <Navigate to="/login" />} />
        <Route path="/edit-profile" element={user ? <EditProfile /> : <Navigate to="/login" />} />
        <Route path="/collection" element={user ? <MyCollection /> : <Navigate to="/login" />} />
        <Route path="/messages" element={user ? <Messages /> : <Navigate to="/login" />} />
        <Route path="/messages/:userId" element={user ? <Messages /> : <Navigate to="/login" />} />
        <Route path="/create-sticker" element={user ? <CreateSticker /> : <Navigate to="/login" />} />
      </Route>

      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  )
}

export default App
''')

add("src/index.css", '''@tailwind base;
@tailwind components;
@tailwind utilities;

/*
 * Paleta oficial do projeto — Cores da bandeira do Brasil
 *  Verde Brasil:   #009739  (primary)
 *  Amarelo:        #FEDD00  (accent)
 *  Azul:           #012169  (secondary)
 *  Branco:         #FFFFFF  (background light)
 *  Dark mode bg:   #0F172A  (substitui branco no modo escuro)
 */

@layer base {
  :root {
    /* Fundo branco no modo claro */
    --background: 0 0% 100%;
    --foreground: 222 47% 11%;
    --card: 0 0% 100%;
    --card-foreground: 222 47% 11%;
    --popover: 0 0% 100%;
    --popover-foreground: 222 47% 11%;

    /* Verde Brasil #009739 = HSL(143, 100%, 30%) */
    --primary: 143 100% 30%;
    --primary-foreground: 0 0% 100%;

    /* Azul #012169 = HSL(221, 98%, 21%) */
    --secondary: 221 98% 21%;
    --secondary-foreground: 0 0% 100%;

    /* Amarelo #FEDD00 = HSL(52, 100%, 50%) */
    --accent: 52 100% 50%;
    --accent-foreground: 221 98% 21%;

    --muted: 210 40% 96%;
    --muted-foreground: 215 16% 47%;

    --destructive: 0 84% 60%;
    --destructive-foreground: 0 0% 100%;

    --border: 214 32% 91%;
    --input: 214 32% 91%;
    --ring: 143 100% 30%;

    --radius: 0.5rem;
  }

  /* Dark mode: branco substituído por #0F172A */
  .dark {
    --background: 222 47% 11%;       /* #0F172A */
    --foreground: 0 0% 100%;
    --card: 222 47% 14%;
    --card-foreground: 0 0% 100%;
    --popover: 222 47% 11%;
    --popover-foreground: 0 0% 100%;

    /* Verde Brasil mais vivo para contrastar no escuro */
    --primary: 143 90% 38%;
    --primary-foreground: 0 0% 100%;

    /* Azul mais claro para contraste no escuro */
    --secondary: 221 80% 50%;
    --secondary-foreground: 0 0% 100%;

    /* Amarelo continua vibrante */
    --accent: 52 100% 50%;
    --accent-foreground: 221 98% 21%;

    --muted: 217 33% 17%;
    --muted-foreground: 215 20% 65%;

    --destructive: 0 63% 31%;
    --destructive-foreground: 0 0% 100%;

    --border: 217 33% 17%;
    --input: 217 33% 17%;
    --ring: 143 90% 38%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground antialiased;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }
  html {
    scroll-behavior: smooth;
  }
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: hsl(var(--muted));
}
::-webkit-scrollbar-thumb {
  background: hsl(var(--muted-foreground) / 0.3);
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--muted-foreground) / 0.5);
}
''')

# ============================================================
# LIB UTILITIES
# ============================================================

add("src/lib/utils.ts", '''import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatRelativeTime(dateStr: string): string {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = Math.floor((now.getTime() - date.getTime()) / 1000)

  if (diff < 5) return "agora"
  if (diff < 60) return `${diff}s`
  if (diff < 3600) return `${Math.floor(diff / 60)}m`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h`
  if (diff < 604800) return `${Math.floor(diff / 86400)}d`
  return date.toLocaleDateString("pt-BR")
}

export function getInitials(name?: string | null): string {
  if (!name) return "?"
  return name
    .split(" ")
    .map((p) => p[0])
    .slice(0, 2)
    .join("")
    .toUpperCase()
}
''')

add("src/lib/supabaseClient.ts", '''import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL as string
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string

if (!supabaseUrl || supabaseUrl === 'sua_url_aqui') {
  console.error('⚠️ VITE_SUPABASE_URL não configurada. Edite o arquivo .env')
}
if (!supabaseAnonKey || supabaseAnonKey === 'sua_chave_aqui') {
  console.error('⚠️ VITE_SUPABASE_ANON_KEY não configurada. Edite o arquivo .env')
}

export const supabase = createClient(
  supabaseUrl || 'https://placeholder.supabase.co',
  supabaseAnonKey || 'placeholder'
)
''')

add("src/lib/types.ts", '''export type Profile = {
  id: string
  username: string
  full_name: string | null
  avatar_url: string | null
  bio: string | null
  favorite_team: string | null
  created_at: string
}

export type Sticker = {
  id: string
  creator_id: string
  athlete_name: string
  team: string
  position: string | null
  number: number | null
  image_url: string
  description: string | null
  created_at: string
  creator?: Profile
}

export type CollectionStatus = 'TENHO' | 'QUERO' | 'REPETIDA'

export type UserCollection = {
  user_id: string
  sticker_id: string
  status: CollectionStatus
  updated_at: string
}

export type Like = {
  user_id: string
  sticker_id: string
  created_at: string
}

export type Comment = {
  id: string
  sticker_id: string
  user_id: string
  content: string
  created_at: string
  user?: Profile
}

export type Follow = {
  follower_id: string
  following_id: string
  created_at: string
}

export type Message = {
  id: string
  sender_id: string
  receiver_id: string
  content: string
  is_read: boolean
  created_at: string
}

export const TEAMS = [
  'Brasil', 'Argentina', 'França', 'Espanha', 'Alemanha', 'Inglaterra',
  'Itália', 'Holanda', 'Portugal', 'Bélgica', 'México', 'EUA',
  'Japão', 'Coreia do Sul', 'Catar', 'Arábia Saudita', 'Marrocos',
  'Croácia', 'Suíça', 'Polônia', 'Senegal', 'Gana', 'Camarões'
]

export const POSITIONS = [
  'Goleiro', 'Lateral Direito', 'Lateral Esquerdo', 'Zagueiro',
  'Volante', 'Meia', 'Atacante', 'Centroavante', 'Ponta'
]
''')

# ============================================================
# CONTEXT - AuthContext
# ============================================================

add("src/context/AuthContext.tsx", '''import { createContext, useContext, useEffect, useState, ReactNode, useCallback } from 'react'
import { User, Session, AuthError } from '@supabase/supabase-js'
import { supabase } from '../lib/supabaseClient'
import { Profile } from '../lib/types'

type AuthContextType = {
  user: User | null
  profile: Profile | null
  session: Session | null
  loading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signUp: (email: string, password: string, username: string, fullName: string) => Promise<void>
  signOut: () => Promise<void>
  resetPassword: (email: string) => Promise<void>
  refreshProfile: () => Promise<void>
  updateProfile: (updates: Partial<Profile>) => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [session, setSession] = useState<Session | null>(null)
  const [profile, setProfile] = useState<Profile | null>(null)
  const [loading, setLoading] = useState(true)

  const fetchProfile = useCallback(async (userId: string) => {
    try {
      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', userId)
        .maybeSingle()

      if (error) {
        console.error('Erro ao buscar perfil:', error.message)
        return null
      }
      setProfile(data)
      return data
    } catch (err) {
      console.error('Exceção ao buscar perfil:', err)
      return null
    }
  }, [])

  useEffect(() => {
    let mounted = true

    supabase.auth.getSession().then(({ data: { session: s } }) => {
      if (!mounted) return
      setSession(s)
      setUser(s?.user ?? null)
      if (s?.user) {
        fetchProfile(s.user.id).finally(() => setLoading(false))
      } else {
        setLoading(false)
      }
    })

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (_event, s) => {
        if (!mounted) return
        setSession(s)
        setUser(s?.user ?? null)
        if (s?.user) {
          await fetchProfile(s.user.id)
        } else {
          setProfile(null)
        }
      }
    )

    return () => {
      mounted = false
      subscription.unsubscribe()
    }
  }, [fetchProfile])

  const signIn = async (email: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) throw error
  }

  const signUp = async (email: string, password: string, username: string, fullName: string) => {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          username,
          full_name: fullName,
        },
      },
    })
    if (error) throw error
    // O trigger handle_new_user() no banco cria o perfil automaticamente
    // Pequeno delay para garantir que o trigger executou
    if (data.user) {
      await new Promise((r) => setTimeout(r, 500))
      await fetchProfile(data.user.id)
    }
  }

  const signOut = async () => {
    await supabase.auth.signOut()
    setProfile(null)
  }

  const resetPassword = async (email: string) => {
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/login`,
    })
    if (error) throw error
  }

  const refreshProfile = async () => {
    if (user) await fetchProfile(user.id)
  }

  const updateProfile = async (updates: Partial<Profile>) => {
    if (!user) throw new Error('Não autenticado')
    const { error } = await supabase
      .from('profiles')
      .update(updates)
      .eq('id', user.id)
    if (error) throw error
    await fetchProfile(user.id)
  }

  const handleError = (err: unknown): AuthError => {
    if (err instanceof AuthError) return err
    return new AuthError(String(err))
  }
  void handleError

  return (
    <AuthContext.Provider
      value={{
        user,
        profile,
        session,
        loading,
        signIn,
        signUp,
        signOut,
        resetPassword,
        refreshProfile,
        updateProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider')
  }
  return context
}
''')

# ============================================================
# UI COMPONENTS (shadcn-style)
# ============================================================

add("src/components/ui/button.tsx", '''import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
''')

add("src/components/ui/card.tsx", '''import * as React from "react"
import { cn } from "@/lib/utils"

const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("rounded-lg border bg-card text-card-foreground shadow-sm", className)}
      {...props}
    />
  )
)
Card.displayName = "Card"

const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
  )
)
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("font-semibold leading-none tracking-tight", className)} {...props} />
  )
)
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} />
  )
)
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
  )
)
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex items-center p-6 pt-0", className)} {...props} />
  )
)
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }
''')

add("src/components/ui/input.tsx", '''import * as React from "react"
import { cn } from "@/lib/utils"

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input }
''')

add("src/components/ui/textarea.tsx", '''import * as React from "react"
import { cn } from "@/lib/utils"

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        className={cn(
          "flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 resize-none",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Textarea.displayName = "Textarea"

export { Textarea }
''')

add("src/components/ui/avatar.tsx", '''import * as React from "react"
import * as AvatarPrimitive from "@radix-ui/react-avatar"
import { cn } from "@/lib/utils"

const Avatar = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Root>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Root
    ref={ref}
    className={cn("relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full", className)}
    {...props}
  />
))
Avatar.displayName = AvatarPrimitive.Root.displayName

const AvatarImage = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Image>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Image>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Image
    ref={ref}
    className={cn("aspect-square h-full w-full", className)}
    {...props}
  />
))
AvatarImage.displayName = AvatarPrimitive.Image.displayName

const AvatarFallback = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Fallback>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Fallback>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Fallback
    ref={ref}
    className={cn(
      "flex h-full w-full items-center justify-center rounded-full bg-muted text-muted-foreground font-medium",
      className
    )}
    {...props}
  />
))
AvatarFallback.displayName = AvatarPrimitive.Fallback.displayName

export { Avatar, AvatarImage, AvatarFallback }
''')

add("src/components/ui/badge.tsx", '''import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default: "border-transparent bg-primary text-primary-foreground hover:bg-primary/80",
        secondary: "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
        destructive: "border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80",
        outline: "text-foreground border-border",
        success: "border-transparent bg-green-500 text-white hover:bg-green-600",
        warning: "border-transparent bg-orange-500 text-white hover:bg-orange-600",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />
}

export { Badge, badgeVariants }
''')

add("src/components/ui/tabs.tsx", '''import * as React from "react"
import * as TabsPrimitive from "@radix-ui/react-tabs"
import { cn } from "@/lib/utils"

const Tabs = TabsPrimitive.Root

const TabsList = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.List>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.List>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.List
    ref={ref}
    className={cn(
      "inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground",
      className
    )}
    {...props}
  />
))
TabsList.displayName = TabsPrimitive.List.displayName

const TabsTrigger = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Trigger>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Trigger
    ref={ref}
    className={cn(
      "inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm",
      className
    )}
    {...props}
  />
))
TabsTrigger.displayName = TabsPrimitive.Trigger.displayName

const TabsContent = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Content>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Content
    ref={ref}
    className={cn(
      "mt-4 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
      className
    )}
    {...props}
  />
))
TabsContent.displayName = TabsPrimitive.Content.displayName

export { Tabs, TabsList, TabsTrigger, TabsContent }
''')

add("src/components/ui/dialog.tsx", '''import * as React from "react"
import * as DialogPrimitive from "@radix-ui/react-dialog"
import { X } from "lucide-react"
import { cn } from "@/lib/utils"

const Dialog = DialogPrimitive.Root
const DialogTrigger = DialogPrimitive.Trigger
const DialogPortal = DialogPrimitive.Portal
const DialogClose = DialogPrimitive.Close

const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      "fixed inset-0 z-50 bg-black/60 backdrop-blur-sm data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className
    )}
    {...props}
  />
))
DialogOverlay.displayName = DialogPrimitive.Overlay.displayName

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        "fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 sm:rounded-lg",
        className
      )}
      {...props}
    >
      {children}
      <DialogPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2">
        <X className="h-4 w-4" />
        <span className="sr-only">Fechar</span>
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPortal>
))
DialogContent.displayName = DialogPrimitive.Content.displayName

const DialogHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("flex flex-col space-y-1.5 text-center sm:text-left", className)} {...props} />
)
DialogHeader.displayName = "DialogHeader"

const DialogFooter = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2", className)} {...props} />
)
DialogFooter.displayName = "DialogFooter"

const DialogTitle = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Title
    ref={ref}
    className={cn("text-lg font-semibold leading-none tracking-tight", className)}
    {...props}
  />
))
DialogTitle.displayName = DialogPrimitive.Title.displayName

const DialogDescription = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Description>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Description
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
))
DialogDescription.displayName = DialogPrimitive.Description.displayName

export {
  Dialog,
  DialogPortal,
  DialogOverlay,
  DialogTrigger,
  DialogClose,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
}
''')

add("src/components/ui/label.tsx", '''import * as React from "react"
import { cn } from "@/lib/utils"

const Label = React.forwardRef<
  HTMLLabelElement,
  React.LabelHTMLAttributes<HTMLLabelElement>
>(({ className, ...props }, ref) => (
  <label
    ref={ref}
    className={cn(
      "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
      className
    )}
    {...props}
  />
))
Label.displayName = "Label"

export { Label }
''')

# ============================================================
# MAIN COMPONENTS
# ============================================================

add("src/components/Layout.tsx", '''import { Outlet, useLocation } from 'react-router-dom'
import Navbar from './Navbar'
import { useEffect } from 'react'

export default function Layout() {
  const location = useLocation()

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' as ScrollBehavior })
  }, [location.pathname])

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />
      <main className="flex-1 container mx-auto px-4 py-6 max-w-5xl w-full">
        <Outlet />
      </main>
      <footer className="border-t py-4 text-center text-xs text-muted-foreground">
        ⚽ Colecionadores da Copa &middot; feito com Supabase + React
      </footer>
    </div>
  )
}
''')

add("src/components/Navbar.tsx", '''import { Link, useNavigate } from 'react-router-dom'
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
''')

add("src/components/StickerCard.tsx", '''import { useState, useEffect } from 'react'
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
''')

add("src/components/CommentSection.tsx", '''import { useState, useEffect, useRef } from 'react'
import { Send, Loader2 } from 'lucide-react'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'
import { Comment, Profile } from '../lib/types'
import { formatRelativeTime, getInitials } from '../lib/utils'

type CommentWithUser = Comment & { user: Profile | null }

interface CommentSectionProps {
  stickerId: string
  onCommentAdded?: () => void
}

export default function CommentSection({ stickerId, onCommentAdded }: CommentSectionProps) {
  const { user, profile: me } = useAuth()
  const [comments, setComments] = useState<CommentWithUser[]>([])
  const [newComment, setNewComment] = useState('')
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    void fetchComments()

    const channel = supabase
      .channel(`comments:${stickerId}`)
      .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'comments',
        filter: `sticker_id=eq.${stickerId}`,
      }, (payload) => {
        // Insere o novo comentário na lista sem refazer fetch
        const newRow = payload.new as Comment
        setComments((prev) => {
          if (prev.find((c) => c.id === newRow.id)) return prev
          return [
            ...prev,
            { ...newRow, user: me }
          ]
        })
      })
      .subscribe()

    return () => {
      void supabase.removeChannel(channel)
    }
  }, [stickerId])

  const fetchComments = async () => {
    setLoading(true)
    try {
      const { data, error } = await supabase
        .from('comments')
        .select('*, user:profiles(*)')
        .eq('sticker_id', stickerId)
        .order('created_at', { ascending: true })

      if (error) throw error
      setComments((data as CommentWithUser[]) || [])
    } catch (err) {
      console.error('Erro ao buscar comentários:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const text = newComment.trim()
    if (!text || !user || submitting) return
    setSubmitting(true)
    try {
      const { data, error } = await supabase
        .from('comments')
        .insert({
          sticker_id: stickerId,
          user_id: user.id,
          content: text,
        })
        .select('*, user:profiles(*)')
        .single()

      if (error) throw error
      setComments((prev) => [...prev, data as CommentWithUser])
      setNewComment('')
      onCommentAdded?.()
      inputRef.current?.focus()
    } catch (err) {
      console.error('Erro ao comentar:', err)
      alert('Não foi possível enviar o comentário.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="space-y-3">
      <form onSubmit={handleSubmit} className="flex gap-2 items-center">
        <Avatar className="h-8 w-8 flex-shrink-0">
          <AvatarImage src={me?.avatar_url || undefined} />
          <AvatarFallback className="text-xs">
            {getInitials(me?.full_name || me?.username)}
          </AvatarFallback>
        </Avatar>
        <Input
          ref={inputRef}
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          placeholder="Comente algo..."
          disabled={submitting}
          className="flex-1"
          maxLength={500}
        />
        <Button
          type="submit"
          size="icon"
          disabled={!newComment.trim() || submitting}
          aria-label="Enviar comentário"
        >
          {submitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
        </Button>
      </form>

      {loading ? (
        <div className="flex justify-center py-2">
          <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
        </div>
      ) : comments.length === 0 ? (
        <p className="text-xs text-muted-foreground text-center py-3">
          Nenhum comentário ainda. Seja o primeiro!
        </p>
      ) : (
        <ul className="space-y-2 max-h-72 overflow-y-auto">
          {comments.map((c) => (
            <li key={c.id} className="flex gap-2 text-sm">
              <Avatar className="h-7 w-7 flex-shrink-0">
                <AvatarImage src={c.user?.avatar_url || undefined} />
                <AvatarFallback className="text-xs">
                  {getInitials(c.user?.full_name || c.user?.username)}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 bg-background rounded-lg px-3 py-2 border">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-xs">
                    {c.user?.full_name || c.user?.username || 'Usuário'}
                  </span>
                  <span className="text-xs text-muted-foreground">
                    {formatRelativeTime(c.created_at)}
                  </span>
                </div>
                <p className="break-words">{c.content}</p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
''')

# ============================================================
# PAGES
# ============================================================

add("src/pages/Login.tsx", '''import { useState, FormEvent } from 'react'
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
''')

add("src/pages/Register.tsx", '''import { useState, FormEvent } from 'react'
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
''')

add("src/pages/ForgotPassword.tsx", '''import { useState, FormEvent } from 'react'
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
''')

add("src/pages/Feed.tsx", '''import { useEffect, useState } from 'react'
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
''')

add("src/pages/Profile.tsx", '''import { useEffect, useState, useCallback } from 'react'
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
''')

add("src/pages/EditProfile.tsx", '''import { useState, useEffect, useRef, FormEvent } from 'react'
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
''')

add("src/pages/MyCollection.tsx", '''import { useEffect, useState, useMemo } from 'react'
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
''')

add("src/pages/Messages.tsx", '''import { useEffect, useState, useRef, FormEvent } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Send, Loader2, MessageSquare, ArrowLeft } from 'lucide-react'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'
import { Message, Profile } from '../lib/types'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Card } from '../components/ui/card'
import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar'
import { cn, getInitials, formatRelativeTime } from '../lib/utils'

interface Conversation {
  other: Profile
  last_message: Message
  unread_count: number
}

export default function Messages() {
  const { userId } = useParams<{ userId?: string }>()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeConversation, setActiveConversation] = useState<Profile | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [newMessage, setNewMessage] = useState('')
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => { void fetchConversations() }, [user])

  useEffect(() => {
    if (userId) {
      void loadConversation(userId)
    }
  }, [userId])

  useEffect(() => {
    if (!activeConversation || !user) return

    void fetchMessages(activeConversation.id)

    // Marcar mensagens recebidas como lidas
    void supabase
      .from('messages')
      .update({ is_read: true })
      .eq('sender_id', activeConversation.id)
      .eq('receiver_id', user.id)
      .eq('is_read', false)

    const channel = supabase
      .channel(`messages:${user.id}:${activeConversation.id}`)
      .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'messages',
        filter: `or(and(sender_id.eq.${user.id},receiver_id.eq.${activeConversation.id}),and(sender_id.eq.${activeConversation.id},receiver_id.eq.${user.id}))`,
      }, (payload) => {
        const msg = payload.new as Message
        setMessages((prev) => {
          if (prev.find((m) => m.id === msg.id)) return prev
          return [...prev, msg]
        })
      })
      .subscribe()

    return () => { void supabase.removeChannel(channel) }
  }, [activeConversation])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const fetchConversations = async () => {
    setLoading(true)
    try {
      const { data, error } = await supabase
        .from('messages')
        .select('*')
        .or(`sender_id.eq.${user!.id},receiver_id.eq.${user!.id}`)
        .order('created_at', { ascending: false })

      if (error) throw error

      // Agrupar por outro usuário
      const grouped = new Map<string, Message>()
      ;((data as Message[]) || []).forEach((msg) => {
        const otherId = msg.sender_id === user!.id ? msg.receiver_id : msg.sender_id
        if (!grouped.has(otherId)) grouped.set(otherId, msg)
      })

      const otherIds = Array.from(grouped.keys())
      if (otherIds.length === 0) {
        setConversations([])
        return
      }

      const { data: profilesData } = await supabase
        .from('profiles')
        .select('*')
        .in('id', otherIds)

      const convs: Conversation[] = (profilesData || []).map((p) => ({
        other: p,
        last_message: grouped.get(p.id)!,
        unread_count: 0,
      }))

      // Contar não lidas
      for (const conv of convs) {
        const { count } = await supabase
          .from('messages')
          .select('*', { count: 'exact', head: true })
          .eq('sender_id', conv.other.id)
          .eq('receiver_id', user!.id)
          .eq('is_read', false)
        conv.unread_count = count || 0
      }

      convs.sort((a, b) =>
        new Date(b.last_message.created_at).getTime() -
        new Date(a.last_message.created_at).getTime()
      )
      setConversations(convs)
    } catch (err) {
      console.error('Erro ao buscar conversas:', err)
    } finally {
      setLoading(false)
    }
  }

  const loadConversation = async (otherUserId: string) => {
    try {
      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', otherUserId)
        .maybeSingle()

      if (error) throw error
      if (data) setActiveConversation(data)
    } catch (err) {
      console.error('Erro ao carregar conversa:', err)
    }
  }

  const fetchMessages = async (otherUserId: string) => {
    try {
      const { data, error } = await supabase
        .from('messages')
        .select('*')
        .or(`and(sender_id.eq.${user!.id},receiver_id.eq.${otherUserId}),and(sender_id.eq.${otherUserId},receiver_id.eq.${user!.id})`)
        .order('created_at', { ascending: true })

      if (error) throw error
      setMessages(data || [])
    } catch (err) {
      console.error('Erro ao buscar mensagens:', err)
    }
  }

  const sendMessage = async (e: FormEvent) => {
    e.preventDefault()
    const text = newMessage.trim()
    if (!text || !activeConversation || sending) return
    setSending(true)
    try {
      const { error } = await supabase.from('messages').insert({
        sender_id: user!.id,
        receiver_id: activeConversation.id,
        content: text,
        is_read: false,
      })
      if (error) throw error
      setNewMessage('')
      // Atualiza lista de conversas após enviar
      void fetchConversations()
    } catch (err) {
      console.error('Erro ao enviar mensagem:', err)
      alert('Não foi possível enviar a mensagem.')
    } finally {
      setSending(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    )
  }

  return (
    <Card className="overflow-hidden h-[calc(100vh-10rem)]">
      <div className="grid h-full md:grid-cols-[280px_1fr]">
        {/* Lista de conversas */}
        <div className={cn(
          "border-r overflow-y-auto bg-muted/20",
          activeConversation && "hidden md:block"
        )}>
          <div className="p-4 border-b font-semibold bg-background sticky top-0 z-10">
            Mensagens
          </div>
          {conversations.length === 0 ? (
            <div className="p-8 text-center text-sm text-muted-foreground space-y-2">
              <MessageSquare className="h-10 w-10 mx-auto opacity-40" />
              <p>Nenhuma conversa ainda</p>
              <p className="text-xs">
                Visite o perfil de alguém e clique em "Mensagem" para começar.
              </p>
            </div>
          ) : (
            <ul>
              {conversations.map((conv) => (
                <li key={conv.other.id}>
                  <button
                    onClick={() => {
                      setActiveConversation(conv.other)
                      navigate(`/messages/${conv.other.id}`, { replace: true })
                    }}
                    className={cn(
                      "w-full p-3 flex items-center gap-3 hover:bg-muted transition-colors text-left border-b",
                      activeConversation?.id === conv.other.id && "bg-muted"
                    )}
                  >
                    <Avatar className="h-10 w-10 flex-shrink-0">
                      <AvatarImage src={conv.other.avatar_url || undefined} />
                      <AvatarFallback className="text-xs">
                        {getInitials(conv.other.full_name || conv.other.username)}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-2">
                        <p className="font-medium text-sm truncate">
                          {conv.other.full_name || conv.other.username}
                        </p>
                        <span className="text-xs text-muted-foreground flex-shrink-0">
                          {formatRelativeTime(conv.last_message.created_at)}
                        </span>
                      </div>
                      <p className={cn(
                        "text-xs truncate",
                        conv.unread_count > 0 ? "text-foreground font-semibold" : "text-muted-foreground"
                      )}>
                        {conv.last_message.sender_id === user!.id && "Você: "}
                        {conv.last_message.content}
                      </p>
                    </div>
                    {conv.unread_count > 0 && (
                      <span className="bg-primary text-primary-foreground text-xs font-bold rounded-full h-5 min-w-[20px] px-1.5 flex items-center justify-center">
                        {conv.unread_count}
                      </span>
                    )}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Janela de chat */}
        <div className={cn(
          "flex flex-col h-full",
          !activeConversation && "hidden md:flex"
        )}>
          {activeConversation ? (
            <>
              <div className="p-3 border-b flex items-center gap-3 bg-background">
                <Button
                  variant="ghost"
                  size="icon"
                  className="md:hidden"
                  onClick={() => {
                    setActiveConversation(null)
                    navigate('/messages', { replace: true })
                  }}
                >
                  <ArrowLeft className="h-4 w-4" />
                </Button>
                <Avatar className="h-9 w-9">
                  <AvatarImage src={activeConversation.avatar_url || undefined} />
                  <AvatarFallback className="text-xs">
                    {getInitials(activeConversation.full_name || activeConversation.username)}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-sm truncate">
                    {activeConversation.full_name || activeConversation.username}
                  </p>
                  <p className="text-xs text-muted-foreground truncate">@{activeConversation.username}</p>
                </div>
              </div>

              <div className="flex-1 overflow-y-auto p-4 space-y-2 bg-muted/10">
                {messages.length === 0 ? (
                  <div className="text-center text-sm text-muted-foreground py-12">
                    <MessageSquare className="h-10 w-10 mx-auto opacity-40 mb-2" />
                    <p>Envie uma mensagem para iniciar a conversa!</p>
                  </div>
                ) : (
                  messages.map((msg, idx) => {
                    const isMine = msg.sender_id === user!.id
                    const prevMine = idx > 0 ? messages[idx - 1].sender_id === user!.id : false
                    const showAvatar = !isMine && !prevMine
                    return (
                      <div
                        key={msg.id}
                        className={cn("flex gap-2 items-end", isMine ? "justify-end" : "justify-start")}
                      >
                        {!isMine && (
                          <Avatar className={cn("h-7 w-7 flex-shrink-0", !showAvatar && "invisible")}>
                            <AvatarImage src={activeConversation.avatar_url || undefined} />
                            <AvatarFallback className="text-xs">
                              {getInitials(activeConversation.full_name || activeConversation.username)}
                            </AvatarFallback>
                          </Avatar>
                        )}
                        <div
                          className={cn(
                            "max-w-[75%] rounded-2xl px-3 py-2 text-sm shadow-sm",
                            isMine
                              ? "bg-primary text-primary-foreground rounded-br-sm"
                              : "bg-background border rounded-bl-sm"
                          )}
                        >
                          <p className="break-words whitespace-pre-wrap">{msg.content}</p>
                          <p className={cn(
                            "text-[10px] mt-1",
                            isMine ? "text-primary-foreground/70" : "text-muted-foreground"
                          )}>
                            {new Date(msg.created_at).toLocaleTimeString('pt-BR', {
                              hour: '2-digit', minute: '2-digit'
                            })}
                          </p>
                        </div>
                      </div>
                    )
                  })
                )}
                <div ref={messagesEndRef} />
              </div>

              <form onSubmit={sendMessage} className="p-3 border-t bg-background flex gap-2">
                <Input
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Digite uma mensagem..."
                  disabled={sending}
                  maxLength={1000}
                  autoFocus
                />
                <Button type="submit" disabled={!newMessage.trim() || sending} size="icon">
                  {sending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                </Button>
              </form>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center text-muted-foreground">
              <div className="text-center space-y-2">
                <MessageSquare className="h-16 w-16 mx-auto opacity-30" />
                <p>Selecione uma conversa para começar</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </Card>
  )
}
''')

add("src/pages/CreateSticker.tsx", '''import { useState, useEffect, useRef, FormEvent } from 'react'
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
''')

# ============================================================
# SQL MIGRATION
# ============================================================

add("supabase/migrations/001_initial_schema.sql", """-- =====================================================
-- Colecionadores da Copa - Schema inicial do banco
-- Execute no SQL Editor do Supabase
-- =====================================================

-- Habilita extensão para UUID
CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";

-- Tipo ENUM para status da coleção
DO $$ BEGIN
  CREATE TYPE collection_status AS ENUM ('TENHO', 'QUERO', 'REPETIDA');
EXCEPTION
  WHEN duplicate_object THEN null;
END $$;

-- =====================================================
-- TABELA: profiles
-- =====================================================
CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username TEXT UNIQUE NOT NULL,
  full_name TEXT,
  avatar_url TEXT,
  bio TEXT,
  favorite_team TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY \"Profiles visíveis para todos\" ON public.profiles
  FOR SELECT USING (true);

CREATE POLICY \"Usuários podem inserir seu próprio perfil\" ON public.profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY \"Usuários podem atualizar seu próprio perfil\" ON public.profiles
  FOR UPDATE USING (auth.uid() = id);

-- Trigger: cria perfil automaticamente ao registrar usuário
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $func$
BEGIN
  INSERT INTO public.profiles (id, username, full_name)
  VALUES (
    NEW.id,
    LOWER(COALESCE(NEW.raw_user_meta_data->>'username', split_part(NEW.email, '@', 1))),
    NEW.raw_user_meta_data->>'full_name'
  )
  ON CONFLICT (id) DO NOTHING;
  RETURN NEW;
END;
$func$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- =====================================================
-- TABELA: stickers
-- =====================================================
CREATE TABLE IF NOT EXISTS public.stickers (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  creator_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  athlete_name TEXT NOT NULL,
  team TEXT NOT NULL,
  position TEXT,
  number INTEGER CHECK (number IS NULL OR (number >= 0 AND number <= 99)),
  image_url TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stickers_creator ON public.stickers(creator_id);
CREATE INDEX IF NOT EXISTS idx_stickers_team ON public.stickers(team);
CREATE INDEX IF NOT EXISTS idx_stickers_created ON public.stickers(created_at DESC);

ALTER TABLE public.stickers ENABLE ROW LEVEL SECURITY;

CREATE POLICY \"Figurinhas visíveis para todos\" ON public.stickers
  FOR SELECT USING (true);

CREATE POLICY \"Usuários autenticados podem criar figurinhas\" ON public.stickers
  FOR INSERT WITH CHECK (auth.uid() = creator_id);

CREATE POLICY \"Usuários podem atualizar suas figurinhas\" ON public.stickers
  FOR UPDATE USING (auth.uid() = creator_id);

CREATE POLICY \"Usuários podem excluir suas figurinhas\" ON public.stickers
  FOR DELETE USING (auth.uid() = creator_id);

-- =====================================================
-- TABELA: user_collections
-- =====================================================
CREATE TABLE IF NOT EXISTS public.user_collections (
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  sticker_id UUID NOT NULL REFERENCES public.stickers(id) ON DELETE CASCADE,
  status collection_status NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (user_id, sticker_id)
);

CREATE INDEX IF NOT EXISTS idx_user_collections_user ON public.user_collections(user_id);

ALTER TABLE public.user_collections ENABLE ROW LEVEL SECURITY;

CREATE POLICY \"Usuários veem apenas sua coleção\" ON public.user_collections
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY \"Usuários podem adicionar à sua coleção\" ON public.user_collections
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY \"Usuários podem atualizar sua coleção\" ON public.user_collections
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY \"Usuários podem remover da sua coleção\" ON public.user_collections
  FOR DELETE USING (auth.uid() = user_id);

-- =====================================================
-- TABELA: likes
-- =====================================================
CREATE TABLE IF NOT EXISTS public.likes (
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  sticker_id UUID NOT NULL REFERENCES public.stickers(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (user_id, sticker_id)
);

CREATE INDEX IF NOT EXISTS idx_likes_sticker ON public.likes(sticker_id);
CREATE INDEX IF NOT EXISTS idx_likes_user ON public.likes(user_id);

ALTER TABLE public.likes ENABLE ROW LEVEL SECURITY;

CREATE POLICY \"Likes visíveis para todos\" ON public.likes
  FOR SELECT USING (true);

CREATE POLICY \"Usuários podem curtir\" ON public.likes
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY \"Usuários podem descurtir\" ON public.likes
  FOR DELETE USING (auth.uid() = user_id);

-- =====================================================
-- TABELA: comments
-- =====================================================
CREATE TABLE IF NOT EXISTS public.comments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  sticker_id UUID NOT NULL REFERENCES public.stickers(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  content TEXT NOT NULL CHECK (length(content) > 0 AND length(content) <= 1000),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_comments_sticker ON public.comments(sticker_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_comments_user ON public.comments(user_id);

ALTER TABLE public.comments ENABLE ROW LEVEL SECURITY;

CREATE POLICY \"Comentários visíveis para todos\" ON public.comments
  FOR SELECT USING (true);

CREATE POLICY \"Usuários podem comentar\" ON public.comments
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY \"Usuários podem atualizar seus comentários\" ON public.comments
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY \"Usuários podem excluir seus comentários\" ON public.comments
  FOR DELETE USING (auth.uid() = user_id);

-- =====================================================
-- TABELA: follows
-- =====================================================
CREATE TABLE IF NOT EXISTS public.follows (
  follower_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  following_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (follower_id, following_id),
  CHECK (follower_id <> following_id)
);

CREATE INDEX IF NOT EXISTS idx_follows_follower ON public.follows(follower_id);
CREATE INDEX IF NOT EXISTS idx_follows_following ON public.follows(following_id);

ALTER TABLE public.follows ENABLE ROW LEVEL SECURITY;

CREATE POLICY \"Follows visíveis para todos\" ON public.follows
  FOR SELECT USING (true);

CREATE POLICY \"Usuários podem seguir outros\" ON public.follows
  FOR INSERT WITH CHECK (auth.uid() = follower_id);

CREATE POLICY \"Usuários podem deixar de seguir\" ON public.follows
  FOR DELETE USING (auth.uid() = follower_id);

-- =====================================================
-- TABELA: messages
-- =====================================================
CREATE TABLE IF NOT EXISTS public.messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  sender_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  receiver_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  content TEXT NOT NULL CHECK (length(content) > 0 AND length(content) <= 2000),
  is_read BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CHECK (sender_id <> receiver_id)
);

CREATE INDEX IF NOT EXISTS idx_messages_conversation ON public.messages(sender_id, receiver_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_messages_receiver ON public.messages(receiver_id, is_read);

ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY \"Usuários veem mensagens que enviaram ou receberam\" ON public.messages
  FOR SELECT USING (auth.uid() = sender_id OR auth.uid() = receiver_id);

CREATE POLICY \"Usuários podem enviar mensagens\" ON public.messages
  FOR INSERT WITH CHECK (auth.uid() = sender_id);

CREATE POLICY \"Usuários podem marcar mensagens recebidas como lidas\" ON public.messages
  FOR UPDATE USING (auth.uid() = receiver_id);

-- =====================================================
-- Habilita Realtime para mensagens e comentários
-- =====================================================
ALTER PUBLICATION supabase_realtime ADD TABLE public.messages;
ALTER PUBLICATION supabase_realtime ADD TABLE public.comments;
ALTER PUBLICATION supabase_realtime ADD TABLE public.likes;

-- =====================================================
-- BUCKETS DE STORAGE
-- Crie manualmente no Dashboard: Storage > New bucket
-- (ou descomente abaixo se usar CLI)
-- =====================================================
-- INSERT INTO storage.buckets (id, name, public) VALUES ('avatars', 'avatars', true) ON CONFLICT DO NOTHING;
-- INSERT INTO storage.buckets (id, name, public) VALUES ('stickers', 'stickers', true) ON CONFLICT DO NOTHING;

-- =====================================================
-- POLÍTICAS DE STORAGE: avatars
-- =====================================================
CREATE POLICY \"Avatares são públicos\" ON storage.objects
  FOR SELECT USING (bucket_id = 'avatars');

CREATE POLICY \"Usuários podem fazer upload do próprio avatar\" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'avatars'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY \"Usuários podem atualizar o próprio avatar\" ON storage.objects
  FOR UPDATE USING (
    bucket_id = 'avatars'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY \"Usuários podem excluir o próprio avatar\" ON storage.objects
  FOR DELETE USING (
    bucket_id = 'avatars'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

-- =====================================================
-- POLÍTICAS DE STORAGE: stickers
-- =====================================================
CREATE POLICY \"Imagens de figurinhas são públicas\" ON storage.objects
  FOR SELECT USING (bucket_id = 'stickers');

CREATE POLICY \"Usuários autenticados podem fazer upload de figurinhas\" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'stickers'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY \"Usuários podem atualizar suas figurinhas\" ON storage.objects
  FOR UPDATE USING (
    bucket_id = 'stickers'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY \"Usuários podem excluir suas figurinhas\" ON storage.objects
  FOR DELETE USING (
    bucket_id = 'stickers'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

-- =====================================================
-- FIM
-- =====================================================
""")

# ============================================================
# README
# ============================================================

add("README.md", '''# ⚽ Colecionadores da Copa

Rede social completa para colecionadores de figurinhas digitais da Copa do Mundo, construída com **React + TypeScript + Supabase + Tailwind CSS**.

![Status](https://img.shields.io/badge/status-pronto-success)
![Stack](https://img.shields.io/badge/stack-React%20%7C%20Supabase%20%7C%20TS-blue)

---

## ✨ Funcionalidades

- 🔐 **Autenticação completa** — Login, Cadastro e Recuperação de senha (via Supabase Auth)
- 📱 **Feed personalizado** — Linha do tempo com figurinhas de quem você segue
- ❤️ **Interações** — Curtir, Comentar e Descurtir figurinhas
- 👤 **Perfis públicos e editáveis** — Avatar, nome, bio, seleção favorita
- 📚 **Coleção pessoal** — Marque figurinhas como `TENHO`, `QUERO` ou `REPETIDA`
- 💬 **Mensagens diretas (DM)** — Chat em tempo real entre usuários
- ✏️ **CRUD completo de figurinhas** — Criar, editar e excluir (com upload de imagem)
- 🌍 **Seguir/Deixar de seguir** — Sistema social completo
- 📤 **Upload de imagens** — Via Supabase Storage com URLs públicas
- 🔄 **Atualizações em tempo real** — Comentários e mensagens via Supabase Realtime

---

## 🛠️ Stack técnica

| Camada | Tecnologia |
|---|---|
| Frontend | Vite + React 18 + TypeScript |
| UI / Estilo | Tailwind CSS + shadcn/ui + Radix UI |
| Backend / BaaS | Supabase (Auth + Database + Storage + Realtime) |
| Roteamento | React Router DOM |
| Ícones | Lucide React |
| Utilitários | class-variance-authority, clsx, tailwind-merge |

---

## 🚀 Como rodar localmente

### 1. Pré-requisitos

- **Node.js 18+** instalado ([baixar aqui](https://nodejs.org))
- Uma conta gratuita no **[Supabase](https://supabase.com)**

### 2. Instalar dependências

```bash
npm install
```

### 3. Configurar o Supabase

#### 3.1. Criar projeto

1. Acesse [supabase.com/dashboard](https://supabase.com/dashboard)
2. Clique em **New project**
3. Escolha um nome e uma senha forte para o banco
4. Selecione a região mais próxima
5. Aguarde ~2 minutos até o projeto inicializar

#### 3.2. Configurar variáveis de ambiente

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com as credenciais do seu projeto Supabase
(em **Project Settings → API**):

```
VITE_SUPABASE_URL=\\'https://seu-projeto.supabase.co\\'
VITE_SUPABASE_ANON_KEY=\\'eyJhbGciOi...\\'
```

> 💡 As chaves são encontradas em **Settings → API** no painel do Supabase.

#### 3.3. Rodar a migração SQL

1. No painel do Supabase, vá em **SQL Editor** (menu lateral)
2. Clique em **New query**
3. Copie **todo** o conteúdo do arquivo `supabase/migrations/001_initial_schema.sql`
4. Cole no editor e clique em **Run** (ou `Ctrl+Enter`)
5. Você deve ver "Success. No rows returned"

#### 3.4. Criar buckets de Storage

No painel do Supabase:

1. Vá em **Storage** (menu lateral)
2. Clique em **New bucket**
3. Crie o bucket **`avatars`** marcado como **Public bucket**
4. Crie o bucket **`stickers`** marcado como **Public bucket**

> As políticas RLS para esses buckets já estão no SQL de migração.

### 4. Rodar o projeto

```bash
npm run dev
```

Abra [http://localhost:5173](http://localhost:5173) no navegador.

### 5. Build de produção

```bash
npm run build
```

Os arquivos otimizados ficarão em `dist/`.

---

## 📦 Deploy

### 🚀 Publicando no GitHub

```bash
git init
git add .
git commit -m "feat: projeto inicial Colecionadores da Copa"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/colecionadores-copa.git
git push -u origin main
```

> ⚠️ Antes de subir, confirme que o arquivo `.env` está no `.gitignore` (já está por padrão).

### ▲ Publicando na Vercel

1. Acesse [vercel.com](https://vercel.com) e faça login com GitHub
2. Clique em **Add New → Project**
3. Importe o repositório `colecionadores-copa`
4. Em **Environment Variables**, adicione:
   - `VITE_SUPABASE_URL` → `https://seu-projeto.supabase.co`
   - `VITE_SUPABASE_ANON_KEY` → sua chave anon
5. Clique em **Deploy**

Em ~1 minuto sua aplicação estará online em uma URL `https://colecionadores-copa.vercel.app`.

#### Configurações adicionais na Vercel (se necessário):

- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`
- **Node Version**: 18.x ou superior

---

## 📂 Estrutura do projeto

```
colecionadores-copa/
├── public/
├── src/
│   ├── components/
│   │   ├── ui/                  # Componentes shadcn/ui
│   │   │   ├── avatar.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── input.tsx
│   │   │   ├── label.tsx
│   │   │   ├── tabs.tsx
│   │   │   └── textarea.tsx
│   │   ├── CommentSection.tsx
│   │   ├── Layout.tsx
│   │   ├── Navbar.tsx
│   │   └── StickerCard.tsx
│   │
│   ├── pages/
│   │   ├── CreateSticker.tsx
│   │   ├── EditProfile.tsx
│   │   ├── Feed.tsx
│   │   ├── ForgotPassword.tsx
│   │   ├── Login.tsx
│   │   ├── Messages.tsx
│   │   ├── MyCollection.tsx
│   │   ├── Profile.tsx
│   │   └── Register.tsx
│   │
│   ├── lib/
│   │   ├── supabaseClient.ts
│   │   ├── types.ts
│   │   └── utils.ts
│   │
│   ├── context/
│   │   └── AuthContext.tsx
│   │
│   ├── App.tsx
│   ├── index.css
│   └── main.tsx
│
├── supabase/
│   └── migrations/
│       └── 001_initial_schema.sql
│
├── .env.example
├── .gitignore
├── index.html
├── package.json
├── postcss.config.js
├── tailwind.config.js
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

---

## 🗄️ Modelo do banco (Supabase)

| Tabela | Função |
|---|---|
| `profiles` | Dados públicos do usuário (username, avatar, bio) |
| `stickers` | Catálogo de figurinhas criadas |
| `user_collections` | Status pessoal: TENHO, QUERO, REPETIDA |
| `likes` | Curtidas em figurinhas |
| `comments` | Comentários em figurinhas |
| `follows` | Relação de seguidores |
| `messages` | Mensagens privadas (DM) |

Todas as tabelas têm **Row Level Security (RLS)** habilitado. Os usuários só podem:
- Editar/excluir suas próprias figurinhas e perfil
- Ver/editar apenas sua própria coleção
- Enviar mensagens como `sender_id = auth.uid()`
- Ler mensagens onde são `sender` ou `receiver`

---

## 🎨 Tema visual

A identidade visual é inspirada nas cores da **bandeira do Brasil**, com modo claro e escuro:

| Cor | Hex | Uso |
|---|---|---|
| 🟢 Verde Brasil | `#009739` | Botões primários, CTAs, logo |
| 🟡 Amarelo | `#FEDD00` | Badges, acentos, highlights |
| 🔵 Azul | `#012169` | Botões secundários, links, gradientes |
| ⚪ Branco | `#FFFFFF` | Fundo do modo claro |
| ⚫ Dark slate | `#0F172A` | Fundo do modo escuro |

- **Modo claro** (padrão): fundo branco, contraste alto, alegre.
- **Modo escuro**: fundo `#0F172A`, ideal para uso noturno e economia de bateria.

A preferência de tema é salva automaticamente em `localStorage`. Você pode customizar todas as cores em `src/index.css` (CSS variables `--primary`, `--secondary`, `--accent`, etc.).

---

## 🐛 Problemas comuns

**`Invalid API key`** — Verifique se o `.env` está correto e reinicie o servidor (`Ctrl+C` e `npm run dev`).

**`new row violates row-level security policy`** — Você esqueceu de rodar o SQL de migração, ou as políticas RLS estão incorretas.

**Imagens não carregam** — Confirme que os buckets `avatars` e `stickers` estão marcados como **public** no Storage.

**`Error: supabase.auth.signUp()` retorna erro de username duplicado** — Os usernames são únicos. Escolha outro.

---

## 📄 Licença

MIT — Use, modifique e distribua livremente. ⚽

---

Feito com 💚💛 para os colecionadores da Copa do Mundo!
''')

# ============================================================
# MAIN - Cria arquivos e gera o ZIP
# ============================================================

def main():
    if BASE_DIR.exists():
        import shutil
        shutil.rmtree(BASE_DIR)
    BASE_DIR.mkdir(parents=True)

    print(f"\n📁 Criando estrutura do projeto em '{PROJECT_NAME}/'...")
    file_count = 0
    for rel_path, content in PROJECT_FILES.items():
        target = BASE_DIR / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        print(f"   ✓ {rel_path}")
        file_count += 1

    print(f"\n   Total: {file_count} arquivos criados")

    # Cria o ZIP
    if os.path.exists(OUTPUT_ZIP):
        os.remove(OUTPUT_ZIP)

    print(f"\n📦 Gerando arquivo ZIP: {OUTPUT_ZIP}")
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for root, _, files in os.walk(PROJECT_NAME):
            for fname in files:
                full = os.path.join(root, fname)
                arcname = os.path.relpath(full, ".")
                zf.write(full, arcname)

    size_kb = os.path.getsize(OUTPUT_ZIP) / 1024
    print(f"   Tamanho do ZIP: {size_kb:.1f} KB")

    # Banner final
    print("\n" + "=" * 60)
    print("✅  PROJETO GERADO COM SUCESSO!")
    print("=" * 60)
    print(f"📂  Pasta:  {PROJECT_NAME}/")
    print(f"📦  ZIP:    {OUTPUT_ZIP}")
    print()
    print("🚀  Próximos passos:")
    print("   1️⃣  Extraia o ZIP ou navegue até a pasta '" + PROJECT_NAME + "'")
    print("   2️⃣  cd " + PROJECT_NAME)
    print("   3️⃣  npm install")
    print("   4️⃣  Configure o arquivo .env com suas credenciais do Supabase")
    print("   5️⃣  Rode o SQL em supabase/migrations/001_initial_schema.sql no Supabase")
    print("   6️⃣  Crie os buckets 'avatars' e 'stickers' no Storage")
    print("   7️⃣  npm run dev")
    print()
    print("📖  Veja o README.md para instruções completas de deploy.")
    print("=" * 60)


if __name__ == "__main__":
    main()
