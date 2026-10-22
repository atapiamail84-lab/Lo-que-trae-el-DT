# Preregistro: Almada en América (compatibilidad técnico-club, prueba en vivo 2026/27)

**Estado:** **CONGELADO el 2026-10-18 a las 23:58 (hora de Ciudad de México), aprobado por Arturo.** Desde ese momento no se cambia ningún umbral ni definición (E-16: lectura literal). Versión v1.0.
**Base:** bitácora v13 (sesión 12), celdas C-1, C-2, C-3 y V-00 (`claude/codigo/sesion12/`), salidas `c_mapa.csv`, `c_preregistro_almada.csv`, `c_ensayo_llegadas.csv`, `c_ensayo_cobertura.csv`.

---

## 1. Qué se pone a prueba

La herramienta de compatibilidad (T-11 reescrito, sesión 12) dice tres cosas que se pueden comprobar con los partidos de Almada en América:
1. **Cuánto va a cambiar el equipo** (más cuanto menos compatibles son técnico y club).
2. **Qué rasgos cambian y cuáles no** (el mapa: los rasgos "del técnico" se mueven hacia él; los "del club" se quedan).
3. **Que los datos reconocen al técnico** (con unos cuantos partidos, el perfil del equipo apunta a quien lo dirige).

Almada es el caso más exigente: era el candidato **menos** compatible con la América de Jardine (0%, puesto 61 de 61).

**Limpieza (D-2):** los 9 partidos de Almada ya descargados (hasta el 2026-09-28) no se han analizado. V-00 solo contó archivos (eventos, 360 y Elo: 9 de 9). Ningún umbral de este documento se eligió mirando 2026/27.

## 2. Definiciones (todas vienen de C-1 y C-3; no se cambian)

- **Perfil del club antes (zc):** últimos 18 partidos de América antes de Almada (hasta 2026-05-11), perfil ajustado y contraído (P-5), en z (÷ τ del rasgo).
- **Perfil del técnico (zt):** Almada en Pachuca (etapa Pachuca · 2, 139 partidos), perfil contraído, en z.
- **Perfil nuevo (zn):** **todos** los partidos de liga de Almada con América disponibles en la re-descarga (K partidos, periodos 1-2), mismo cálculo y contracción con n = K.
- **Rasgos:** los 65 con confiabilidad ≥ 0.5 (C-1).
- **Pesos:** eje técnico del mapa **sin las parejas de Almada** (un técnico fuera), recortado a [0, 1].
- **Distancia:** raíz del promedio ponderado de diferencias al cuadrado, en z.
- **Cobertura de la brecha (por rasgo):** (zn − zc) / (zt − zc). 0 = América no se movió; 1 = quedó igual que Almada; 0.5 = cubrió la mitad.

## 3. Predicciones

| Id | Predicción | Umbral (se cumple si…) | Tasa en el ensayo (27 llegadas, K = 12) |
|---|---|---|---|
| **P1** | América cambia más que una llegada típica | distancia(zc → zn) **> percentil 75** del ensayo con el mismo K (indicativo: K = 9 → 1.01; K = 12 → 1.06; K = 15 → 1.06) | 25% por construcción |
| **P2** | Lo del técnico viaja: defensores en el área en córner y defensores zonales | cobertura **≥ 0.5 en los dos** (natural, valores de fw5: defensores en el área de 8.75 a ≤ 7.71; zonales de 3.78 a ≤ 3.13) | 67% y 57% por separado |
| **P3** | Lo del club no viaja: segundos hasta el último tercio | cobertura **< 0.5** (se queda por encima de 11.75) | 63% |
| **P4** | Identificación a ciegas: con solo los partidos de 2026/27, los datos señalan a Almada | Almada en el **10% más parecido** de los candidatos (percentil ≥ 90; con 62 candidatos, puesto ≤ 6) | 37% |

**P4, detalle:**
- Candidatos: la última etapa de 15+ partidos de cada técnico de la liga terminada antes del inicio de Almada en América, fuera de América, más Almada en Pachuca.
- Rasgos: solo los que se leen en pocos partidos (reloj de medición ≤ 20) y con peso > 0.
- Por azar, Almada caería en el percentil 50.
- Contraste: antes de llegar, Almada era el **más lejano** a América (61 de 61). Si P4 se cumple, el equipo pasó de no parecerse en nada a parecerse a él.

**Notas de lectura:**
- P2 es asimétrica por la contracción hacia la liga (con pocos partidos el perfil nuevo se acerca a la media de la liga): en defensores en el área la liga queda entre América y Almada (ayuda ~12% de la brecha); en zonales queda del lado de América (estorba).
- Cada predicción se reporta por separado (cumple / no cumple) con su valor. No hay una calificación conjunta.

