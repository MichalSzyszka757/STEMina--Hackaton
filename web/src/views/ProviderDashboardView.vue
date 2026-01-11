<script setup>
import { ref, reactive } from 'vue'

// 1. IMPORT DANYCH Z PLIKU (To musi być ta ścieżka do wygenerowanego pliku)
import { providerTasks as tasks } from '@/data/taskData.js'

// --- STATE ---
const isEditingProfile = ref(false)
const viewState = ref('init') // 'init', 'edit_offer', 'swiping', 'chat'
const currentJobStack = ref([]) // Zlecenia przefiltrowane do przeglądania
const myMatches = ref([])       // Zaakceptowane
const activeChatPartner = ref(null)
const swipeAnimation = ref('')

// Profil Firmy
const providerProfile = reactive({
    name: 'Moja Firma Budowlana',
    email: 'biuro@firma1.pl',
    avatar: 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=400&q=80',

    // --- WAŻNE: To musi pasować do nazw z generatora Python ---
    category: 'Budowlana',
    years: 5,
    priceLevel: 1, // 1 = Standard
    range: 50,     // Dajmy większy zasięg na start
    availableFrom: new Date().toISOString().substr(0, 10) // Dzisiaj
})

// --- LOGIKA ---

// Funkcja szukająca zleceń (Filtrowanie danych)
const searchForJobs = () => {
    // FILTROWANIE:
    const filtered = tasks.filter(job => {
        const categoryMatch = job.category === providerProfile.category;
        const rangeMatch = job.range <= providerProfile.range;
        const dateMatch = job.date >= providerProfile.availableFrom;

        return categoryMatch && rangeMatch && dateMatch;
    });

    // Mieszamy wyniki i przypisujemy
    currentJobStack.value = filtered.sort(() => Math.random() - 0.5);

    // Przełącz widok
    viewState.value = 'swiping'
}

const swipe = (direction) => {
    if (currentJobStack.value.length === 0) return

    swipeAnimation.value = direction === 'right' ? 'fly-right' : 'fly-left'

    setTimeout(() => {
        const job = currentJobStack.value[0]
        if (direction === 'right') {
            myMatches.value.push(job)
        }
        currentJobStack.value.shift()
        swipeAnimation.value = ''
    }, 300)
}

const getBudgetSign = (level) => {
    if (level === 0) return '$'
    if (level === 1) return '$$'
    return '$$$'
}

// --- HELPERS ---
const openChat = (job) => { activeChatPartner.value = job; viewState.value = 'chat' }
</script>

