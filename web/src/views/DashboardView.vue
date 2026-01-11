<script setup>
import { ref, computed } from 'vue'
// NAPRAWA: Importujemy 'providerData' (tak nazwał to skrypt Python)
import { providerData } from '../data/providerData.js'

// --- KONFIGURACJA DANYCH ---

// Przypisujemy dane z bazy do zmiennej reaktywnej
// Komentarz: Używamy ref, aby w przyszłości można było te dane modyfikować (np. po pobraniu z API)
const allCandidates = ref(providerData)

// NAPRAWA: Definiujemy etykiety tutaj, bo skrypt Python ich nie generuje
const budgetLabels = {
  BUDGET: 'Budżetowy',
  STANDARD: 'Standard',
  PREMIUM: 'Premium',
}

// Zmienna do wyszukiwarki tekstowej
const searchQuery = ref('')

// --- LOGIKA FILTROWANIA ---

/**
 * Filtruje kandydatów na podstawie wpisanego tekstu.
 * Sprawdza nazwę firmy oraz opis.
 */
const filteredCandidates = computed(() => {
  if (!searchQuery.value) return allCandidates.value

  const lowerQuery = searchQuery.value.toLowerCase()
  return allCandidates.value.filter(
    (candidate) =>
      candidate.name.toLowerCase().includes(lowerQuery) ||
      candidate.description.toLowerCase().includes(lowerQuery),
  )
})

/**
 * Funkcja pomocnicza do pobierania koloru badge'a w zależności od ceny.
 * @param {string} tier - np. 'BUDGET', 'PREMIUM'
 */
const getPriceColor = (tier) => {
  switch (tier) {
    case 'BUDGET':
      return 'bg-green-100 text-green-800'
    case 'PREMIUM':
      return 'bg-purple-100 text-purple-800'
    default:
      return 'bg-blue-100 text-blue-800'
  }
}
</script>

<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-6">Znajdź Specjalistę</h1>

    <div class="mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Szukaj po nazwie lub opisie..."
        class="w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 outline-none"
      />
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="candidate in filteredCandidates"
        :key="candidate.id"
        class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow border border-gray-100"
      >
        <div class="p-5">
          <div class="flex justify-between items-start mb-4">
            <div>
              <h3 class="text-xl font-bold text-gray-800">{{ candidate.name }}</h3>
              <p class="text-sm text-gray-500">
                {{ candidate.city }} • {{ candidate.distance || candidate.location }} km
              </p>
            </div>
            <span
              :class="[
                'px-3 py-1 rounded-full text-xs font-semibold',
                getPriceColor(candidate.price_tier),
              ]"
            >
              {{ budgetLabels[candidate.price_tier] || candidate.price_tier }}
            </span>
          </div>

          <p class="text-gray-600 mb-4 line-clamp-3">
            {{ candidate.description }}
          </p>

          <div class="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
            <div class="text-sm">
              <span class="font-semibold text-gray-700">Ocena:</span>
              <span class="text-yellow-500 font-bold"
                >★ {{ candidate.rating ? candidate.rating.toFixed(1) : 'Nowy' }}</span
              >
            </div>
            <button
              class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm"
            >
              Wybierz
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="filteredCandidates.length === 0" class="text-center text-gray-500 mt-10">
      Nie znaleziono wykonawców pasujących do wyszukiwania.
    </div>
  </div>
</template>
