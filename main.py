import streamlit as st
import base64

# Configuración de página (para la pestaña del navegador)
st.set_page_config(page_title="Pantry Food - Nutrición", page_icon="🥗", layout="centered")

# --- FUNCIÓN MÁGICA PARA EL LOGO ---
# Esta función convierte la imagen que me pasaste en código para que la app la entienda.
def render_logo(image_path, width=250):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin-bottom: 30px;">
                <img src="data:image/png;base64,{encoded_image}" width="{width}" alt="Pantry Food Logo">
            </div>
            """,
            unsafe_allow_stdio_markdown=True,
        )
    except FileNotFoundError:
        st.error(f"Error: No se encontró el archivo '{image_path}'.")

# --- 2. BASE DE DATOS DE PLATOS ---
menu_pantry = [
    {"nombre": "Bowl de Calentado Pantry", "tipo": "completo", "p": 39.6, "c": 6.7, "g": 11.1},
    {"nombre": "Pechuga en Salsa de Champiñones", "tipo": "proteina", "p": 39.6, "c": 6.7, "g": 11.1},
    {"nombre": "Pierna Pernil Salsa Criolla", "tipo": "proteina", "p": 71.0, "c": 8.0, "g": 25.0},
    {"nombre": "Patty de Hamburguesa Res BBQ", "tipo": "proteina", "p": 25.0, "c": 16.0, "g": 28.0},
    {"nombre": "Bowl de Pasta con Pollo Napolitana", "tipo": "completo", "p": 36.0, "c": 68.0, "g": 11.0},
    {"nombre": "Habichuelas Mantequilla (Acomp.)", "tipo": "acompañamiento", "p": 3.0, "c": 9.0, "g": 4.5},
    {"nombre": "Arroz con Ajonjolí (Acomp.)", "tipo": "acompañamiento", "p": 6.0, "c": 42.0, "g": 6.3}
]

# --- 3. DISEÑO DE LA INTERFAZ ---

# Muestra tu logo centrado (usamos el archivo 'image_6.png' que me pasaste)
# Asegúrate de subir 'image_6.png' a la misma carpeta en GitHub que 'main.py'
render_logo("LOGO_ESLOGAN_Mesa de trabajo 1 copia.png", width=300)

st.title("Asistente Nutricional Inteligente")
st.write("Configura tus metas de macros y armamos tu menú semanal con nuestros productos.")
st.markdown("---")

# Casillas de entrada (UI con iconos y valores por defecto)
st.subheader("Configura tus Macros para hoy:")
col1, col2, col3 = st.columns(3)
with col1:
    meta_p = st.number_input("🍖 Proteína (P) deseada", min_value=0, value=80, help="Gramos totales para el día.")
with col2:
    meta_c = st.number_input("🍚 Carbs (C) deseados", min_value=0, value=120, help="Gramos totales para el día.")
with col3:
    meta_g = st.number_input("🥑 Grasas (G) deseadas", min_value=0, value=45, help="Gramos totales para el día.")

st.markdown("---")

# Estilo para el botón (Verde marca)
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #2e7d32;
    color:white;
    font-weight: bold;
    width: 100%;
    border-radius: 10px;
    height: 50px;
}
</style>""", unsafe_allow_html=True)

if st.button("Buscar mi Menú Perfecto"):
    opciones = []
    
    # Lógica de búsqueda (Combos y Platos Únicos)
    proteinas = [i for i in menu_pantry if i["tipo"] == "proteina"]
    acomp = [i for i in menu_pantry if i["tipo"] == "acompañamiento"]
    completos = [i for i in menu_pantry if i["tipo"] == "completo"]

    # Evaluar Platos Completos (Bowls)
    for plato in completos:
        error = abs(plato["p"]-meta_p) + abs(plato["c"]-meta_c)
        opciones.append({"nombre": f"🍲 {plato['nombre']} (Plato Único)", "error": error, "data": plato})

    # Evaluar Combinaciones (Proteína + Acompañamiento)
    for p in proteinas:
        for a in acomp:
            p_t, c_t, g_t = p["p"]+a["p"], p["c"]+a["c"], p["g"]+a["g"]
            error = abs(p_t-meta_p) + abs(c_t-meta_c)
            opciones.append({
                "nombre": f"🍗 {p['nombre']} + 🍚 {a['nombre']}",
                "error": error, 
                "data": {"p": p_t, "c": c_t, "g": g_t}
            })

    opciones.sort(key=lambda x: x["error"])
    
    if opciones:
        st.subheader("Tus 2 mejores opciones:")
        for i in range(min(2, len(opciones))):
            res = opciones[i]
            with st.expander(f"Opción {i+1}: {res['nombre']}", expanded=(i==0)):
                st.write(f"**Macros Resultantes:**")
                st.write(f"🥩 P: {res['data']['p']}g  |  🍚 C: {res['data']['c']}g  |  🥑 G: {res['data']['g']}g")
                st.info("Esta combinación es la que más se acerca a tus objetivos diarios.")
    else:
        st.warning("No encontramos platos que se ajusten a esos macros. Prueba a cambiar tus metas.")
