# Lo que trae el técnico

**Hackathon ISAC 2026 · Club América, pista 2: "La historia de un entrenador a través de los datos".**
Participación individual: Arturo (Universidad Panamericana).

¿Qué compra un club cuando contrata un técnico? Con cinco temporadas de eventos StatsBomb 360 de la Liga MX medimos 85 rasgos de estilo y comparamos a técnicos que cambiaron de club con clubes que cambiaron de técnico. El hallazgo central es que el técnico decide cómo juega el equipo y quién juega decide cuánto le rinde. Una prueba en vivo con Guillermo Almada en el América, con predicciones congeladas antes de ver sus partidos, cumplió las cuatro predicciones.

- **Reporte interactivo:** https://atapiamail84-lab.github.io/Lo-que-trae-el-DT/reporte/ (el archivo está en `reporte/index.html`)
- **Video (5 min):** _(enlace en el formulario de entrega)_

Este repositorio contiene **el código que produjo cada número del reporte**. No contiene datos: las reglas del reto prohíben publicarlos.

---

## Contenido

| Ruta | Qué es |
|---|---|
| `cuadernos/1_analisis_completo.ipynb` | Todo el análisis en orden de ejecución, de la descarga de datos a las tablas del reporte (147 celdas). Sin salidas. |
| `cuadernos/2_fase_final.ipynb` | La fase final: prueba en vivo de Almada (E, X6, V-1) y exportación al reporte (G-0 a G-10), 35 celdas. Conserva las salidas de G-8, G-9, G-10 y G-9b. |
| `reporte/index.html` | El reporte interactivo (versión entregada el 22-oct-2026). Se ve publicado en el enlace de arriba. |
| `docs/preregistro_almada.md` | Las cuatro predicciones sobre Almada, congeladas el 18-oct-2026 a las 23:58, con sus aclaraciones fechadas y el resultado. |

## Cómo se ejecutó

- **Entorno:** Google Colab con Google Drive montado. Los datos se descargaron una sola vez de la API de StatsBomb y se guardaron en Drive como parquet. Ningún análisis vuelve a descargar.
- **Credenciales:** el usuario y la clave de la API se leen de los Secretos de Colab (`userdata.get('SB_USER')`, `userdata.get('SB_PASS')`). No están escritos en el código.
- **Tres cuadernos, una sola cadena.** Por su tamaño, Colab empezó a fallar al cargar el cuaderno, así que el trabajo continuó en un segundo cuaderno y la fase final corrió en un tercero. Los cuadernos no comparten memoria: cada celda lee sus insumos de archivos en Drive y escribe ahí sus resultados. Por eso se pueden correr en cuadernos distintos sin cambiar ningún número. Varias celdas verifican que sus insumos existan y se detienen si falta un paso previo.
- **Limpieza de cuadernos:** dos veces se usó Antigravity (IA de Google) para quitar las salidas de un cuaderno pesado y poder abrirlo. Comprobamos celda por celda que el código quedó idéntico al original: 117 de 117 celdas en la primera limpieza y 147 de 147 en la segunda.
- **Semilla fija:** 2026 en todos los remuestreos y placebos.
- **Pruebas con datos inventados:** las celdas principales se corrieron primero sobre una liga inventada, con y sin efecto, para comprobar que encuentran lo que deben y nada más.

### Orden de ejecución (prefijos de las celdas)

| Bloque | Celdas | Qué hace |
|---|---|---|
| Datos | celdas iniciales, D1, D2, E3, IDS, BP1, BP2 | Descarga, conversión a parquet, tabla de técnicos y etapas, viabilidad del 360 |
| Objetos base | R-00, R0, R1 | Definiciones del framework: posesión, secuencia, transición, fase de presión, balón parado |
| Métricas y nivel | R2a, R2b, R2c, R3 (Elo y Elo de xG) | Componentes por equipo-partido, presión, calibración de pases, nivel de cada equipo |
| Contexto y confiabilidad | R4, R5, R6r | Ajuste por rival, nivel, localía, marcador y tramo; confiabilidad, reloj de medición y contracción |
| Rasgos de estilo | R6a-R6d, R7a-R7d, R8a-R8u, R9 | Ataque, transiciones, OBV, uso de jugadores, banquillo, balón parado, organización defensiva 360 |
| Validaciones previas | E9, V-T, X5, PC, PA | Capa predictiva, holdout 2025/26, extensión a cinco temporadas |
| Mapa de dueños y compatibilidad | C-0, C-1, C-1b, C-2, C-3, F-1, F-2 | Mapa de dos ejes con placebo, compatibilidad técnico-club, ensayo en 27 llegadas |
| Pruebas complementarias | R8h, K1, K1b, D1, D1b, L1, A1, A2, M1, B7 | Emparejamiento aéreo, concordancia con StatsBomb, duración de etapas, territorio por titular fuera |
| Prueba en vivo (Almada) | E-00 a E-5, X6-*, V-1 | Re-descarga con corte 19-oct, reajuste completo, validación contra lo previo y evaluación literal del preregistro |
| Reporte | G-0 a G-10 | Exportación de agregados al reporte |