<template>
  <div class="app-container">

    <div class="sidebar">
      <div class="user-profile-section">
          <div class="profile-header">
              <div class="profile-avatar" :style="{ backgroundImage: `url(${providerProfile.avatar})` }"></div>
              <div class="profile-info">
                  <h3 v-if="!isEditingProfile">{{ providerProfile.name }}</h3>
                  <input v-else v-model="providerProfile.name" class="input-clean" style="font-weight:bold;">

                  <p v-if="!isEditingProfile">{{ providerProfile.category }} | {{ providerProfile.years }} lat</p>
                  <button class="btn-small" @click="isEditingProfile = !isEditingProfile">
                    {{ isEditingProfile ? 'Zapisz Profil' : 'Edytuj Profil' }}
                  </button>
              </div>
          </div>

          <div v-if="isEditingProfile" style="display:flex; flex-direction:column; gap:10px; margin-top:10px;">
              <label class="label-mini">Kategoria</label>
              <select v-model="providerProfile.category" class="input-clean">
                  <option>Budowlana</option>
                  <option>Hydrauliczna</option>
                  <option>Elektryczna</option>
                  <option>IT i Grafika</option>
                  <option>Sprzątająca</option>
                  <option>Florystyczna</option>
                  <option>Transport i Przeprowadzki</option>
                  <option>Motoryzacyjna</option>
                  <option>Ogrody i Tereny Zielone</option>
              </select>

              <label class="label-mini">Lata na rynku</label>
              <input type="number" v-model="providerProfile.years" class="input-clean">

              <label class="label-mini">Poziom Cen (Min.)</label>
              <select v-model="providerProfile.priceLevel" class="input-clean">
                  <option :value="0">Budget ($)</option>
                  <option :value="1">Standard ($$)</option>
                  <option :value="2">Premium ($$$)</option>
              </select>
          </div>
      </div>

      <div class="sidebar-header" style="height: 50px; font-size: 16px;">
        <span>Moje Zlecenia</span>
      </div>

      <div class="sidebar-content">
        <div v-for="job in myMatches" :key="job.id" class="match-item" @click="openChat(job)">
             <div class="match-avatar" style="font-size:12px;">{{ job.id }}</div>
             <div>
                 <strong>{{ job.title }}</strong><br>
                 <small>{{ job.date }}</small>
             </div>
             <span style="margin-left:auto">💬</span>
        </div>
      </div>
    </div>

    <div class="main-area">

      <div v-if="viewState === 'init'" class="placeholder-box" @click="viewState = 'edit_offer'">
          <div style="font-size: 50px; color: #fd297b;">🛠️</div>
          <h2>Znajdź Zlecenia</h2>
          <p>Skonfiguruj swoją ofertę i dostępność.</p>
      </div>

      <div v-if="viewState === 'edit_offer'" class="tinder-card editable-card">
          <h2>Twoja Oferta</h2>
          <p>Doprecyzuj, jakich zleceń szukasz dzisiaj.</p>

          <label class="label-mini">Szukam zleceń dostępnych OD:</label>
          <input type="date" v-model="providerProfile.availableFrom" class="input-clean">

          <label class="label-mini">Maksymalny Dojazd (km)</label>
          <input type="range" v-model="providerProfile.range" min="0" max="100" class="single-slider">
          <div style="text-align:right; font-size:12px; color:#888;">{{ providerProfile.range }} km</div>

          <div class="action-area" style="margin-top:auto;">
              <button class="btn-main" @click="searchForJobs">Szukaj Zleceń 🔍</button>
          </div>
      </div>

      <div v-if="viewState === 'swiping'" style="display:flex; flex-direction: column; align-items: center;">
          <div v-if="currentJobStack.length > 0"
               class="tinder-card candidate-card"
               :class="swipeAnimation"
               :style="{ backgroundImage: `url(${currentJobStack[0].img})` }">

              <div class="card-overlay">
                  <h2>{{ currentJobStack[0].title }}</h2>
                  <p>{{ currentJobStack[0].desc }}</p>

                  <div style="display:flex; gap:10px; margin-top:10px;">
                      <span class="info-pill">📅 {{ currentJobStack[0].date }}</span>
                      <span class="info-pill price-pill">{{ getBudgetSign(currentJobStack[0].budgetLevel) }}</span>
                      <span class="info-pill">📍 {{ currentJobStack[0].range }} km</span>
                  </div>
              </div>
          </div>

          <div v-else class="tinder-card" style="justify-content:center; align-items:center; color:#999; padding: 20px; text-align:center;">
              <h2>Brak pasujących zleceń 😔</h2>
              <p>Spróbuj zwiększyć zasięg (km), zmienić datę lub kategorię.</p>
              <button class="btn-outline" @click="viewState='edit_offer'">Zmień kryteria</button>
          </div>

          <div v-if="currentJobStack.length > 0" style="display:flex; gap:20px; margin-top:20px;">
              <button class="btn-control nope" @click="swipe('left')">✖</button>
              <button class="btn-control like" @click="swipe('right')">❤</button>
          </div>
      </div>

      <div v-if="viewState === 'chat'" class="chat-window">
         <div class="chat-header">
             <div style="display: flex; align-items: center;">
                 <div :style="{ backgroundImage: `url(${activeChatPartner.img})` }" class="chat-avatar-small"></div>
                 <strong>{{ activeChatPartner.title }}</strong>
             </div>
             <button @click="viewState='swiping'" class="chat-close-btn">✕</button>
         </div>

         <div class="chat-body">
             <div class="chat-bubble received">
                 Cześć! Jesteśmy zainteresowani Twoim zleceniem.
             </div>
         </div>

         <div class="chat-input-area">
             <input type="text" placeholder="Napisz wiadomość..." class="chat-input">
         </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* --- STYLIZACJA CHATU (ZGODNA Z DASHBOARDVIEW) --- */

.chat-window {
    width: 100%;
    max-width: 600px; /* Szerokość jak na zdjęciu */
    height: 70vh; /* Wysokość okna */
    background: white;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    animation: popIn 0.3s ease;
}

.chat-header {
    padding: 20px;
    border-bottom: 1px solid #eee;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.chat-avatar-small {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-size: cover;
    background-position: center;
    margin-right: 15px;
    border: 1px solid #eee;
}

.chat-close-btn {
    border: none;
    background: none;
    font-size: 20px;
    cursor: pointer;
    color: #999;
}
.chat-close-btn:hover { color: #333; }

.chat-body {
    flex: 1;
    padding: 20px;
    background: #f9f9f9; /* Delikatne tło */
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}

.chat-bubble {
    padding: 12px 18px;
    border-radius: 18px;
    width: fit-content;
    margin-bottom: 10px;
    font-size: 14px;
    line-height: 1.4;
    max-width: 80%;
}

.chat-bubble.received {
    background: #eee;
    color: #333;
    border-bottom-left-radius: 2px; /* Efekt dymka */
}

.chat-input-area {
    padding: 15px;
    border-top: 1px solid #eee;
    background: white;
}

.chat-input {
    width: 100%;
    border: 1px solid #ddd;
    padding: 12px 20px;
    border-radius: 30px;
    outline: none;
    font-family: inherit;
    transition: 0.3s;
    box-sizing: border-box; /* Ważne żeby padding nie rozpychał */
}
.chat-input:focus {
    border-color: #fd297b;
}

@keyframes popIn {
    from { transform: scale(0.95); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
}

/* --- POZOSTAŁE STYLE (BEZ ZMIAN) --- */
.msg { background:white; padding:10px; border-radius:10px; width:fit-content; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
</style>
