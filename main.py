import streamlit as st
import base64

# 1. Configuración de la página
st.set_page_config(page_title="Pantry Food - Menú Semanal", page_icon="🥗", layout="centered")

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
        st.error(f"⚠️ No se encuentra el archivo: {image_path}. Asegúrate de que el nombre coincida exactamente en GitHub.")

# --- 2. BASE DE DATOS EXCLUSIVA (ESTA SEMANA) ---
# Hemos eliminado todos los platos de semanas anteriores.
menu_pantry = [
    # PROTEÍNAS
    {"nombre": "Pollo en Salsa Verde de Espinaca", "tipo": "proteina", "p": 33.0, "c": 8.0, "g": 15.0},
    {"nombre": "Tilapia Mantequilla", "tipo": "proteina", "p": 34.0, "c": 2.0, "g": 25.0},
    {"nombre": "Pollo Miel Mostaza", "tipo": "proteina", "p": 30.0, "c": 18.0, "g": 14.0},
    {"nombre": "Pulled Pork", "tipo": "proteina", "p": 39.0, "c": 0.0, "g": 27.0},
    
    # ACOMPAÑAMIENTOS
    {"nombre": "Coliflor Cremoso", "tipo": "acompañamiento", "p": 6.5, "c": 10.0, "g": 10.6},
    {"nombre": "Arroz con Zanahoria", "tipo": "acompañamiento", "p": 4.2, "c": 41.0, "g": 3.2},
    {"nombre": "Puré de Papa Criolla", "tipo": "acompañamiento", "p": 5.53, "c": 31.75, "g": 8.53},
    {"nombre": "Habichuelas Mantequilla", "tipo": "acompañamiento", "p": 3.0, "c": 9.0, "g": 4.5},
    
    # PLATOS ÚNICOS
    {"nombre": "Pasta Boloñesa (Plato Único)", "tipo": "completo", "p": 46.0, "c": 66.0, "g": 30.0}
]

# --- 3. MOSTRAR LOGO ---
# Usamos el nombre exacto de tu archivo de imagen
render_logo("Rename LOGO_ESLOGAN_Mesa de trabajo 1 copia.png to image_6")

st.markdown("<h1 style='text-align: center;'>Asistente Nutricional</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Selecciona tus metas y te armamos el menú ideal con los platos disponibles esta semana.</p>", unsafe_allow_html=True)

# --- 4. ENTRADA DE USUARIO ---
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    meta_p = st.number_input("Proteína (g)", min_value=0, value=40)
with col2:
    meta_c = st.number_input("Carbs (g)", min_value=0, value=50)
with col3:
    meta_g = st.number_input("Grasas (g)", min_value=0, value=25)

# Estilo del botón verde
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #2e7d32;
    color: white;
    width: 100%;
    border-radius: 8px;
    font-weight: bold;
    height: 3em;
}
</style>""", unsafe_allow_html=True)

if st.button("CALCULAR MI MENÚ"):
    opciones = []
    
    proteinas = [i for i in menu_pantry if i["tipo"] == "proteina"]
    acomp = [i for i in menu_pantry if i["tipo"] == "acompañamiento"]
    completos = [i for i in menu_pantry if i["tipo"] == "completo"]

    # Evaluar Platos Únicos
    for plato in completos:
        # Error calculado basado en cercanía a proteína y carbohidratos
        error = abs(plato["p"]-meta_p) + abs(plato["c"]-meta_c)
        opciones.append({"nombre": f"🍲 {plato['nombre']}", "error": error, "data": plato})

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

    # Ordenar por el que mejor se ajuste
    opciones.sort(key=lambda x: x["error"])
    
    st.subheader("Tus opciones recomendadas:")
    if opciones:
        for i in range(min(2, len(opciones))):
            res = opciones[i]
            with st.expander(f"Opción {i+1}: {res['nombre']}", expanded=(i==0)):
                st.write(f"**Aporte por porción:**")
                st.write(f"🥩 P: {res['data']['p']}g  |  🍚 C: {res['data']['c']}g  |  🥑 G: {res['data']['g']}g")
                st.success("¡Disfruta tu comida Pantry Food!")
    else:
        st.warning("No hay combinaciones que se acerquen a esos valores.")
