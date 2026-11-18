# patch_v2_1.py · sesión 25 (18-nov-2026)
# Agrega xShift y xRead al reporte v2 publicado (reporte/index.html, commit d0faf8c).
# Uso: python3 patch_v2_1.py entrada.html salida.html
# No toca DATA: xShift y xRead se calculan en el navegador con los perfiles ya incrustados
# (e.cad: zc, zt, zn por rasgo) y el reloj de cada rasgo (r.reloj = xRead).
# Almada en el América usa los 10 valores del anexo A2 del deck v3 (versión X6 de la prueba en vivo).
import sys, re

src, dst = sys.argv[1], sys.argv[2]
h = open(src, encoding='utf-8').read()
assert 'const DATA = ' in h and 'xShift' not in h, 'entrada inesperada (¿ya parcheada?)'

def rep(old, new, n=1):
    global h
    c = h.count(old)
    assert c == n, f'se esperaban {n} apariciones y hay {c}: {old[:80]!r}'
    h = h.replace(old, new)

# ---------------------------------------------------------------- 1. CSS
CSS = r"""
/* v2.1 · xShift y xRead */
.xm{padding:20px 0 22px;border-bottom:1px solid var(--rule)}
.xm-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr) minmax(0,1.35fr);gap:0 26px;margin-top:10px}
.xm-card{display:grid;gap:6px;align-content:start}
.xm-card h3{font-size:1.9rem;font-weight:800;letter-spacing:-.01em;color:var(--club-am)}
.xm-card p{font-size:.95rem}
.xm-card .uso{font-size:.8rem;color:var(--ink-2)}
.xm-rap{grid-column:3;grid-row:1 / span 2;border-left:1px solid var(--rule);padding-left:22px;display:grid;gap:8px;align-content:start}
.xm-rap h4{margin:0;font-size:.82rem;font-weight:600;color:var(--ink-2)}
.xm-cmp{grid-column:1 / span 2;grid-row:2;margin-top:18px;padding-top:14px;border-top:1px solid var(--rule);display:grid;gap:10px;align-content:start}
.xm-cmp label{display:grid;gap:4px;max-width:520px}
.xm-grid>*{min-width:0}
.xm-cmp label .sel-et{width:100%}
.xm-sig>span:last-child{flex:1;min-width:0}
.xm-quien{font-size:1.35rem;font-weight:800;letter-spacing:-.01em;line-height:1.1}
.xm-quien small{display:block;font-size:.85rem;font-weight:500;color:var(--ink-2);margin-top:3px}
.xm-par{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);gap:10px;align-items:stretch}
.xm-caja{border:1px solid var(--rule);padding:9px 11px;display:grid;gap:2px;align-content:start;font-size:.86rem}
.xm-caja.t{border-color:var(--club-am);border-width:2px}
.xm-caja .et{font-size:.72rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--ink-2)}
.xm-caja b{font-size:1rem}
.xm-caja span{color:var(--ink-2)}
.xm-menos{align-self:center;text-align:center;font-size:.78rem;color:var(--ink-2);line-height:1.2}
.xm-menos b{display:block;font-size:1.3rem;color:var(--ink)}
.xm-sig{display:flex;gap:8px;align-items:flex-start;font-size:.88rem;font-weight:600;color:var(--ink);max-width:none}
.xm-sig .fd,.xm-sig .fm{font-size:1.5rem;line-height:1;color:var(--club-am)}
.xm-sig .fm,.xm-sig .tm{display:none}
.xm-rap h4{color:var(--club-am)!important}

.xm-rap label{display:grid;gap:4px}
.xm-rap .ver-btn{justify-self:start}
@media (max-width:920px){.xm-sig .fd,.xm-sig .td{display:none}.xm-sig .fm,.xm-sig .tm{display:inline}.xm-grid{grid-template-columns:minmax(0,1fr);gap:16px}.xm-cmp,.xm-rap{grid-column:1;grid-row:auto}.xm-rap{border-left:0;padding-left:0;border-top:0;padding-top:0}.xm-par{grid-template-columns:minmax(0,1fr)}.xm-menos b{display:inline}}
.xs-t{display:grid;margin-top:10px}
.xs-f{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,.8fr) minmax(0,.9fr) minmax(0,.8fr);gap:8px;padding:6px 0;border-bottom:1px solid var(--rule);font-size:.85rem;align-items:baseline}
.xs-f small{display:block;color:var(--ink-2);font-size:.76rem}
.xs-f.cab{font-weight:600;color:var(--ink-2);border-bottom:2px solid var(--rule-2);font-size:.76rem;padding-top:0}
.xs-f .xs-v{font-weight:700;font-variant-numeric:tabular-nums}
.xs-f.poco{color:var(--ink-2)} .xs-f.poco .xs-v{font-weight:500}
.xm-rap .xs-f{grid-template-columns:minmax(0,1.8fr) minmax(0,.9fr) minmax(0,.7fr)}
.xs-ok{color:var(--ok);font-weight:600} .xs-no{color:var(--ink-3)}
.xs-pl{font-size:.82rem;margin-top:10px;line-height:1.9}
.xs-pl .chip{margin-right:4px}
.xs-svg{width:100%;max-width:780px;height:auto;display:block;margin-top:8px}
.xs-d #xs{padding:10px 0 4px}
.alm-xs{margin-top:30px;padding-top:18px;border-top:2px solid var(--rule-2);display:grid;gap:6px}
"""
i = h.find('</style>', h.find('/* Concepto:'))
assert i > 0
h = h[:i] + CSS + h[i:]