### Qué celda sostiene cada sección del reporte

| Sección del reporte | Celdas principales |
|---|---|
| Resumen | C-1, G-2, V-1, D1 |
| 01 · Así juega cada técnico | R4-R9 (rasgos), G-0 (cadena de relevos), G-3, G-4/G-4b (cancha y percentiles), G-5, G-6, G-7 (marcador), R7b (banquillo), G-9, G-9b, G-10 (córners, saque de meta y pase largo reales) |
| 02 · La prueba en vivo | C-3, preregistro, E-00 a E-5, X6-9, V-1 |
| 03 · ¿De quién es cada rasgo? | C-1, C-1b, C-2, G-2, A2, L1, R5 y R6r (relojes) |
| 04 · Qué decide cada quien | C-1, C-2 (compatibilidad), R8h y G-8 (HOPS), D1 (duración), R5 (semáforo), L1 |
| 05 · Cómo lo medimos | K1, K1b (concordancia), R5, R6r, G-9b (prueba de mitades) |

## Datos

- **Fuente:** eventos y fotos 360 de StatsBomb, Liga MX, del Apertura 2021 al Clausura 2026, más 11 partidos del Apertura 2026 para la prueba en vivo. Acceso por API otorgado por los organizadores.
- **Uso:** solo para esta competencia. El repositorio no incluye eventos, fotos 360 ni ningún archivo de datos. El reporte publica solo resultados agregados.

## Uso de inteligencia artificial

Proyecto individual. El código y el reporte HTML se escribieron con Claude (Anthropic), que nunca tuvo acceso a los datos. Yo corrí cada celda en mi Colab, revisé cada resultado y tomé las decisiones de método y de criterio futbolístico, registradas con fecha en la bitácora del proyecto. Entre ellas:

- el principio que guía el reporte: los datos informan y el criterio futbolístico decide;
- elegir técnico con perfiles anónimos, para que la fama no pese en la decisión;
- emparejar las marcas del córner por capacidad aérea (HOPS) en vez de estatura;
- en la prueba de Almada, la cuarta predicción: que los datos lo reconocieran a ciegas.

Antigravity (Google) solo quitó las salidas de los cuadernos pesados; el código quedó idéntico.

## Referencias

1. Bertrand, M. y Schoar, A. (2003). Managing with style: The effect of managers on firm policies. *The Quarterly Journal of Economics, 118*(4), 1169-1208. https://doi.org/10.1162/003355303322552775
2. Goldin, C. y Rouse, C. (2000). Orchestrating impartiality: The impact of "blind" auditions on female musicians. *American Economic Review, 90*(4), 715-741. https://doi.org/10.1257/aer.90.4.715
3. Kuhn, H. W. (1955). The Hungarian method for the assignment problem. *Naval Research Logistics Quarterly, 2*(1-2), 83-97. https://doi.org/10.1002/nav.3800020109
4. Hudl StatsBomb. (2023, 31 de mayo). *Introducing HOPS: A new way to evaluate heading ability*. https://www.hudl.com/blog/introducing-hops-a-new-way-to-evaluate-heading-ability
5. Pulling, C., Robins, M. T. y Rixon, T. (2013). Defending corner kicks: Analysis from the English Premier League. *International Journal of Performance Analysis in Sport, 13*(1), 135-148.

Librerías: pandas, NumPy, SciPy, scikit-learn, statsmodels, Shapely (Voronoi), PyArrow y requests en Python; D3.js para las gráficas del reporte.
