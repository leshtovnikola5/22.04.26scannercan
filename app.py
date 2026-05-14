import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="Е-Скенер за храна")
st.title("🛡️ Детектор на вредни съставки")
st.write("Направете снимка на етикета и аз ще проверя за опасни Е-номера.")

vredni_neshta = [
    "E621", "E102", "E110", "E250", "E110", "E122", "E124", "E951", "E954", "E621", "E150d", "E211",
           "sodium benzoate", "potassium sorbate", "aspartame", "caramel color", "E955", "sucralose", "E950",
           "acesulfame", "E220", "E228", "Мононатриев глутамат", "Тартразин", "Сънсет жълто FCF", "Натриев нитрит",
           "Кармоизин", "Понсо 4R", "Аспартам", "Захарин", "Амониево-сулфитен карамел", "Натриев бензоат", "Калиев сорбат", "Сукралоза", "Ацесулфам К", "Серен диоксид", "Калиев бисулфит",
]

@st.cache_resource
def load_ai():
    return easyocr.Reader(['bg', 'en'], gpu=False)

chitatel = load_ai()

izbor = st.radio("Как ще подадете снимка?", ["Качване от файл", "Снимка с камерата"])

if izbor == "Качване от файл":
    snimka = st.file_uploader("Избери файл", type=["jpg", "png"])
else:
    snimka = st.camera_input("Снимай етикета")

if snimka is not None:
    # Отваряме снимката
    img = Image.open(snimka)
    st.image(img, caption="Вашият етикет", use_container_width=True)
    
    with st.spinner('Чета етикета...'):
        img_array = np.array(img)
        
        rezultat = chitatel.readtext(img_array, detail=0)
        celyat_tekst = " ".join(rezultat).lower()
        
        st.subheader("Текст от етикета:")
        st.write(celyat_tekst)

        namereni = []
        for element in vredni_neshta:
            if element.lower() in celyat_tekst:
                namereni.append(element)

        st.divider()
        if namereni:
            st.error(f"⚠️ ВНИМАНИЕ! Намерени вредни съставки: {', '.join(namereni)}")
        else:
            st.success("✅ Не открих нищо опасно от моя списък!")

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
