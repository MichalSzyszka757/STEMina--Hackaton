import { ref } from 'vue';
import apiClient from '@/api/axiosClient'; // Twój klient API

export function useCategories() {
  const data = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  const fetchProducts = async () => {
    isLoading.value = true;
    try {
      // ZMIANA TUTAJ: Zamiast setTimeout, prawdziwy strzał
      const response = await apiClient.get('/categories');
      
      // Opcjonalnie: Mapowanie, jeśli struktura API różni się od Twojej starej stałej
      // data.value = response.data.results; 
      data.value = response.data;
      
    } catch (e) {
      console.error(e);
      error.value = 'Nie udało się pobrać danych';
    } finally {
      isLoading.value = false;
    }
  };

  return { data, isLoading, error, fetchProducts };
}