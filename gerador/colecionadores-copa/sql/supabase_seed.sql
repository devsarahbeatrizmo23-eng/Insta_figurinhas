-- =====================================================
-- Supabase Seed Data para Teste
-- Execute no SQL Editor do Supabase como service_role
-- =====================================================

-- Habilita extensão para hash de senha
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Usuários de autenticação de teste
INSERT INTO auth.users (id, aud, role, email, encrypted_password, email_confirmed_at, created_at, raw_user_meta_data)
VALUES
  ('11111111-1111-1111-1111-111111111111', 'authenticated', 'authenticated', 'andre@example.com', crypt('Andre123!', gen_salt('bf')), NOW(), NOW(), '{"username": "andre", "full_name": "André Silva"}'::json),
  ('22222222-2222-2222-2222-222222222222', 'authenticated', 'authenticated', 'maria@example.com', crypt('Maria123!', gen_salt('bf')), NOW(), NOW(), '{"username": "maria", "full_name": "Maria Souza"}'::json),
  ('33333333-3333-3333-3333-333333333333', 'authenticated', 'authenticated', 'carlos@example.com', crypt('Carlos123!', gen_salt('bf')), NOW(), NOW(), '{"username": "carlos", "full_name": "Carlos Lima"}'::json),
  ('44444444-4444-4444-4444-444444444444', 'authenticated', 'authenticated', 'ana@example.com', crypt('Ana123!', gen_salt('bf')), NOW(), NOW(), '{"username": "ana", "full_name": "Ana Pereira"}'::json)
ON CONFLICT (id) DO NOTHING;

-- Perfis de usuário de teste
INSERT INTO public.profiles (id, username, full_name, avatar_url, bio, favorite_team, created_at)
VALUES
  ('11111111-1111-1111-1111-111111111111', 'andre', 'André Silva', 'https://i.pravatar.cc/150?img=1', 'Fã de futebol e colecionador de figurinhas.', 'Brasil', NOW()),
  ('22222222-2222-2222-2222-222222222222', 'maria', 'Maria Souza', 'https://i.pravatar.cc/150?img=2', 'Coleciono figurinhas desde criança.', 'Argentina', NOW()),
  ('33333333-3333-3333-3333-333333333333', 'carlos', 'Carlos Lima', 'https://i.pravatar.cc/150?img=3', 'Sempre em busca de novas figurinhas.', 'Portugal', NOW()),
  ('44444444-4444-4444-4444-444444444444', 'ana', 'Ana Pereira', 'https://i.pravatar.cc/150?img=4', 'Gosto de trocar figurinhas com os amigos.', 'França', NOW())
ON CONFLICT (id) DO NOTHING;

-- Figurinhas de teste
INSERT INTO public.stickers (id, creator_id, athlete_name, team, position, number, image_url, description, created_at)
VALUES
  ('aaaa0000-0000-0000-0000-000000000001', '11111111-1111-1111-1111-111111111111', 'Neymar Jr', 'Brasil', 'Atacante', 10, 'https://images.supabase.io/sticker-1.png', 'Craque habilidoso e líder do time.', NOW()),
  ('aaaa0000-0000-0000-0000-000000000002', '22222222-2222-2222-2222-222222222222', 'Lionel Messi', 'Argentina', 'Atacante', 30, 'https://images.supabase.io/sticker-2.png', 'Melhor jogador do planeta.', NOW()),
  ('aaaa0000-0000-0000-0000-000000000003', '33333333-3333-3333-3333-333333333333', 'Cristiano Ronaldo', 'Portugal', 'Atacante', 7, 'https://images.supabase.io/sticker-3.png', 'Goleador implacável.', NOW()),
  ('aaaa0000-0000-0000-0000-000000000004', '11111111-1111-1111-1111-111111111111', 'Kylian Mbappé', 'França', 'Atacante', 7, 'https://images.supabase.io/sticker-4.png', 'Velocidade e potência no ataque.', NOW()),
  ('aaaa0000-0000-0000-0000-000000000005', '22222222-2222-2222-2222-222222222222', 'Virgil van Dijk', 'Holanda', 'Zagueiro', 4, 'https://images.supabase.io/sticker-5.png', 'Defesa sólida e liderança.', NOW()),
  ('aaaa0000-0000-0000-0000-000000000006', '33333333-3333-3333-3333-333333333333', 'Kevin De Bruyne', 'Bélgica', 'Meio-campo', 17, 'https://images.supabase.io/sticker-6.png', 'Maestro do meio-campo.', NOW())