# ---------------------------------------------------------------- 2. HTML
rep('<div class="hall" id="hallazgos"></div>',
    '<div class="xm" id="xmetricas"></div>\n  <div class="hall" id="hallazgos"></div>')
rep('<details class="trajo-d" id="trajo-d"><summary id="trajo-s">Qué trajo, rasgo por rasgo</summary><div class="trajo" id="trajo"></div></details>',
    '<details class="trajo-d xs-d" id="xs-d" open><summary id="xs-s">xShift y xRead de esta etapa</summary><div id="xs"></div></details>\n'
    '  <details class="trajo-d" id="trajo-d"><summary id="trajo-s">Qué trajo, rasgo por rasgo</summary><div class="trajo" id="trajo"></div></details>')
rep('<div class="alm-lectura" id="alm-lectura"></div>',
    '<div class="alm-lectura" id="alm-lectura"></div>\n  <div class="alm-xs" id="alm-xs"></div>')

# Cómo lo medimos: grupo nuevo al inicio y renumeración del resto
h, k = re.subn(r'(<details class="grupo" id="g-[a-z]+"><summary><h3>)(\d+)\.',
               lambda m: m.group(1) + str(int(m.group(2)) + 1) + '.', h)
assert k == 10, k
GX = """<details class="grupo" id="g-x"><summary><h3>1. xShift y xRead: las dos métricas propias</h3><span class="cuenta">2 métricas</span></summary><div class="objetos">
     <div><b>xShift: qué es</b><span class="gris">La brecha completa entre el perfil del técnico y el del club, en cada rasgo que viaja con él: hacia dónde y cuánto jala. Perfil del técnico: su etapa anterior de 15 partidos o más en otro club, ajustada por contexto y contraída (a una etapa corta se le cree menos). Perfil del club: sus últimos 18 partidos antes del relevo (mínimo 10). xShift = técnico − club, calculado en desviaciones y mostrado en la unidad del rasgo.</span></div>
     <div><b>xShift: qué no es</b><span class="gris">No dice cuánto de esa brecha va a llegar ni si el técnico es bueno. Cuánto llega se mide aparte, con el recorrido: a los 12 partidos, el equipo recorre en promedio 53% de la brecha en lo que trae el técnico y 29% en lo del plantel (27 llegadas). Al terminar la etapa, 52% de los equipos quedó más cerca del técnico nuevo que de su club anterior; al azar serían 26%.</span></div>
     <div><b>xShift: cuándo se usa</b><span class="gris">Antes de contratar (qué compras), cuando el rival estrena técnico (qué preparar) y con el técnico actual: junto al recorrido, dice qué parte de su idea ya llegó. Existe cuando el técnico tuvo una etapa previa en la liga y hay datos del club antes de su llegada: 24 de las 87 etapas. Una brecha menor a media desviación se marca como "jala poco": con menos, cualquier movimiento se confunde con el ruido.</span></div>
     <div><b>xRead: qué es</b><span class="gris">Partidos que necesita un rasgo para medirse con confianza (confiabilidad 0.7): desde qué partido los números separan la idea del técnico del azar de cada partido. xRead = 2.33 × σ² ÷ τ². σ²: cuánto brinca el rasgo de un partido a otro (rival y partido). τ²: cuánto difieren de verdad los técnicos entre sí (señal). 2.33 = 0.7 ÷ 0.3.</span></div>
     <div><b>xRead: cómo se estima</b><span class="gris">Cada etapa se parte en dos mitades al azar: lo que comparten es señal; lo que las separa, ruido. El intervalo usa 500 remuestreos de etapas sobre 50 repartos. Se calcula para la diferencia típica entre técnicos: uno extremo se lee antes. Con n partidos, confiabilidad = 1 ÷ (1 + 0.43 × xRead ÷ n): llega a 0.7 justo cuando n = xRead.</span></div>
     <div><b>xRead: el corte</b><span class="gris">0.7 es el estándar de la psicometría. Con otro corte, todos los xRead se escalan igual y su orden no cambia: con 0.6, × 0.64 (intensidad de presión: 13 partidos); con 0.8, × 1.71 (36).</span></div>
     <div><b>De dónde vienen</b><span class="gris">xShift sale del eje "viaja con el técnico", que sigue a los directivos que cambian de empresa (Bertrand y Schoar, 2003). xRead sale de la psicometría: la confiabilidad de una medida y cuántas observaciones necesita (Spearman-Brown).</span></div>
     <div><b>Siguiente paso: xShift+</b><span class="gris">Brecha × cobertura esperada según la duración de la etapa: cuánto va a llegar, no solo hacia dónde. Hoy solo existe el promedio (53% a los 12 partidos en lo que trae el técnico).</span></div>
    </div></details>
    """
