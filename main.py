import streamlit as st

# 1. Base de datos con la información que me pasaste
menu_pantry = [
    {"nombre": "Bowl de Calentado Pantry", "tipo": "completo", "p": 39.6, "c": 6.7, "g": 11.1},
    {"nombre": "Pechuga en Salsa de Champiñones", "tipo": "proteina", "p": 39.6, "c": 6.7, "g": 11.1},
    {"nombre": "Pierna Pernil Salsa Criolla", "tipo": "proteina", "p": 71.0, "c": 8.0, "g": 25.0},
    {"nombre": "Patty de Hamburguesa Res BBQ", "tipo": "proteina", "p": 25.0, "c": 16.0, "g": 28.0},
    {"nombre": "Bowl de Pasta con Pollo Napolitana", "tipo": "completo", "p": 36.0, "c": 68.0, "g": 11.0},
    {"nombre": "Habichuelas Mantequilla", "tipo": "acompañamiento", "p": 3.0, "c": 9.0, "g": 4.5},
    {"nombre": "Arroz con Ajonjolí", "tipo": "acompañamiento", "p": 6.0, "c": 42.0, "g": 6.3}
]

st.set_page_config(page_title="Pantry Food - Nutrición", page_icon="🥗")

st.title("🥗 Pantry Food: Asistente Nutricional")
st.write("Configura tus metas de hoy para armar tu menú semanal.")

# Casillas de entrada para el usuario
col1, col2, col3 = st.columns(3)
with col1:
    meta_p = st.number_input("Proteína (P) deseada", min_value=0, value=40)
with col2:
    meta_c = st.number_input("Carbohidratos (C) deseados", min_value=0, value=50)
with col3:
    meta_g = st.number_input("Grasas (G) deseadas", min_value=0, value=20)

if st.button("Calcular mi Menú Ideal"):
    opciones = []
    
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
    
    st.subheader("Tus 2 mejores opciones para hoy:")
    for i in range(min(2, len(opciones))):
        res = opciones[i]
        with st.expander(f"Opción {i+1}: {res['nombre']}"):
            st.write(f"**Macros Resultantes:**")
            st.write(f"P: {res['data']['p']}g  |  C: {res['data']['c']}g  |  G: {res['data']['g']}g")
            st.info("Esta combinación es la que más se acerca a tus objetivos.")
