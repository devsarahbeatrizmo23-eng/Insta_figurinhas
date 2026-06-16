import { Routes, Route, Navigate } from 'react-router-dom'
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
