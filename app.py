import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
import pandas as pd
from PIL import Image
import numpy as np

st.set_page_config(
    page_title="Vad?",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded")

### INDATA

df = pd.read_csv('data.csv')

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
        with st.form(key="opacity_form"):
            header = "Hur högt uppskattar du priset?"
            opacity = st.slider(header, 1, 5, 3)
            submitted_opacity = st.form_submit_button("Spara")

            if submitted_opacity:
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
            Detta verktyg har utvecklats av Urbanworks för att stödja SKBs styrelse i att visualisera prioriteringar vid skapandet av en god boendemiljö. Ordens storlek i ordmolnet återspeglar hur högt varje faktor är prioriterad. Färgerna visar den relativa kostnaden för respektive faktor. Den genererade bilden är en visuell representation av förhållandet mellan olika prioriteringar och kostnader, och ska ses som ett stöd för förståelse och dialog, inte som en exakt avbildning av verkliga värden.''')

    st.write("")  
    st.write("")  

    # Setup logo
    image = Image.open('Urban Works_logga_svart_300 dpi.png')
    st.image(image, width=200)

    image1 = Image.open('SKB - logga.png')
    st.image(image1, width=200)

        # Define your levels and colors
    colors = {
        'Lågt': '#BED9E7',
        'Rimligt': '#BED9E7',
        'Dyrt': '#69A5C0',
        'Väldigt dyrt': '#69A5C0',
        'Prisdrivande': '#004D73'
    }

    # Create font properties
    label_font = FontProperties(family='sans-serif', size=12, weight='normal')
    title_font = FontProperties(family='sans-serif', size=14, weight='bold')

    # Create a list of legend patches
    legend_patches = [
        mpatches.Patch(color=color, label=level)
        for level, color in colors.items()
    ]

    # Create a figure and add the legend
    fig, ax = plt.subplots()
    ax.axis('off')  # Hide axes

    # Add the legend in the center of the figure
    legend = ax.legend(
        handles=legend_patches,
        loc='lower left',
        frameon=False,
        title='Teckenförklaring - Pris',
        prop=label_font,
        title_fontproperties=title_font
    )

    
    # Change text color of labels
    for text in legend.get_texts():
        text.set_color('#7d7d7d')

    # Change title color
    legend.get_title().set_color('#7d7d7d')

    # Display in Streamlit
    st.pyplot(fig)


st.sidebar.header("Hur viktiga är dessa faktorer för en bra produkt?")
for word in sorted(st.session_state.word_data.keys()):
    st.session_state.word_data[word] = st.sidebar.slider(
        label=word,
        min_value=1,
        max_value=5,
        value=st.session_state.word_data[word],
        key=f"weight_slider_{word}"
    )

    

### VISUALISERA ORDMOLNET
# --- Display Word Cloud ---

def color_func(word, font_size, position, orientation, font_path, random_state=None):
    opacity = st.session_state.opacity_map.get(word, 3)

    color_map = {
        1: '#009f7f',
        2: '#f26532',
        3: '#f26532',
        4: '#d1123e',
        5: '#d1123e'
    }

    return color_map.get(opacity, '#D9D9D6')


with col[0]:

    st.markdown('# Övning 1: VAD')

    if st.session_state.word_data:
        frequencies = st.session_state.word_data

        mask = np.array(Image.open('mask.png'))

        wc = WordCloud(
            scale=2,
            mask=mask,
            font_path='GalanoGrotesqueAltRegular.otf',  # Replace with your font path if needed
            width=1280,
            height=720,
            background_color="white",
            prefer_horizontal=1.0,
        ).generate_from_frequencies(frequencies)

        wc = wc.recolor(color_func=color_func)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)





    





