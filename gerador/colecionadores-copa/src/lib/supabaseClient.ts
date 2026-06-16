/// <reference types="vite/client" />
import { createClient } from '@supabase/supabase-js'

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
