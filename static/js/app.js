const { createApp } = Vue;

createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            viewState: 'init', // Startujemy od widoku "init" (pusty placeholder)
            
            // Model nowego zlecenia (rozszerzony o suwaki i kategorie)
            newOrder: {
                category: 'IT',
                title: '',
                desc: '',
                deadline: '',
                budget: 5000,     // Domyślna wartość suwaka
                range: 20,        // Domyślna wartość km
                delivery: false,
                availability: 'Od zaraz'
            },

            myOrders: [], // Historia zleceń (lewa kolumna)
            candidates: [], // Firmy do swipowania
            matches: []
        }
    },
    methods: {
        resetView() {
            this.viewState = 'create';
            // Resetujemy formularz do czystego stanu
            this.newOrder = {
                category: 'IT',
                title: '',
                desc: '',
                deadline: '',
                budget: 5000,
                range: 20,
                delivery: false,
                availability: 'Od zaraz'
            };
        },

        async saveAndMatch() {
            if(!this.newOrder.title) {
                alert("Wpisz chociaż nazwę usługi!");
                return;
            }

            // 1. Zapisz zlecenie do lewej kolumny (kopia obiektu)
            this.myOrders.push({...this.newOrder});

            // 2. Pobierz firmy (symulacja - w prawdziwej apce wysłałbyś kategorię do API)
            // Możemy tutaj dodać parametr do URL np. ?category=IT
            const response = await fetch('/api/companies');
            this.candidates = await response.json();
            
            // 3. Przełącz na widok swipowania
            this.viewState = 'swiping';
        },

        swipe(direction) {
            if (direction === 'right') {
                // Dodajemy do matchy
                this.matches.push(this.candidates[0]);
            }
            this.candidates.shift();
        }
    }
}).mount('#app');