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

def calcular_cap_rate_bruto(valor_propiedad, renta_mensual):
    ingresos_anuales = renta_mensual * 12
    cap_rate = (ingresos_anuales / valor_propiedad) * 100
    return cap_rate

def calcular_cap_rate_neto(valor_propiedad, renta_mensual, ocupacion):
    ingresos_anuales = renta_mensual * 12 * (ocupacion/100)
    cap_rate = (ingresos_anuales / valor_propiedad) * 100
    return cap_rate

def calcular_flujo_caja(renta_mensual, ocupacion, cuota_mensual, gastos_comunes, seguro_arriendo, mantencion_mensual):
    ingresos = renta_mensual * (ocupacion/100)
    gastos = cuota_mensual + gastos_comunes + seguro_arriendo + mantencion_mensual
    flujo_mensual = ingresos - gastos
    flujo_anual = flujo_mensual * 12
    return flujo_mensual, flujo_anual

# Configuración de la página
st.set_page_config(
    page_title="Calculadora Inmobiliaria",
    page_icon="🏠",
    layout="wide"
)

# Título y descripción
st.markdown("<h1 style='text-align: center;'>GLUTZ CREATIONS</h1>", unsafe_allow_html=True)
st.title("Calculadora de Inversión Inmobiliaria")
st.markdown("""
Esta calculadora te ayudará a analizar la rentabilidad de tu inversión inmobiliaria,
comparando las opciones de compra y arriendo.
""")

# Sidebar para inputs
st.sidebar.header("Parámetros de Inversión")

# Inputs para el crédito
st.sidebar.subheader("Datos del Crédito")
valor_propiedad = st.sidebar.number_input("Valor de la Propiedad ($)", min_value=0, value=50000000, format="%d")
pie = st.sidebar.number_input("Pie (%)", min_value=0, max_value=100, value=20)
tasa_anual = st.sidebar.number_input("Tasa de Interés Anual (%)", min_value=0.0, value=5.5)
plazo_anos = st.sidebar.number_input("Plazo del Crédito (años)", min_value=1, value=30)

# Inputs para el arriendo y gastos
st.sidebar.subheader("Datos del Arriendo y Gastos")
renta_mensual = st.sidebar.number_input("Renta Mensual ($)", min_value=0, value=300000, format="%d")
gastos_comunes = st.sidebar.number_input("Gastos Comunes Mensuales ($)", min_value=0, value=50000, format="%d")
seguro_arriendo = st.sidebar.number_input("Seguro de Arriendo Mensual ($)", min_value=0, value=15000, format="%d")
mantencion_mensual = st.sidebar.number_input("Mantención Mensual ($)", min_value=0, value=30000, format="%d")
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
cap_rate_bruto = calcular_cap_rate_bruto(valor_propiedad, renta_mensual)
cap_rate_neto = calcular_cap_rate_neto(valor_propiedad, renta_mensual, ocupacion)

# Proyección de valores
valores_proyectados = calcular_proyeccion_valor(valor_propiedad, tasa_plusvalia, años_proyeccion)
valor_final = valores_proyectados[-1]

# Cálculos de flujo de caja
flujo_mensual, flujo_anual = calcular_flujo_caja(
    renta_mensual, ocupacion, cuota_mensual, 
    gastos_comunes, seguro_arriendo, mantencion_mensual
)

# Sección de Análisis Principal
st.subheader("Análisis de Crédito vs Arriendo")

# Métricas principales en una fila de 4 columnas
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.metric("Cuota Mensual", f"${cuota_mensual:,.0f}")
    st.metric("Monto del Crédito", f"${monto_credito:,.0f}")

with col_m2:
    st.metric("Monto del Pie", f"${valor_propiedad * (pie/100):,.0f}")
    st.metric("CAE", f"{cae:.2f}%")

with col_m3:
    st.metric("Renta Mensual Total", f"${renta_mensual + gastos_comunes + seguro_arriendo:,.0f}")
    st.metric("Renta Mensual Real", f"${renta_mensual * (ocupacion/100):,.0f}")

