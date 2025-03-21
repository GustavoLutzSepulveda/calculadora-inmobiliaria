import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def calcular_cuota_credito(monto, tasa_anual, plazo_anos):
    tasa_mensual = tasa_anual / 12 / 100
    num_pagos = plazo_anos * 12
    cuota = monto * (tasa_mensual * (1 + tasa_mensual)**num_pagos) / ((1 + tasa_mensual)**num_pagos - 1)
    return cuota

def calcular_rentabilidad_arriendo(valor_propiedad, renta_mensual, ocupacion):
    ingresos_anuales = renta_mensual * 12 * (ocupacion/100)
    rentabilidad_anual = (ingresos_anuales / valor_propiedad) * 100
    return rentabilidad_anual

def calcular_rentabilidad_pie(valor_propiedad, pie, renta_mensual, gastos_comunes, seguro_arriendo, ocupacion):
    monto_pie = valor_propiedad * (pie/100)
    ingresos_anuales = (renta_mensual - gastos_comunes - seguro_arriendo) * 12 * (ocupacion/100)
    rentabilidad_pie = (ingresos_anuales / monto_pie) * 100
    return rentabilidad_pie

def calcular_proyeccion_valor(valor_inicial, tasa_plusvalia, años):
    valores = []
    for año in range(años + 1):
        valor = valor_inicial * (1 + tasa_plusvalia/100)**año
        valores.append(valor)
    return valores

def calcular_cae(tasa_nominal, plazo_anos):
    tasa_mensual = tasa_nominal / 12 / 100
    num_pagos = plazo_anos * 12
    cae = ((1 + tasa_mensual)**12 - 1) * 100
    return cae

# Configuración de la página
st.set_page_config(
    page_title="Calculadora Inmobiliaria",
    page_icon="🏠",
    layout="wide"
)

# Título y descripción
st.title("Calculadora de Inversión Inmobiliaria")
st.markdown("""
Esta calculadora te ayudará a analizar la rentabilidad de tu inversión inmobiliaria,
comparando las opciones de compra y arriendo.
""")

# Sidebar para inputs
st.sidebar.header("Parámetros de Inversión")

# Inputs para el crédito
st.sidebar.subheader("Datos del Crédito")
valor_propiedad = st.sidebar.number_input("Valor de la Propiedad ($)", min_value=0, value=50000000)
pie = st.sidebar.number_input("Pie (%)", min_value=0, max_value=100, value=20)
tasa_anual = st.sidebar.number_input("Tasa de Interés Anual (%)", min_value=0.0, value=5.5)
plazo_anos = st.sidebar.number_input("Plazo del Crédito (años)", min_value=1, value=30)

# Inputs para el arriendo
st.sidebar.subheader("Datos del Arriendo")
renta_mensual = st.sidebar.number_input("Renta Mensual ($)", min_value=0, value=300000)
gastos_comunes = st.sidebar.number_input("Gastos Comunes Mensuales ($)", min_value=0, value=50000)
seguro_arriendo = st.sidebar.number_input("Seguro de Arriendo Mensual ($)", min_value=0, value=15000)
ocupacion = st.sidebar.slider("Porcentaje de Ocupación (%)", min_value=0, max_value=100, value=95)

# Inputs para proyección
st.sidebar.subheader("Proyección Futura")
tasa_plusvalia = st.sidebar.number_input("Tasa de Plusvalía Anual (%)", min_value=0.0, value=3.0)
años_proyeccion = st.sidebar.number_input("Años de Proyección", min_value=1, value=10)

# Cálculos
monto_credito = valor_propiedad * (1 - pie/100)
cuota_mensual = calcular_cuota_credito(monto_credito, tasa_anual, plazo_anos)
rentabilidad_anual = calcular_rentabilidad_arriendo(valor_propiedad, renta_mensual, ocupacion)
rentabilidad_pie = calcular_rentabilidad_pie(valor_propiedad, pie, renta_mensual, gastos_comunes, seguro_arriendo, ocupacion)
cae = calcular_cae(tasa_anual, plazo_anos)

# Proyección de valores
valores_proyectados = calcular_proyeccion_valor(valor_propiedad, tasa_plusvalia, años_proyeccion)
valor_final = valores_proyectados[-1]

# Crear dos columnas para mostrar resultados
col1, col2 = st.columns(2)

