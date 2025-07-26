import streamlit as st
from PIL import Image

# Dizionario esteso di colori e loro nomi
colori_nomi = {
    (255, 0, 0): "Rosso",
    (200, 0, 0): "Rosso scuro",
    (255, 100, 100): "Rosa acceso",
    (255, 192, 203): "Rosa",
    (255, 165, 0): "Arancione",
    (255, 215, 0): "Oro",
    (255, 255, 0): "Giallo",
    (240, 230, 140): "Kaki chiaro",
    (189, 183, 107): "Kaki",
    (0, 255, 0): "Verde",
    (34, 139, 34): "Verde foresta",
    (0, 128, 0): "Verde scuro",
    (173, 255, 47): "Verde giallastro",
    (0, 255, 255): "Ciano",
    (0, 128, 128): "Verde acqua",
    (0, 0, 255): "Blu",
    (100, 149, 237): "Blu fiordaliso",
    (65, 105, 225): "Blu reale",
    (0, 0, 139): "Blu scuro",
    (138, 43, 226): "Indaco",
    (75, 0, 130): "Indaco scuro",
    (255, 0, 255): "Magenta",
    (128, 0, 128): "Viola",
    (148, 0, 211): "Viola intenso",
    (255, 255, 255): "Bianco",
    (211, 211, 211): "Grigio chiaro",
    (169, 169, 169): "Grigio",
    (128, 128, 128): "Grigio scuro",
    (0, 0, 0): "Nero",
    (139, 69, 19): "Marrone",
    (160, 82, 45): "Marrone rossiccio",
    (245, 222, 179): "Beige",
    (210, 180, 140): "Marrone chiaro"
}

# Trova il nome del colore più simile
def nome_colore(rgb):
    def distanza(c1, c2):
        return sum((a - b) ** 2 for a, b in zip(c1, c2))
    più_vicino = min(colori_nomi.keys(), key=lambda c: distanza(rgb, c))
    return colori_nomi[più_vicino]

st.set_page_config(page_title="Color Picker Web", layout="centered")
st.title("🎨 Color Picker Web")

uploaded_file = st.file_uploader("Carica un'immagine", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Clicca sull'immagine per ottenere il colore", use_column_width=True)

    coords = st.text_input("📍 Inserisci coordinate X,Y (es: 100,150):")
    if coords:
        try:
            x, y = map(int, coords.split(","))
            if 0 <= x < image.width and 0 <= y < image.height:
                rgb = image.getpixel((x, y))
                hex_color = '#%02x%02x%02x' % rgb
                nome = nome_colore(rgb)
                st.markdown("### 🎯 Risultato")
                st.markdown(f"- **Nome colore**: {nome}")
                st.markdown(f"- **RGB**: {rgb}")
                st.markdown(f"- **HEX**: `{hex_color}`")
                st.color_picker("Anteprima", hex_color, disabled=True)
            else:
                st.error(f"Coordinate fuori dall'immagine. Dimensioni: {image.width}x{image.height}")
        except:
            st.error("⚠️ Inserisci coordinate valide nel formato X,Y (es: 50,80)")
else:
    st.info("⬆️ Carica un'immagine per iniziare.")