ON CONFLICT (id) DO NOTHING;

-- Coleções de teste
INSERT INTO public.user_collections (user_id, sticker_id, status, updated_at)
VALUES
  ('11111111-1111-1111-1111-111111111111', 'aaaa0000-0000-0000-0000-000000000001', 'TENHO', NOW()),
  ('11111111-1111-1111-1111-111111111111', 'aaaa0000-0000-0000-0000-000000000002', 'QUERO', NOW()),
  ('22222222-2222-2222-2222-222222222222', 'aaaa0000-0000-0000-0000-000000000001', 'REPETIDA', NOW()),
  ('33333333-3333-3333-3333-333333333333', 'aaaa0000-0000-0000-0000-000000000004', 'TENHO', NOW()),
  ('44444444-4444-4444-4444-444444444444', 'aaaa0000-0000-0000-0000-000000000003', 'QUERO', NOW())
ON CONFLICT DO NOTHING;

-- Likes de teste
INSERT INTO public.likes (user_id, sticker_id, created_at)
VALUES
  ('11111111-1111-1111-1111-111111111111', 'aaaa0000-0000-0000-0000-000000000002', NOW()),
  ('22222222-2222-2222-2222-222222222222', 'aaaa0000-0000-0000-0000-000000000001', NOW()),
  ('33333333-3333-3333-3333-333333333333', 'aaaa0000-0000-0000-0000-000000000004', NOW()),
  ('44444444-4444-4444-4444-444444444444', 'aaaa0000-0000-0000-0000-000000000003', NOW())
ON CONFLICT DO NOTHING;

-- Comentários de teste
INSERT INTO public.comments (id, sticker_id, user_id, content, created_at)
VALUES
  ('bbbb0000-0000-0000-0000-000000000001', 'aaaa0000-0000-0000-0000-000000000001', '22222222-2222-2222-2222-222222222222', 'Essa figurinha é demais!', NOW()),
  ('bbbb0000-0000-0000-0000-000000000002', 'aaaa0000-0000-0000-0000-000000000002', '11111111-1111-1111-1111-111111111111', 'Quero muito essa aqui.', NOW()),
  ('bbbb0000-0000-0000-0000-000000000003', 'aaaa0000-0000-0000-0000-000000000004', '33333333-3333-3333-3333-333333333333', 'Ótima escolha de jogador!', NOW()),
  ('bbbb0000-0000-0000-0000-000000000004', 'aaaa0000-0000-0000-0000-000000000003', '44444444-4444-4444-4444-444444444444', 'Essa figurinha é rara.', NOW())
ON CONFLICT DO NOTHING;

-- Seguidores de teste
INSERT INTO public.follows (follower_id, following_id, created_at)
VALUES
  ('11111111-1111-1111-1111-111111111111', '22222222-2222-2222-2222-222222222222', NOW()),
  ('22222222-2222-2222-2222-222222222222', '33333333-3333-3333-3333-333333333333', NOW()),
  ('33333333-3333-3333-3333-333333333333', '11111111-1111-1111-1111-111111111111', NOW()),
  ('44444444-4444-4444-4444-444444444444', '11111111-1111-1111-1111-111111111111', NOW())
ON CONFLICT DO NOTHING;

-- Mensagens de teste
INSERT INTO public.messages (id, sender_id, receiver_id, content, is_read, created_at)
VALUES
  ('cccc0000-0000-0000-0000-000000000001', '11111111-1111-1111-1111-111111111111', '22222222-2222-2222-2222-222222222222', 'Oi Maria, você tem a figurinha do Neymar?', false, NOW()),
  ('cccc0000-0000-0000-0000-000000000002', '22222222-2222-2222-2222-222222222222', '11111111-1111-1111-1111-111111111111', 'Tenho sim! Quer trocar?', false, NOW()),
  ('cccc0000-0000-0000-0000-000000000003', '33333333-3333-3333-3333-333333333333', '44444444-4444-4444-4444-444444444444', 'Pode me avisar quando tiver a figurinha do CR7?', false, NOW())
ON CONFLICT DO NOTHING;