with col_m4:
    st.metric("CAP Rate Bruto", f"{cap_rate_bruto:.2f}%")
    st.metric("CAP Rate Neto", f"{cap_rate_neto:.2f}%")

# Separador
st.markdown("---")

# Gráficos principales en dos columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Composición de la Cuota Mensual")
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
    fig_credito.update_layout(
        title='Evolución del Crédito',
        xaxis_title='Meses',
        yaxis_title='Monto ($)'
    )
    st.plotly_chart(fig_credito, use_container_width=True)

with col2:
    st.subheader("Distribución de Gastos Mensuales")
    # Gráfico de composición de gastos mensuales
    fig_gastos = go.Figure()
    gastos_labels = ['Cuota Crédito', 'Gastos Comunes', 'Seguro', 'Mantención']
    gastos_valores = [cuota_mensual, gastos_comunes, seguro_arriendo, mantencion_mensual]
    
    fig_gastos.add_trace(go.Pie(
        labels=gastos_labels,
        values=gastos_valores,
        textinfo='label+percent',
        hole=.3
    ))
    fig_gastos.update_layout(title='Composición de Gastos')
    st.plotly_chart(fig_gastos, use_container_width=True)

# Separador
st.markdown("---")

# Análisis de Rentabilidad
st.subheader("Análisis de Rentabilidad")
col3, col4 = st.columns(2)

with col3:
    # Tabla de comparación
    st.markdown("#### Comparación Detallada")
    datos = {
        'Concepto': ['Cuota/Costo Mensual', 'Valor Total', 'Rentabilidad Anual', 'Rentabilidad sobre Pie', 'CAE', 'CAP Rate Bruto', 'CAP Rate Neto'],
        'Crédito': [f"${cuota_mensual:,.0f}", f"${valor_propiedad:,.0f}", "N/A", "N/A", f"{cae:.2f}%", "N/A", "N/A"],
        'Arriendo': [f"${renta_mensual * (ocupacion/100):,.0f}", 
                    f"${renta_mensual * 12 * (ocupacion/100):,.0f}", 
                    f"{rentabilidad_anual:.2f}%",
                    f"{rentabilidad_pie:.2f}%",
                    "N/A",
                    f"{cap_rate_bruto:.2f}%",
                    f"{cap_rate_neto:.2f}%"]
    }
    df = pd.DataFrame(datos)
    st.dataframe(df)

with col4:
    st.markdown("#### Indicadores de Rentabilidad")
    # Gráfico de rentabilidad comparativa
    fig_rentabilidad = go.Figure()
    fig_rentabilidad.add_trace(go.Bar(
        name='Indicadores',
        x=['CAP Rate Bruto', 'CAP Rate Neto', 'Rentabilidad sobre Pie'],
        y=[cap_rate_bruto, cap_rate_neto, rentabilidad_pie],
        text=[f"{cap_rate_bruto:.2f}%", f"{cap_rate_neto:.2f}%", f"{rentabilidad_pie:.2f}%"],
        textposition='auto',
    ))
    fig_rentabilidad.update_layout(
        yaxis_title='Porcentaje (%)'
    )
    st.plotly_chart(fig_rentabilidad, use_container_width=True)

# Separador
st.markdown("---")

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

# Nueva sección de Flujo de Caja
st.subheader("Análisis de Flujo de Caja")
col7, col8 = st.columns(2)

with col7:
    # Métricas de flujo de caja
    st.metric("Flujo de Caja Mensual", f"${flujo_mensual:,.0f}")
    st.metric("Flujo de Caja Anual", f"${flujo_anual:,.0f}")
    
    # Tabla detallada de flujo mensual
    datos_flujo = {
        'Concepto': ['Ingresos', 'Gastos', 'Flujo Neto'],
        'Mensual': [
            f"${renta_mensual * (ocupacion/100):,.0f}",
            f"${(cuota_mensual + gastos_comunes + seguro_arriendo + mantencion_mensual):,.0f}",
            f"${flujo_mensual:,.0f}"
        ],
        'Anual': [
            f"${renta_mensual * (ocupacion/100) * 12:,.0f}",
            f"${(cuota_mensual + gastos_comunes + seguro_arriendo + mantencion_mensual) * 12:,.0f}",
            f"${flujo_anual:,.0f}"
        ]
    }
    df_flujo = pd.DataFrame(datos_flujo)
    st.dataframe(df_flujo)

