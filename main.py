import streamlit as st

# 1. Configuración de la Base de Datos
menu_pantry = [
    {"nombre": "Lasaña de Carne", "tipo": "completo", "p": 27.6, "c": 44.8, "g": 19.3},
    {"nombre": "Pechuga en Champiñones", "tipo": "proteina", "p": 31.9, "c": 11.1, "g": 13.2},
    {"nombre": "Cazuela de Frijoles", "tipo": "completo", "p": 18.2, "c": 54.3, "g": 16.5},
    {"nombre": "Carne Desmechada", "tipo": "proteina", "p": 26.6, "c": 23.9, "g": 11.9},
    {"nombre": "Pollo en Mostaza", "tipo": "proteina", "p": 31.9, "c": 11.1, "g": 13.2},
    {"nombre": "Arroz Integral (Acomp.)", "tipo": "acompañamiento", "p": 3.5, "c": 35.0, "g": 1.5},
    {"nombre": "Ensalada del Día (Acomp.)", "tipo": "acompañamiento", "p": 2.0, "c": 4.0, "g": 7.0}
]

# 2. Interfaz Visual
st.title("🥗 Pantry Food: Asistente Nutricional")
st.write("Ingresa tus objetivos de hoy para recomendarte el menú perfecto.")

# Casillas para los Macros
col1, col2, col3 = st.columns(3)
with col1:
    meta_g = st.number_input("Grasas (g)", min_value=0, value=20)
with col2:
    meta_c = st.number_input("Carbs (g)", min_value=0, value=50)
with col3:
    meta_p = st.number_input("Proteína (g)", min_value=0, value=30)

if st.button("Buscar mi Menú"):
    opciones = []

    # Lógica de búsqueda (Combos y Platos Únicos)
    proteinas = [i for i in menu_pantry if i["tipo"] == "proteina"]
    acomp = [i for i in menu_pantry if i["tipo"] == "acompañamiento"]
    completos = [i for i in menu_pantry if i["tipo"] == "completo"]

    # Evaluar Platos Completos
    for plato in completos:
        error = abs(plato["p"]-meta_p) + abs(plato["c"]-meta_c) + abs(plato["g"]-meta_g)
        opciones.append({"nombre": f"🌟 {plato['nombre']} (Bowl Completo)", "error": error, "data": plato})

    # Evaluar Combinaciones (Proteína + Acompañamiento)
    for p in proteinas:
        for a in acomp:
            p_t, c_t, g_t = p["p"]+a["p"], p["c"]+a["c"], p["g"]+a["g"]
            error = abs(p_t-meta_p) + abs(c_t-meta_c) + abs(g_t-meta_g)
            opciones.append({
                "nombre": f"🍗 {p['nombre']} + 🍚 {a['nombre']}",
                "error": error, 
                "data": {"p": p_t, "c": c_t, "g": g_t}
            })

    # Mostrar resultados
    opciones.sort(key=lambda x: x["error"])
    st.subheader("Tus mejores opciones:")
    
    for i in range(min(2, len(opciones))):
        res = opciones[i]
        with st.expander(f"Opción {i+1}: {res['nombre']}"):
            st.write(f"**Proteína:** {res['data']['p']}g | **Carbs:** {res['data']['c']}g | **Grasas:** {res['data']['g']}g")
            st.success("¡Esta opción se ajusta a tu meta!")
