from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Model bilgisi
MODEL_ADI = "savasy/bert-base-turkish-sentiment-cased"

# Tokenizer ve model yükleniyor
tokenizer = AutoTokenizer.from_pretrained(MODEL_ADI)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_ADI)

# Etiket sıralaması (modelin sırası bu şekildedir)
etiketler = ["Negatif", "Nötr", "Pozitif"]

def duygu_tahmini(metin: str) -> str:
    """
    Kullanıcının yazdığı metni analiz eder, model tahmini yapar
    ve anahtar kelimelerle gerektiğinde düzeltir.
    """
    if not metin.strip():
        return "Girdi boş!"

    # Metni modele ver
    inputs = tokenizer(metin, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        skorlar = outputs.logits.softmax(dim=1).numpy()[0] #outputs.logits: Modelin ham çıktısı (üç duygu için puanlar) =>softmax: Bu puanları yüzde gibi dağıtır.
    
    # İlk tahmini al
    tahmin = etiketler[skorlar.argmax()] #argmax: En yüksek puanı alan duygunun index’ini bulur.

    # Anahtar kelime düzeltmesi (sadece 'Nötr' durumunda)
    pozitif_kelimeler = [
        "iyi", "çok iyi", "harika", "mükemmel", "süper", "mutluyum", 
        "keyfim yerinde", "enerjik", "şahaneyim", "neşeliyim", "heyecanlıyım"
    ]
    negatif_kelimeler = [
        "kötü", "çok kötü", "berbat", "rezalet", "üzgünüm", "bittim", 
        "çöktüm", "yorgunum", "depresyondayım", "mutsuzum"
    ]

    metin_kucuk = metin.lower()

    # Eğer model 'Nötr' dediyse, ama metin bariz pozitif/negatif kelime içeriyorsa düzelt
    if tahmin == "Nötr":
        if any(kelime in metin_kucuk for kelime in pozitif_kelimeler):
            tahmin = "Pozitif"
        elif any(kelime in metin_kucuk for kelime in negatif_kelimeler):
            tahmin = "Negatif"

    return tahmin  