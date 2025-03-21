import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# Después de las importaciones
VALOR_UF = 38899.12  # Valor UF al día de hoy

def convertir_uf_a_pesos(valor_uf):
    return valor_uf * VALOR_UF

def convertir_pesos_a_uf(valor_pesos):
    return valor_pesos / VALOR_UF

def calcular_proyeccion_valor_con_uf(valor_inicial_pesos, tasa_plusvalia, tasa_uf, años):
    valores_pesos = []
    valores_uf = []
    valor_actual_pesos = valor_inicial_pesos
    valor_actual_uf = convertir_pesos_a_uf(valor_inicial_pesos)
    
    for año in range(años + 1):
        valores_pesos.append(valor_actual_pesos)
        valores_uf.append(valor_actual_uf)
        
        # Actualizar valores para el siguiente año
        valor_actual_pesos *= (1 + tasa_plusvalia/100) * (1 + tasa_uf/100)
        valor_actual_uf *= (1 + tasa_plusvalia/100)
    
    return valores_pesos, valores_uf

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

# Título con enlace
st.markdown("""
<div style='text-align: center;'>
    <h1><a href='https://www.glutz.cl/portafolio' target='_blank' style='text-decoration: none; color: #FF4B4B;'>GLUTZ CREATIONS</a></h1>
    <h2>Calculadora de Inversión Inmobiliaria</h2>
</div>
""", unsafe_allow_html=True)

# Después del título y antes del sidebar
st.markdown(f"""
<div style='background-color: #0E1117; padding: 10px; border-radius: 5px; margin-bottom: 20px; border: 1px solid #FF4B4B;'>
    <h4 style='text-align: center; margin: 0; color: #FFFFFF;'>Valor UF Actual: <span style='color: #FF4B4B'>${VALOR_UF:,.2f}</span></h4>
</div>
""", unsafe_allow_html=True)

# Descripción
st.markdown("""
Esta calculadora te ayudará a analizar la rentabilidad de tu inversión inmobiliaria,
comparando las opciones de compra y arriendo.
""")

# Sidebar para inputs
st.sidebar.header("Configuración")
usar_uf = st.sidebar.toggle("Mostrar valores en UF", value=False)

# En el sidebar, al inicio
st.sidebar.header("Parámetros de Inversión")
st.sidebar.subheader("Datos del Crédito")

if usar_uf:
    valor_propiedad_uf = st.sidebar.number_input("Valor de la Propiedad (UF)", 
                                                min_value=0.0, 
                                                value=1285.0,  # Aproximadamente 50M en UF
                                                format="%.2f")
    valor_propiedad = convertir_uf_a_pesos(valor_propiedad_uf)
else:
    valor_propiedad = st.sidebar.number_input("Valor de la Propiedad ($)", 
                                            min_value=0, 
                                            value=50000000, 
                                            format="%d")

# Agregar inputs del crédito
pie = st.sidebar.number_input("Pie (%)", min_value=0, max_value=100, value=20)
tasa_anual = st.sidebar.number_input("Tasa de Interés Anual (%)", min_value=0.0, value=5.5)
plazo_anos = st.sidebar.number_input("Plazo del Crédito (años)", min_value=1, value=30)

if usar_uf:
    renta_mensual_uf = st.sidebar.number_input("Renta Mensual (UF)", 
                                              min_value=0.0, 
                                              value=7.71,  # Aproximadamente 300k en UF
                                              format="%.2f")
    renta_mensual = convertir_uf_a_pesos(renta_mensual_uf)
    
    gastos_comunes_uf = st.sidebar.number_input("Gastos Comunes Mensuales (UF)", 
                                               min_value=0.0, 
                                               value=1.29,  # Aproximadamente 50k en UF
                                               format="%.2f")
    gastos_comunes = convertir_uf_a_pesos(gastos_comunes_uf)
    
    seguro_arriendo_uf = st.sidebar.number_input("Seguro de Arriendo Mensual (UF)", 
                                                min_value=0.0, 
                                                value=0.39,  # Aproximadamente 15k en UF
                                                format="%.2f")
    seguro_arriendo = convertir_uf_a_pesos(seguro_arriendo_uf)
    
    mantencion_mensual_uf = st.sidebar.number_input("Mantención Mensual (UF)", 
                                                   min_value=0.0, 
                                                   value=0.77,  # Aproximadamente 30k en UF
                                                   format="%.2f")
    mantencion_mensual = convertir_uf_a_pesos(mantencion_mensual_uf)
