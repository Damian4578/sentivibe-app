import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# 1. Konfiguracja strony
st.set_page_config(page_title="SentiVibe", page_icon="🎙️")

# 2. Twój Klucz (pamiętaj o cudzysłowie na końcu!)
API_KEY = "AIzaSyDwAlyHn2kFUgXU6B9tGrsVIPCZvs9AVrY" 

# 3. Panel boczny (VIP)
with st.sidebar:
    st.header("SentiVibe VIP")
    kod = st.text_input("Wpisz kod dostępu:", type="password")
    if kod == "PREMIER2024":
        st.success("🌟 Tryb VIP AKTYWNY")
        is_vip = True
    else:
        st.warning("Tryb Darmowy (z reklamami)")
        is_vip = False

# 4. Logika AI
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    st.title("🎙️ SentiVibe.com")
    st.write("Wybierz eksperta i zacznij działać!")
    
    tryb = st.selectbox("Ekspert:", ["💼 Praca", "❤️ Związki", "🏛️ Urząd"])
    
    user_text = st.text_area("Opisz sytuację (lub nagraj wiadomość poniżej):")

    # Dodatek mikrofonu dla VIP
    if is_vip:
        audio = mic_recorder(start_prompt="Nagraj wiadomość (VIP)", stop_prompt="Zatrzymaj", key='recorder')
        if audio:
            st.audio(audio['bytes'])
            st.info("Nagranie odebrane!")

    if st.button("SentiVibe - Generuj Pomoc"):
        if user_text:
            with st.spinner('Ekspert myśli...'):
                prompt = f"Działaj jako ekspert ({tryb}). Pomóż użytkownikowi: {user_text}"
                response = model.generate_content(prompt)
                st.success(response.text)
                
                # REKLAMA - wyświetla się tylko jeśli NIE jest VIP
                if not is_vip:
                    st.divider()
                    st.info("👉 **Rekomendacja eksperta:** [Sprawdź profesjonalne wsparcie tutaj](TWOJ_LINK_Z_MYLEAD)")
        else:
            st.error("Wpisz tekst!")
else:
    st.warning("Błąd konfiguracji klucza API!")
