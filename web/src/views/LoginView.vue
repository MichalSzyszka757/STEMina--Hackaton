<template>
    <div id="app" class="landing-container">
        <h1>Matchmaker dla B2B</h1>
        <div class="login-box">
            <h2 style="color: #fd297b;">Witaj</h2>
            <input type="text" v-model="username" placeholder="Nazwa użytkownika (admin)">
            <input type="password" v-model="password" placeholder="Hasło (admin)">
            <button class="btn-main" @click="handleLogin">Zaloguj się</button>
            <p style="font-size: 12px; color: #888; margin-top: 15px;">Nie masz konta? Zarejestruj się</p>
        </div>
    </div>
</template>