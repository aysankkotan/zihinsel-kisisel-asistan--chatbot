# Gerekli kütüphaneleri içe aktar
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

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
    
    # Modeli seç (gemini-2.5-flash yoksa listedeki ilk modeli kullan)
    model_name = 'gemini-2.5-flash' if 'models/gemini-2.5-flash' in available_models else available_models[0].split('/')[-1]
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
            "role": "assistant",
            "content": "Merhaba! Ben Zihinsel Sağlık Asistanınızım. Bugün nasıl hissediyorsunuz?"
        }
    ]

# Tüm sohbet geçmişini bir dosyaya kaydet
def save_chat_history():
    with open("chat_history.txt", "w", encoding="utf-8") as f:
        for msg in st.session_state.messages:
            f.write(f"{msg['role']}:{msg['content']}\n")

# Eğer önceden kayıtlı sohbet geçmişi varsa yükle
try:
    if os.path.exists("chat_history.txt"):
        with open("chat_history.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            st.session_state.messages = []
            for line in lines:
                if ":" in line:
                    role, content = line.split(":", 1)
                    st.session_state.messages.append({"role": role, "content": content.strip()})
            
            # Eğer hiç mesaj yoksa başlangıç mesajını ekle
            if not st.session_state.messages:
                st.session_state.messages = [
                    {"role": "assistant", "content": "Merhaba! Ben Zihinsel Sağlık Asistanınızım. Bugün nasıl hissediyorsunuz?"}
                ]
except Exception as e:
    print(f"Sohbet geçmişi yüklenirken hata oluştu: {e}")
    st.session_state.messages = [
        {"role": "assistant", "content": "Merhaba! Ben Zihinsel Sağlık Asistanınızım. Bugün nasıl hissediyorsunuz?"}
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
    # Tüm mesajları göster
    for message in st.session_state.messages:
        role = message["role"]  # Doğrudan rolu kullan
        with st.chat_message(role):
            st.write(message["content"])

def add_user_message(content: str):
    """
    Kullanıcı mesajını sohbet geçmişine ekler ve ekranda gösterir
    
    Args:
        content (str): Kullanıcının gönderdiği mesaj metni
    """
    st.session_state.messages.append({"role": "user", "content": content})
    with st.chat_message("user"):
        st.write(content)

def add_assistant_message(content: str):
    """
    Asistan yanıtını sohbet geçmişine ekler ve ekranda gösterir
    
    Args:
        content (str): Asistanın oluşturduğu yanıt metni
    """
    st.session_state.messages.append({"role": "assistant", "content": content})
    with st.chat_message("assistant"):
        st.write(content)

# --- Ana Uygulama ---
def main():
    """Uygulamanın ana fonksiyonu"""
    # Başlık ve açıklama ekle
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🧠 Zihinsel Sağlık Asistanı")
        st.caption("Zihinsel sağlık ve esenlik için destekleyici bir yapay zeka asistanı")
    
    # Sohbeti temizle butonu
    with col2:
        if st.button("Sohbeti Temizle 🗑️", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": "Merhaba! Sohbet geçmişi temizlendi. Size nasıl yardımcı olabilirim?"}
            ]
            # Dosyayı temizle
            open("chat_history.txt", "w").close()
            st.rerun()
    
    # Sohbet mesajlarını göster
    st.divider()
    display_chat()
    
    # Kullanıcı giriş alanı
    if prompt := st.chat_input("Bugün nasıl hissediyorsunuz?"):
        # Kullanıcı mesajını ekle (otomatik olarak gösterilecek)
        add_user_message(prompt)
        
        # Asistan yanıtını oluştur
        with st.spinner("Düşünüyorum..."):
            response = generate_response(prompt)
            # Asistan yanıtını ekle (otomatik olarak gösterilecek)
            add_assistant_message(response)
        
        # Sohbet geçmişini kaydet
        save_chat_history()

# --- Uygulamayı Çalıştır ---
if __name__ == "__main__":
    main()
