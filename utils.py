import base64
import json
import random
import streamlit as st
from datetime import datetime
import os
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta
import seaborn as sns
from model import duygu_tahmini
from pymongo import MongoClient
from dotenv import load_dotenv

def rastgele_hadis_getir(json_dosya="hadisler.json"):
    try:
        with open(json_dosya, "r", encoding="utf-8") as f:
            veriler = json.load(f) #JSON içeriği Python sözlüğüne (dict) çevrilir. 
        hadisler = veriler.get("hadisler", [])
        return random.choice(hadisler) if hadisler else "Bugün için hadis bulunamadı."
    except:
        return "Hadis dosyası okunamadı."
# Arka plan ayarlama fonksiyonu
def set_background(image_path):
    try:
        with open(image_path, "rb") as img_file: #Görsel ikili (binary) olarak açılır. İçeriği base64 formatına çevrilir.Bu format, HTML içinde gömülü resim göstermek için kullanılır.


            encoded = base64.b64encode(img_file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("Arka plan görseli bulunamadı.")

# Rastgele alıntı getir
def rastgele_alinti_getir(json_dosya="alintilar.json"):
    try:
        with open(json_dosya, "r", encoding="utf-8") as f:
            alintilar = json.load(f)["alintilar"]
        return random.choice(alintilar) if alintilar else "Bugünlük alıntı bulunamadı."
    except:
        return "Alıntı dosyası okunamadı."
    

#duygu kaydetme
def duygu_kaydet(duygu, json_dosya="duygu_kayit.json"):
    """
    Tarihle birlikte duygu kaydını JSON dosyasına ekler.
    JSON bozulmuşsa sıfırdan başlar. Duygu tipi otomatik stringe dönüştürülür.
    """
    kayit = {
        "tarih": datetime.today().strftime("%Y-%m-%d"),
        "duygu": str(duygu)  # float32, NoneType gibi durumlara karşı koruma
    }

    # Dosya varsa oku, yoksa boş liste başlat
    if os.path.exists(json_dosya):
        try:
            with open(json_dosya, "r", encoding="utf-8") as f:
                veriler = json.load(f)
        except (json.JSONDecodeError, ValueError):
            veriler = []
    else:
        veriler = []

    veriler.append(kayit)

    # Kaydı JSON olarak yaz, JSON uyumsuz türleri otomatik string yap
    with open(json_dosya, "w", encoding="utf-8") as f:
        json.dump(veriler, f, indent=4, ensure_ascii=False, default=str)


def duygu_grafigi_goster(json_dosya="duygu_kayit.json"):
    if not os.path.exists(json_dosya):
        st.info("Henüz duygu kaydı yok.")
        return

    with open(json_dosya, "r", encoding="utf-8") as f:
        veriler = json.load(f)

    df = pd.DataFrame(veriler)

    if df.empty or "duygu" not in df.columns:
        st.warning("Geçerli veri bulunamadı.")
        return

    df["tarih"] = pd.to_datetime(df["tarih"])

    # ❌ "Girdi boş!" kayıtlarını filtrele
    df = df[~df["duygu"].isin(["Girdi boş!", "", None])]

    # 📆 Son 7 gün
    son_7_gun = datetime.today() - timedelta(days=6)
    df = df[df["tarih"] >= son_7_gun]

    if df.empty:
        st.warning("Son 7 güne ait geçerli duygu kaydı yok.")
        return

    # 📊 Gruplama
    grafik_df = df.groupby([df["tarih"].dt.date, "duygu"]).size().unstack(fill_value=0)

    # 🟩 Renk tanımı
    renkler = {
        "Pozitif": "#4CAF50",   # yeşil
        "Negatif": "#F44336",   # kırmızı
        "Nötr": "#9E9E9E"       # gri
    }

    # 🔁 Eksik duygu kolonlarını sıfırla (örneğin 'Nötr' yoksa ekle)
    for duygu in ["Pozitif", "Negatif", "Nötr"]:
        if duygu not in grafik_df.columns:
            grafik_df[duygu] = 0

    grafik_df = grafik_df[["Pozitif", "Nötr", "Negatif"]]  # sırayı belirle

    # 🖼️ Grafik çizimi
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = grafik_df.plot(kind="bar", stacked=True, ax=ax, color=[renkler[d] for d in grafik_df.columns])

    # 🏷️ Etiket ekle
    for container in ax.containers:
        ax.bar_label(container, label_type='center', color='white', fontsize=9, weight='bold')

    # 🎨 Tasarım ayarları
    ax.set_title("Son 7 Günlük Ruh Hali Takibi", fontsize=14)
    ax.set_xlabel("Tarih", fontsize=12)
    ax.set_ylabel("Girdi Sayısı", fontsize=12)
    ax.set_xticklabels([t.strftime("%d %b") for t in grafik_df.index], rotation=45)
    ax.legend(title="Duygu")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()

    st.pyplot(fig)

def favori_alinti_kaydet(alinti, dosya_adi="favori_alintilar.json"):
    if not os.path.exists(dosya_adi):
        with open(dosya_adi, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    with open(dosya_adi, "r", encoding="utf-8") as f:
        try:
            mevcutlar = json.load(f)
        except json.JSONDecodeError:
            mevcutlar = []

    if alinti not in mevcutlar:
        mevcutlar.append(alinti)
        with open(dosya_adi, "w", encoding="utf-8") as f:
            json.dump(mevcutlar, f, ensure_ascii=False, indent=4)

def favori_alintilari_getir(dosya_adi="favori_alintilar.json"):
    if os.path.exists(dosya_adi):
        with open(dosya_adi, "r", encoding="utf-8") as f:
            return json.load(f)
    return []





def mongo_uzerinden_oneri_getir(duygu):
    try:
        mongo_uri = os.getenv("MONGO_URI")
        db_name = os.getenv("DB_NAME")
        collection_name = os.getenv("COLLECTION_ADI")

        client = MongoClient(mongo_uri)
        db = client[db_name]
        koleksiyon = db[collection_name]

        # Duygu eşleşmesini küçük/büyük harf farkı gözetmeden yap
        belgeler = list(koleksiyon.find({"duygu": {"$regex": f"^{duygu}$", "$options": "i"}}))

        if not belgeler:
            print(f"[UYARI] '{duygu}' için öneri bulunamadı.")  # loglama
            return "Şu an için öneri bulunamadı."

        secilen = random.choice(belgeler)
        return secilen.get("mesaj", "Öneri eksik.")
    except Exception as e:
        print(f"[HATA] Mongo bağlantısı: {e}")  # loglama
        return "Bağlantı hatası."







load_dotenv()

def mongo_uzerinden_oneri_ekle(duygu, kategori, mesaj):
    try:
        mongo_uri = os.getenv("MONGO_URI")
        db_name = os.getenv("DB_NAME")
        collection_name = os.getenv("COLLECTION_ADI")

        client = MongoClient(mongo_uri)
        db = client[db_name]
        koleksiyon = db[collection_name]

        belge = {
            "duygu": duygu,
            "kategori": kategori,
            "mesaj": mesaj
        }

        sonuc = koleksiyon.insert_one(belge)
        return True, f"Öneri başarıyla eklendi. ID: {sonuc.inserted_id}"

    except Exception as e:
        return False, f"Hata oluştu: {e}"