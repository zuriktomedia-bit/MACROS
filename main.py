import streamlit as st
import base64

# 1. Configuración de la página
st.set_page_config(page_title="Pantry Food - Menú Actual", page_icon="🥗", layout="centered")

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
        st.error(f"⚠️ No se encuentra el logo: {image_path}")

# --- 2. BASE DE DATOS EXCLUSIVA (MENÚ NUEVO) ---
menu_pantry = [
    # PROTEÍNAS
    {"nombre": "Pierna Pernil Miel Mostaza", "tipo": "proteina", "p": 50.0, "c": 20.0, "g": 32.0},
    {"nombre": "Pechuga Curry Verde", "tipo": "proteina", "p": 28.0, "c": 6.0, "g": 16.0},
    {"nombre": "Pulled Pork", "tipo": "proteina", "p": 39.0, "c": 0.0, "g": 27.0},
    
    # ACOMPAÑAMIENTOS
    {"nombre": "Garbanzos Criollos", "tipo": "acompañamiento", "p": 11.0, "c": 38.0, "g": 7.0},
    {"nombre": "Brócoli Mantequilla", "tipo": "acompañamiento", "p": 3.9, "c": 9.5, "g": 12.7},
    {"nombre": "Spaguetti al Burro", "tipo": "acompañamiento", "p": 11.0, "c": 60.0, "g": 13.0},
    
    # PLATOS ÚNICOS (BOWLS)
    {"nombre": "Bowl Arroz Verde", "tipo": "completo", "p": 32.0, "c": 58.0, "g": 16.0}
]

# --- 3. MOSTRAR LOGO ---
render_logo("LOGO_ESLOGAN_Mesa de trabajo 1 copia.png")

st.markdown("<h1 style='text-align: center;'>Asistente Nutricional</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ingresa tus macros y armaremos tu menú con los platos de esta semana.</p>", unsafe_allow_html=True)

# --- 4. ENTRADA DE USUARIO ---
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    meta_p = st.number_input("🍖 Proteína (g)", min_value=0, value=40)
with col2:
    meta_c = st.number_input("🍚 Carbs (g)", min_value=0, value=50)
with col3:
    meta_g = st.number_input("🥑 Grasas (g)", min_value=0, value=25)

# Estilo del botón verde Pantry
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
        # Cálculo de cercanía
        diff = abs(plato["p"]-meta_p) + abs(plato["c"]-meta_c)
        opciones.append({"nombre": f"🍲 {plato['nombre']} (Plato Único)", "error": diff, "data": plato})

    # Evaluar Combinaciones (Proteína + Acompañamiento)
    for p in proteinas:
        for a in acomp:
            p_t = p["p"] + a["p"]
            c_t = p["c"] + a["c"]
            g_t = p["g"] + a["g"]
            diff = abs(p_t-meta_p) + abs(c_t-meta_c)
            opciones.append({
                "nombre": f"🍗 {p['nombre']} + 🍚 {a['nombre']}",
                "error": diff, 
                "data": {"p": p_t, "c": c_t, "g": g_t}
            })

    # Ordenar por el que mejor se ajuste (menor diferencia)
    opciones.sort(key=lambda x: x["error"])
    
    st.subheader("Tus opciones recomendadas:")
    if opciones:
        for i in range(min(2, len(opciones))):
            res = opciones[i]
            with st.expander(f"Opción {i+1}: {res['nombre']}", expanded=(i==0)):
                st.write(f"**Aporte Nutricional Total:**")
                st.write(f"🥩 Proteína: {res['data']['p']}g")
                st.write(f"🍞 Carbohidratos: {res['data']['c']}g")
                st.write(f"🥑 Grasas: {res['data']['g']}g")
                st.success("¡Sabor, calidad y rapidez con Pantry Food!")
    else:
        st.warning("No hay combinaciones cercanas. Intenta ajustar tus metas.")
