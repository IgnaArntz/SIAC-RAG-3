import streamlit as st

from app.monitoring.metrics import get_metrics

st.set_page_config(
    page_title="SIAC Dashboard",
    layout="wide"
)

st.title("📊 Dashboard de Observabilidad SIAC")

metrics = get_metrics()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Consultas",
    metrics["total_requests"]
)

col2.metric(
    "Exitosas",
    metrics["successful_requests"]
)

col3.metric(
    "Errores",
    metrics["errors"]
)

col4.metric(
    "Latencia Promedio",
    f"{metrics['average_latency']} s"
)

st.json(metrics)