rep('<details class="grupo" id="g-cob">', GX + '<details class="grupo" id="g-cob">')
rep('<span class="cuenta">8 existentes · 12 propias</span>', '<span class="cuenta">8 existentes · 13 propias</span>')
rep('<span class="cuenta">18 términos</span>', '<span class="cuenta">19 términos</span>')

# ---------------------------------------------------------------- 3. "reloj" -> xRead en el texto visible
rep('(su reloj)', '(su xRead)', 2)
rep('<h3>Reloj de medición: cuándo los números alcanzan a la idea</h3>', '<h3>xRead: desde qué partido se puede medir cada rasgo</h3>')
rep('<h3>Reloj de implantación: cuándo la idea llega al campo</h3>', '<h3>Implantación: cuándo la idea llega al campo</h3>')
rep('antes de su reloj, los números', 'antes de su xRead, los números')
rep('Antes de su reloj, el analista', 'Antes de su xRead, el analista')
rep('el reloj de cada rasgo.', 'el xRead de cada rasgo.')
rep('<th>Reloj</th>', '<th>xRead</th>')
rep('aritmética del reloj,', 'aritmética del xRead,')
rep('con su reloj.', 'con su xRead.')
rep("reloj de medición e implantación','Todos (O-1 a O-12), confiabilidad, reloj de medición, prueba de mitades'",
    "xRead e implantación','Todos (O-1 a O-12), confiabilidad, xRead, prueba de mitades'")
rep("'confiabilidad, relojes, firmeza'", "'confiabilidad, xRead, firmeza'")
rep("Ocho métricas que ya existían y doce propias", "Ocho métricas que ya existían y trece propias")
rep("${n} partidos; ${k==='ok'?'le bastan':'necesita'} ${r.reloj}", "${n} partidos; xRead ${r.reloj}")
rep("['Reloj de medición','Partidos que necesita un rasgo para llegar a confiabilidad 0.7.']",
    "['xShift','Brecha técnico-club en cada rasgo que viaja con él: hacia dónde y cuánto jala.'],['xRead','Partidos que necesita un rasgo para llegar a confiabilidad 0.7: desde cuándo se puede medir.']")
rep("const MET_PR=[['Dueño del rasgo'",
    "const MET_PR=[['xShift','Brecha técnico-club en cada rasgo que viaja con él: hacia dónde y cuánto jala.','g-x'],['Dueño del rasgo'")
