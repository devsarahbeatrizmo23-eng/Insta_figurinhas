# ⚽ Colecionadores da Copa

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
VITE_SUPABASE_URL=\'https://seu-projeto.supabase.co\'
VITE_SUPABASE_ANON_KEY=\'eyJhbGciOi...\'
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
