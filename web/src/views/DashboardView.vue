<script setup>
import { ref, reactive, computed } from 'vue'

// --- DANE UŻYTKOWNIKA (PROFIL) ---
const isEditingProfile = ref(false)
const userProfile = reactive({
    name: 'Jan Kowalski',
    address: 'ul. Prosta 1, Warszawa',
    phone: '+48 500 600 700',
    email: 'jan@firma.pl',
    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=400&q=80'
})

// --- STAN APLIKACJI ---
const viewState = ref('init') // 'init', 'create', 'swiping', 'chat'
const activeOrderIndex = ref(-1) // Indeks aktualnie wybranego zlecenia (-1 = brak/nowe)

const myOrders = ref([])

// Formularz nowego zlecenia
const newOrder = reactive({
  category: 'IT',
  title: '',
  desc: '',
  deadline: '',
  range: 50,
  availability: 'Od zaraz',
  budgetMin: 2000,
  budgetMax: 8000
})

// Mockowe dane kandydatów
const allCandidates = [
  { id: 1, name: "Code Wizards", desc: "Software House Python/Vue.", category: 'IT', img: "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?auto=format&fit=crop&w=400&q=80" },
  { id: 2, name: "Pixel Studio", desc: "Design i Branding.", category: 'IT', img: "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=400&q=80" },
  { id: 3, name: "Bud-Rem", desc: "Biura pod klucz.", category: 'Budownictwo', img: "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=400&q=80" },
  { id: 4, name: "Gastro Cheff", desc: "Catering premium.", category: 'Gastronomia', img: "https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=400&q=80" }
]

const currentCandidates = ref([]) // Kandydaci filtrowani do swipowania
const activeChatPartner = ref(null) // Z kim gadamy

// --- LOGIKA SUWAKA BUDŻETU ---
const minPriceLimit = 0
const maxPriceLimit = 20000
const sliderStyle = computed(() => {
  const minPercent = ((newOrder.budgetMin - minPriceLimit) / (maxPriceLimit - minPriceLimit)) * 100
  const maxPercent = ((newOrder.budgetMax - minPriceLimit) / (maxPriceLimit - minPriceLimit)) * 100
  return { left: `${minPercent}%`, width: `${maxPercent - minPercent}%` }
})
const validateMin = () => { if (newOrder.budgetMin > newOrder.budgetMax - 500) newOrder.budgetMin = newOrder.budgetMax - 500 }
const validateMax = () => { if (newOrder.budgetMax < newOrder.budgetMin + 500) newOrder.budgetMax = newOrder.budgetMin + 500 }

// --- AKCJE ---

// 1. Zapisz nowe zlecenie
const saveAndMatch = () => {
  if (!newOrder.title) return alert("Wpisz nazwę zlecenia!")
  
  // Tworzymy obiekt zlecenia z WŁASNĄ listą matches
  const orderData = { 
    ...newOrder, 
    id: Date.now(),
    displayBudget: `${newOrder.budgetMin} - ${newOrder.budgetMax}`,
    matches: [] // Pusta lista matchy dla tego konkretnego zlecenia
  }
  
  myOrders.value.push(orderData)
  
  // Ustawiamy to zlecenie jako aktywne
  activeOrderIndex.value = myOrders.value.length - 1
  
  // Pobieramy kandydatów pasujących do kategorii
  currentCandidates.value = allCandidates.filter(c => c.category === newOrder.category || c.category === 'IT')
  
  viewState.value = 'swiping'
}

// 2. Wybór zlecenia z listy (po lewej)
const selectOrder = (index) => {
    // Jeśli klikamy to samo, to zwijamy (opcjonalne), tutaj po prostu ustawiamy aktywne
    activeOrderIndex.value = index
    
    // Jeśli zlecenie nie ma jeszcze matchy, możemy wznowić szukanie, 
    // ale tutaj zakładamy, że wchodzimy w tryb podglądu/czatu
    if (myOrders.value[index].matches.length > 0) {
        viewState.value = 'chat_overview' // Widok ogólny albo czat
    } else {
        // Jak nie ma matchy, to może znowu swipowanie?
        // Na razie zostawmy init, żeby użytkownik wybrał co chce robić
        // viewState.value = 'swiping' // Opcjonalnie
    }
}

// 3. Swipe
const swipe = (direction) => {
  if (direction === 'right' && currentCandidates.value.length > 0) {
    // DODAJEMY MATCHA TYLKO DO AKTYWNEGO ZLECENIA
    if (activeOrderIndex.value !== -1) {
        myOrders.value[activeOrderIndex.value].matches.push(currentCandidates.value[0])
    }
  }
  
  currentCandidates.value.shift()

  if (currentCandidates.value.length === 0) {
    alert("Przejrzano wszystkich kandydatów dla tego zlecenia.")
    viewState.value = 'chat_overview' // Przejdź do widoku gdzie widać listę (czyli nic w main area, tylko sidebar aktywny)
  }
}

// 4. Otwórz czat
const openChat = (partner) => {
    activeChatPartner.value = partner
    viewState.value = 'chat'
}

