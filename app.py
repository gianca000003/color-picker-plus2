import streamlit as st
from PIL import Image
import pyperclip
from streamlit_image_coordinates import streamlit_image_coordinates

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

st.set_page_config(page_title="Color Picker Web", layout="centered")
st.title("🎨 Color Picker Web")

uploaded = st.file_uploader("Carica un'immagine", type=["png", "jpg", "jpeg"])
if uploaded:
    image = Image.open(uploaded).convert("RGB")
    
    coords = streamlit_image_coordinates(image)
    st.image(image, caption="Clicca sull’immagine per ottenere il colore", use_column_width=True)

    if coords:
        x, y = coords["x"], coords["y"]
        rgb = image.getpixel((x, y))
        hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        nome = nome_colore(rgb)

        st.markdown("### 🎯 Risultato")
        st.markdown(f"- **Colore**: {nome}")
        st.markdown(f"- **RGB**: {rgb}")
        st.markdown(f"- **HEX**: `{hex_color}`")
        st.color_picker("Anteprima", hex_color, disabled=True)

        pyperclip.copy(hex_color)
        st.success("HEX copiato automaticamente negli appunti!")
else:
    st.info("⬆️ Carica un’immagine per iniziare.")
