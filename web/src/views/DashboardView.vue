<script setup>
import { ref, reactive, computed } from 'vue'

// --- 1. DANE I KONFIGURACJA ---
const budgetLabels = ['Budget', 'Standard', 'Premium']

// Funkcja pomocnicza do wyświetlania dolarów
const getBudgetSign = (level) => {
    if (level === 0) return '$'       // Budget
    if (level === 1) return '$$'      // Standard
    return '$$$'                      // Premium
}
// Funkcja obliczająca styl gwiazdki (gradient)
const getStarStyle = (index, rating) => {
    // index to numer gwiazdki (1, 2, 3...)
    // rating to np. 3.5
    // Obliczamy ile % tej konkretnej gwiazdki ma być wypełnione
    const fill = Math.max(0, Math.min(1, rating - (index - 1))) * 100;

    // Jeśli gwiazdka jest pusta
    if (fill === 0) return { color: 'rgba(255, 255, 255, 0.3)' }
    
    // Jeśli gwiazdka jest pełna
    if (fill === 100) return { color: '#ffd700' }

    // Jeśli jest ułamkowa (np. 50%), używamy gradientu na tekście
    return {
        background: `linear-gradient(90deg, #ffd700 ${fill}%, rgba(255,255,255,0.3) ${fill}%)`,
        backgroundClip: 'text',
        '-webkit-background-clip': 'text',
        '-webkit-text-fill-color': 'transparent',
        color: 'transparent' // fallback
    }
}

// Mockowe dane kandydatów
const allCandidates = [
  { id: 1, name: "Code Wizards", years: 5, priceLevel: 2, rating: 4.8, desc: "Software House Python/Vue.", category: 'IT', img: "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?auto=format&fit=crop&w=600&q=80" },
  { id: 2, name: "Pixel Studio", years: 3, priceLevel: 1, rating: 3.5, desc: "Design i Branding.", category: 'IT', img: "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=600&q=80" },
  { id: 3, name: "Bud-Rem", years: 12, priceLevel: 1, rating: 4.2, desc: "Biura pod klucz.", category: 'Budownictwo', img: "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=600&q=80" },
  { id: 4, name: "Gastro Cheff", years: 8, priceLevel: 2, rating: 5.0, desc: "Catering premium.", category: 'Gastronomia', img: "https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=600&q=80" },
  { id: 5, name: "Marketing Ninja", years: 2, priceLevel: 0, rating: 2.5, desc: "Kampanie FB & Google Ads.", category: 'Marketing', img: "https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=600&q=80" }
]

// --- 2. STAN APLIKACJI ---
const isEditingProfile = ref(false)
const viewState = ref('init') 
const activeOrderIndex = ref(-1) 
const myOrders = ref([])
const currentCandidates = ref([]) 
const activeChatPartner = ref(null)
// Nowa zmienna do sterowania animacją karty
const swipeAnimation = ref('') 

const userProfile = reactive({
    name: 'Jan Kowalski',
    address: 'ul. Witolda Budryka 4, 30-072 Kraków', 
    phone: '+48 500 600 700',
    email: 'jan@firma.pl',
    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=400&q=80'
})

const newOrder = reactive({
  category: 'IT',
  title: '',
  desc: '',
  deadline: '', 
  range: 50,
  budgetLevel: 1 
})

// --- 3. LOGIKA ---

const rangeLabel = computed(() => {
    return newOrder.range >= 100 ? 'Nielimitowany' : `${newOrder.range} KM`
})

const loadCandidatesForOrder = (order) => {
    const matchedIds = order.matches.map(m => m.id)
    return allCandidates.filter(c => 
        (c.category === order.category || c.category === 'IT') && 
        !matchedIds.includes(c.id)
    )
}

