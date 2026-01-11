<script setup>
import { ref, reactive, onMounted } from 'vue'

// --- STATE ---
const isEditingProfile = ref(false)
const viewState = ref('init') // 'init', 'edit_offer', 'swiping', 'chat'
const currentJobStack = ref([]) // Zlecenia pobrane z API
const myMatches = ref([])       // Zaakceptowane zlecenia
const activeChatPartner = ref(null)
const swipeAnimation = ref('') 
const isLoading = ref(false)
const apiError = ref(null)

// Profil Firmy (Providera)
const providerProfile = reactive({
    name: 'Moja Firma Budowlana',
    email: 'biuro@firma1.pl',
    avatar: 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=400&q=80',
    category: 'Budowlana', 
    years: 5,
    priceLevel: 1, // 1 = Standard
    range: 50,     // km
    availableFrom: new Date().toISOString().substr(0, 10)
})

// --- LOGIKA POŁĄCZENIA Z BACKENDEM ---

// Funkcja pomocnicza: Obrazek dla kategorii (jeśli backend nie zwraca URL)
const getCategoryImage = (categoryName) => {
    return `https://source.unsplash.com/random/600x800/?${categoryName},job`
}

// Funkcja pomocnicza: Mapowanie budżetu (liczba z backendu -> poziom $, $$, $$$)
const mapBudgetToLevel = (budget) => {
    if (!budget) return 1;
    if (budget < 1000) return 0; // Budget
    if (budget < 5000) return 1; // Standard
    return 2; // Premium
}

const fetchAndFilterJobs = async () => {
    isLoading.value = true;
    apiError.value = null;
    try {
        // 1. POBIERANIE: To zapytanie idzie przez nasze Proxy do Pythona
        const response = await fetch('/api/v1/tasks'); 
        
        if (!response.ok) {
            throw new Error(`Błąd API: ${response.status}`);
        }

        const backendTasks = await response.json();

        // 2. MAPOWANIE: Dostosowanie danych z Pythona do Twojego wyglądu
        const mappedTasks = backendTasks.map(task => ({
            id: task.id,
            // Jeśli backend nie ma tytułu, tworzymy go dynamicznie
            title: task.title || `${task.category?.name || 'Zlecenie'} #${task.id}`,
            category: task.category?.name || 'Inne',
            desc: task.description || 'Brak opisu zlecenia.',
            budgetLevel: mapBudgetToLevel(task.budget), 
            range: task.distance || Math.floor(Math.random() * 40) + 5, // Mock dystansu
            date: task.due_date ? task.due_date.split('T')[0] : '2026-05-20',
            img: getCategoryImage(task.category?.name || 'work')
        }));

        // 3. FILTROWANIE: Dopasowanie do profilu firmy
        const filtered = mappedTasks.filter(job => {
            const cat1 = (job.category || '').toLowerCase();
            const cat2 = (providerProfile.category || '').toLowerCase();
            // Luźne dopasowanie kategorii
            const categoryMatch = cat1.includes(cat2) || cat2.includes(cat1);
            const rangeMatch = job.range <= providerProfile.range;
            const dateMatch = job.date >= providerProfile.availableFrom;

            return categoryMatch && rangeMatch && dateMatch;
        });

        currentJobStack.value = filtered.sort(() => Math.random() - 0.5);
        viewState.value = 'swiping';

    } catch (error) {
        console.error("Błąd:", error);
        apiError.value = "Nie udało się pobrać zleceń. Upewnij się, że backend działa.";
    } finally {
        isLoading.value = false;
    }
}

// --- POZOSTAŁE FUNKCJE UI ---

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
                  <option>IT</option>
                  <option>Sprzątająca</option>
                  <option>Ogrody</option>
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

      <div class="sidebar-header">
        <span>Moje Zlecenia (Matche)</span>
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

          <div v-if="apiError" style="color: red; font-size: 12px; margin-top: 15px; text-align: center; background: #fff0f0; padding: 10px; border-radius: 8px;">
              ⚠️ {{ apiError }}
          </div>

          <div class="action-area" style="margin-top:auto;">
              <button class="btn-main" @click="fetchAndFilterJobs" :disabled="isLoading">
                  {{ isLoading ? 'Łączenie z bazą...' : 'Szukaj Zleceń 🔍' }}
              </button>
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
              <div v-if="!isLoading">
                  <div style="font-size: 40px; margin-bottom: 10px;">🏁</div>
                  <h2>Brak pasujących zleceń</h2>
                  <p>Brak zleceń w bazie dla Twoich kryteriów.</p>
                  <button class="btn-outline" @click="viewState='edit_offer'">Zmień kryteria</button>
              </div>
              <div v-else>
                  <h2>Ładowanie...</h2>
              </div>
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
                 Cześć! Jesteśmy zainteresowani tym zleceniem. Kiedy możemy omówić szczegóły?
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
/* --- STYLIZACJA KARTY --- */
.candidate-card {
    background-size: cover;
    background-position: center;
    position: relative;
    overflow: hidden;
    color: white;
    transition: transform 0.3s ease, opacity 0.3s ease;
}

.card-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.6) 50%, transparent 100%);
    padding: 30px 20px;
    box-sizing: border-box;
}

.info-pill {
    background: rgba(255,255,255,0.25);
    backdrop-filter: blur(5px);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.3);
}

.price-pill { color: #ffd700; border-color: rgba(255, 215, 0, 0.4); }

/* --- STYLIZACJA CHATU (ZE ZDJĘCIA) --- */
.chat-window {
    width: 100%;
    max-width: 600px; /* Szerokość jak na screenshocie */
    height: 70vh;
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
    margin-right: 15px; 
    border: 1px solid #eee;
}

.chat-close-btn {
    border: none; background: none; font-size: 20px; cursor: pointer; color: #999;
}
.chat-close-btn:hover { color: #333; }

.chat-body {
    flex: 1;
    padding: 20px;
    background: #f9f9f9;
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
    padding: 20px;
    border-top: 1px solid #eee;
    background: white;
}

.chat-input {
    width: 100%;
    border: 1px solid #ddd;
    padding: 12px 20px;
    border-radius: 30px;
    outline: none;
    transition: 0.3s;
    box-sizing: border-box;
    font-family: inherit;
}
.chat-input:focus { border-color: #fd297b; }

@keyframes popIn { from { transform: scale(0.95); opacity: 0; } to { transform: scale(1); opacity: 1; } }

/* --- BUTTONY STEROWANIA (Like/Nope) --- */
.btn-control {
    width: 70px; height: 70px; border-radius: 50%; border: none; background: white; font-size: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); cursor: pointer; 
    transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.btn-control.nope { color: #ec5e6f; }
.btn-control.like { color: #4caf50; }
.btn-control:hover { transform: scale(1.15); }

/* Inne */
.fly-right { transform: translateX(120%) rotate(20deg) !important; opacity: 0; }
.fly-left { transform: translateX(-120%) rotate(-20deg) !important; opacity: 0; }
</style>