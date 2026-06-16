-- =====================================================
-- Colecionadores da Copa - Schema inicial do banco
-- Execute no SQL Editor do Supabase
-- =====================================================

-- Habilita extensão para UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

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

CREATE POLICY "Profiles visíveis para todos" ON public.profiles
  FOR SELECT USING (true);

CREATE POLICY "Usuários podem inserir seu próprio perfil" ON public.profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "Usuários podem atualizar seu próprio perfil" ON public.profiles
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

CREATE POLICY "Figurinhas visíveis para todos" ON public.stickers
  FOR SELECT USING (true);

CREATE POLICY "Usuários autenticados podem criar figurinhas" ON public.stickers
  FOR INSERT WITH CHECK (auth.uid() = creator_id);

CREATE POLICY "Usuários podem atualizar suas figurinhas" ON public.stickers
  FOR UPDATE USING (auth.uid() = creator_id);

CREATE POLICY "Usuários podem excluir suas figurinhas" ON public.stickers
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

CREATE POLICY "Usuários veem apenas sua coleção" ON public.user_collections
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Usuários podem adicionar à sua coleção" ON public.user_collections
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Usuários podem atualizar sua coleção" ON public.user_collections
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Usuários podem remover da sua coleção" ON public.user_collections
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

CREATE POLICY "Likes visíveis para todos" ON public.likes
  FOR SELECT USING (true);

CREATE POLICY "Usuários podem curtir" ON public.likes
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Usuários podem descurtir" ON public.likes
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

CREATE POLICY "Comentários visíveis para todos" ON public.comments
  FOR SELECT USING (true);

CREATE POLICY "Usuários podem comentar" ON public.comments
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Usuários podem atualizar seus comentários" ON public.comments
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Usuários podem excluir seus comentários" ON public.comments
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

CREATE POLICY "Follows visíveis para todos" ON public.follows
  FOR SELECT USING (true);

CREATE POLICY "Usuários podem seguir outros" ON public.follows
  FOR INSERT WITH CHECK (auth.uid() = follower_id);

CREATE POLICY "Usuários podem deixar de seguir" ON public.follows
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

CREATE POLICY "Usuários veem mensagens que enviaram ou receberam" ON public.messages
  FOR SELECT USING (auth.uid() = sender_id OR auth.uid() = receiver_id);

CREATE POLICY "Usuários podem enviar mensagens" ON public.messages
  FOR INSERT WITH CHECK (auth.uid() = sender_id);

CREATE POLICY "Usuários podem marcar mensagens recebidas como lidas" ON public.messages
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
CREATE POLICY "Avatares são públicos" ON storage.objects
  FOR SELECT USING (bucket_id = 'avatars');

CREATE POLICY "Usuários podem fazer upload do próprio avatar" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'avatars'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Usuários podem atualizar o próprio avatar" ON storage.objects
  FOR UPDATE USING (
    bucket_id = 'avatars'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Usuários podem excluir o próprio avatar" ON storage.objects
  FOR DELETE USING (
    bucket_id = 'avatars'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

-- =====================================================
-- POLÍTICAS DE STORAGE: stickers
-- =====================================================
CREATE POLICY "Imagens de figurinhas são públicas" ON storage.objects
  FOR SELECT USING (bucket_id = 'stickers');

CREATE POLICY "Usuários autenticados podem fazer upload de figurinhas" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'stickers'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Usuários podem atualizar suas figurinhas" ON storage.objects
  FOR UPDATE USING (
    bucket_id = 'stickers'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Usuários podem excluir suas figurinhas" ON storage.objects
  FOR DELETE USING (
    bucket_id = 'stickers'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

-- =====================================================
-- FIM
-- =====================================================
