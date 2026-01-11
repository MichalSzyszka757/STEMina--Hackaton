export const taskData = [
  {
    id: "c567d890-1234-5678-9012-345678901234",
    title: "Strzyżenie męskie",
    details: "Szukam fryzjera, który ogarnie krótkie cieniowanie boków (fade).",
    status: "OPEN",

    // Wymagania Klienta (Matching)
    budget: "STANDARD",      // Enum
    deadline_limit: "2week", // Enum
    max_distance: 20,        // km
    client_location: 0,      // Lokalizacja klienta (np. centrum)

    // Powiązania
    client_id: "uuid-klienta-jan",
    category_id: "uuid-kategorii-fryzjer",

    // Termin
    deadline: "2026-02-01T12:00:00",
    created_at: "2026-01-11T09:00:00"
  },
  {
    id: "d678e901-2345-6789-0123-456789012345",
    title: "Cieknący kran w kuchni",
    details: "Kran kapie, uszczelka do wymiany albo cała bateria. Proszę o szybki kontakt.",
    status: "OPEN",

    budget: "BUDGET",
    deadline_limit: "week",
    max_distance: 10,
    client_location: 5,

    client_id: "uuid-klienta-maria",
    category_id: "uuid-kategorii-hydraulik",

    deadline: "2026-01-15T18:00:00",
    created_at: "2026-01-10T14:30:00"
  },
  {
    id: "e789f012-3456-7890-1234-567890123456",
    title: "Sprzątanie biura 100m2",
    details: "Kompleksowe sprzątanie po remoncie. Mycie okien, podłóg.",
    status: "ASSIGNED", // Zadanie już przypisane

    budget: "PREMIUM",
    deadline_limit: "week",
    max_distance: 50,
    client_location: 15,

    client_id: "uuid-klienta-firma-xyz",
    category_id: "uuid-kategorii-sprzatanie",
    provider_id: "f47ac10b-58cc-4372-a567-0e02b2c3d479", // Przypisane do Salon Idealny (przykładowo)

    deadline: "2026-01-20T08:00:00",
    created_at: "2026-01-09T10:00:00"
  }
];
