import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuración de página
st.set_page_config(
    page_title="OLAP Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        padding: 0.5rem 0;
        border-bottom: 2px solid #3498db;
    }
    
    /* Mejorar selectores */
    .stSelectbox > div > div > div {
        background-color: #f8f9fa !important;
        color: #333 !important;
        border: 1px solid #ddd !important;
        border-radius: 4px !important;
    }
    
    .stSelectbox > div > div > div > div {
        color: #333 !important;
        background-color: white !important;
    }
    
    .stMultiSelect > div > div > div {
        background-color: #f8f9fa !important;
        border: 1px solid #ddd !important;
    }
    
    /* Estilo del sidebar más sobrio */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
        color: #ecf0f1 !important;
    }
    
    .sidebar .sidebar-content .element-container {
        color: #ecf0f1 !important;
    }
    
    .sidebar .sidebar-content h2,
    .sidebar .sidebar-content h3,
    .sidebar .sidebar-content .markdown-text-container {
        color: #ecf0f1 !important;
    }
    
    .sidebar .sidebar-content .stInfo {
        background-color: rgba(52, 73, 94, 0.8) !important;
        border: 1px solid #7f8c8d !important;
        color: #ecf0f1 !important;
    }
    
    .operation-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        background-color: #e3f2fd;
        color: #1976d2;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    
    /* Mejorar contraste de texto en selectores */
    .stSelectbox label,
    .stMultiSelect label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    /* Placeholder text styling */
    .stSelectbox > div > div > div[data-baseweb="select"] > div {
        color: #666 !important;
    }
