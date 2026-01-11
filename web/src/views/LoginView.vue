<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth';

const router = useRouter()

// Dane formularza
const username = ref('');
const password = ref('');

// Pobieramy logikę z composable
const { login, isLoading, error } = useAuth();

const handleLogin = async () => {
  // Wywołujemy akcję - walidacja i przekierowanie dzieją się wewnątrz useAuth
  await login(username.value, password.value);
}
</script>

<template>
  <div class="landing-container">
    <div class="login-box">
      <div style="font-size: 40px; color: #fd297b; margin-bottom: 10px;">🔥</div>
      <h2 style="margin: 0 0 20px 0;">Matchmaker B2B</h2>
      
      <form style="text-align: left;" @submit.prevent="handleLogin">
          <input 
            v-model="username" 
            class="input-clean" 
            type="text" 
            placeholder="Nazwa użytkownika" 
            style="margin-bottom: 15px; border-bottom: 1px solid #ddd;"
          >
          <input 
            v-model="password" 
            class="input-clean" 
            type="password" 
            placeholder="Hasło" 
            style="margin-bottom: 25px; border-bottom: 1px solid #ddd;"
            @keyup.enter="handleLogin"
          >
          <button type="submit" class="btn-main">Zaloguj się</button>
        </form>

      
      
      <p v-if="error" style="color: red; font-size: 13px; margin-top: 15px;">{{ error }}</p>
      <p style="color: #999; font-size: 12px; margin-top: 20px;">Nie masz konta? Zarejestruj się</p>
    </div>
  </div>
</template>