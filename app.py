import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# Заглавие
st.title("Програма за откриване на вредни съставки")

st.write("Качи снимка на етикет от продукт.")

# Качване на снимка
file = st.file_uploader("Избери снимка", type=["jpg", "png", "jpeg"])

# Примерни вредни съставки
harmful = ["E621", "E102", "E110", "E250"]

if file is not None:
    # Показваме снимката
    image = Image.open(file)
    st.image(image, caption="Твоята снимка")

    st.write("Чета текста от снимката...")

    # OCR
    reader = easyocr.Reader(['en', 'bg'])
    img = np.array(image)
    result = reader.readtext(img)

    # Събираме текста
    text = ""
    for r in result:
        text += r[1] + " "

    st.subheader("Намерен текст:")
    st.write(text)

    # Търсим вредни съставки
    found = []

    for item in harmful:
        if item.lower() in text.lower():
            found.append(item)

    st.subheader("Резултат:")

    if len(found) > 0:
        st.write("⚠️ Намерени са вредни съставки:")
        for f in found:
            st.write("- " + f)
    else:
        st.write("✅ Няма намерени вредни съставки.")