const saveAndMatch = () => {
  if (!newOrder.title) return alert("Wpisz nazwę zlecenia!")
  const orderData = { 
    ...newOrder, 
    id: Date.now(),
    displayBudget: budgetLabels[newOrder.budgetLevel],
    matches: [] 
  }
  myOrders.value.push(orderData)
  activeOrderIndex.value = myOrders.value.length - 1
  currentCandidates.value = loadCandidatesForOrder(orderData)
  viewState.value = 'swiping'
}

const selectOrder = (index) => {
    activeOrderIndex.value = index
    if (myOrders.value[index].matches.length > 0) {
        viewState.value = 'chat_overview' 
    }
}

const resumeSwiping = (index, event) => {
    if(event) event.stopPropagation(); 
    activeOrderIndex.value = index
    const order = myOrders.value[index]
    currentCandidates.value = loadCandidatesForOrder(order)
    viewState.value = 'swiping'
}

// Zaktualizowana logika Swipowania z animacją
const swipe = (direction) => {
  if (currentCandidates.value.length === 0) return

  // 1. Ustaw klasę animacji
  swipeAnimation.value = direction === 'right' ? 'fly-right' : 'fly-left'

  // 2. Poczekaj aż animacja się skończy (np. 300ms) zanim usuniesz dane
  setTimeout(() => {
      if (direction === 'right') {
        if (activeOrderIndex.value !== -1) {
            myOrders.value[activeOrderIndex.value].matches.push(currentCandidates.value[0])
        }
      }
      
      // Usuń kartę i zresetuj animację
      currentCandidates.value.shift()
      swipeAnimation.value = ''

      if (currentCandidates.value.length === 0) {
        // Małe opóźnienie dla UX
        setTimeout(() => {
             // viewState handled by template logic
        }, 100)
      }
  }, 300) 
}

const openChat = (partner) => {
    activeChatPartner.value = partner
    viewState.value = 'chat'
}

const resetView = () => {
    viewState.value = 'create'
    activeOrderIndex.value = -1 
    newOrder.title = ''
    newOrder.desc = ''
    newOrder.range = 50
    newOrder.budgetLevel = 1
}
</script>

