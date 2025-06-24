import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import numpy as np

st.set_page_config(
    page_title="Vad?",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded")

### INDATA

df = pd.read_excel('data.xlsx', sheet_name='Blad1')

worddict = dict(zip(df['word'], df['weight']))
colordict = dict(zip(df['word'], df['color']))


# Session state initialization
if "word_data" not in st.session_state:
    st.session_state.word_data = worddict  # word -> weight (1–3)
if "opacity_map" not in st.session_state:
    st.session_state.opacity_map = colordict  # word -> opacity (1–3)


col = st.columns((4, 2), gap='medium')

with col[1]:

    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')

    ### LÄGG TILL ORD
    with st.form(key="word_form"):
        word = st.text_input("Lägg till en ny faktor:")
        submitted = st.form_submit_button("Lägg till")

        if submitted and word:
            cleaned = word.strip()

            # Ask for opacity if not already known
            if cleaned not in st.session_state.opacity_map:
                st.session_state.new_word = cleaned
                st.session_state.awaiting_opacity = True
                st.rerun()
            else:
                # If word is new, assign default weight
                if cleaned not in st.session_state.word_data:
                    st.session_state.word_data[cleaned] = 1



    if st.session_state.get("awaiting_opacity", False):
        st.subheader(f"Hur högt uppskattar du priset?")
        opacity = st.slider("(1 = lågt, 3=högt, 5 = Väldigt högt)", 1, 5, 3)
        if st.button("Submit Opacity"):
            st.session_state.opacity_map[st.session_state.new_word] = opacity

            # If new word, assign default weight
            if st.session_state.new_word not in st.session_state.word_data:
                st.session_state.word_data[st.session_state.new_word] = 1

            # Clear temp state
            del st.session_state["awaiting_opacity"]
            del st.session_state["new_word"]
            st.rerun()

    # Beskrivning
    with st.expander('Beskrivning', expanded=False):
        st.write('''
            Detta verktyg är utvecklat av Urbanworks i syfte att understödja SKBs styrelse till ett evidenbaserat förhållningssätt i framtagandet av en ny markstrategi. Datan som ligger till grund för kartan du ser är hämtad från
                 Traveltime, kommunernas markpolicys, SCB, Svensk Mäklarstatistik, Boverket och SKB. Vi på Urbanworks har utifrån detta dataunderlag poängsatt kommunerna i varje kategori. Verktyget kan användas för att visa hur olika 
                 prioriteringar kan leda till att olika kommuner blir attraktiva för SKB att investera i.''')

    st.write("")  
    st.write("")  


    # Setup logo
    image = Image.open('Urban Works_logga_svart_300 dpi.png')
    st.image(image, width=200)

    image1 = Image.open('SKB - logga.png')
    st.image(image1, width=200)

st.sidebar.header("Hur viktig är dessa faktorer för en bra produkt?")
for word in sorted(st.session_state.word_data.keys()):
    st.session_state.word_data[word] = st.sidebar.slider(
        label=word,
        min_value=1,
        max_value=5,
        value=st.session_state.word_data[word],
        key=f"weight_slider_{word}"
    )

with col[0]:

    st.markdown('# Övning 1: VAD')

    ### TÖM ORDMOLNET
    # --- Reset ---
    if st.button("Börja om med en ny wordcloud"):
        st.session_state.word_data = worddict
        st.session_state.opacity_map = colordict


    ### VISUALISERA ORDMOLNET
    # --- Display Word Cloud ---
    if st.session_state.word_data:

        # Frequencies - Definiera frequencies utifrån word_data
        frequencies = {
        word: weight
        for word, weight in st.session_state.word_data.items()
        }

    if st.session_state.word_data:
        frequencies = st.session_state.word_data

        def color_func(word, font_size, position, orientation, font_path, random_state=None):
            opacity = st.session_state.opacity_map.get(word, 3)

            color_map = {
                1: '#D9D9D6',
                2: '#E3ECF0',
                3: '#BED9E7',
                4: '#69A5C0',
                5: '#004D73'
            }

            return color_map.get(opacity, '#D9D9D6')
        

        mask = np.array(Image.open('mask.png'))
        wc = WordCloud(
            scale=2,
            mask=mask,
            font_path='GalanoGrotesqueAltRegular.otf',  # Replace with your font path if needed
            width=1280,
            height=720,
            background_color="white",
            prefer_horizontal=0.5,
        ).generate_from_frequencies(frequencies)

        wc = wc.recolor(color_func=color_func)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)



        

        

    #st.json(frequencies, expanded=True)
    

