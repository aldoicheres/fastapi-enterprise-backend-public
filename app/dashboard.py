import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="Business Intelligence Dashboard", page_icon="📊", layout="wide")

st.title("📊 Panel de Control y KPIs Corporativos")
st.markdown("Dashboard interactivo conectado al backend de **FastAPI Enterprise Core**.")

# URL del endpoint analítico de tu API
API_URL = "http://localhost:8000/api/analytics/metrics/summary"

# Botón para actualizar o consultar datos en tiempo real
if st.button("🔄 Actualizar Métricas"):
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            metricas = data.get("metricas", {})

            # Mostrar KPIs en tarjetas visuales (Columns de Streamlit)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(label="Total de Registros", value=metricas.get("total_registros", 0))
            with col2:
                st.metric(label="Edad Promedio de Usuarios", value=f"{metricas.get('edad_promedio_usuarios', 0)} años")
            with col3:
                st.metric(label="Estado del Sistema", value="Operativo")

            st.success("Datos obtenidos y sincronizados exitosamente con la API.")
        else:
            st.error("Error al conectar con los endpoints analíticos de la API.")
    except Exception as e:
        st.error(f"No se pudo establecer conexión con el servidor FastAPI: {e}")

st.markdown("---")
st.caption("Desarrollado como módulo complementario de Business Intelligence para Portfolio Profesional.")