import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="Здравен скенер", page_icon="🛡️")

st.title("🛡️ AI Здравен Скенер")
st.write("Сканирай етикет и провери дали продуктът е подходящ за теб.")

harmful_e = [
    "E621", "E102", "E110", "E250",
    "E122", "E124", "E951", "E954",
    "E150d", "E211", "E955", "E950",
    "E220", "E228"
]

diabetes_words = [
    "sugar", "glucose", "fructose",
    "glucose-fructose syrup",
    "dextrose", "maltodextrin",
    "захар", "глюкозен сироп",
    "фруктоза"
]

high_blood_pressure = [
    "salt", "sodium", "натрий",
    "сол", "sodium benzoate"
]

allergens = [
    "milk", "soy", "gluten",
    "wheat", "peanut", "nuts",
    "мляко", "соя", "глутен",
    "фъстъци", "ядки", "яйца"
]

@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'], gpu=False)

reader = load_reader()

choice = st.radio(
    "Как искаш да добавиш снимка?",
    ["Качи снимка", "Използвай камера"]
)

if choice == "Качи снимка":
    file = st.file_uploader(
        "Избери снимка",
        type=["jpg", "png", "jpeg"]
    )
else:
    file = st.camera_input("Снимай етикет")

if file is not None:

    image = Image.open(file)

    st.image(image, caption="Сканиран етикет")

    with st.spinner("🔍 Анализирам етикета..."):

        img = np.array(image)

        result = reader.readtext(img, detail=0)

        text = " ".join(result).lower()

    st.subheader("📄 Намерен текст")
    st.write(text)

    found_e = []
    found_diabetes = []
    found_pressure = []
    found_allergens = []

    for item in harmful_e:
        if item.lower() in text:
            found_e.append(item)

    for item in diabetes_words:
        if item.lower() in text:
            found_diabetes.append(item)

    for item in high_blood_pressure:
        if item.lower() in text:
            found_pressure.append(item)

    for item in allergens:
        if item.lower() in text:
            found_allergens.append(item)

    st.divider()

    score = 0

    if found_e:
        score += len(found_e)

        st.error(
            "⚠️ Вредни добавки: " +
            ", ".join(found_e)
        )

    if found_diabetes:
        score += len(found_diabetes)

        st.warning(
            "🍬 Внимание за диабетици: " +
            ", ".join(found_diabetes)
        )

    if found_pressure:
        score += len(found_pressure)

        st.warning(
            "❤️ Високо съдържание на сол/натрий: " +
            ", ".join(found_pressure)
        )

    if found_allergens:
        score += len(found_allergens)

        st.warning(
            "🤧 Алергени: " +
            ", ".join(found_allergens)
        )

    st.subheader("⭐ Оценка на продукта")

    if score == 0:
        st.success("✅ Изглежда като добър избор.")
    elif score <= 3:
        st.warning("⚠️ Продуктът е със среден риск.")
    else:
        st.error("❌ Продуктът не е особено здравословен.")