rep("['Reloj de medición','Partidos para que un rasgo se lea (confiabilidad 0.7).','#dueno'],\n ['Reloj de implantación',",
    "['xRead','Partidos para que un rasgo se lea (confiabilidad 0.7).','g-x'],\n ['Implantación',")

# mayúscula inicial automática de las etiquetas: no aplica a xShift ni xRead
rep("/^[^A-Za-z]*(xG|yd|vs\\.)/.test(t)", "/^[^A-Za-z]*(xG|yd|vs\\.|xShift|xRead)/.test(t)")

# "Qué trajo" (v2): el punto de partida es la ventana del club, no siempre un solo técnico
rep("}: con ${ant} ${vv(o.r,o.c)}", "}: ${xsCon(e)} ${vv(o.r,o.c)}")
rep("entre el ${e.club} de ${ant} (0%)", "entre el ${e.club} ${xsDe(e)} (0%)")
rep("y el ${e.club} de ${ant} jugaban", "y el ${e.club} ${xsDe(e)} jugaban")
rep("como con ${ant} ·", "como ${xsCon(e)} ·")

# ---------------------------------------------------------------- 4. KPIs
rep("function pintarKPI(){const K=[\n",
    "function pintarKPI(){const K=[\n"
    "  ['xShift por rasgo','unidad del rasgo','Al firmar al técnico, cuando el rival estrena técnico o para evaluar al actual','Analistas y cuerpo técnico','Hacia dónde y cuánto jala el técnico al equipo en cada rasgo que viaja con él. Junto al recorrido, dice qué parte de su idea ya llegó.','xmetricas'],\n"
    "  ['xRead por rasgo','partidos','Antes de evaluar cualquier rasgo','Analistas','Desde qué partido se puede medir cada rasgo con confianza. Antes de su xRead, los números no distinguen la idea del azar.','relojes'],\n")

# ---------------------------------------------------------------- 5. irRetrato abre el panel nuevo
rep("todo();if(cfg.ir==='#trajo-d')document.getElementById('trajo-d').open=true;",
    "todo();if(cfg.ir==='#trajo-d')document.getElementById('trajo-d').open=true;if(cfg.ir==='#xs-d')document.getElementById('xs-d').open=true;")