with col1:
    st.subheader("Análisis de Crédito")
    st.metric("Cuota Mensual", f"${cuota_mensual:,.0f}")
    st.metric("Monto del Crédito", f"${monto_credito:,.0f}")
    st.metric("Monto del Pie", f"${valor_propiedad * (pie/100):,.0f}")
    st.metric("CAE", f"{cae:.2f}%")
    
    # Gráfico de composición de la cuota
    meses = np.arange(1, plazo_anos * 12 + 1)
    saldo = monto_credito
    intereses = []
    capital = []
    
    for mes in meses:
        interes_mes = saldo * (tasa_anual / 12 / 100)
        capital_mes = cuota_mensual - interes_mes
        saldo -= capital_mes
        
        intereses.append(interes_mes)
        capital.append(capital_mes)
    
    fig_credito = go.Figure()
    fig_credito.add_trace(go.Scatter(x=meses, y=intereses, name='Interés', stackgroup='one'))
    fig_credito.add_trace(go.Scatter(x=meses, y=capital, name='Capital', stackgroup='one'))
    fig_credito.update_layout(title='Composición de la Cuota Mensual')
    st.plotly_chart(fig_credito, use_container_width=True)

with col2:
    st.subheader("Análisis de Arriendo")
    ingresos_mensuales_reales = renta_mensual * (ocupacion/100)
    st.metric("Renta Mensual Total", f"${renta_mensual + gastos_comunes + seguro_arriendo:,.0f}")
    st.metric("Renta Mensual Real (con ocupación)", f"${ingresos_mensuales_reales:,.0f}")
    st.metric("Rentabilidad Anual", f"{rentabilidad_anual:.2f}%")
    st.metric("Rentabilidad sobre el Pie", f"{rentabilidad_pie:.2f}%")
    
    # Gráfico de comparación mensual
    fig_comparacion = go.Figure()
    fig_comparacion.add_trace(go.Bar(name='Crédito', x=['Cuota Mensual'], y=[cuota_mensual]))
    fig_comparacion.add_trace(go.Bar(name='Arriendo Total', x=['Cuota Mensual'], 
                                   y=[renta_mensual + gastos_comunes + seguro_arriendo]))
    fig_comparacion.add_trace(go.Bar(name='Arriendo Real', x=['Cuota Mensual'], 
                                   y=[ingresos_mensuales_reales + gastos_comunes + seguro_arriendo]))
    fig_comparacion.update_layout(title='Comparación Mensual')
    st.plotly_chart(fig_comparacion, use_container_width=True)

# Análisis adicional
st.subheader("Análisis de Rentabilidad")
col3, col4 = st.columns(2)

with col3:
    # Tabla de comparación
    datos = {
        'Concepto': ['Cuota/Costo Mensual', 'Valor Total', 'Rentabilidad Anual', 'Rentabilidad sobre Pie', 'CAE'],
        'Crédito': [f"${cuota_mensual:,.0f}", f"${valor_propiedad:,.0f}", "N/A", "N/A", f"{cae:.2f}%"],
        'Arriendo': [f"${ingresos_mensuales_reales + gastos_comunes + seguro_arriendo:,.0f}", 
                    f"${renta_mensual * 12 * (ocupacion/100):,.0f}", 
                    f"{rentabilidad_anual:.2f}%",
                    f"{rentabilidad_pie:.2f}%",
                    "N/A"]
    }
    df = pd.DataFrame(datos)
    st.dataframe(df)

with col4:
    # Gráfico de rentabilidad
    fig_rentabilidad = go.Figure()
    fig_rentabilidad.add_trace(go.Indicator(
        mode="gauge+number",
        value=rentabilidad_pie,
        title={'text': "Rentabilidad sobre el Pie"},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    st.plotly_chart(fig_rentabilidad, use_container_width=True)

# Nueva sección de proyección
st.subheader("Proyección del Valor de la Propiedad")
col5, col6 = st.columns(2)

with col5:
    # Gráfico de proyección
    años = list(range(años_proyeccion + 1))
    fig_proyeccion = go.Figure()
    fig_proyeccion.add_trace(go.Scatter(
        x=años,
        y=valores_proyectados,
        mode='lines+markers',
        name='Valor Proyectado'
    ))
    fig_proyeccion.update_layout(
        title='Proyección del Valor de la Propiedad',
        xaxis_title='Años',
        yaxis_title='Valor ($)',
        showlegend=True
    )
    st.plotly_chart(fig_proyeccion, use_container_width=True)

with col6:
    # Métricas de proyección
    st.metric("Valor Inicial", f"${valor_propiedad:,.0f}")
    st.metric("Valor Proyectado", f"${valor_final:,.0f}")
    st.metric("Plusvalía Total", f"${valor_final - valor_propiedad:,.0f}")
    st.metric("Plusvalía Porcentual", f"{((valor_final/valor_propiedad - 1) * 100):.2f}%")
    
    # Tabla de proyección anual
    datos_proyeccion = {
        'Año': años,
        'Valor Proyectado': [f"${valor:,.0f}" for valor in valores_proyectados],
        'Plusvalía': [f"${valor - valor_propiedad:,.0f}" for valor in valores_proyectados],
        'Plusvalía %': [f"{((valor/valor_propiedad - 1) * 100):.2f}%" for valor in valores_proyectados]
    }
    df_proyeccion = pd.DataFrame(datos_proyeccion)
    st.dataframe(df_proyeccion)