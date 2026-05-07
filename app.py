import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.title("Програма за откриване на вредни съставки")

st.write("Качи снимка на етикет от продукт.")

file = st.file_uploader("Избери снимка", type=["jpg", "png", "jpeg"])

harmful = ["E621", "E102", "E110", "E250", "E110", "E122", "E124", "E951", "E954", "E621", "E150d", "E211",
           "sodium benzoate", "potassium sorbate", "aspartame", "caramel color", "E955", "sucralose", "E950",
           "acesulfame", "E220", "E228", "Мононатриев глутамат", "Тартразин", "Сънсет жълто FCF", "Натриев нитрит",
           "Кармоизин", "Понсо 4R", "Аспартам", "Захарин", "Амониево-сулфитен карамел", "Натриев бензоат", "Калиев сорбат", "Сукралоза", "Ацесулфам К", "Серен диоксид", "Калиев бисулфит",
          
          
          ]

if file is not None:
    image = Image.open(file)
    st.image(image, caption="Твоята снимка")

    st.write("Чета текста от снимката...")

    reader = easyocr.Reader(['en', 'bg'])
    img = np.array(image)
    result = reader.readtext(img)

    text = ""
    for r in result:
        text += r[1] + " "

    st.subheader("Намерен текст:")
    st.write(text)

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
