# Gerekli kütüphaneleri içe aktar
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List, Dict, Any

# --- Ortam Değişkenlerini Yükleme ---
# .env dosyasından ortam değişkenlerini yükle
load_dotenv()

# Google Gemini API Yapılandırması
try:
    # .env dosyasından API anahtarını al
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        # Eğer API anahtarı bulunamazsa kullanıcıya hata göster ve uygulamayı durdur
        st.error("GOOGLE_API_KEY bulunamadı. Lütfen .env dosyanızı veya Streamlit secrets ayarlarınızı kontrol edin.")
        st.stop()
    
    # Gemini API'sini yapılandır
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Kullanılabilir modelleri listele
    print("Kullanılabilir modeller:")
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            available_models.append(m.name)
    
    # Modeli seç (eğer gemini-1.0-pro yoksa listedeki ilk modeli kullan)
    model_name = 'gemini-1.0-pro' if 'models/gemini-1.0-pro' in available_models else available_models[0].split('/')[-1]
    print(f"\nKullanılan model: {model_name}")
    
    # Modeli yükle
    model = genai.GenerativeModel(model_name)
except Exception as e:
    # API başlatılırken hata oluşursa kullanıcıya bilgi ver
    st.error(f"Gemini API başlatılırken hata oluştu: {str(e)}")
    st.stop()

# --- Uygulama Yapılandırması ---
# Sayfa başlığını, ikonunu ve düzenini ayarla
st.set_page_config(
    page_title="Mental Health Assistant",  # Tarayıcı sekme başlığı
    page_icon="🧠",                       # Tarayıcı sekme ikonu
    layout="wide"                         # Geniş düzen kullan
)

# --- Oturum Durumu Başlatma ---
# Eğer mesaj geçmişi yoksa, başlangıç mesajını oluştur
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",  # Asistan rolü
            "content": "Merhaba! Ben Zihinsel Sağlık Asistanınızım. Bugün nasıl hissediyorsunuz?"  # Hoş geldin mesajı
        }
    ]

# --- Sistem Talimatları ---
# Asistanın nasıl davranacağını belirleyen sistem talimatları
SYSTEM_PROMPT = """
Sen şefkatli ve profesyonel bir zihinsel sağlık asistanısın. Kullanıcılara destek olmak, 
yol göstermek ve kaynak sağlamak için buradasın.

Yönergeler:
1. Tüm yanıtlarında anlayışlı, yargısız ve destekleyici ol
2. Genel zihinsel sağlık bilgileri ve başa çıkma stratejileri sun
3. Uygun olduğunda profesyonel yardım öner
4. Sınırlarını koru (profesyonel yardımın yerine geçmediğini unutma)
5. Yanıtlarını kısa ve anlaşılır tut
6. Kullanıcı krizdeyse, acil servisleri veya bir kriz hattını aramasını öner
7. Aktif dinleme ve doğrulama üzerine odaklan

Her zaman şefkatli ve profesyonel bir şekilde yanıt ver.
"""

# --- Yardımcı Fonksiyonlar ---
def generate_response(user_input: str) -> str:
    """
    Gemini modelini kullanarak yanıt oluşturur
    
    Args:
        user_input (str): Kullanıcının girdiği metin
        
    Returns:
        str: Modelin oluşturduğu yanıt metni
    """
    try:
        # Bağlam için konuşma geçmişini ekle
        messages = [
            {"role": "user", "parts": [SYSTEM_PROMPT]},
            {"role": "model", "parts": ["Bu yönergeleri anladım ve uyacağım."]},
        ]
        
        # Son 4 mesajı bağlam olarak ekle (performans için sınırlı tutuyoruz)
        for msg in st.session_state.messages[-4:]:
            role = "user" if msg["role"] == "user" else "model"
            messages.append({"role": role, "parts": [msg["content"]]})
        
        # Yeni kullanıcı mesajını ekle
        messages.append({"role": "user", "parts": [user_input]})
        
        # Modelden yanıt oluştur
        response = model.generate_content(messages)
        return response.text
    except Exception as e:
        # Hata durumunda kullanıcıya bilgi ver
        return f"Üzgünüm, bir hata oluştu: {str(e)}. Lütfen tekrar deneyin."

# --- Kullanıcı Arayüzü Bileşenleri ---
def display_chat():
    """Sohbet mesajlarını ekranda gösterir"""
    for message in st.session_state.messages:
        # Her mesajı rolüne göre (kullanıcı/asistan) görüntüle
        with st.chat_message(message["role"]):
            st.write(message["content"])

def add_user_message(content: str):
    """
    Kullanıcı mesajını sohbet geçmişine ekler
    
    Args:
        content (str): Kullanıcının gönderdiği mesaj metni
    """
    st.session_state.messages.append({"role": "user", "content": content})

def add_assistant_message(content: str):
    """
    Asistan yanıtını sohbet geçmişine ekler
    
    Args:
        content (str): Asistanın oluşturduğu yanıt metni
    """
    st.session_state.messages.append({"role": "assistant", "content": content})

# --- Ana Uygulama ---
def main():
    """Uygulamanın ana fonksiyonu"""
    # Başlık ve açıklama ekle
    st.title("🧠 Zihinsel Sağlık Asistanı")
    st.caption("Zihinsel sağlık ve esenlik için destekleyici bir yapay zeka asistanı")
    
    # Sohbet mesajlarını göster
    display_chat()
    
    # Kullanıcı giriş alanı
    if prompt := st.chat_input("Bugün nasıl hissediyorsunuz?"):
        # Kullanıcı mesajını sohbet geçmişine ekle
        add_user_message(prompt)
        
        # Kullanıcı mesajını ekranda göster
        with st.chat_message("user"):
            st.write(prompt)
        
        # Asistan yanıtını oluştur ve göster
        with st.chat_message("assistant"):
            with st.spinner("Düşünüyorum..."):
                # Modelden yanıt oluştur
                response = generate_response(prompt)
                # Yanıtı ekranda göster
                st.write(response)
        
        # Asistan yanıtını sohbet geçmişine ekle
        add_assistant_message(response)

# --- Uygulamayı Çalıştır ---
if __name__ == "__main__":
    main()