## 4. Procedimiento de evaluación (día 20)

1. **Re-descarga** de 2026/27 con corte fijo: partidos jugados hasta el **2026-10-19** (aprobado por Arturo).
2. **R1 de 2026/27 en una carpeta nueva** (`datos_parquet/fw6/`), **nunca en fw1**. Requiere el código de R1 (pendiente de Arturo: subir R-00, R0 y R1).
3. **Elo de 2026/27** para los partidos nuevos (extensión del Elo; hoy cubre 88 de 88 partidos hasta el 2026-09-28).
4. **X6:** carpeta espejo con 2026/27 agregada a las temporadas de ajuste; corren sin cambios R4a, R4b, R6a, R6b, R6c, R7a, R7u, R7b, R7c, R8a, R8z, R8u y R6r-1 por prefijo (patrón X5 / D-11).
   - Validación obligatoria: los perfiles de las etapas ya existentes deben coincidir con fw5 (correlación ≥ 0.99 por rasgo).
   - zt, zc y zn se recalculan con X6. Si zt o zc cambian más de 0.1 z en un rasgo de P2-P4, se reporta junto al resultado.
5. **V-1:** celda de evaluación que reutiliza literal el código de C-3 (misma función de perfil, mismos pesos, mismos candidatos) y lee los umbrales de este documento. Antes de evaluar a Almada, V-1 se corre sobre una llegada histórica y debe reproducir el número de C-3 (buena práctica 13).
6. **Lo que no se pueda medir a tiempo se reporta como "no evaluado"**, nunca como cumplido.

## 5. Congelación

- Aprobado por: Arturo · Fecha y hora: 2026-10-18, 23:58 (America/Mexico_City).
- Cualquier cambio posterior se agrega como aclaración fechada al final, sin tocar las secciones 1 a 4.

---

## Aclaración 1 · 2026-10-20, 11:35 (America/Mexico_City) · aprobada por Arturo ANTES de correr X6 y de ver cualquier perfil de 2026/27

Hecho que la motiva: la re-descarga (sesión 13, E-1) dio **K = 11** partidos de Almada (el partido del 11-oct no tiene 360: los rasgos de 360 se leen con 10). El ensayo de C-3 se corrió con K = 9, 12 y 15, no con 11. Además, al revisar el código de X6 aparecieron dos huecos de procedimiento. Ningún umbral ni definición de las secciones 1 a 3 cambia.

1. **Versión de referencia (Arturo: "todo X6").** zt, zc, zn, los pesos (eje técnico sin las parejas de Almada) y el umbral de P1 salen de X6. El umbral de P1 es el **percentil 75 del ensayo de C-3 corrido con K = 11** sobre X6, con el mismo código de C-3 (los valores de K = 9, 12 y 15 de la sección 3 eran indicativos). La **lista de rasgos es la congelada de C-1** (los 65 de `salidas/fw5/c_mapa.csv`), no se vuelve a seleccionar con la confiabilidad de X6. Lo mismo calculado sobre fw5 se reporta como sensibilidad.
2. **Candidatos de P4 (Arturo: "recortado al 19-jul").** Son las mismas 61 etapas del ranking de C-1 (`c_ranking_america.csv`) más Almada en Pachuca (62). El perfil de cada candidato usa **solo sus partidos anteriores al 2026-07-19**, con la misma función de perfil de C-1/C-3 (`perfil_club`, contraído con su n). Así se cumple "terminada antes del inicio de Almada" aunque el técnico siga dirigiendo en 2026/27.
3. **R8p en X6 (Arturo: "centroides congelados").** R8u necesita los playbooks de R8p, que la sección 4 no listaba. En X6 se calculan las mismas huellas 360 de R8p-1 y cada córner se asigna al playbook más cercano de los **centroides de fw5** (`salidas/fw5/r8p_km_ofensivo.csv` y `r8p_km_defensivo.csv`); no se vuelve a agrupar. Validación: los córners de 2021/22-2025/26 conservan su etiqueta al 100%.
4. **Prueba de reproducción de V-1 (paso 5).** Antes de evaluar a Almada, V-1 corre sobre fw5 y debe reproducir **las 27 llegadas de `c_ensayo_llegadas.csv` con K = 9, 12 y 15** (cambio con K partidos, percentil y puesto de identificación; diferencia ≈ 0). Si no reproduce, no se evalúa.
5. **Cambios de ruta en X6.** Las celdas R8a-1, R8p-1, R8z-1 y R8u-0 tienen la raíz de Drive escrita en el código. En X6 se usan copias en las que **solo cambia la línea de la raíz** (apunta a la carpeta espejo) y, en R8p, la asignación por centroides congelados (punto 3). Ninguna otra línea cambia.

