import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="Здравен скенер", page_icon="🛡️", layout="centered")

st.title("🛡️ AI Здравен Скенер")
st.write("Сканирай етикет и провери дали продуктът е подходящ за теб.")

harmful_e = ["e621", "e102", "e110", "e250", "e122", "e124", "e951", "e954", "e150d", "e211", "e955", "e950", "e220", "e228"]
diabetes_words = ["sugar", "glucose", "fructose", "glucose-fructose syrup", "dextrose", "maltodextrin", "захар", "глюкозен сироп", "фруктоза"]
high_blood_pressure = ["salt", "sodium", "натрий", "сол", "sodium benzoate"]
allergens = ["milk", "soy", "gluten", "wheat", "peanut", "nuts", "мляко", "соя", "глутен", "фъстъци", "ядки", "яйца"]

@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'], gpu=False)

reader = load_reader()

choice = st.radio(
    "Как искаш да добавиш снимка?",
    ["Качи снимка", "Използвай камера"],
    horizontal=True
)

if choice == "Качи снимка":
    file = st.file_uploader("Избери снимка", type=["jpg", "png", "jpeg"])
else:
    file = st.camera_input("Снимай етикет")

if file is not None:
    image = Image.open(file)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(image, caption="Сканиран етикет", use_container_width=True)

    with st.spinner("🔍 Анализирам етикета..."):
        img = np.array(image)
        result = reader.readtext(img, detail=0)
        text = " ".join(result).lower()
        text_cleaned = text.replace("e ", "e")

    with col2:
        st.subheader("📄 Намерен текст")
        st.text_area("Извлечен текст от OCR:", value=text, height=200, disabled=True)

    found_e = [item.upper() for item in harmful_e if item in text_cleaned]
    found_diabetes = [item for item in diabetes_words if item in text]
    found_pressure = [item for item in high_blood_pressure if item in text]
    found_allergens = [item for item in allergens if item in text]

    st.divider()
    st.subheader("📊 Резултати от анализа")

    score = 0

    if found_e:
        score += len(found_e)
        st.error(f"⚠️ **Вредни добавки:** {', '.join(found_e)}")

    if found_diabetes:
        score += len(found_diabetes)
        st.warning(f"🍬 **Внимание за диабетици:** {', '.join(found_diabetes)}")

    if found_pressure:
        if "sodium benzoate" in found_pressure and "sodium" in found_pressure:
            found_pressure.remove("sodium")
        score += len(found_pressure)
        st.warning(f"❤️ **Високо съдържание на сол/натрий:** {', '.join(found_pressure)}")

    if found_allergens:
        score += len(found_allergens)
        st.warning(f"🤧 **Алергени:** {', '.join(found_allergens)}")

    st.markdown("---")
    st.subheader("⭐ Крайна оценка на продукта")

    if score == 0:
        st.success("✅ **Отличен избор!** Не са открити рискови съставки в нашата база данни.")
    elif score <= 2:
        st.warning("⚠️ **Нисък до среден риск.** Продуктът съдържа някои съставки, които изискват внимание.")
    else:
        st.error("❌ **Висок риск / Нездравословен избор.** Намерени са множество нежелани съставки.")
