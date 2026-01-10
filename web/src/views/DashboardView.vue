<script setup>
</script>

<!-- <template>
  <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />
    </div>
  </header>

  <main>
    <TheWelcome />
  </main>
</template> -->

<template>
  <div id="app" class="app-container">

    <div class="sidebar">
      <div class="sidebar-header">
        <i class="fa-solid fa-layer-group" style="margin-right: 10px;"></i>
        <span>Twoje Zlecenia</span>
      </div>

      <div class="sidebar-content">
        <button class="btn-outline" @click="resetView">
          <i class="fa-solid fa-plus"></i> Nowe Zlecenie
        </button>
        <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">

        <div v-for="(order, index) in myOrders" :key="index" class="match-item">
          <div class="avatar"
            style="background: #fd297b; color: white; display: flex; align-items: center; justify-content: center;">
            <i class="fa-solid fa-file-lines"></i>
          </div>
          <div>
            <strong>[[ order.title ]]</strong><br>
            <small>[[ order.category ]]</small>
          </div>
        </div>
      </div>
    </div>

    <div class="main-area">

      <div v-if="viewState === 'init'" class="placeholder-box" @click="viewState = 'create'">
        <div class="placeholder-content">
          <i class="fa-solid fa-circle-plus" style="font-size: 50px; color: #fd297b; margin-bottom: 20px;"></i>
          <h2>Utwórz pierwsze zlecenie</h2>
          <p>Kliknij, aby zdefiniować potrzeby i znaleźć partnera B2B.</p>
        </div>
      </div>

      <div v-if="viewState === 'create'" class="creation-container">
        <div class="tinder-card editable-card">
          <div class="card-scroll">
            <label class="label-mini">KATEGORIA</label>
            <select v-model="newOrder.category" class="input-clean">
              <option value="IT">IT & Programowanie</option>
              <option value="Gastro">Gastronomia / Catering</option>
              <option value="Marketing">Marketing & Social Media</option>
              <option value="Budowlanka">Budownictwo / Remonty</option>
            </select>

            <input type="text" v-model="newOrder.title" class="input-title"
              placeholder="Jaki typ usługi potrzebny? (np. Tort Urodzinowy)">

            <textarea v-model="newOrder.desc" class="input-desc"
              placeholder="Szczegóły poprawnego wykonania zadania..."></textarea>

            <div class="form-row">
              <div>
                <label class="label-mini">TERMIN WYKONANIA</label>
                <input type="date" v-model="newOrder.deadline" class="input-clean">
              </div>
              <div style="display: flex; align-items: center;">
                <input type="checkbox" id="delivery" v-model="newOrder.delivery"
                  style="width: auto; margin-right: 10px;">
                <label for="delivery" style="font-size: 14px; color: #555;">Dostawa dostępna</label>
              </div>
            </div>

            <div class="slider-container">
              <label class="label-mini">BUDŻET (PLN): <strong>[[ newOrder.budget ]] zł</strong></label>
              <input type="range" v-model="newOrder.budget" min="100" max="50000" step="100" class="slider">
            </div>

            <div class="slider-container">
              <label class="label-mini">ZASIĘG USŁUGI: <strong>[[ newOrder.range ]] km</strong></label>
              <input type="range" v-model="newOrder.range" min="0" max="100" class="slider">
            </div>

            <label class="label-mini">WYMAGANA DOSTĘPNOŚĆ</label>
            <select v-model="newOrder.availability" class="input-clean">
              <option>Od zaraz</option>
              <option>W ciągu tygodnia</option>
              <option>Do uzgodnienia</option>
            </select>
          </div>
        </div>

        <button class="btn-main big-btn" @click="saveAndMatch">
          Znajdź Match <i class="fa-solid fa-magnifying-glass"></i>
        </button>
      </div>

      <div v-if="viewState === 'swiping'" class="card-stack">
        <div v-if="candidates.length > 0" class="tinder-card">
          <div class="card-img" :style="{ backgroundImage: 'url(' + candidates[0].img + ')' }"></div>
          <div class="card-info">
            <h2>[[ candidates[0].name ]]</h2>
            <p>[[ candidates[0].desc ]]</p>
            <div style="margin-top: 10px;">
              <span class="tag">[[ newOrder.category ]]</span>
              <span class="tag">[[ newOrder.range ]] km od Ciebie</span>
            </div>
          </div>
          <div class="controls">
            <button class="control-btn nope" @click="swipe('left')"><i class="fa-solid fa-times"></i></button>
            <button class="control-btn like" @click="swipe('right')"><i class="fa-solid fa-heart"></i></button>
          </div>
        </div>
        <div v-else class="empty-state">
          <h3>To wszyscy w kategorii [[ newOrder.category ]]!</h3>
          <button class="btn-outline" @click="resetView">Wróć do edycji</button>
        </div>
      </div>

    </div>
  </div>

</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
