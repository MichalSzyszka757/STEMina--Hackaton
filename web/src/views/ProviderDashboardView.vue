<script setup>
import { ref, computed } from 'vue'
// NAPRAWA: Importujemy 'taskData' i aliasujemy jako 'tasks'
import { taskData as tasksRaw } from '@/data/taskData.js'

// --- KONFIGURACJA DANYCH ---

// Przypisanie danych do zmiennej reaktywnej
const tasks = ref(tasksRaw)

// --- LOGIKA ---

/**
 * Formatuje datę z formatu ISO na czytelny string.
 * @param {string} dateString
 */
const formatDate = (dateString) => {
  if (!dateString) return 'Brak terminu'
  const date = new Date(dateString)
  return date.toLocaleDateString('pl-PL', {
    day: 'numeric',
    month: 'long',
    hour: '2-digit',
    minute: '2-digit',
  })
}

/**
 * Filtruje zadania, aby pokazać tylko te "OPEN" (otwarte).
 * W przyszłości tutaj może być logika matchingu.
 */
const openTasks = computed(() => {
  return tasks.value.filter((t) => t.status === 'OPEN')
})
</script>

<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Dostępne Zlecenia</h1>
      <span class="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-sm">
        Znaleziono: {{ openTasks.length }}
      </span>
    </div>

    <div class="space-y-4">
      <div
        v-for="task in openTasks"
        :key="task.id"
        class="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:border-blue-300 transition-all"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <h2 class="text-xl font-semibold text-gray-800 mb-2">{{ task.title }}</h2>
            <p class="text-gray-600 mb-4">{{ task.details }}</p>

            <div class="flex flex-wrap gap-3 text-sm text-gray-500">
              <span class="flex items-center gap-1">
                📅 Termin: {{ formatDate(task.deadline) }}
              </span>
              <span class="flex items-center gap-1">
                💰 Budżet: <span class="font-medium text-gray-700">{{ task.budget }}</span>
              </span>
              <span class="flex items-center gap-1">
                📍 Dystans max: {{ task.max_distance }} km
              </span>
            </div>
          </div>

          <div class="ml-4 flex flex-col gap-2">
            <button
              class="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 font-medium transition-colors shadow-sm"
            >
              Aplikuj
            </button>
            <button class="text-gray-400 hover:text-red-500 text-sm py-1 transition-colors">
              Odrzuć
            </button>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="openTasks.length === 0"
      class="text-center py-12 bg-gray-50 rounded-xl border border-dashed border-gray-300"
    >
      <p class="text-gray-500 text-lg">Brak nowych zleceń w Twojej okolicy.</p>
    </div>
  </div>
</template>
