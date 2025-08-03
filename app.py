import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates

# Dizionario HEX -> nome colore italiano
colori_hex = {
    "#ff0000": "Rosso",
    "#c80000": "Rosso scuro",
    "#ffc0cb": "Rosa",
    "#ff69b4": "Fucsia",
    "#ffa500": "Arancione",
    "#ff8c00": "Arancione scuro",
    "#ffff00": "Giallo",
    "#eee8aa": "Giallo paglierino",
    "#00ff00": "Verde",
    "#008000": "Verde scuro",
    "#228b22": "Verde foresta",
    "#00ffff": "Ciano",
    "#00bfff": "Azzurro",
    "#87cefa": "Azzurro chiaro",
    "#0000ff": "Blu",
    "#00008b": "Blu scuro",
    "#8a2be2": "Blu viola",
    "#800080": "Viola",
    "#9370db": "Viola chiaro",
    "#4b0082": "Indaco",
    "#000000": "Nero",
    "#808080": "Grigio",
    "#d3d3d3": "Grigio chiaro",
    "#ffffff": "Bianco",
    "#8b4513": "Marrone",
    "#a0522d": "Marrone chiaro",
    "#ff00ff": "Magenta",
    "#c71585": "Magenta scuro",
    "#fffaf0": "Avorio"
}

def nome_colore_da_hex(hex_value):
    nome = colori_hex.get(hex_value.lower())
    if nome:
        return nome
    # Fallback: distanza RGB per trovare colore simile
    rgb = tuple(int(hex_value[i:i+2], 16) for i in (1,3,5))
    def dist(c_hex):
        c_rgb = tuple(int(c_hex[i:i+2], 16) for i in (1,3,5))
        return sum((a-b)**2 for a,b in zip(rgb, c_rgb))
    vicino = min(colori_hex.keys(), key=dist)
    return colori_hex[vicino] + " (approssimato)"

# Configurazione pagina
st.set_page_config(page_title="Rilevamento Colore Preciso", layout="centered")
st.title("🎯 Colore Preciso con HEX (al pixel originale)")

uploaded = st.file_uploader("Carica un'immagine (png/jpg)", type=["png","jpg","jpeg"])
if uploaded:
    orig = Image.open(uploaded).convert("RGB")
    w,h = orig.size

    zoom = st.slider("🔍 Zoom (1–10×)", 1, 10, 3)
    img_zoom = orig.resize((w*zoom, h*zoom), resample=Image.NEAREST)

    coords = streamlit_image_coordinates(img_zoom)

    if coords:
        x_z, y_z = coords["x"], coords["y"]
        x_o, y_o = x_z // zoom, y_z // zoom
        rgb = orig.getpixel((x_o, y_o))
        hexc = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        nome = nome_colore_da_hex(hexc)

        # Disegna il cerchio nel punto cliccato
        img_c = img_zoom.copy()
        draw = ImageDraw.Draw(img_c)
        r = 10
        draw.ellipse((x_z-r, y_z-r, x_z+r, y_z+r), outline="red", width=3)

        st.image(img_c, caption="📍 Punto cliccato (immagine zoomata)", use_column_width=True)
        st.markdown("### 🎨 Risultato Preciso")
        st.markdown(f"- **Nome**: {nome}")
        st.markdown(f"- **RGB**: {rgb}")
        st.markdown(f"- **HEX**: `{hexc}`")
        st.color_picker("Anteprima colore", hexc, disabled=True)
    else:
        st.image(img_zoom, caption="Clicca su un punto per rilevare il colore", use_column_width=True)
else:
    st.info("⬆️ Carica un’immagine per iniziare.")