const resetView = () => {
    viewState.value = 'create'
    activeOrderIndex.value = -1 // Reset wyboru
    // Czyścimy formularz
    newOrder.title = ''
    newOrder.desc = ''
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
              <input v-model="userProfile.name" class="input-clean" placeholder="Imię i nazwisko" style="font-size: 12px; padding: 5px;">
              <input v-model="userProfile.email" class="input-clean" placeholder="Email" style="font-size: 12px; padding: 5px;">
              <input v-model="userProfile.phone" class="input-clean" placeholder="Telefon" style="font-size: 12px; padding: 5px;">
              <input v-model="userProfile.address" class="input-clean" placeholder="Adres" style="font-size: 12px; padding: 5px;">
              <input v-model="userProfile.avatar" class="input-clean" placeholder="URL zdjęcia" style="font-size: 12px; padding: 5px;">
          </div>
      </div>

      <div class="sidebar-header" style="height: 50px; font-size: 16px;">
        <span>Moje Zlecenia</span>
      </div>
      
      <div class="sidebar-content">
        <button v-if="viewState !== 'create' && viewState !== 'init'" 
                @click="resetView" 
                style="width:100%; padding: 10px; border: 2px dashed #fd297b; color: #fd297b; background: white; border-radius: 10px; cursor: pointer; font-weight: bold; margin-bottom: 20px;">
          + Nowe Zlecenie
        </button>

        <div v-for="(order, index) in myOrders" :key="index">
            
            <div class="match-item" 
                 :class="{ 'active-order': activeOrderIndex === index }"
                 @click="selectOrder(index)">
                <div class="match-avatar" style="width: 35px; height: 35px; font-size: 14px;">
                    {{ order.category.charAt(0) }}
                </div>
                <div style="flex: 1;">
                    <strong style="font-size: 13px;">{{ order.title }}</strong><br>
                    <span style="font-size: 10px; color: #888;">{{ order.displayBudget }} PLN</span>
                </div>
                <div v-if="order.matches.length > 0" style="background: #fd297b; color: white; border-radius: 10px; padding: 2px 6px; font-size: 10px;">
                    {{ order.matches.length }}
                </div>
            </div>

            <div v-if="activeOrderIndex === index" class="sub-match-list">
                <div v-if="order.matches.length === 0" style="font-size: 11px; color: #999; padding: 5px;">
                    Brak matchy. Swipuj dalej!
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

            <label class="label-mini" style="margin-top: 25px;">
                BUDŻET: <span style="color: #fd297b;">{{ newOrder.budgetMin }} - {{ newOrder.budgetMax }} zł</span>
            </label>
            <div class="range-slider">
                <div class="slider-track"></div>
                <div class="slider-range-color" :style="sliderStyle"></div>
                <input type="range" :min="minPriceLimit" :max="maxPriceLimit" step="100" v-model.number="newOrder.budgetMin" @input="validateMin">
                <input type="range" :min="minPriceLimit" :max="maxPriceLimit" step="100" v-model.number="newOrder.budgetMax" @input="validateMax">
            </div>

            <label class="label-mini" style="margin-top: 25px;">ZASIĘG: {{ newOrder.range }} KM</label>
            <input type="range" v-model="newOrder.range" min="0" max="200" class="single-slider">
        </div>
        <div class="action-area">
            <button class="btn-main" @click="saveAndMatch">Znajdź Match 🔍</button>
        </div>
      </div>

      <div v-if="viewState === 'swiping'" style="display:flex; flex-direction: column; align-items: center;">
         <div v-if="currentCandidates.length > 0" class="tinder-card" 
              :style="{ backgroundImage: `url(${currentCandidates[0].img})`, backgroundSize: 'cover', backgroundPosition: 'center' }">
            <div style="position: absolute; bottom: 0; left: 0; padding: 25px; color: white; background: linear-gradient(transparent, rgba(0,0,0,0.9)); width: 100%; box-sizing: border-box;">
                <h2 style="margin: 0;">{{ currentCandidates[0].name }}</h2>
                <p>{{ currentCandidates[0].desc }}</p>
                <span style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 15px; font-size: 12px;">{{ newOrder.range }} km stąd</span>
            </div>
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
              <div style="background: #fd297b; color: white; padding: 10px 15px; border-radius: 15px; width: fit-content; margin-left: auto;">Super, kiedy możecie zacząć?</div>
          </div>
          <div style="padding: 15px; border-top: 1px solid #eee; display: flex;">
              <input type="text" placeholder="Napisz wiadomość..." style="flex: 1; border: 1px solid #ddd; padding: 10px; border-radius: 20px; outline: none;">
          </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* Dodatkowe style lokalne dla przycisków swipowania, jeśli nie ma ich w globalnym */
.btn-control {
    width: 70px; height: 70px; border-radius: 50%; border: none; background: white; font-size: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); cursor: pointer; transition: 0.2s;
}
.btn-control.nope { color: #ec5e6f; }
.btn-control.like { color: #4caf50; }
.btn-control:hover { transform: scale(1.1); }
</style>