with col8:
    # Gráfico de composición de gastos mensuales
    fig_gastos = go.Figure()
    gastos_labels = ['Cuota Crédito', 'Gastos Comunes', 'Seguro', 'Mantención']
    gastos_valores = [cuota_mensual, gastos_comunes, seguro_arriendo, mantencion_mensual]
    
    fig_gastos.add_trace(go.Pie(
        labels=gastos_labels,
        values=gastos_valores,
        textinfo='label+percent',
        hole=.3
    ))
    fig_gastos.update_layout(title='Distribución de Gastos Mensuales')
    st.plotly_chart(fig_gastos, use_container_width=True)

# Después de todas las secciones existentes, agregar:
st.markdown("---")
st.subheader("Fórmulas Utilizadas")

# Crear tres columnas para las fórmulas
col_formulas1, col_formulas2, col_formulas3 = st.columns(3)

with col_formulas1:
    st.markdown("#### Fórmulas de Crédito")
    st.markdown("""
    **Cuota Mensual:**
    ```
    tasa_mensual = tasa_anual / 12 / 100
    num_pagos = plazo_años * 12
    cuota = monto * (tasa_mensual * (1 + tasa_mensual)^num_pagos) / ((1 + tasa_mensual)^num_pagos - 1)
    ```
    
    **CAE (Costo Anual Efectivo):**
    ```
    CAE = ((1 + tasa_mensual)^12 - 1) * 100
    ```
    
    **Monto del Crédito:**
    ```
    monto_credito = valor_propiedad * (1 - pie/100)
    ```
    """)

with col_formulas2:
    st.markdown("#### Fórmulas de Rentabilidad")
    st.markdown("""
    **CAP Rate Bruto:**
    ```
    cap_rate_bruto = (renta_mensual * 12 / valor_propiedad) * 100
    ```
    
    **CAP Rate Neto:**
    ```
    cap_rate_neto = (renta_mensual * 12 * ocupacion/100 / valor_propiedad) * 100
    ```
    
    **Rentabilidad sobre el Pie:**
    ```
    ingresos_anuales = (renta_mensual - gastos_comunes - seguro) * 12 * ocupacion/100
    monto_pie = valor_propiedad * (pie/100)
    rentabilidad_pie = (ingresos_anuales / monto_pie) * 100
    ```
    """)

with col_formulas3:
    st.markdown("#### Fórmulas de Flujo y Proyección")
    st.markdown("""
    **Flujo de Caja Mensual:**
    ```
    ingresos = renta_mensual * (ocupacion/100)
    gastos = cuota_mensual + gastos_comunes + seguro + mantencion
    flujo_mensual = ingresos - gastos
    flujo_anual = flujo_mensual * 12
    ```
    
    **Proyección del Valor:**
    ```
    valor_futuro = valor_inicial * (1 + tasa_plusvalia/100)^año
    ```
    
    **Plusvalía Total:**
    ```
    plusvalia = valor_final - valor_inicial
    plusvalia_porcentual = (valor_final/valor_inicial - 1) * 100
    ```
    """)

# Agregar nota al pie
st.markdown("---")
st.markdown("""
**Notas:**
- Todos los porcentajes se expresan en base anual
- La ocupación afecta directamente a los ingresos por arriendo
- El CAP Rate considera el valor total de la propiedad
- La rentabilidad sobre el pie considera solo el monto del pie como inversión
""")

# Agregar mensaje personal
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #FF4B4B;'>❤️ Glutz los quiere mucho, estudien los números ❤️</h3>", unsafe_allow_html=True)
