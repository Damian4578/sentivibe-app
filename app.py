import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# 1. Konfiguracja strony SentiVibe
st.set_page_config(page_title="SentiVibe - Twój Asystent", page_icon="🎙️")

# 2. Twój Klucz API (Wklej go między cudzysłowy poniżej)
API_KEY = "AIzaSyDwAlyHn2kFUgXU6B9tGrsVIPCZvs9AVrY" 

# 3. Logika VIP w panelu bocznym
with st.sidebar:
    st.header("🌟 SentiVibe VIP")
    kod_vip = st.text_input("Wpisz kod dostępu:", type="password")
    is_vip = (kod_vip == "PREMIER2024")
    
    if is_vip:
        st.success("Tryb VIP AKTYWNY")
    else:
        st.info("Tryb Darmowy (z reklamami)")

# 4. Połączenie z "Mózgiem" AI
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    st.title("🎙️ SentiVibe.com")
    st.caption("Profesjonalny asystent komunikacji i emocji.")
    
    # Wybór Eksperta
    tryb = st.selectbox("Wybierz eksperta:", ["💼 Praca (HR)", "❤️ Związki (Mediator)", "🏛️ Urząd (Prawnik)"])
    
    # Interfejs Mikrofonu TYLKO dla VIP
    audio_data = None
    if is_vip:
        st.subheader("🎤 Powiedz, co Cię gryzie:")
        audio_data = mic_recorder(start_prompt="Nagraj (VIP)", stop_prompt="Zatrzymaj", key='recorder')
        if audio_data:
            st.audio(audio_data['bytes'])
            st.info("Nagranie odebrane!")

    # Pole tekstowe dla wszystkich
    user_text = st.text_area("Opisz sytuację tekstowo:", placeholder="Np. Szef kazał mi zostać po godzinach...")

    # PRZYCISK GENEROWANIA (Naprawiony!)
    if st.button("SentiVibe - Generuj Pomoc"):
        # Sprawdzamy czy cokolwiek zostało podane (tekst LUB nagranie u VIP-a)
        if user_text or (is_vip and audio_data):
            with st.spinner('Analizuję sytuację...'):
                # Jeśli jest tylko nagranie, AI dostaje informację o tym
                tresc = user_text if user_text else "Użytkownik nagrał wiadomość głosową (VIP)."
                
                prompt = f"Działaj jako ekspert ({tryb}). Pomóż użytkownikowi rozwiązać ten problem: {tresc}"
                response = model.generate_content(prompt)
                
                st.subheader("💡 Twoje rozwiązanie:")
                st.write(response.text)
                
                # REKLAMA (Znika dla VIP)
                if not is_vip:
                    st.divider()
                    st.info("👉 **Rekomendacja eksperta:** [Sprawdź profesjonalne wsparcie tutaj](https://twoj-link-z-mylead.pl)")
        else:
            st.error("Wpisz tekst wiadomości lub użyj mikrofonu (VIP)!")
else:
    st.warning("Błąd: Brak klucza API. Sprawdź ustawienia!")

# Stopka
st.markdown("---")
st.markdown("<center><small>SentiVibe.com © 2026</small></center>", unsafe_allow_all_headers=True)
