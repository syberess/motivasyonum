import streamlit as st
import json
from model import duygu_tahmini
from utils import rastgele_hadis_getir, rastgele_alinti_getir, set_background
from utils import duygu_kaydet, duygu_grafigi_goster
from utils import favori_alinti_kaydet, favori_alintilari_getir
from utils import mongo_uzerinden_oneri_getir, mongo_uzerinden_oneri_ekle

# ✅ Sayfa yapılandırması
st.set_page_config(
    page_title="Motivasyonum 💡",  # Sekme başlığı
    page_icon="💡",                # Sekme simgesi (emoji ya da .ico da olabilir)
    layout="centered",             # Genişlik: 'centered' ya da 'wide'
    initial_sidebar_state="expanded"  # Sidebar varsayılan durumu
)
# 🎨 Tema Seçimi - Sidebar
tema = st.sidebar.selectbox("🎨 Tema Seçimi", ["Gündüz", "Gece"])

# 🎨 Tema CSS ayarı
if tema == "Gece":
    st.markdown("""
        <style>
        .stApp { background-color: #121212; color: #E0E0E0; }
        </style>
    """, unsafe_allow_html=True)
    secili_gorsel = "assets/gece.jpg"
else:
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF; color: #000000; }
        </style>
    """, unsafe_allow_html=True)
    secili_gorsel = "assets/gunduz.jpg"

# 🎨 Arka Plan Görseli
set_background(secili_gorsel)

# Sidebar'da Yönetici Paneli (Gizli)
with st.sidebar.expander("➕ Yeni Öneri Ekle (Yönetici Paneli)"):
    duygu_secim = st.selectbox("Duygu", ["Pozitif", "Negatif", "Nötr"], key="sidebar_duygu")
    kategori = st.text_input("Kategori", placeholder="Örnek: Teselli, Farkındalık", key="sidebar_kategori")
    mesaj = st.text_area("Mesaj", placeholder="Örnek: Kendine güven, her şey daha iyi olacak.", key="sidebar_mesaj")

    if st.button("📩 Öneriyi Kaydet", key="sidebar_gonder"):
        if mesaj.strip() == "":
            st.warning("Mesaj alanı boş bırakılamaz.")
        else:
            basarili, yanit = mongo_uzerinden_oneri_ekle(duygu_secim, kategori, mesaj)
            if basarili:
                st.sidebar.success("✅ Öneri başarıyla eklendi!")
            else:
                st.sidebar.error(yanit)

# 🎨 Ek CSS Stil
st.markdown("""
    <style>
    .stApp { filter: brightness(0.6); }
    .stTextArea textarea {
        background-color: rgba(30, 30, 30, 0.8) !important;
        color: #ffffff !important;
        font-size: 16px;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
    }
    .kutucuk {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 30px;
        border-radius: 15px;
        margin-top: 40px;
    }
    .alinan-yazi {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 10px;
        border-radius: 10px;
        color: #ddd;
        font-size: 18px;
        text-align: center;
        margin-bottom: 20px;
    }
    /*Mobil uyumluluk*/
    @media (max-width: 768px) {
    .stTextArea textarea {
        font-size: 14px !important;
        padding: 10px !important;
    }
    .kutucuk, .alinan-yazi {
        padding: 15px !important;
        font-size: 16px !important;
    }
    .stButton > button {
        font-size: 14px !important;
        padding: 8px 12px !important;
    }
}

    </style>
""", unsafe_allow_html=True)

# 🧘 Başlık ve alıntı kutusu
alinti = rastgele_alinti_getir()
st.markdown(f"""
    <div style='background-color: rgba(0, 0, 0, 0.65); padding: 30px; border-radius: 15px; margin-top: 30px; text-align: center;'>
        <h1 style='color: #ffa500;'>🧘 motivasyonum</h1>
        <h4 style='color: #ddd;'>Bugünkü ruh halini yaz, seni anlayalım ve motive edelim</h4>
        <p style='color: #ccc; font-size: 18px; margin-top: 20px;'>💬 {alinti}</p>
    </div>
