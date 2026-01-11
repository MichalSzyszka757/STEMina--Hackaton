<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')

const handleLogin = async () => {
    if (username.value === 'admin' && password.value === 'admin') {
        router.push('/dashboard')
    } else if (username.value === 'firma1' && password.value === 'firma1') {
        router.push('/provider')
    } else {
        error.value = "Nieprawidłowy login lub hasło (admin/admin lub firma1/firma1)"
    }
  }
</script>

<template>
  <div class="landing-container">
    <div class="login-box">
      <div style="font-size: 40px; color: #fd297b; margin-bottom: 10px;">🔥</div>
      <h2 style="margin: 0 0 20px 0;">Matchmaker B2B</h2>
      
      <div style="text-align: left;">
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
      </div>

      <button class="btn-main" @click="handleLogin">Zaloguj się</button>
      
      <p v-if="error" style="color: red; font-size: 13px; margin-top: 15px;">{{ error }}</p>
      <p style="color: #999; font-size: 12px; margin-top: 20px;">Nie masz konta? Zarejestruj się</p>
    </div>
  </div>
</template>