"""Streamlit dashboard for multimodal health monitoring."""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def main():
    """Main Streamlit dashboard application."""
    try:
        import streamlit as st
    except ImportError:
        print("Streamlit not installed. Run: pip install streamlit")
        return

    st.set_page_config(
        page_title="Saúde da Mulher - Monitoramento Multimodal",
        page_icon="🏥",
        layout="wide",
    )

    st.title("🏥 Sistema Multimodal de IA - Saúde da Mulher")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("📋 Navegação")
        page = st.radio(
            "Selecione a página:",
            ["Visão Geral", "Análise de Vídeo", "Análise de Áudio",
             "Análise de Texto", "Alertas", "Relatórios"]
        )

        st.markdown("---")
        st.header("🔍 Filtros")
        risk_level = st.selectbox(
            "Nível de Risco:",
            ["Todos", "Crítico", "Alto", "Médio", "Baixo"]
        )

        st.markdown("---")
        st.caption("FIAP 8IADT - Tech Challenge Fase 4")

    # Main content
    if page == "Visão Geral":
        _render_overview(st)
    elif page == "Análise de Vídeo":
        _render_video_analysis(st)
    elif page == "Análise de Áudio":
        _render_audio_analysis(st)
    elif page == "Análise de Texto":
        _render_text_analysis(st)
    elif page == "Alertas":
        _render_alerts(st)
    elif page == "Relatórios":
        _render_reports(st)


def _render_overview(st):
    """Render overview dashboard page."""
    import pandas as pd
    import numpy as np

    st.header("📊 Visão Geral do Sistema")

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pacientes Monitoradas", "12", "+3 hoje")
    with col2:
        st.metric("Alertas Ativos", "3", delta="2 críticos", delta_color="inverse")
    with col3:
        st.metric("Vídeos Processados", "47", "+5 hoje")
    with col4:
        st.metric("Consultas Analisadas", "28", "+8 hoje")

    st.markdown("---")

    # Risk distribution chart
    st.subheader("Distribuição de Risco das Pacientes")

    risk_data = pd.DataFrame({
        "Paciente": [f"PAC-{i:03d}" for i in range(1, 13)],
        "Score de Risco": np.random.uniform(10, 95, 12),
        "Status": np.random.choice(["Normal", "Observação", "Alerta", "Crítico"], 12,
                                    p=[0.3, 0.35, 0.25, 0.1]),
    })

    st.bar_chart(risk_data.set_index("Paciente")["Score de Risco"])

    # Recent alerts table
    st.subheader("🚨 Alertas Recentes")
    alerts_df = pd.DataFrame([
        {"Horário": "08:15", "Paciente": "PAC-003", "Tipo": "Sangramento",
         "Severidade": "Crítico", "Origem": "Vídeo"},
        {"Horário": "08:10", "Paciente": "PAC-007", "Tipo": "Depressão Pós-Parto",
         "Severidade": "Alto", "Origem": "Áudio"},
        {"Horário": "07:55", "Paciente": "PAC-011", "Tipo": "Interação Medicamentosa",
         "Severidade": "Alto", "Origem": "Texto"},
        {"Horário": "07:42", "Paciente": "PAC-005", "Tipo": "Pré-eclâmpsia",
         "Severidade": "Médio", "Origem": "Sinais Vitais"},
    ])
    st.dataframe(alerts_df, use_container_width=True, hide_index=True)


def _render_video_analysis(st):
    """Render video analysis page."""
    st.header("🎬 Análise de Vídeo - YOLOv8")

    uploaded = st.file_uploader("Upload de vídeo cirúrgico", type=["mp4", "avi", "mov"])
    if uploaded:
        st.video(uploaded)
        st.info("Processando vídeo... (demonstração)")

    st.subheader("Configuração do Modelo")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Modelo:", ["YOLOv8n - Nano", "YOLOv8s - Small", "YOLOv8m - Medium"])
        st.slider("Confiança mínima:", 0.0, 1.0, 0.5, 0.05)
    with col2:
        st.selectbox("Alvo de Detecção:", ["Sangramento anômalo", "Áreas críticas",
                                            "Instrumentos cirúrgicos"])
        st.slider("Intervalo de frames:", 1, 60, 10)

    st.info("📊 Resultados da análise aparecerão aqui após o processamento.")


