import { Outlet, useLocation } from 'react-router-dom'
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
