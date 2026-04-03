import streamlit as st
import base64

# 1. Configuración de la página
st.set_page_config(page_title="Pantry Food - Nutrición", page_icon="🥗", layout="centered")

# --- FUNCIÓN PARA MOSTRAR EL LOGO ---
def render_logo(image_path, width=300):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{encoded_image}" width="{width}">
            </div>
            """,
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        st.error(f"⚠️ No se encuentra el archivo: {image_path}. Asegúrate de haberlo subido a GitHub.")

# --- 2. BASE DE DATOS ACTUALIZADA ---
menu_pantry = [
    {"nombre": "Bowl de Calentado Pantry", "tipo": "completo", "p": 39.6, "c": 6.7, "g": 11.1},
    {"nombre": "Pechuga en Salsa de Champiñones", "tipo": "proteina", "p": 39.6, "c": 6.7, "g": 11.1},
    {"nombre": "Pierna Pernil Salsa Criolla", "tipo": "proteina", "p": 71.0, "c": 8.0, "g": 25.0},
    {"nombre": "Patty de Hamburguesa Res BBQ", "tipo": "proteina", "p": 25.0, "c": 16.0, "g": 28.0},
    {"nombre": "Bowl de Pasta con Pollo Napolitana", "tipo": "completo", "p": 36.0, "c": 68.0, "g": 11.0},
    {"nombre": "Habichuelas Mantequilla (Acomp.)", "tipo": "acompañamiento", "p": 3.0, "c": 9.0, "g": 4.5},
    {"nombre": "Arroz con Ajonjolí (Acomp.)", "tipo": "acompañamiento", "p": 6.0, "c": 42.0, "g": 6.3}
]

# --- 3. MOSTRAR LOGO ---
# Aquí usamos exactamente el nombre que me pasaste
render_logo("LOGO_ESLOGAN_Mesa de trabajo 1 copia.png")

st.markdown("<h1 style='text-align: center;'>Asistente Nutricional Inteligente</h1>", unsafe_allow_html=True)
st.write("Ingresa tus metas de hoy y te diré qué productos de **Pantry Food** elegir.")

# --- 4. ENTRADA DE USUARIO ---
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    meta_p = st.number_input("🍖 Proteína (g)", min_value=0, value=80)
with col2:
    meta_c = st.number_input("🍚 Carbs (g)", min_value=0, value=120)
with col3:
    meta_g = st.number_input("🥑 Grasas (g)", min_value=0, value=45)

# Estilo del botón verde
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #2e7d32;
    color: white;
    width: 100%;
    border-radius: 8px;
}
</style>""", unsafe_allow_html=True)

if st.button("Calcular mi Menú Ideal"):
    opciones = []
    
    proteinas = [i for i in menu_pantry if i["tipo"] == "proteina"]
    acomp = [i for i in menu_pantry if i["tipo"] == "acompañamiento"]
    completos = [i for i in menu_pantry if i["tipo"] == "completo"]

    for plato in completos:
        error = abs(plato["p"]-meta_p) + abs(plato["c"]-meta_c)
        opciones.append({"nombre": f"🍲 {plato['nombre']} (Plato Único)", "error": error, "data": plato})

    for p in proteinas:
        for a in acomp:
            p_t, c_t, g_t = p["p"]+a["p"], p["c"]+a["c"], p["g"]+a["g"]
            error = abs(p_t-meta_
