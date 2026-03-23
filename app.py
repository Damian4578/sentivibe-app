import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# 1. Konfiguracja strony
st.set_page_config(page_title="SentiVibe - Twój Asystent", page_icon="🎙️")

# 2. Klucz API (Upewnij się, że jest poprawny!)
API_KEY = "AIzaSyDwAlyHn2kFUgXU6B9tGrsVIPCZvs9AVrY" 

# 3. Logika VIP (Panel boczny)
with st.sidebar:
    st.header("🌟 SentiVibe VIP")
    kod_vip = st.text_input("Wpisz kod dostępu:", type="password")
    is_vip = (kod_vip == "PREMIER2024")
    
    if is_vip:
        st.success("Tryb VIP AKTYWNY")
    else:
        st.info("Tryb Darmowy (z reklamami)")

# 4. Główne okno aplikacji
st.title("🎙️ SentiVibe.com")
st.caption("Profesjonalny asystent komunikacji i emocji.")

if API_KEY:
    try:
        # Konfiguracja bazowa
        genai.configure(api_key=API_KEY)
        
        # PRÓBA WYBORU MODELU (Różne nazwy dla różnych wersji API)
        model_name = 'gemini-1.5-flash' # Standard 2026
        model = genai.GenerativeModel(model_name)
        
        # Wybór Eksperta
        tryb = st.selectbox("Wybierz eksperta:", ["💼 Praca (HR)", "❤️ Związki (Mediator)", "🏛️ Urząd (Prawnik)"])
        
        # Interfejs Mikrofonu
        audio_data = None
        if is_vip:
            st.subheader("🎤 Powiedz, co Cię gryzie:")
            audio_data = mic_recorder(start_prompt="Nagraj (VIP)", stop_prompt="Zatrzymaj", key='recorder')
            if audio_data:
                st.audio(audio_data['bytes'])
        
        user_text = st.text_area("Opisz sytuację tekstowo:", placeholder="Np. Szef kazał mi zostać po godzinach...")

        # PRZYCISK GENEROWANIA
        if st.button("SentiVibe - Generuj Pomoc"):
            if user_text or (is_vip and audio_data):
                with st.spinner('SentiVibe analizuje dane...'):
                    context = user_text if user_text else "Użytkownik przesłał nagranie głosowe."
                    full_prompt = f"Jesteś ekspertem: {tryb}. Pomóż rozwiązać ten problem: {context}"
                    
                    try:
                        # Wymuszamy najprostszą metodę generowania
                        response = model.generate_content(full_prompt)
                        st.subheader("💡 Twoje rozwiązanie:")
                        st.write(response.text)
                        
                        if not is_vip:
                            st.divider()
                            st.info("👉 **Rekomendacja:** [Profesjonalne wsparcie](https://twoj-link-z-mylead.pl)")
                    except Exception as e:
                        # Jeśli flash nie działa, próbujemy starszy gemini-pro
                        try:
                            alt_model = genai.GenerativeModel('gemini-pro')
                            response = alt_model.generate_content(full_prompt)
                            st.write(response.text)
                        except:
                            st.error(f"Błąd modelu AI: {e}. Sprawdź czy Twój klucz API jest aktywny w Google AI Studio.")
            else:
                st.error("Wpisz wiadomość!")
                
    except Exception as e:
        st.error(f"Błąd systemu: {e}")
else:
    st.warning("Błąd: Brak klucza API.")

# Stopka
st.markdown("---")
st.markdown("<center><small>SentiVibe.com © 2026</small></center>", unsafe_allow_html=True)
