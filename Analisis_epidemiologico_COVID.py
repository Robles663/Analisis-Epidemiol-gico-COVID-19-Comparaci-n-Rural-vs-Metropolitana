import pandas as pd
import plotly_express as px
from scipy.stats import ttest_ind

confirm_case = pd.read_csv(
    r"C:\Users\TuUsuario\Proyectos\Analisis-Epidemiologico-COVID-19-Comparacion-Rural-vs-Metropolitana\Dataframe\Casos_Diarios_Municipio_Confirmados_20230625.csv"
)


# Modificar el dataframe para que las fechas se coloque en 1 columna
confirm_case_modify = confirm_case.melt(
    id_vars=['cve_ent', 'poblacion', 'nombre'],
    var_name='fecha',
    value_name='casos'
)
confirm_case_modify['fecha'] = pd.to_datetime(
    confirm_case_modify['fecha'], dayfirst=True)
confirm_case_modify['poblacion'] = confirm_case_modify['poblacion'].astype(int)

# Agregar columna con mes y año para un mejor estudio
confirm_case_modify['year_month'] = confirm_case_modify['fecha'].dt.to_period(
    'M')

# Municipios rurales
rural_confirm_raw = confirm_case_modify[confirm_case_modify['poblacion'] < 50000].sort_values(
    by=['nombre', 'fecha']).reset_index(drop=True)

# Municipios metropolitanos
metro_confirm_raw = confirm_case_modify[confirm_case_modify['poblacion'] >= 500000].sort_values(
    by=['nombre', 'fecha']).reset_index(drop=True)

# Visualizar graficamente la cantidad de casos por municipios metropolitanos
metro_confirm_scatter = px.scatter(metro_confirm_raw,
                                   x='fecha',
                                   y='casos',
                                   labels={'casos': 'Cantidad de casos diarios',
                                           'fecha': 'Fecha', 'nombre': 'Municipio'},
                                   title='Cantidad de casos confirmados de COVID en municipios metropolitanos (poblacion > 500000)',
                                   color='nombre',
                                   color_discrete_sequence=px.colors.qualitative.Set2)
metro_confirm_scatter.show()

# Visualizar graficamente la cantidad de casos por municipios rurales
rural_confirm_scatter = px.scatter(rural_confirm_raw,
                                   x='fecha',
                                   y='casos',
                                   labels={'casos': 'Cantidad de casos diarios',
                                           'fecha': 'Fecha', 'nombre': 'Municipio'},
                                   title='Cantidad de casos confirmados de COVID en municipio rurales (poblacion < 50000)',
                                   color='nombre',
                                   color_discrete_sequence=px.colors.qualitative.Set2)
rural_confirm_scatter.show()

# Suavizar datos por municipios rurales y metropolitanos para evitar ruido en los datos
metro_confirm = metro_confirm_raw.copy()
metro_confirm['casos_suavizado'] = metro_confirm.groupby('nombre')['casos'].rolling(
    window=7, min_periods=1, center=True).mean().reset_index(level=0, drop=True)

rural_confirm = rural_confirm_raw.copy()
rural_confirm['casos_suavizado'] = rural_confirm.groupby('nombre')['casos'].rolling(
    window=7, min_periods=1, center=True).mean().reset_index(level=0, drop=True)

# Obteniendo proyeccion proporcional de contagio a cada 100,000 habitantes esto para evitar el sesgo por tamaño poblacional
metro_confirm['tasa_100k_suavizado'] = (
    metro_confirm['casos_suavizado'] / metro_confirm['poblacion']) * 100000
rural_confirm['tasa_100k_suavizado'] = (
    rural_confirm['casos_suavizado'] / rural_confirm['poblacion']) * 100000

# Filtrado de municipios graves con mayor a 150 casos por semana
metro_confirm['riesgo'] = 'No alto'
metro_confirm.loc[metro_confirm['tasa_100k_suavizado']
                  >= 150, 'riesgo'] = 'Alto'
metro_confirm.loc[metro_confirm['tasa_100k_suavizado']
                  >= 250, 'riesgo'] = 'Crítico'

rural_confirm['riesgo'] = 'No alto'
rural_confirm.loc[rural_confirm['tasa_100k_suavizado']
                  >= 150, 'riesgo'] = 'Alto'
rural_confirm.loc[rural_confirm['tasa_100k_suavizado']
                  >= 250, 'riesgo'] = 'Crítico'

picos_rural_confirm = rural_confirm.loc[rural_confirm.groupby(
    'nombre')['tasa_100k_suavizado'].idxmax(), ['nombre', 'year_month']]
picos_metro_confirm = metro_confirm.loc[metro_confirm.groupby(
    'nombre')['tasa_100k_suavizado'].idxmax(), ['nombre', 'year_month']]

metro_merge = metro_confirm.merge(
    picos_metro_confirm,
    on='nombre',
    how='inner',
    suffixes=('', '_pico')
)

rural_merge = rural_confirm.merge(
    picos_rural_confirm,
    on='nombre',
    how='inner',
    suffixes=('', '_pico')
)

metro_pico_window = metro_merge.copy()
metro_pico_window['distancia_pico'] = (
    metro_pico_window['year_month'] - metro_pico_window['year_month_pico']).apply(lambda x: x.n)

rural_pico_window = rural_merge.copy()
rural_pico_window['distancia_pico'] = (
    rural_pico_window['year_month'] - rural_pico_window['year_month_pico']).apply(lambda x: x.n)

metro_pico_window = metro_pico_window[metro_pico_window['distancia_pico'].between(
    -2, 2)]
rural_pico_window = rural_pico_window[rural_pico_window['distancia_pico'].between(
    -2, 2)]

comparacion = pd.concat([
    rural_pico_window.assign(tipo='Rural'),
    metro_pico_window.assign(tipo='Metropolitano')
])

curva_media = (
    comparacion
    .groupby(['tipo', 'distancia_pico'])['tasa_100k_suavizado']
    .mean()
    .reset_index()
)

fig = px.line(
    curva_media,
    x='distancia_pico',
    y='tasa_100k_suavizado',
    color='tipo',
    markers=True,
    title='Comparación de dinámica de contagio alrededor del pico',
    labels={'tasa_100k_suavizado': 'Tasa por cada 100k habitantes',
            'distancia_pico': 'Cantidad de meses antes y despues del pico (pico 0)'},
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig.show()

metro_0 = comparacion[
    (comparacion['tipo'] == 'Metropolitano') &
    (comparacion['distancia_pico'] == 0)
]['tasa_100k_suavizado']

rural_0 = comparacion[
    (comparacion['tipo'] == 'Rural') &
    (comparacion['distancia_pico'] == 0)
]['tasa_100k_suavizado']

t_stat, p_value = ttest_ind(metro_0, rural_0, equal_var=False)
alpha = 0.05
print("t:", t_stat)
print("p-value:", p_value)

if p_value > alpha:
    print('El patrón de contagio entre municipio rural y metropolitano podría considerarse similar estadísticamente.')
else:
    print('El tipo de municipio sí influye en el comportamiento del contagio.')