def _render_audio_analysis(st):
    """Render audio analysis page."""
    st.header("🎙️ Análise de Áudio - Voice Analytics")

    uploaded = st.file_uploader("Upload de áudio de consulta", type=["wav", "mp3", "flac"])
    if uploaded:
        st.audio(uploaded)

    st.subheader("Análise de Voz")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Emoção Detectada", "Ansiedade", delta="Score: 0.72")
        st.metric("Hesitação", "3.2s médio", delta="Alto")
    with col2:
        st.metric("Tom de Voz", "Agudo (+12%)", delta="Anormal")
        st.metric("Ritmo", "Acelerado", delta="Ansiedade")

    st.info("🔍 Transcrição da consulta aparecerá aqui.")


def _render_text_analysis(st):
    """Render text analysis page."""
    st.header("📝 Análise de Texto - NLP Clínico")

    text_input = st.text_area("Cole o laudo médico ou prescrição:",
                               height=200,
                               placeholder="Ex: Paciente gestante, 32 semanas...")

    if st.button("Analisar Texto"):
        st.subheader("Resultados")
        col1, col2 = st.columns(2)
        with col1:
            st.success("✅ Entidades clínicas extraídas")
            st.code("Medicamentos: metildopa 500mg\nCondições: pré-eclâmpsia\nSinais: PA 150/95 mmHg")
        with col2:
            st.warning("⚠️ Alertas")
            st.code("Nível de Risco: ALTO\n- Pressão arterial elevada\n- Necessita revisão da dosagem")


def _render_alerts(st):
    """Render alerts page."""
    st.header("🚨 Central de Alertas")

    severity_filter = st.selectbox("Filtrar por severidade:",
                                    ["Todos", "Crítico", "Alto", "Médio", "Baixo"])

    # Sample alerts
    alerts = [
        {"id": "ALT-001", "severity": "critical", "time": "08:15",
         "patient": "PAC-003", "message": "Sangramento anômalo detectado em vídeo cirúrgico",
         "source": "Vídeo"},
        {"id": "ALT-002", "severity": "high", "time": "08:10",
         "patient": "PAC-007", "message": "Indicadores vocais de depressão pós-parto",
         "source": "Áudio"},
        {"id": "ALT-003", "severity": "high", "time": "07:55",
         "patient": "PAC-011", "message": "Interação medicamentosa: ocitocina + misoprostol",
         "source": "Texto"},
        {"id": "ALT-004", "severity": "medium", "time": "07:42",
         "patient": "PAC-005", "message": "PA elevada: 155/98 mmHg - Risco pré-eclâmpsia",
         "source": "Sinais Vitais"},
    ]

    for alert in alerts:
        color = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
        with st.expander(f"{color.get(alert['severity'], '⚪')} [{alert['severity'].upper()}] "
                         f"{alert['time']} - {alert['patient']}: {alert['message']}"):
            st.write(f"**Origem:** {alert['source']}")
            st.write(f"**ID:** {alert['id']}")
            col1, col2 = st.columns(2)
            with col1:
                st.button("✓ Confirmar", key=f"ack_{alert['id']}")
            with col2:
                st.button("📋 Detalhes", key=f"det_{alert['id']}")


def _render_reports(st):
    """Render reports page."""
    st.header("📄 Relatórios")

    st.subheader("Relatórios Gerados")
    reports = [
        {"name": "Relatório de Análise de Vídeo - PAC-003",
         "date": "2026-06-22", "type": "Vídeo", "status": "Concluído"},
        {"name": "Relatório de Análise de Áudio - PAC-007",
         "date": "2026-06-22", "type": "Áudio", "status": "Concluído"},
        {"name": "Relatório de Fusão Multimodal - PAC-011",
         "date": "2026-06-22", "type": "Multimodal", "status": "Concluído"},
    ]

    for report in reports:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"📄 {report['name']}")
            st.caption(f"{report['date']} | Tipo: {report['type']}")
        with col2:
            st.write(f"✅ {report['status']}")
        with col3:
            st.button("📥 Download", key=f"dl_{report['name']}")

    st.markdown("---")
    st.subheader("Gerar Novo Relatório")
    st.selectbox("Tipo de Relatório:",
                  ["Fusão Multimodal", "Análise de Vídeo", "Análise de Áudio",
                   "Análise de Texto", "Relatório Técnico Completo"])
    st.text_input("ID da Paciente:", "PAC-XXX")
    st.button("Gerar Relatório")


if __name__ == "__main__":
    main()
