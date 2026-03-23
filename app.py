import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# 1. Konfiguracja strony
st.set_page_config(page_title="SentiVibe", page_icon="🎙️")

# 2. Tu wklej swój klucz API z Google AI Studio
# Możesz go też podpiąć w Settings -> Secrets w Streamlit Cloud jako API_KEY
API_KEY = "AIzaSyDwAlyHn2kFUgXU6B9tGrsVIPCZvs9AVrY" 

if API_KEY and API_KEY != "TWÓJ_KLUCZ_API_TUTAJ":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    st.title("🎙️ SentiVibe.com")
    st.write("Wybierz eksperta i zacznij działać!")
    
    tryb = st.selectbox("Ekspert:", ["💼 Praca", "❤️ Związki", "🏛️ Urząd"])
    
    user_text = st.text_area("Opisz sytuację:")
    
    if st.button("Generuj pomoc"):
        if user_text:
            response = model.generate_content(f"Działaj jako ekspert ({tryb}). Pomóż użytkownikowi: {user_text}")
            st.success(response.text)
        else:
            st.error("Wpisz tekst!")
else:
    st.warning("Uzupełnij API_KEY w kodzie lub w Secrets!")
