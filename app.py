import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates
import numpy as np
from sklearn.cluster import KMeans

# Dizionario esteso di colori con nomi in italiano
colori_nomi = {
    (255, 0, 0): "Rosso",
    (200, 0, 0): "Rosso scuro",
    (255, 69, 0): "Rosso aranciato",
    (255, 99, 71): "Pomodoro",
    (255, 192, 203): "Rosa",
    (255, 182, 193): "Rosa chiaro",
    (255, 105, 180): "Fucsia",
    (255, 165, 0): "Arancione",
    (255, 140, 0): "Arancione scuro",
    (255, 215, 0): "Oro",
    (255, 255, 0): "Giallo",
    (255, 255, 224): "Giallo chiaro",
    (238, 232, 170): "Giallo paglierino",
    (173, 255, 47): "Verde giallastro",
    (0, 255, 0): "Verde",
    (0, 128, 0): "Verde scuro",
    (34, 139, 34): "Verde foresta",
    (46, 139, 87): "Verde mare",
    (0, 255, 255): "Ciano",
    (0, 206, 209): "Ciano scuro",
    (0, 191, 255): "Azzurro",
    (135, 206, 250): "Azzurro chiaro",
    (0, 0, 255): "Blu",
    (0, 0, 139): "Blu scuro",
    (25, 25, 112): "Blu mezzanotte",
    (138, 43, 226): "Blu viola",
    (128, 0, 128): "Viola",
    (147, 112, 219): "Viola chiaro",
    (75, 0, 130): "Indaco",
    (0, 0, 0): "Nero",
    (105, 105, 105): "Grigio scuro",
    (128, 128, 128): "Grigio",
    (169, 169, 169): "Grigio chiaro",
    (211, 211, 211): "Grigio molto chiaro",
    (139, 69, 19): "Marrone",
    (160, 82, 45): "Marrone chiaro",
    (210, 105, 30): "Cioccolato",
    (255, 250, 240): "Avorio",
    (255, 240, 245): "Lavanda chiaro",
    (255, 0, 255): "Magenta",
    (199, 21, 133): "Magenta scuro"
}

def nome_colore(rgb):
    def distanza(c1, c2):
        return sum((a - b) ** 2 for a, b in zip(c1, c2))
    più_vicino = min(colori_nomi.keys(), key=lambda c: distanza(rgb, c))
    return colori_nomi[più_vicino]

def semplifica_immagine(img, n_colori=8):
    img_np = np.array(img)
    h, w, _ = img_np.shape
    img_flat = img_np.reshape((-1, 3))

    kmeans = KMeans(n_clusters=n_colori, n_init='auto', random_state=42)
    kmeans.fit(img_flat)
    colori_trovati = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_

    diz_rgb = np.array(list(colori_nomi.keys()))
    def colore_dizionario_piu_vicino(col):
        dists = np.sum((diz_rgb - col) ** 2, axis=1)
        return diz_rgb[np.argmin(dists)]

    colori_mappati = np.array([colore_dizionario_piu_vicino(c) for c in colori_trovati])
    img_simplified = colori_mappati[labels].reshape((h, w, 3)).astype(np.uint8)
    return Image.fromarray(img_simplified)

# Streamlit App
st.set_page_config(page_title="Color Picker Web", layout="centered")
st.title("🎨 Color Picker Web")

# Session state
if "coords" not in st.session_state:
    st.session_state.coords = None
if "rgb" not in st.session_state:
    st.session_state.rgb = None

uploaded = st.file_uploader("Carica un'immagine", type=["png", "jpg", "jpeg"])
if uploaded:
    image = Image.open(uploaded).convert("RGB")

    coords = streamlit_image_coordinates(image)

    if coords:
        st.session_state.coords = coords
        x, y = coords["x"], coords["y"]
        st.session_state.rgb = image.getpixel((x, y))

    # Disegna il cerchietto rosso se cliccato
    img_to_show = image.copy()
    if st.session_state.coords:
        x, y = st.session_state.coords["x"], st.session_state.coords["y"]
        draw = ImageDraw.Draw(img_to_show)
        raggio = 10
        draw.ellipse((x - raggio, y - raggio, x + raggio, y + raggio), outline="red", width=3)

    st.image(img_to_show, caption="Clicca per ottenere il colore", use_column_width=True)

    if st.session_state.rgb:
        rgb = st.session_state.rgb
        hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        nome = nome_colore(rgb)

        st.markdown("### 🎯 Risultato")
        st.markdown(f"- **Colore**: {nome}")
        st.markdown(f"- **RGB**: {rgb}")
        st.markdown(f"- **HEX**: `{hex_color}`")
        st.color_picker("Anteprima", hex_color, disabled=True)
        st.code(hex_color, language="text")
        st.info("Copia il codice HEX sopra cliccando sull’icona 📋")

    # Slider per personalizzare il numero di colori
    st.markdown("### 🧪 Semplificazione dell'immagine")
    num_colori = st.slider("Numero di colori principali da rilevare", 3, 15, 8)
    simplified = semplifica_immagine(image, n_colori=num_colori)
    st.image(simplified, caption="Immagine con colori ridotti", use_column_width=True)

else:
    st.info("⬆️ Carica un’immagine per iniziare.")