# ---------------------------------------------------------------- 6. JS nuevo
JS = r"""
/* ---------- v2.1 · xShift y xRead ---------- */
const XS_ALM=[['r7u:inicio_linea_3_5',-15],['r8:zonales',-1.3],['r8:def_area_360',-2.1],['r7c:altura_laterales',-3.8],['r8:pct_marca',4.5],
  ['r8:pegados_portero',-0.02],['r4:intensidad_ppda',1.0],['r7c:libertad_posicional',-1.6],['r7u:cambio_familia_90',-0.13],['r8:envio_segundo_palo',-10]];
const XS_U={'%':'pts','pts':'pts','jug.':'jug.','yd':'yd','por 90':'por 90','acciones por 100 pases rivales':''};
const xsCap=s=>s?s[0].toUpperCase()+s.slice(1):s, xsNom=r=>xsCap(r.corto||r.nombre);
function xsTxt(r,nat){const a=Math.abs(nat),d=a>=10?0:a<.2?2:1,u=XS_U[r.unidad]!=null?XS_U[r.unidad]:uTxt(r);return sg(nat,d)+(u?' '+u:'')}
function xsDir(o){return o.r.pal?o.r.pal[o.z>=0?0:1]:(o.z>=0?'sube':'baja')}
function xsEtapa(k){const e=E[k];if(!e||!e.previa||!e.antecesor||!e.cad)return null;const L=[];
  for(const r of DATA.rasgos){if(r.dueno!=='V'||!r.legible)continue;const v=e.cad[r.id];if(!v||v.zt==null||v.zc==null)continue;
    const z=v.zt-v.zc;L.push({id:r.id,r,z,nat:z*r.tau,xr:r.reloj,cob:(v.zn!=null&&Math.abs(z)>=.5)?(v.zn-v.zc)/z:null})}
  return L.length?L.sort((a,b)=>Math.abs(b.z)-Math.abs(a.z)):null}
function xsAlmada(){const A=DATA.almada,cb={};((A&&A.rasgos)||[]).forEach(x=>{cb[x.rasgo]=x.cob});
  return XS_ALM.filter(([id])=>R[id]).map(([id,nat])=>{const r=R[id];return {id,r,z:nat/r.tau,nat,xr:r.reloj,cob:cb[id]!=null?cb[id]:null}}).sort((a,b)=>Math.abs(b.z)-Math.abs(a.z))}
const XS_ET=Object.keys(E).filter(k=>xsEtapa(k)).sort((a,b)=>corto(E[a].tecnico).localeCompare(corto(E[b].tecnico),'es')||E[a].desde.localeCompare(E[b].desde));
function xsMapa(L,n,etq){const W=640,H=330,ml=40,mr=14,mt=40,mb=40,X=45,ymax=Math.max(2.5,Math.min(4.6,d3.max(L,o=>Math.abs(o.z))*1.1));
  const x=d3.scaleLinear([0,X],[ml,W-mr]).clamp(true),y=d3.scaleLinear([0,ymax],[H-mb,mt]).clamp(true);
  let g=`<rect x="${ml}" y="${y(.5)}" width="${W-mr-ml}" height="${y(0)-y(.5)}" fill="var(--rule)" opacity=".6"/>
   <text x="${ml+6}" y="${y(.5)+12}" font-size="9.5" fill="var(--ink-2)">jala poco: menos de media desviación</text>
   <line x1="${x(17)}" x2="${x(17)}" y1="${mt-22}" y2="${H-mb}" stroke="var(--ink-3)" stroke-dasharray="3 3"/>
   <text x="${ml+2}" y="${mt-26}" font-size="10.5" font-weight="700" fill="var(--ink)">Prepáralo desde el lunes</text>
   <text x="${ml+2}" y="${mt-13}" font-size="9.5" fill="var(--ink-2)">se mide en un torneo o menos (17 partidos)</text>
   <text x="${x(17)+6}" y="${mt-26}" font-size="10.5" font-weight="700" fill="var(--ink)">Decide el criterio</text>
   <text x="${x(17)+6}" y="${mt-13}" font-size="9.5" fill="var(--ink-2)">los números tardan más de un torneo</text>`;
  if(n){const xn=x(Math.min(n,X)),der=xn>W-150;g+=`<line x1="${xn}" x2="${xn}" y1="${mt-4}" y2="${H-mb}" stroke="var(--club-am)" stroke-width="1.6"/>
   <text x="${xn+(der?-5:5)}" y="${H-mb-6}" text-anchor="${der?'end':'start'}" font-size="9.5" font-weight="700" fill="var(--club-am)">${etq||'esta etapa'}: ${n} partidos${n>X?' →':''}</text>`}
  g+=[0,10,20,30,40].map(t=>`<text x="${x(t)}" y="${H-mb+14}" text-anchor="middle" font-size="9.5" fill="var(--ink-3)">${t}</text>`).join('')
   +d3.range(0,Math.floor(ymax)+1).map(t=>`<text x="${ml-6}" y="${y(t)+3}" text-anchor="end" font-size="9.5" fill="var(--ink-3)">${t}</text>`).join('')
   +`<line x1="${ml}" x2="${W-mr}" y1="${y(0)}" y2="${y(0)}" stroke="var(--ink-3)"/>
   <text x="${W-mr}" y="${H-6}" text-anchor="end" font-size="10" fill="var(--ink-2)">xRead: partidos para medirlo →</text>
   <text x="11" y="${(mt+H-mb)/2}" font-size="10" fill="var(--ink-2)" transform="rotate(-90 11 ${(mt+H-mb)/2})" text-anchor="middle">jala más (xShift en desviaciones) →</text>`;
  const pts=L.map(o=>({o,px:x(o.xr),py:y(Math.abs(o.z))})).sort((a,b)=>a.py-b.py);
  const cajas=pts.map(p=>[p.px-6,p.py-6,12,12]).concat([[ml,mt-36,W-mr-ml,26],[ml+4,y(.5)+2,185,12]]);if(n){const xn=x(Math.min(n,X)),wl=150;cajas.push([xn>W-150?xn-wl-5:xn+3,H-mb-16,wl,12])}
  for(const p of pts){const fuerte=Math.abs(p.o.z)>=.5,up=p.o.z>=0;
    g+=`<path d="${up?`M${p.px},${p.py-5.5}L${p.px+5},${p.py+3.5}L${p.px-5},${p.py+3.5}Z`:`M${p.px},${p.py+5.5}L${p.px+5},${p.py-3.5}L${p.px-5},${p.py-3.5}Z`}" fill="${fuerte?'var(--club-am)':'var(--ghost)'}"><title>${xsNom(p.o.r)}: xShift ${xsTxt(p.o.r,p.o.nat)} (${xsDir(p.o)}), xRead ${p.o.xr}</title></path>`}
  for(const p of pts){if(Math.abs(p.o.z)<.5)continue;const t=`${xsNom(p.o.r)} ${xsTxt(p.o.r,p.o.nat)}`,w=t.length*5.15+4;
    const pref=p.px+w+9>W-mr?-1:1;let hecho=false;
    for(const lado of [pref,-pref]){if(hecho)break;for(const dy of [0,-11,11,-22,22,-33,33]){const lx=lado>0?p.px+8:p.px-8-w,by=p.py+3.5+dy;const bx=[lx,by-9,w,11];
      if(lx<ml||lx+w>W-mr||by>H-mb-2)continue;
      if(cajas.some(c=>bx[0]<c[0]+c[2]&&bx[0]+bx[2]>c[0]&&bx[1]<c[1]+c[3]&&bx[1]+bx[3]>c[1]))continue;
      cajas.push(bx);hecho=true;
      g+=`${dy?`<line x1="${p.px+(lado>0?4:-4)}" y1="${p.py}" x2="${lado>0?lx-1:lx+w+1}" y2="${by-3}" stroke="var(--ink-3)" stroke-width=".6"/>`:''}<text x="${lado>0?lx:lx+w}" y="${by}" text-anchor="${lado>0?'start':'end'}" font-size="10" fill="var(--ink)" font-weight="600">${t}</text>`;break}}}
  return `<svg class="xs-svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="Rasgos que viajan con el técnico según cuánto jalan (xShift) y desde qué partido se miden (xRead)">${g}</svg>
   <p class="chico gris">Triángulo hacia arriba: el técnico sube ese rasgo frente al club; hacia abajo: lo baja. En gris y sin etiqueta, los que jalan poco (están en la tabla). Pasa el cursor sobre un triángulo para ver el detalle.</p>`}
function xsTabla(L,n,cob,max){const F=(max?L.filter(o=>Math.abs(o.z)>=.5).slice(0,max):L);
  const cab=`<div class="xs-f cab"><span>Rasgo que viaja con el técnico</span><span>xShift</span><span>xRead</span>${cob?'<span>Recorrido</span>':''}</div>`;
  return `<div class="xs-t">${cab}${F.map(o=>`<div class="xs-f${Math.abs(o.z)<.5?' poco':''}"><span>${xsNom(o.r)}<small>${Math.abs(o.z)<.5?'jala poco':xsCap(xsDir(o))}</small></span><span class="xs-v">${xsTxt(o.r,o.nat)}</span><span>${o.xr} partidos${n?(n>=o.xr?'<small class="xs-ok">ya se mide</small>':'<small class="xs-no">todavía no</small>'):''}</span>${cob?`<span>${o.cob==null?'<small>—</small>':pctR(o.cob)}</span>`:''}</div>`).join('')}</div>`}
function xsPlantel(){const P=DATA.rasgos.filter(r=>r.dueno==='P'&&r.legible).sort((a,b)=>a.reloj-b.reloj);
  return `<p class="xs-pl"><b>Del plantel: explótalo o cúbrelo.</b> <span class="gris">No viajan con el técnico (xShift ≈ 0): los mueve quién juega. Con su xRead:</span> ${P.map(r=>`<span class="chip">${xsNom(r)} <i>${r.reloj}</i></span>`).join('')}</p>`}
function xsVentana(e){const p=e.ant_part||0,ini=e.desde<'2022-07';return {n:ini?Math.min(18,p):18,p,solo:ini||p>=18,ini,int:e.ant_rol==='interino'}}
const xsDe=e=>xsVentana(e).solo?`de ${corto(e.antecesor)}`:'antes de su llegada';
const xsCon=e=>xsVentana(e).solo?`con ${corto(e.antecesor)}`:'antes de su llegada';
function xsVentTxt(e){const v=xsVentana(e),a=corto(e.antecesor);
  return v.solo?`Sus últimos ${v.n} partidos antes de la llegada, todos con ${a}${v.ini?' (los datos empiezan en el Apertura 2021)':''}`
    :`Sus últimos 18 partidos antes de la llegada: ${v.p} con ${a}${v.int?' (interino)':''} y ${18-v.p} con el técnico anterior a él`}
const XS_MES=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
const xsPer=v=>v&&v.desde?(v.desde.slice(0,4)===v.hasta.slice(0,4)?v.desde.slice(0,4):`${v.desde.slice(0,4)} a ${v.hasta.slice(0,4)}`):'';
const xsMes=f=>f?`${XS_MES[+f.slice(5,7)-1]} de ${f.slice(0,4)}`:'';
function xsQuien(k){if(k==='alm'){const a=E['Pachuca · 2'];return {tec:'Guillermo Almada',club:'América',per:'Apertura 2026',n:11,
    t:{club:'Pachuca',per:xsPer(a),n:a.partidos},c:{tit:'El América de André Jardine',det:'Sus últimos 18 partidos antes de la llegada, todos con Jardine (hasta mayo de 2026)'}}}
  const e=E[k],p=E[e.previa]||{};return {tec:corto(e.tecnico),club:e.club,per:xsPer(e),n:e.partidos,
    t:{club:clubDe(e.previa),per:xsPer(p),n:p.partidos},c:{tit:`El ${e.club} ${xsDe(e)}`,det:`${xsVentTxt(e)} (hasta ${xsMes(e.desde)})`}}}
function pintarXM(){const el=document.getElementById('xmetricas');if(!el)return;
  const ops=[['alm','Guillermo Almada · América (prueba en vivo, 2026)'],...XS_ET.map(k=>[k,`${corto(E[k].tecnico)} · ${E[k].club} (${xsPer(E[k])})`])];
  el.innerHTML=`<span class="eyebrow">Dos métricas nuevas</span>
   <div class="xm-grid">
    <div class="xm-card"><h3>xShift</h3><p>Hacia dónde y cuánto jala un técnico al equipo, rasgo por rasgo: la brecha entre su equipo anterior y el club, en lo que viaja con él.</p>
     <span class="uso">Sirve antes de contratar, para preparar al rival que cambia de técnico y para evaluar al técnico actual: cuánto de esa brecha ya recorrió el equipo.</span></div>
    <div class="xm-card"><h3>xRead</h3><p>Desde qué partido se puede medir con confianza cada rasgo. Antes, los números no separan la idea del técnico del azar de cada partido.</p>
     <span class="uso">Sirve para saber qué ya se puede evaluar, de un técnico propio o de un rival, y qué todavía no.</span></div>
    <div class="xm-cmp"><label class="chico"><b>Elige una llegada de técnico</b><select class="sel-et" id="xm-sel">${ops.map(([k,t])=>`<option value="${k}">${t}</option>`).join('')}</select></label>
     <div id="xm-quien"></div></div>
    <div class="xm-rap"><h4 id="xm-tit"></h4><div id="xm-lista"></div><button type="button" class="ver-btn" id="xm-ir">Ver su ficha completa →</button></div>
   </div>`;
  const sel=document.getElementById('xm-sel');
  const pinta=()=>{const k=sel.value,L=k==='alm'?xsAlmada():xsEtapa(k),m=L.filter(o=>Math.abs(o.z)>=.5).length,q=xsQuien(k);
    document.getElementById('xm-quien').innerHTML=`<div class="xm-quien">${q.tec} llega al ${q.club}<small>Etapa que se evalúa: ${q.club}, ${q.per}, ${q.n} partidos</small></div>
     <div class="xm-par">
      <div class="xm-caja t"><span class="et">Lo que trae</span><b>Su ${q.t.club}</b><span>Su etapa anterior: ${q.t.per}, ${q.t.n} partidos</span></div>
      <div class="xm-menos"><b>−</b>xShift = lo que trae menos lo que encuentra</div>
      <div class="xm-caja"><span class="et">Lo que encuentra</span><b>${q.c.tit}</b><span>${q.c.det}</span></div>
     </div>
     <p class="xm-sig"><span class="fd">→</span><span class="fm">↓</span> <span>El resultado, rasgo por rasgo, está en la tabla <span class="td">de la derecha</span><span class="tm">de abajo</span>: cuánto jala en cada rasgo (xShift) y desde qué partido se puede medir (xRead). Solo cuentan los rasgos que viajan con el técnico.</span></p>`;
    document.getElementById('xm-tit').textContent=`Resultado: lo que más jala ${q.tec} al ${q.club}`;
    document.getElementById('xm-lista').innerHTML=xsTabla(L,0,false,6)+`<p class="chico gris" style="margin-top:6px">${m>6?`Los 6 que más jalan, de ${m} con al menos media desviación.`:`${m} de ${L.length} rasgos jalan al menos media desviación.`}</p>`;
    document.getElementById('xm-ir').textContent=k==='alm'?'Ver la prueba en vivo →':'Ver su ficha completa →'};
  sel.onchange=pinta;pinta();
  document.getElementById('xm-ir').onclick=()=>{const k=sel.value;if(k==='alm'){document.getElementById('alm-xs').scrollIntoView({behavior:'smooth',block:'start'});return}
    irRetrato({grupo:E[k].grupo,etapa:k,capa:'sin',ir:'#xs-d'})}}
function pintarXS(){const T=document.getElementById('xs');if(!T)return;const e=E[st.etapa],L=xsEtapa(st.etapa),prev=e.previa?clubDe(e.previa):null;
  document.getElementById('xs-s').textContent=L?`xShift y xRead: qué jala ${corto(e.tecnico)} desde su ${prev}`:'xShift y xRead de esta etapa';
  if(!L){T.innerHTML=`<p class="chico gris">${!e.previa?'Sin una etapa previa de 15 partidos o más dentro de la liga, no hay contra qué medir la brecha: esta etapa no tiene xShift (se resolvería con más ligas).':'No hay partidos del club antes de su llegada dentro de los datos: esta etapa no tiene xShift.'} El xRead de cada rasgo sí aplica: está junto a cada rasgo de la ficha.</p>`;return}
  T.innerHTML=`<p class="chico gris">xShift: la brecha entre su ${prev} y el ${e.club} ${xsDe(e)} en los ${L.length} rasgos que viajan con el técnico. Lo que encuentra: ${xsVentTxt(e).replace(/^Sus/,'sus')}. xRead: partidos para medir cada uno. Recorrido: cuánto de esa brecha cubrió el equipo en esta etapa (solo donde la brecha es de media desviación o más).</p>
   ${xsMapa(L,e.partidos)}${xsTabla(L,e.partidos,true)}${xsPlantel()}`}
function pintarAlmXS(){const el=document.getElementById('alm-xs');if(!el)return;const L=xsAlmada();
  el.innerHTML=`<h3>El mapa de Almada en el América: xShift y xRead</h3>
   <p class="chico gris">Hacia dónde y cuánto jala Almada al América (su Pachuca frente a los últimos 18 partidos con Jardine) y desde qué partido se puede medir cada rasgo. La línea de color marca los 11 partidos evaluados. Cálculo con la versión de la prueba en vivo, que suma el Apertura 2026.</p>
   ${xsMapa(L,11,'evaluados')}${xsTabla(L,11,true)}
   <p class="chico gris">Son los 10 rasgos que viajan con el técnico dentro de la herramienta congelada en el preregistro. Los otros 5 (organización defensiva 360 y huella defensiva por rol) se sumaron después y no tienen xShift de Almada. El recorrido solo se evaluó en los dos rasgos de la predicción P2.</p>
   ${xsPlantel()}`}
"""
rep("function todo(){if(!todo.una){pintarHistoria();pintarResumen();",
    JS + "\nfunction todo(){if(!todo.una){pintarXM();pintarAlmXS();pintarHistoria();pintarResumen();")
rep("pintarCadena();pintarCuanto();", "pintarCadena();pintarXS();pintarCuanto();")

open(dst, 'w', encoding='utf-8').write(h)
left = [m.start() for m in re.finditer(r'[Rr]eloj de (medición|implantación)', h)]
print('ok', len(h), 'restos "reloj de medición/implantación":', len(left))