## Aclaración 2 · 2026-10-20, 13:30 (America/Mexico_City) · corrección de conteo, antes de correr V-1 y de ver cualquier perfil de 2026/27

- El ranking de C-1 (`c_ranking_america.csv`) tiene **61 filas y ya incluye a Almada en Pachuca** (fue el puesto 61 de 61). Por lo tanto, los candidatos de P4 de la Aclaración 1, punto 2, son esas **61 etapas** (Almada en Pachuca y 60 técnicos más), no 62. El "puesto ≤ 6 de 62" de la sección 3 era una ilustración; la regla que decide es **percentil ≥ 90** (con 60 técnicos de comparación: como máximo 6 más parecidos que Almada, es decir, puesto ≤ 7 de 61). La regla no cambia.

## Resultado · 2026-10-20, 16:47 (America/Mexico_City) · V-1 v1.0, lectura literal (E-16)

**Controles previos (todos cumplidos):**
- Re-descarga con corte 2026-10-19: **K = 11** partidos de Almada (2026-07-19 a 2026-10-18); 10 con 360 (el del 11-oct no tiene). E-1 a E-5: reproducción idéntica de lo existente.
- X6 (X6-9): tramos de 2021/22 a 2025/26 idénticos a fw5 en los ocho bloques (100%) · perfiles de las 124 etapas con los mismos partidos: correlación mínima **0.9998** en los 65 rasgos (umbral 0.99) · confiabilidad: cambio máximo 0.026; ningún rasgo bajaría de 0.5.
- V-1 reproduce C-3 sobre fw5: 27 llegadas, 78 filas, diferencia máxima 1.4e-14.
- Definiciones verificadas: zt = Pachuca · 2 (139 partidos) · zc = últimos 18 partidos de América hasta 2026-05-11.
- Cambios de zt y zc (X6 − fw5) en los 32 rasgos de P2-P4: máximo 0.060 z (Almada) y 0.025 z (América). **Ninguno supera 0.1 z: nada que reportar.**

| Id | Valor | Umbral | Resultado |
|---|---|---|---|
| **P1** | distancia 1.188 z | > 1.041 (p75 del ensayo con K = 11, X6) | **Cumple** |
| **P2** | cobertura 0.94 (defensores en el área en córner) y 1.06 (zonales) | ≥ 0.5 en los dos | **Cumple** |
| **P3** | cobertura 0.47 (segundos hasta el último tercio) | < 0.5 | **Cumple** (por poco) |
| **P4** | percentil 100: **puesto 1 de 61** | percentil ≥ 90 | **Cumple** |

**Detalle en unidades naturales (América antes → América con Almada · Almada en Pachuca · liga):**
- Defensores en el área en córner en contra: 8.76 → **6.81** · 6.69 · 8.51 (umbral natural del preregistro: ≤ 7.71).
- Defensores zonales en córner en contra: 3.78 → **2.40** · 2.48 · 4.03 (umbral natural: ≤ 3.13).
- Segundos hasta el último tercio: 13.44 → **11.86** · 10.10 · 11.70 (umbral natural: por encima de 11.75).

**P4, detalle:** 32 rasgos (reloj ≤ 20 y peso > 0). Distancia de Almada en Pachuca 0.542; siguientes: Esteban Solari (Pachuca · 4) 0.804, Pablo Repetto (Santos · 4) 0.881, Marcos Ambriz (León · 7) 0.893. Siete candidatos recortados al 19-jul. En el ensayo con K = 11, el técnico real quedó en el 10% más parecido en 37% de las llegadas (percentil mediano 85).

**Sensibilidad fw5** (pesos, umbral, zt y zc de fw5; zn de X6): P1 1.186 > 1.045 · P2 0.94 y 1.06 · P3 0.47 → **mismo veredicto en P1-P3.**

**Lectura (reglas del anexo de la sesión 13):**
- Cada predicción se reporta por separado; no hay calificación conjunta.
- Es **un caso con 11 partidos** (10 para los rasgos 360): una demostración en vivo. La validación del método siguen siendo las 27 llegadas.
- P3 se cumple por un margen pequeño (0.47 frente a 0.5): se dice así.
- En P4, dos de los vecinos más cercanos son técnicos posteriores de Pachuca (Solari, Lozano). Es coherente con que el club conserve parte del legado de Almada, pero Almada queda claramente primero (0.54 frente a 0.80).

**Incidente sin efecto (registrado):** la versión de R7u-0 del cuaderno de Arturo (v1.0 con un ajuste local de ruta) reescribió `fw5/r7u_tramos.parquet` con los mismos insumos de fw5. X6-9 muestra que fw5/r7u_tramos y la recalculación de X6 son idénticos al 100% en los partidos previos, así que el contenido de fw5 no cambió. La corrida válida de X6 usó la R7u-0 v1.1 del proyecto.