</style>
""", unsafe_allow_html=True)

# Funciones auxiliares
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('ventas.csv', parse_dates=['Fecha'])
        df['Mes'] = df['Fecha'].dt.month
        df['Año'] = df['Fecha'].dt.year
        df['Trimestre'] = df['Fecha'].dt.quarter
        df['Día_Semana'] = df['Fecha'].dt.day_name()
        return df
    except FileNotFoundError:
        st.error("Archivo 'ventas.csv' no encontrado. Por favor, asegúrate de que el archivo existe.")
        return None

def create_kpi_metrics(df):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_ventas = df['Ventas'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3>Ventas Totales</h3>
            <h2>${total_ventas:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_productos = df['Producto'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <h3>Productos</h3>
            <h2>{total_productos}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_regiones = df['Región'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <h3>Regiones</h3>
            <h2>{total_regiones}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        promedio_ventas = df['Ventas'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>Venta Promedio</h3>
            <h2>${promedio_ventas:.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

# Cargar datos
df = load_data()
if df is None:
    st.stop()

# Header principal
st.markdown('<h1 class="main-header">OLAP Analytics Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# KPIs principales
create_kpi_metrics(df)
st.markdown("---")

# Sidebar para controles con estilo más sobrio
with st.sidebar:
    st.markdown("## Panel de Control")
    
    # Filtros globales
    st.markdown("### Filtros Globales")
    
    años_disponibles = sorted(df['Año'].unique())
    año_seleccionado = st.selectbox(
        "Año:", 
        años_disponibles, 
        index=len(años_disponibles)-1,
        help="Selecciona el año para filtrar los datos"
    )
    
    # Filtrar datos por año
    df_filtrado = df[df['Año'] == año_seleccionado]
    
    # Información del dataset filtrado con estilo más sobrio
    st.markdown("### Información del Dataset")
    st.markdown(f"""
    **Registros totales:** {len(df_filtrado):,}  
    **Periodo:** {año_seleccionado}  
    **Última actualización:** Hoy
    """)

# Layout principal con pestañas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Slice Analysis", 
    "Dice Operations", 
    "Roll-up Analysis", 
    "Drill-down Explorer", 
    "Pivot Tables"
])

# TAB 1: SLICE ANALYSIS MEJORADO
with tab1:
    st.markdown('<div class="section-header">Slice Analysis</div>', unsafe_allow_html=True)
    st.markdown('<span class="operation-badge">SLICE</span>Análisis detallado por múltiples dimensiones', unsafe_allow_html=True)
    
    # Filtros separados para Producto y Región
    col_filtros1, col_filtros2 = st.columns(2)
    
    with col_filtros1:
        st.markdown("#### Filtro por Producto:")
        productos_disponibles = ["Todos"] + sorted(df_filtrado['Producto'].unique())
        producto_seleccionado = st.selectbox(
            "Selecciona un producto:",
            productos_disponibles,
            key="slice_producto_individual",
            help="Filtra los datos por un producto específico"
        )
    
    with col_filtros2:
        st.markdown("#### Filtro por Región:")
        regiones_disponibles = ["Todas"] + sorted(df_filtrado['Región'].unique())
        region_seleccionada = st.selectbox(
            "Selecciona una región:",
            regiones_disponibles,
            key="slice_region_individual",
            help="Filtra los datos por una región específica"
        )
    
    # Aplicar filtros
    df_slice = df_filtrado.copy()
    filtros_aplicados = []
    
    if producto_seleccionado != "Todos":
        df_slice = df_slice[df_slice['Producto'] == producto_seleccionado]
        filtros_aplicados.append(f"Producto: {producto_seleccionado}")
    
    if region_seleccionada != "Todas":
        df_slice = df_slice[df_slice['Región'] == region_seleccionada]
        filtros_aplicados.append(f"Región: {region_seleccionada}")
    
    # Mostrar filtros aplicados
    if filtros_aplicados:
        st.info(f"Filtros aplicados: {' | '.join(filtros_aplicados)}")
    else:
        st.info("Mostrando todos los datos (sin filtros aplicados)")
    
    # Layout de métricas y visualización
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Métricas del Slice:")
        st.metric("Total Ventas", f"${df_slice['Ventas'].sum():,.0f}")
        st.metric("Registros", f"{len(df_slice):,}")
        if len(df_slice) > 0:
            st.metric("Venta Promedio", f"${df_slice['Ventas'].mean():.0f}")
        else:
            st.metric("Venta Promedio", "$0")
    
    with col2:
        if len(df_slice) > 0:
            # Visualización temporal
            ventas_temporales = df_slice.groupby('Mes')['Ventas'].sum().reset_index()
            
            if len(ventas_temporales) > 0:
                fig_slice = px.line(
                    ventas_temporales, 
                    x='Mes', 
                    y='Ventas',
                    title=f'Evolución temporal - Filtros: {", ".join(filtros_aplicados) if filtros_aplicados else "Sin filtros"}',
                    markers=True
                )
                fig_slice.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12)
                )
                st.plotly_chart(fig_slice, use_container_width=True)
            else:
                st.warning("No hay datos suficientes para mostrar la evolución temporal")
        else:
            st.warning("No hay datos que coincidan con los filtros seleccionados")
    
    # Tabla detallada (colapsible)
    with st.expander("Ver datos detallados del slice"):
        if len(df_slice) > 0:
            st.dataframe(df_slice, use_container_width=True)
        else:
            st.write("No hay datos para mostrar")

# TAB 2: DICE OPERATIONS
with tab2:
    st.markdown('<div class="section-header">Dice Operations</div>', unsafe_allow_html=True)
    st.markdown('<span class="operation-badge">DICE</span>Análisis con filtros múltiples simultáneos', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Filtros Múltiples:")
        productos_dice = st.multiselect(
            "Productos:", 
            sorted(df_filtrado['Producto'].unique()), 
            default=list(df_filtrado['Producto'].unique())[:3],
            key="dice_productos",
            help="Selecciona múltiples productos para el análisis"
        )
        
        regiones_dice = st.multiselect(
            "Regiones:", 
            sorted(df_filtrado['Región'].unique()), 
            default=list(df_filtrado['Región'].unique())[:2],
            key="dice_regiones",
            help="Selecciona múltiples regiones para el análisis"
        )
        
        # Filtro adicional por trimestre
        trimestres_dice = st.multiselect(
            "Trimestres:",
            sorted(df_filtrado['Trimestre'].unique()),
            default=sorted(df_filtrado['Trimestre'].unique()),
            key="dice_trimestres",
            help="Selecciona los trimestres a analizar"
        )
    
    with col2:
        if productos_dice and regiones_dice and trimestres_dice:
            df_dice = df_filtrado[
                (df_filtrado['Producto'].isin(productos_dice)) & 
                (df_filtrado['Región'].isin(regiones_dice)) &
                (df_filtrado['Trimestre'].isin(trimestres_dice))
            ]
            
            if len(df_dice) > 0:
                # Heatmap de correlaciones
                pivot_dice = df_dice.pivot_table(
                    values='Ventas', 
                    index='Región', 
                    columns='Producto', 
                    aggfunc='sum', 
                    fill_value=0
                )
                
                fig_dice = px.imshow(
                    pivot_dice.values,
                    x=pivot_dice.columns,
                    y=pivot_dice.index,
                    color_continuous_scale='RdYlBu_r',
                    title="Heatmap: Ventas por Región y Producto"
                )
                fig_dice.update_layout(height=400)
                st.plotly_chart(fig_dice, use_container_width=True)
                
                # Métricas del dice
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Total Filtrado", f"${df_dice['Ventas'].sum():,.0f}")
                with col_m2:
                    st.metric("Registros", f"{len(df_dice):,}")
                with col_m3:
                    porcentaje = (len(df_dice) / len(df_filtrado)) * 100
                    st.metric("% del Total", f"{porcentaje:.1f}%")
            else:
                st.warning("No hay datos que coincidan con los filtros seleccionados")
        else:
            st.info("Selecciona al menos un elemento en cada filtro para ver el análisis")

# TAB 3: ROLL-UP ANALYSIS
with tab3:
    st.markdown('<div class="section-header">Roll-up Analysis</div>', unsafe_allow_html=True)
    st.markdown('<span class="operation-badge">ROLL-UP</span>Agregación hacia niveles más generales', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Nivel de agregación:")
        nivel_rollup = st.selectbox(
            "Selecciona nivel:", 
            ["Año", "Trimestre", "Mes"],
            key="rollup_nivel",
            help="Nivel de agregación temporal"
        )
        
        dimension_rollup = st.selectbox(
            "Dimensión adicional:",
            ["Producto", "Región", "Ninguna"],
            key="rollup_dimension",
            help="Dimensión adicional para el análisis"
        )
    
    with col2:
        if dimension_rollup == "Ninguna":
            rollup_data = df_filtrado.groupby(nivel_rollup)['Ventas'].sum().reset_index()
            fig_rollup = px.bar(
                rollup_data, 
                x=nivel_rollup, 
                y='Ventas',
                title=f"Roll-up: Ventas por {nivel_rollup}",
                color='Ventas',
                color_continuous_scale='viridis'
            )
        else:
            rollup_data = df_filtrado.groupby([nivel_rollup, dimension_rollup])['Ventas'].sum().reset_index()
            fig_rollup = px.bar(
                rollup_data, 
                x=nivel_rollup, 
                y='Ventas',
                color=dimension_rollup,
                title=f"Roll-up: Ventas por {nivel_rollup} y {dimension_rollup}",
                barmode='group'
            )
        
        fig_rollup.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_rollup, use_container_width=True)
        
        # Mostrar top performers
        st.markdown("#### Top Performers")
        if dimension_rollup != "Ninguna":
            top_data = rollup_data.nlargest(5, 'Ventas')
            for i, row in top_data.iterrows():
                st.write(f"**{row[nivel_rollup]} - {row[dimension_rollup]}:** ${row['Ventas']:,.0f}")

# TAB 4: DRILL-DOWN EXPLORER
with tab4:
    st.markdown('<div class="section-header">Drill-down Explorer</div>', unsafe_allow_html=True)
    st.markdown('<span class="operation-badge">DRILL-DOWN</span>Navegación desde general hacia específico', unsafe_allow_html=True)
    
    # Drill-down interactivo
    drill_data = df_filtrado.groupby(['Año', 'Trimestre', 'Mes', 'Producto', 'Región'])['Ventas'].sum().reset_index()
    
    # Sunburst chart para drill-down
    fig_drill = px.sunburst(
        drill_data, 
        path=['Trimestre', 'Mes', 'Región', 'Producto'], 
        values='Ventas',
        title="Explorador Jerárquico - Click para hacer drill-down",
        height=600
    )
    fig_drill.update_layout(
        font_size=10,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_drill, use_container_width=True)
    
    # Drill-down por niveles
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Drill-down por Niveles")
        # Nivel 1: Trimestre
        trimestre_drill = st.selectbox(
            "1. Trimestre:", 
            sorted(df_filtrado['Trimestre'].unique()), 
            key="drill_trimestre",
            help="Primer nivel de drill-down"
        )
        df_nivel1 = df_filtrado[df_filtrado['Trimestre'] == trimestre_drill]
        
        # Nivel 2: Mes
        meses_disponibles = sorted(df_nivel1['Mes'].unique())
        mes_drill = st.selectbox(
            "2. Mes:", 
            meses_disponibles, 
            key="drill_mes",
            help="Segundo nivel de drill-down"
        )
        df_nivel2 = df_nivel1[df_nivel1['Mes'] == mes_drill]
    
    with col2:
        # Visualización del drill-down
        if len(df_nivel2) > 0:
            ventas_drill = df_nivel2.groupby(['Región', 'Producto'])['Ventas'].sum().reset_index()
            
            fig_drill_bar = px.treemap(
                ventas_drill,
                path=['Región', 'Producto'],
                values='Ventas',
                title=f"Drill-down: T{trimestre_drill} - Mes {mes_drill}"
            )
            st.plotly_chart(fig_drill_bar, use_container_width=True)
            
            # Métricas del nivel actual
            st.metric("Ventas del Periodo", f"${df_nivel2['Ventas'].sum():,.0f}")

# TAB 5: PIVOT TABLES
with tab5:
    st.markdown('<div class="section-header">Pivot Tables</div>', unsafe_allow_html=True)
    st.markdown('<span class="operation-badge">PIVOT</span>Tablas dinámicas y matrices de correlación', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Configuración de Pivot:")
        
        indice_pivot = st.selectbox(
            "Índice (filas):", 
            ["Región", "Producto", "Mes", "Trimestre"], 
            key="pivot_index",
            help="Selecciona la dimensión para las filas"
        )
        columna_pivot = st.selectbox(
            "Columnas:", 
            ["Producto", "Región", "Mes", "Trimestre"], 
            key="pivot_columns",
            help="Selecciona la dimensión para las columnas"
        )
        
        if indice_pivot == columna_pivot:
            st.warning("El índice y las columnas no pueden ser iguales")
        else:
            # Crear pivot table
            pivot_table = df_filtrado.pivot_table(
                values='Ventas', 
                index=indice_pivot, 
                columns=columna_pivot, 
                aggfunc='sum', 
                fill_value=0
            )
            
            # Botón de exportación
            if st.button("Exportar a Excel", key="export_pivot"):
                pivot_table.to_excel('cubo_para_powerbi.xlsx')
                st.success("Archivo 'cubo_para_powerbi.xlsx' exportado correctamente!")
    
    with col2:
        if indice_pivot != columna_pivot:
            # Mostrar pivot table como heatmap
            fig_pivot = px.imshow(
                pivot_table.values,
                x=pivot_table.columns,
                y=pivot_table.index,
                color_continuous_scale='Viridis',
                title=f"Matriz: {indice_pivot} vs {columna_pivot}",
                aspect="auto"
            )
            fig_pivot.update_layout(height=500)
            st.plotly_chart(fig_pivot, use_container_width=True)
            
            # Mostrar tabla numérica
            with st.expander("Ver tabla numérica"):
                st.dataframe(pivot_table, use_container_width=True)
            
            # Estadísticas de la tabla pivot
            st.markdown("#### Estadísticas:")
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.metric("Máximo", f"${pivot_table.values.max():,.0f}")
            with col_s2:
                st.metric("Promedio", f"${pivot_table.values.mean():,.0f}")
            with col_s3:
                st.metric("Mínimo", f"${pivot_table.values.min():,.0f}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>OLAP Analytics Dashboard</strong> | Desarrollado con Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)