""", unsafe_allow_html=True)

# ⭐ Beğendim butonu
if st.button("⭐ Bu alıntıyı beğendim"):
    favori_alinti_kaydet(alinti)
    st.success("Alıntı favorilere eklendi!")


metin = st.text_area("📝 Bugün nasıl hissediyorsun?", placeholder="Örnek: Bugün biraz yorgun hissediyorum ama geçecek...")

# Tavsiye Alma
if st.button("💡 Tavsiye Al"):
    if not metin.strip():
        st.warning("Lütfen bir şeyler yaz.")
    else:
        duygu = duygu_tahmini(metin)
        mesaj = mongo_uzerinden_oneri_getir(duygu)

        # 🟢 Duygu yalnızca burada kaydediliyor!
        duygu_kaydet(duygu)

        if duygu == "Negatif":
            st.markdown(f"""
            <div style='background-color: rgba(0, 0, 0, 0.55); padding: 20px; border-radius: 12px; margin-top: 25px;'>
                <p style='color: #e0f7fa; font-weight: bold; font-size: 18px;'>💭 Tespit edilen duygu: 
                    <span style="background-color:#8b0000; color:white; padding: 4px 8px; border-radius: 5px;">{duygu}</span></p>
                <p style='color: #e6f2ff; font-size: 16px;'>💬 {mesaj}</p>
                <p style='color: #ff9999; font-size: 20px; font-weight: bold; margin-top: 10px;'>🌧️ Zor bir gün olabilir…</p>
            </div>
            """, unsafe_allow_html=True)

        elif duygu == "Pozitif":
            st.markdown(f"""
            <div style='background-color: rgba(255, 255, 255, 0.15); padding: 20px; border-radius: 12px; margin-top: 25px;'>
                <p style='color: #d0f0c0; font-weight: bold; font-size: 18px;'>💭 Tespit edilen duygu: 
                    <span style="background-color:#228B22; color:white; padding: 4px 8px; border-radius: 5px;">{duygu}</span></p>
                <p style='color: #ccffcc; font-size: 16px;'>💬 {mesaj}</p>
                <p style='color: #90ee90; font-size: 20px; font-weight: bold; margin-top: 10px;'>🌞 Enerjin çok yüksek!</p>
            </div>
            """, unsafe_allow_html=True)

        elif duygu == "Nötr":
            st.markdown(f"""
            <div style='background-color: rgba(255, 255, 255, 0.20); padding: 20px; border-radius: 12px; margin-top: 25px;'>
                <p style='color: #fff8dc; font-weight: bold; font-size: 18px;'>💭 Tespit edilen duygu: 
                    <span style="background-color:#DAA520; color:black; padding: 4px 8px; border-radius: 5px;">{duygu}</span></p>
                <p style='color: #fdf5e6; font-size: 16px;'>💬 {mesaj}</p>
                <p style='color: #f5deb3; font-size: 20px; font-weight: bold; margin-top: 10px;'>🌤️ Dengede bir ruh hali.</p>
            </div>
            """, unsafe_allow_html=True)

# Günün Hadisi
if st.button("📖 Günün Hadisini Göster"):
    hadis = rastgele_hadis_getir()
    st.markdown(f"""
        <div style='background-color: rgba(0, 0, 0, 0.6); padding: 20px; border-radius: 10px; margin-top: 20px; text-align: center;'>
            <h3 style='color: #ffd700;'>🌟 Günün Hadisi</h3>
            <p style='color: #eee; font-size: 18px;'>{hadis}</p>
        </div>
    """, unsafe_allow_html=True)

# Duygu kaydetme & grafik
st.subheader("📊 Ruh Hali Takibin")
duygu_grafigi_goster()

# Favori alıntılar
favoriler = favori_alintilari_getir()
if favoriler:
    st.markdown("### 💖 Favorilerim")
    for fav in favoriler:
        st.markdown(f"- {fav}")

# Footer
st.markdown("""
    <hr style="border-top: 1px solid #bbb;">
    <p style='text-align: center; color: #eee; font-size: 14px; background-color: rgba(0,0,0,0.5); padding: 10px; border-radius: 10px;'>
    💡 <i>Bu uygulama seni anlamak ve desteklemek için tasarlandı. Unutma, yalnız değilsin 💙</i>
    </p>
""", unsafe_allow_html=True)
