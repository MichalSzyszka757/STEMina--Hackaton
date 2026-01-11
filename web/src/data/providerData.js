export const providerData = [
  {
    id: "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    role: "PROVIDER",
    name: "Salon Idealny",
    description: "Profesjonalne usługi fryzjerskie i barberskie. Strzyżenie na najwyższym poziomie.",
    email_address: "match@p.pl",
    phone_number: "123-456-789",

    // Lokalizacja
    city: "Kraków",
    address: "ul. Floriańska 15",
    location: 10, // Dystans od centrum (int)

    // Pola matchingu
    price_tier: "STANDARD", // Enum: BUDGET, STANDARD, PREMIUM
    lead_time: "week",      // Enum: week, 2week, 3week

    // Szczegóły profilu
    rating: 4.8,
    starting_year: 2015,
    owner: "Jan Kowalski",
    specialization_id: "uuid-kategorii-fryzjer", // Placeholder
    is_active: true
  },
  {
    id: "a123b456-7890-1234-5678-9abcde012345",
    role: "PROVIDER",
    name: "Hydraulik 24h",
    description: "Szybkie naprawy awarii hydraulicznych. Dojazd w 30 minut.",
    email_address: "kontakt@hydraulik24.pl",
    phone_number: "987-654-321",

    city: "Kraków",
    address: "ul. Długa 50",
    location: 5,

    price_tier: "BUDGET",
    lead_time: "week",

    rating: 4.2,
    starting_year: 2020,
    owner: "Marek Nowak",
    specialization_id: "uuid-kategorii-hydraulik",
    is_active: true
  },
  {
    id: "b987c654-3210-0987-6543-210987654321",
    role: "PROVIDER",
    name: "Salon Ekskluzywny",
    description: "Luksusowe zabiegi spa i pielęgnacja włosów dla wymagających.",
    email_address: "drogi@p.pl",
    phone_number: "555-555-555",

    city: "Kraków",
    address: "Rynek Główny 10",
    location: 0,

    price_tier: "PREMIUM",
    lead_time: "2week",

    rating: 5.0,
    starting_year: 2010,
    owner: "Anna Wiśniewska",
    specialization_id: "uuid-kategorii-fryzjer",
    is_active: true
  }
];
