import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates

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
        
        # Disegna il puntatore rosso sul punto cliccato
        img_con_puntatore = image.copy()
        draw = ImageDraw.Draw(img_con_puntatore)
        raggio = 10
        draw.ellipse((x - raggio, y - raggio, x + raggio, y + raggio), outline="red", width=3)
        
        st.image(img_con_puntatore, caption="Hai cliccato qui", use_column_width=True)

        st.markdown("### 🎯 Risultato")
        st.markdown(f"- **Colore**: {nome}")
        st.markdown(f"- **RGB**: {rgb}")
        st.markdown(f"- **HEX**: `{hex_color}`")
        st.color_picker("Anteprima", hex_color, disabled=True)

        st.code(hex_color, language="text")
        st.info("Copia il codice HEX sopra cliccando sull’icona 📋")

else:
    st.info("⬆️ Carica un’immagine per iniziare.")