else:
    renta_mensual = st.sidebar.number_input("Renta Mensual ($)", 
                                          min_value=0, 
                                          value=300000, 
                                          format="%d")
    gastos_comunes = st.sidebar.number_input("Gastos Comunes Mensuales ($)", 
                                           min_value=0, 
                                           value=50000, 
                                           format="%d")
    seguro_arriendo = st.sidebar.number_input("Seguro de Arriendo Mensual ($)", 
                                            min_value=0, 
                                            value=15000, 
                                            format="%d")
    mantencion_mensual = st.sidebar.number_input("Mantención Mensual ($)", 
                                               min_value=0, 
                                               value=30000, 
                                               format="%d")

# Inputs para el arriendo y gastos
st.sidebar.subheader("Datos del Arriendo y Gastos")
ocupacion = st.sidebar.slider("Porcentaje de Ocupación (%)", min_value=0, max_value=100, value=95)

# Inputs para proyección
st.sidebar.subheader("Proyección Futura")
tasa_plusvalia = st.sidebar.number_input("Tasa de Plusvalía Anual (%)", min_value=0.0, value=3.0)
tasa_uf = st.sidebar.number_input("Tasa de Crecimiento UF Anual (%)", min_value=0.0, value=3.0)
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
valores_proyectados_pesos, valores_proyectados_uf = calcular_proyeccion_valor_con_uf(
    valor_propiedad, tasa_plusvalia, tasa_uf, años_proyeccion
)

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
    
    if usar_uf:
        valores_mostrar = valores_proyectados_uf
        unidad = "UF"
    else:
        valores_mostrar = valores_proyectados_pesos
        unidad = "$"
    
    fig_proyeccion.add_trace(go.Scatter(
        x=años,
        y=valores_mostrar,
        mode='lines+markers',
        name='Valor Proyectado'
    ))
    fig_proyeccion.update_layout(
        title=f'Proyección del Valor de la Propiedad ({unidad})',
        xaxis_title='Años',
        yaxis_title=f'Valor ({unidad})',
        showlegend=True
    )
    st.plotly_chart(fig_proyeccion, use_container_width=True)

with col6:
    # Métricas de proyección
    if usar_uf:
        valor_inicial_mostrar = valores_proyectados_uf[0]
        valor_final_mostrar = valores_proyectados_uf[-1]
        unidad = "UF"
    else:
        valor_inicial_mostrar = valores_proyectados_pesos[0]
        valor_final_mostrar = valores_proyectados_pesos[-1]
        unidad = "$"
    
    if unidad == "UF":
        st.metric("Valor Inicial", f"{valor_inicial_mostrar:,.2f} UF")
        st.metric("Valor Proyectado", f"{valor_final_mostrar:,.2f} UF")
        st.metric("Plusvalía Total", f"{valor_final_mostrar - valor_inicial_mostrar:,.2f} UF")
    else:
        st.metric("Valor Inicial", f"${valor_inicial_mostrar:,.0f}")
        st.metric("Valor Proyectado", f"${valor_final_mostrar:,.0f}")
        st.metric("Plusvalía Total", f"${valor_final_mostrar - valor_inicial_mostrar:,.0f}")
    
    st.metric("Plusvalía Porcentual", f"{((valor_final_mostrar/valor_inicial_mostrar - 1) * 100):.2f}%")
    
    # Tabla de proyección anual
    datos_proyeccion = {
        'Año': años,
        f'Valor Proyectado ({unidad})': [f"{valor:,.2f} UF" if usar_uf else f"${valor:,.0f}" 
                                        for valor in valores_mostrar],
        'Plusvalía': [f"{valor - valores_mostrar[0]:,.2f} UF" if usar_uf else f"${valor - valores_mostrar[0]:,.0f}" 
                      for valor in valores_mostrar],
        'Plusvalía %': [f"{((valor/valores_mostrar[0] - 1) * 100):.2f}%" for valor in valores_mostrar]
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

# Al final del archivo, antes de la sección de fórmulas
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; color: #666;'>
    <p>Calculadora creada por <a href='https://www.glutz.cl' target='_blank' style='text-decoration: none; color: #FF4B4B;'>Glutz</a></p>
</div>
""", unsafe_allow_html=True)