<template>
  <div class="app-container">
    
    <div class="sidebar">
      <div class="user-profile-section">
          <div class="profile-header">
              <div class="profile-avatar" :style="{ backgroundImage: `url(${userProfile.avatar})` }"></div>
              <div class="profile-info" v-if="!isEditingProfile">
                  <h3>{{ userProfile.name }}</h3>
                  <p>{{ userProfile.email }}</p>
                  <button class="btn-small" @click="isEditingProfile = true">Edytuj dane</button>
              </div>
              <div class="profile-info" v-else>
                  <button class="btn-small" @click="isEditingProfile = false">Zapisz</button>
              </div>
          </div>
          <div v-if="!isEditingProfile" style="font-size: 12px; color: #555;">
              <p><i class="fa-solid fa-phone"></i> {{ userProfile.phone }}</p>
              <p><i class="fa-solid fa-location-dot"></i> {{ userProfile.address }}</p>
          </div>
          <div v-else style="display: flex; flex-direction: column; gap: 5px;">
              <label style="font-size: 10px; color: #999;">Imię i Nazwisko</label>
              <input v-model="userProfile.name" class="input-clean" placeholder="Imię i nazwisko" style="font-size: 12px; padding: 5px;">
              
              <label style="font-size: 10px; color: #999;">Email</label>
              <input v-model="userProfile.email" class="input-clean" placeholder="Email" style="font-size: 12px; padding: 5px;">
              
              <label style="font-size: 10px; color: #999;">Telefon</label>
              <input v-model="userProfile.phone" class="input-clean" placeholder="Telefon" style="font-size: 12px; padding: 5px;">
              
              <label style="font-size: 10px; color: #999;">Adres</label>
              <input v-model="userProfile.address" class="input-clean" placeholder="Adres" style="font-size: 12px; padding: 5px;">
              
              <label style="font-size: 10px; color: #999;">Link do Avatara</label>
              <input v-model="userProfile.avatar" class="input-clean" placeholder="URL zdjęcia" style="font-size: 12px; padding: 5px;">
          </div>
      </div>

      <div class="sidebar-header" style="height: 50px; font-size: 16px;">
        <span>Moje Zlecenia</span>
      </div>
      
      <div class="sidebar-content">
        <button v-if="viewState !== 'create' && viewState !== 'init'" @click="resetView" class="btn-new-order">
          + Nowe Zlecenie
        </button>

        <div v-for="(order, index) in myOrders" :key="index">
            <div class="match-item" :class="{ 'active-order': activeOrderIndex === index }" @click="selectOrder(index)">
                <div class="match-avatar" style="width: 35px; height: 35px; font-size: 14px;">{{ order.category.charAt(0) }}</div>
                <div style="flex: 1;">
                    <strong style="font-size: 13px;">{{ order.title }}</strong><br>
                    <span style="font-size: 10px; color: #888;">{{ order.displayBudget }}</span>
                </div>
                <button class="btn-resume" @click="resumeSwiping(index, $event)" title="Szukaj dalej">🔍</button>
                <div v-if="order.matches.length > 0" class="badge">{{ order.matches.length }}</div>
            </div>
            
            <div v-if="activeOrderIndex === index" class="sub-match-list">
                <div v-if="order.matches.length === 0" style="font-size: 11px; color: #999; padding: 5px;">
                    Brak par. Kliknij lupę 🔍 aby szukać.
                </div>
                <div v-for="match in order.matches" :key="match.id" class="sub-match-item" @click="openChat(match)">
                    <div class="match-avatar" :style="{ backgroundImage: `url(${match.img})` }" style="width: 25px; height: 25px; margin-right: 10px;"></div>
                    <span>{{ match.name }}</span>
                    <i class="fa-solid fa-comment-dots" style="margin-left: auto; color: #ccc;"></i>
                </div>
            </div>
        </div>
      </div>
    </div>

    <div class="main-area">
      
      <div v-if="viewState === 'init'" class="placeholder-box" @click="viewState = 'create'">
        <div style="font-size: 60px; color: #fd297b; margin-bottom: 20px;">+</div>
        <h2>Utwórz zlecenie</h2>
        <p>Zdefiniuj potrzeby i znajdź wykonawcę.</p>
      </div>

      <div v-if="viewState === 'create'" style="display:flex; flex-direction: column; align-items: center;">
        <div class="tinder-card editable-card">
            <label class="label-mini">KATEGORIA</label>
            <select v-model="newOrder.category" class="input-clean">
                <option value="IT">IT & Programowanie</option>
                <option value="Gastronomia">Gastronomia / Catering</option>
                <option value="Budownictwo">Budownictwo / Remonty</option>
                <option value="Marketing">Marketing</option>
            </select>
            <input type="text" v-model="newOrder.title" class="input-title" placeholder="Czego potrzebujesz?">
            <textarea v-model="newOrder.desc" class="input-clean" rows="3" placeholder="Szczegóły..." style="resize: none;"></textarea>

            <label class="label-mini" style="margin-top: 30px;">
                POZIOM BUDŻETU: <span style="color: #fd297b; font-weight: 800;">{{ budgetLabels[newOrder.budgetLevel] }}</span>
            </label>
            <div class="step-slider-container">
                <input type="range" min="0" max="2" step="1" v-model="newOrder.budgetLevel" class="step-slider">
                <div class="step-labels">
                    <span :class="{ 'active-label': newOrder.budgetLevel == 0 }">Budget</span>
                    <span :class="{ 'active-label': newOrder.budgetLevel == 1 }">Standard</span>
                    <span :class="{ 'active-label': newOrder.budgetLevel == 2 }">Premium</span>
                </div>
            </div>

            <label class="label-mini" style="margin-top: 25px;">ZASIĘG: <strong style="color:#333">{{ rangeLabel }}</strong></label>
            <input type="range" v-model="newOrder.range" min="0" max="100" class="single-slider">
            
            <label class="label-mini" style="margin-top: 25px;">TERMIN</label>
            <input type="date" v-model="newOrder.deadline" class="input-clean" style="font-family: sans-serif; color: #555;">
        </div>
        <div class="action-area">
            <button class="btn-main" @click="saveAndMatch">Znajdź Match 🔍</button>
        </div>
      </div>

      <div v-if="viewState === 'swiping'" style="display:flex; flex-direction: column; align-items: center;">
         
         <div v-if="currentCandidates.length > 0" 
              class="tinder-card candidate-card" 
              :class="swipeAnimation"
              :style="{ backgroundImage: `url(${currentCandidates[0].img})` }">
            
            <div class="card-overlay">
                <h2 style="margin: 0; font-size: 28px; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">
                    {{ currentCandidates[0].name }}, 
                    <span style="font-weight: 400; font-size: 24px;">{{ currentCandidates[0].years }} lat</span>
                </h2>
                
                <p style="margin: 5px 0 15px 0; font-size: 16px; opacity: 0.9; text-shadow: 0 1px 2px rgba(0,0,0,0.5);">
                    {{ currentCandidates[0].desc }}
                </p>
                
                <div style="display: flex; gap: 10px;">
                    <span class="info-pill">
                        📍 {{ newOrder.range }} km
                    </span>
                    <span class="info-pill price-pill">
                        {{ getBudgetSign(currentCandidates[0].priceLevel) }}
                    </span>
                    <div class="info-pill stars-pill">
                      <span v-for="n in 5" :key="n" 
                            class="star-icon" 
                            :style="getStarStyle(n, currentCandidates[0].rating)">
                          ★
                      </span>
                      <span style="margin-left: 5px; font-size: 12px; font-weight: bold;">
                          {{ currentCandidates[0].rating }}
                      </span>
                  </div>
                </div>
            </div>
         </div>
         
         <div v-else class="tinder-card" style="display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; color:#888;">
            <div style="font-size:50px; margin-bottom:20px;">🏁</div>
            <h2>To już wszyscy!</h2>
            <p style="padding: 0 40px;">Brak nowych firm w tej kategorii.</p>
            <button class="btn-outline" style="margin-top:30px;" @click="viewState = 'create'">Wróć do edycji</button>
         </div>

         <div v-if="currentCandidates.length > 0" style="display: flex; gap: 30px; margin-top: 30px;">
             <button @click="swipe('left')" class="btn-control nope">✖</button>
             <button @click="swipe('right')" class="btn-control like">❤</button>
         </div>
      </div>

      <div v-if="viewState === 'chat'" class="chat-window" style="width: 100%; max-width: 600px; height: 80vh; background: white; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); display: flex; flex-direction: column; overflow: hidden;">
          <div style="padding: 20px; border-bottom: 1px solid #eee; display: flex; align-items: center; justify-content: space-between;">
              <div style="display: flex; align-items: center;">
                  <div :style="{ backgroundImage: `url(${activeChatPartner.img})` }" style="width: 40px; height: 40px; border-radius: 50%; background-size: cover; margin-right: 10px;"></div>
                  <strong>{{ activeChatPartner.name }}</strong>
              </div>
              <button @click="viewState = 'chat_overview'" style="border:none; background:none; font-size: 20px; cursor: pointer;">✕</button>
          </div>
          <div style="flex: 1; padding: 20px; background: #f9f9f9; overflow-y: auto;">
              <div style="background: #eee; padding: 10px 15px; border-radius: 15px; width: fit-content; margin-bottom: 10px;">Cześć! Jesteśmy zainteresowani Twoim zleceniem.</div>
          </div>
          <div style="padding: 15px; border-top: 1px solid #eee; display: flex;">
              <input type="text" placeholder="Napisz wiadomość..." style="flex: 1; border: 1px solid #ddd; padding: 10px; border-radius: 20px; outline: none;">
          </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* Style Layoutu Karty */
