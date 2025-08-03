import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates

# Dizionario HEX -> Nome del colore in italiano
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
    # Match esatto
    nome = colori_hex.get(hex_value.lower())
    if nome:
        return nome

    # Fallback: colore più vicino
    rgb = tuple(int(hex_value[i:i+2], 16) for i in (1, 3, 5))
    def distanza(c_hex):
        c_rgb = tuple(int(c_hex[i:i+2], 16) for i in (1, 3, 5))
        return sum((a - b) ** 2 for a, b in zip(rgb, c_rgb))
    più_vicino = min(colori_hex.keys(), key=distanza)
    return colori_hex[più_vicino] + " (approssimato)"

# Impostazioni pagina
st.set_page_config(page_title="Rilevatore di Colore con HEX", layout="centered")
st.title("🎯 Rilevatore di Colore Preciso con HEX")

# Upload immagine
uploaded_file = st.file_uploader("Carica un'immagine", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image_originale = Image.open(uploaded_file).convert("RGB")

    # Zoom regolabile
    zoom = st.slider("🔍 Zoom", 1, 10, 3)
    width, height = image_originale.size
    image_zoom = image_originale.resize((width * zoom, height * zoom), resample=Image.NEAREST)

    # Interazione clic
    coords = streamlit_image_coordinates(image_zoom)

    if coords:
        x_zoom, y_zoom = coords["x"], coords["y"]
        x_orig, y_orig = x_zoom // zoom, y_zoom // zoom

        rgb = image_originale.getpixel((x_orig, y_orig))
        hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        nome = nome_colore_da_hex(hex_color)

        # Aggiungi cerchio rosso sul punto cliccato
        img_con_cerchio = image_zoom.copy()
        draw = ImageDraw.Draw(img_con_cerchio)
        raggio = 10
        draw.ellipse((x_zoom - raggio, y_zoom - raggio, x_zoom + raggio, y_zoom + raggio), outline="red", width=3)

        # Mostra immagine e info
        st.image(img_con_cerchio, caption="📍 Punto cliccato", use_column_width=True)

        st.markdown("### Risultato preciso:")
        st.markdown(f"- **Nome**: {nome}")
        st.markdown(f"- **RGB**: {rgb}")
        st.markdown(f"- **HEX**: `{hex_color}`")
        st.color_picker("Anteprima", hex_color, disabled=True)
    else:
        st.image(image_zoom, caption="Clicca sull'immagine per identificare un colore", use_column_width=True)

else:
    st.info("⬆️ Carica un’immagine per iniziare.")
