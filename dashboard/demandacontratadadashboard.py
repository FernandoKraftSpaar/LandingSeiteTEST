import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Demanda de Energia",
    page_icon="⚡",
    layout="wide" # 'wide' para usar mais espaço da tela
)

# --- Título do Dashboard ---
st.title("⚡ Dashboard de Análise de Demanda Contratada")
st.markdown("Use este dashboard para monitorar a demanda medida e evitar multas por ultrapassagem.")

# --- Constantes e Parâmetros da Empresa ---
# Este valor deve ser o que está no contrato com a concessionária
DEMANDA_CONTRATADA_KW = 150  # Exemplo: 150 kW
# Valor hipotético da tarifa da multa por kW excedido (consulte sua fatura)
TARIFA_MULTA_POR_KW = 50.85  # Exemplo: R$ 50,85 por kW

# --- Geração de Dados de Exemplo (Simulação) ---
# Em um caso real, você carregaria seus dados de um arquivo CSV, Excel ou banco de dados.
def gerar_dados_exemplo():
    datas = pd.to_datetime(pd.date_range(start="2025-01-01", end="2025-10-20", freq="D"))
    # Simula a demanda medida, com alguns picos que ultrapassam o contratado
    demanda_medida = np.random.normal(loc=130, scale=15, size=len(datas))
    # Adiciona picos de ultrapassagem em alguns dias aleatórios
    indices_pico = np.random.choice(len(datas), size=10, replace=False)
    demanda_medida[indices_pico] *= 1.4
    
    df = pd.DataFrame({
        'Data': datas,
        'Demanda Medida (kW)': demanda_medida.clip(min=80) # Garante uma demanda mínima
    })
    return df

df_energia = gerar_dados_exemplo()

# --- Barra Lateral (Sidebar) com Filtros ---
st.sidebar.header("Filtros")
data_inicio = st.sidebar.date_input(
    "Data de Início",
    df_energia['Data'].min().date()
)
data_fim = st.sidebar.date_input(
    "Data de Fim",
    df_energia['Data'].max().date()
)

# Converte as datas do filtro para o formato datetime
data_inicio_dt = pd.to_datetime(data_inicio)
data_fim_dt = pd.to_datetime(data_fim)

# Filtra o DataFrame com base no intervalo de datas selecionado
df_filtrado = df_energia[
    (df_energia['Data'] >= data_inicio_dt) & 
    (df_energia['Data'] <= data_fim_dt)
].copy()


# --- Cálculos Principais ---
# Encontra a demanda máxima no período filtrado
demanda_maxima_periodo = df_filtrado['Demanda Medida (kW)'].max()

# Calcula o quanto foi excedido
demanda_excedida = max(0, demanda_maxima_periodo - DEMANDA_CONTRATADA_KW)

# Calcula a multa
multa_estimada = demanda_excedida * TARIFA_MULTA_POR_KW

# Define o status e a cor
if demanda_excedida > 0:
    status = "NEGATIVO (MULTA)"
    cor_status = "red"
else:
    status = "POSITIVO (EFETIVO)"
    cor_status = "green"

# --- Exibição dos KPIs (Indicadores Chave) ---
st.markdown("### Resumo do Período Selecionado")

# Organiza os KPIs em colunas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Demanda Contratada",
        value=f"{DEMANDA_CONTRATADA_KW:.0f} kW"
    )

with col2:
    st.metric(
        label="Pico de Demanda Medida",
        value=f"{demanda_maxima_periodo:.2f} kW",
        delta=f"{demanda_maxima_periodo - DEMANDA_CONTRATADA_KW:.2f} kW vs Contratada",
        delta_color="inverse" # Vermelho se positivo (ruim), verde se negativo (bom)
    )

with col3:
    st.metric(
        label="Multa Estimada no Período",
        value=f"R$ {multa_estimada:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

with col4:
    st.markdown(f"**Status da Operação:**")
    # Usa HTML para colorir o texto
    st.markdown(f"<h3 style='color: {cor_status};'>{status}</h3>", unsafe_allow_html=True)


# --- Gráfico Dinâmico ---
st.markdown("### Histórico de Demanda Medida")

fig = px.line(
    df_filtrado,
    x='Data',
    y='Demanda Medida (kW)',
    title='Demanda Medida ao Longo do Tempo'
)

# Adiciona uma linha horizontal para representar a Demanda Contratada
fig.add_hline(
    y=DEMANDA_CONTRATADA_KW,
    line_dash="dash",
    line_color="red",
    annotation_text="Demanda Contratada",
    annotation_position="bottom right"
)

# Melhora a visualização do gráfico
fig.update_layout(
    xaxis_title="Data",
    yaxis_title="Demanda (kW)",
    legend_title="Legenda",
    height=500
)

# Exibe o gráfico no dashboard
st.plotly_chart(fig, use_container_width=True)

# --- Tabela de Dados ---
st.markdown("### Dados Detalhados do Período")
st.dataframe(df_filtrado.style.format({'Demanda Medida (kW)': '{:.2f}'}))