// src/composables/useAuth.js
import { ref } from 'vue';
import apiClient from '@/api/axiosClient'; // Twój klient axios z poprzednich kroków
import { useRouter } from 'vue-router';
import qs from 'querystring';

// Stan globalny (poza funkcją), aby dane użytkownika były dostępne w całej aplikacji
// (Można to też zrobić w Pinia, ale na start ref/reactive wystarczy)
const user = ref(null);
const token = ref(localStorage.getItem('auth_token') || null);

export function useAuth() {
  const isLoading = ref(false);
  const error = ref(null);
  const router = useRouter();

  const login = async (username, password) => {
    isLoading.value = true;
    error.value = null;

    try {
      // 1. Prawdziwy strzał do API
      // Zakładamy, że API zwraca obiekt: { token: 'xyz...', role: 'admin', user: {...} }
      const response = await apiClient.post('/auth/token', {
        username: username, // lub email, zależnie od API
        password: password },
        {headers: { 'Content-Type': 'application/x-www-form-urlencoded' }}
      );

      const { access_token: newToken, role } = response.data;

      // 2. Zapisanie tokena
      token.value = newToken;
      localStorage.setItem('auth_token', newToken);
      
      // Opcjonalnie: Ustawienie nagłówka dla przyszłych zapytań (jeśli nie używasz interceptora)
      // apiClient.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;

      // 3. Logika przekierowania (zachowujemy Twoją logikę biznesową)
      //if (role === 'admin') {
        await router.push('/dashboard');
      //} else if (role === 'firma') { // Zakładam, że API zwróci rolę np. 'firma'
      //  await router.push('/provider');
      //} else {
      //  // Fallback dla innych ról
      //  await router.push('/');
      //}

    } catch (err) {
      // Obsługa błędów z API (np. 401 Unauthorized)
      console.error(err);
      error.value = err.response?.data?.message || 'Błąd logowania. Sprawdź dane.';
    } finally {
      isLoading.value = false;
    }
  };

  const logout = () => {
    token.value = null;
    user.value = null;
    localStorage.removeItem('auth_token');
    router.push('/login');
  };

  return {
    token,
    isLoading,
    error,
    login,
    logout
  };
}