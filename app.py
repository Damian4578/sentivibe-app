import streamlit as st
import requests

# 1. Konfiguracja strony
st.set_page_config(page_title="SentiVibe AI", page_icon="🎙️")

# 2. TWÓJ TOKEN HUGGING FACE (Wklej go między cudzysłowy poniżej)
HF_TOKEN = "hf_gfHjYoPUGhBkvUSslRvnZazaRhYdTBd"

# Model Mistral - darmowy i świetny po polsku
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_ai(text, tryb_eksperta):
    # Tworzymy instrukcję dla modelu
    prompt = f"Jesteś ekspertem: {tryb_eksperta}. Odpowiedz krótko i konkretnie po polsku na problem: {text}"
    payload = {
        "inputs": f"<s>[INST] {prompt} [/INST]",
        "parameters": {"max_new_tokens": 500, "temperature": 0.7}
    }
    # Wysyłamy zapytanie do Hugging Face przez requests
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# 3. Interfejs SentiVibe
st.title("🎙️ SentiVibe.com")
st.write("Twoje wsparcie w trudnych rozmowach.")

with st.sidebar:
    st.header("🌟 VIP")
    kod = st.text_input("Kod:", type="password")
    is_vip = (kod == "PREMIER2024")

tryb = st.selectbox("Ekspert:", ["💼 Praca", "❤️ Związki", "🏛️ Urząd"])
user_text = st.text_area("Opisz sytuację:")

if st.button("Generuj Pomoc"):
    if user_text:
        with st.spinner('SentiVibe AI pracuje...'):
            try:
                res = query_ai(user_text, tryb)
                
                # Wyciąganie odpowiedzi z formatu HuggingFace
                if isinstance(res, list) and len(res) > 0:
                    raw_text = res[0].get('generated_text', '')
                    answer = raw_text.split("[/INST]")[-1].strip()
                    st.success("💡 Odpowiedź:")
                    st.write(answer)
                    
                    if not is_vip:
                        st.divider()
                        st.info("👉 [Rekomendacja eksperta](TWOJ_LINK_MYLEAD)")
                else:
                    st.info("🤖 AI się budzi... Kliknij przycisk jeszcze raz za 10 sekund!")
            except Exception as e:
                st.error("Wystąpił błąd połączenia. Spróbuj ponownie.")
    else:
        st.error("Wpisz tekst!")

st.markdown("---")
st.markdown("<center><small>SentiVibe.com © 2026</small></center>", unsafe_allow_html=True)