.candidate-card {
    background-size: cover;
    background-position: center;
    position: relative;
    overflow: hidden;
    color: white;
    /* Płynne przejścia dla animacji */
    transition: transform 0.3s ease, opacity 0.3s ease;
}

/* Overlay gradientowy na dole karty */
.card-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    /* Gradient od przezroczystego do czarnego */
    background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.6) 50%, transparent 100%);
    padding: 30px 20px;
    box-sizing: border-box;
}

/* Styl tagów (km, cena) */
.info-pill {
    background: rgba(255,255,255,0.25);
    backdrop-filter: blur(5px);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.3);
}

.price-pill {
    color: #ffd700; /* Złoty kolor dla dolarów */
    border-color: rgba(255, 215, 0, 0.4);
}

/* ANIMACJE SWIPOWANIA */
.fly-right {
    transform: translateX(120%) rotate(20deg) !important;
    opacity: 0;
}

.fly-left {
    transform: translateX(-120%) rotate(-20deg) !important;
    opacity: 0;
}

/* Style przycisków sterowania */
.btn-control {
    width: 70px; height: 70px; border-radius: 50%; border: none; background: white; font-size: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); cursor: pointer; 
    transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Sprężysty efekt */
}
.btn-control.nope { color: #ec5e6f; }
.btn-control.like { color: #4caf50; }

/* Efekt wychylania po najechaniu */
.btn-control:hover { 
    transform: scale(1.15); 
}
.btn-control.like:hover {
    box-shadow: 0 10px 25px rgba(76, 175, 80, 0.4);
}
.btn-control.nope:hover {
    box-shadow: 0 10px 25px rgba(236, 94, 111, 0.4);
}

/* --- Style dla Gwiazdek --- */

.stars-pill {
    display: flex;
    align-items: center;
    border-color: rgba(255, 255, 255, 0.3); /* Biała ramka jak reszta */
    padding: 6px 10px; /* Nieco mniejszy padding żeby nie było za szerokie */
}

.star-icon {
    font-size: 14px;
    margin-right: 1px;
    color: rgba(255, 255, 255, 0.3); /* Kolor nieaktywnej gwiazdki (półprzezroczysty biały) */
    transition: color 0.3s;
}


/* Pozostałe style (Suwaki itp.) - bez zmian */
.step-slider-container { margin-top: 10px; width: 100%; }
.step-slider { -webkit-appearance: none; width: 100%; height: 6px; background: #eee; border-radius: 5px; outline: none; cursor: pointer; }
.step-slider::-webkit-slider-thumb { -webkit-appearance: none; width: 24px; height: 24px; border-radius: 50%; background: #fd297b; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.2); cursor: pointer; transition: transform 0.2s; }
.step-slider::-webkit-slider-thumb:hover { transform: scale(1.1); }
.step-labels { display: flex; justify-content: space-between; margin-top: 10px; font-size: 12px; color: #aaa; font-weight: 600; }
.active-label { color: #fd297b; font-weight: bold; }
.single-slider { -webkit-appearance: none; width: 100%; height: 6px; background: #eee; border-radius: 5px; outline: none; margin-top: 10px; }
.single-slider::-webkit-slider-thumb { -webkit-appearance: none; width: 20px; height: 20px; border-radius: 50%; background: #fd297b; cursor: pointer; }
.btn-new-order { width:100%; padding: 10px; border: 2px dashed #fd297b; color: #fd297b; background: white; border-radius: 10px; cursor: pointer; font-weight: bold; margin-bottom: 20px; }
.badge { background: #fd297b; color: white; border-radius: 10px; padding: 2px 6px; font-size: 10px; }
.btn-resume { background: none; border: none; cursor: pointer; font-size: 16px; margin: 0 10px; padding: 5px; border-radius: 50%; transition: background 0.2s; }
.btn-resume:hover { background: #eee; }
.btn-outline { background: transparent; border: 2px solid #fd297b; color: #fd297b; padding: 10px 20px; border-radius: 25px; cursor: pointer; font-weight: bold; transition: 0.3s; }
.btn-outline:hover { background: #fd297b; color: white; }
</style>