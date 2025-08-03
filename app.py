import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates
import numpy as np

# Dizionario esteso di colori con nomi in italiano
colori_nomi = {
    (255, 0, 0): "Rosso",
    (200, 0, 0): "Rosso scuro",
    (255, 192, 203): "Rosa",
    (255, 165, 0): "Arancione",
    (255, 255, 0): "Giallo",
    (0, 255, 0): "Verde",
    (0, 0, 255): "Blu",
    (128, 0, 128): "Viola",
    (0, 0, 0): "Nero",
    (255, 255, 255): "Bianco",
    (128, 128, 128): "Grigio",
    (139, 69, 19): "Marrone",
    (0, 255, 255): "Ciano",
    (255, 0, 255): "Magenta"
}

def nome_colore(rgb):
    def distanza(c1, c2):
        return sum((a - b) ** 2 for a, b in zip(c1, c2))
    più_vicino = min(colori_nomi.keys(), key=lambda c: distanza(rgb, c))
    return colori_nomi[più_vicino]

# Configurazione app
st.set_page_config(page_title="Rilevatore di Colore", layout="centered")
st.title("🎨 Rilevatore di Colore")

# Caricamento immagine
uploaded_file = st.file_uploader("Carica un'immagine (JPG o PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image_originale = Image.open(uploaded_file).convert("RGB")

    # Zoom selezionabile
    zoom = st.slider("🔍 Zoom immagine", 1, 5, 1)
    larghezza, altezza = image_originale.size
    nuova_dimensione = (larghezza * zoom, altezza * zoom)
    image_zoom = image_originale.resize(nuova_dimensione, resample=Image.NEAREST)

    # Coordinate del click
    coords = streamlit_image_coordinates(image_zoom)

    # Disegna cerchio sul punto cliccato (se presente)
    if coords:
        x_click, y_click = coords["x"], coords["y"]
        rgb = image_zoom.getpixel((x_click, y_click))
        nome = nome_colore(rgb)
        hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

        img_con_cerchio = image_zoom.copy()
        draw = ImageDraw.Draw(img_con_cerchio)
        raggio = 10
        draw.ellipse((x_click - raggio, y_click - raggio, x_click + raggio, y_click + raggio), outline="red", width=3)

        st.image(img_con_cerchio, caption="📍 Punto cliccato", use_column_width=True)

        st.markdown("### 🧾 Risultato del colore")
        st.markdown(f"- **Colore**: {nome}")
        st.markdown(f"- **RGB**: {rgb}")
        st.markdown(f"- **HEX**: `{hex_color}`")
        st.color_picker("Anteprima colore", hex_color, disabled=True)
    else:
        st.image(image_zoom, caption="Clicca per rilevare un colore", use_column_width=True)

else:
    st.info("⬆️ Carica un’immagine per iniziare.")
