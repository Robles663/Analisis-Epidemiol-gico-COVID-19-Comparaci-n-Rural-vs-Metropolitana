# Analisis-Epidemiol-gico-COVID-19-Comparaci-n-Rural-vs-Metropolitana
Este proyecto realiza un análisis comparativo de la dinámica de contagio de COVID-19 entre municipios rurales y metropolitanos, utilizando técnicas de análisis de datos y estadística inferencial.

## Objetivo 
Este proyecto analiza la dinámica de contagios de COVID-19 en municipios rurales y metropolitanos de México, con el fin de identificar diferencias en la propagación alrededor del pico de contagios.

- Ajuste por tamaño poblacional
- Identificación de picos epidemiológicos
- Análisis temporal alrededor del pico de contagio
- Comparación estadística entre distribuciones

El análisis busca responder si el tipo de municipio influye en la evolución del contagio o si ambos presentan patrones estadísticamente similares.

## Resultados principales
### Grafica comparativa
<img width="650" height="450" alt="Comparacion_dinamica_alrededor_de_pico" src="https://github.com/user-attachments/assets/35018ba0-2b6a-4967-ae1d-74d1154eb146" />  

La gráfica muestra que los municipios metropolitanos alcanzaron tasas de contagio cercanas a **50 casos por cada 100k habitantes** en el pico, mientras que los municipios rurales llegaron a aproximadamente **13 casos por cada 100k habitantes**.

### Prueba t-test
t = 34.09, p-value ≈ 4.19e-194.  
El resultado confirma que la diferencia entre municipios metropolitanos y rurales es **estadísticamente significativa**.

## Conclusión
Los municipios metropolitanos presentaron tasas de contagio mucho más altas y concentradas alrededor del pico, mientras que los rurales tuvieron un impacto más moderado. Además, la curva rural muestra una pendiente más ligera después del pico, lo que indica que, aunque el número de casos es menor, el descenso ocurre de manera más lenta en comparación con las áreas metropolitanas. Esta diferencia puede estar relacionada con la menor accesibilidad a servicios de atención médica en zonas rurales, en contraste con la disponibilidad más amplia en áreas metropolitanas. En conjunto, los resultados evidencian cómo la densidad poblacional y la infraestructura sanitaria influyen en la rapidez y magnitud de la propagación del COVID-19.

## Reproducir el análisis
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Robles663/Analisis-Epidemiol-gico-COVID-19-Comparaci-n-Rural-vs-Metropolitana.git
2. Instalar dependencias:
   pip install -r requirements.txt
