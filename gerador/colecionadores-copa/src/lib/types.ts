export type Profile = {
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
