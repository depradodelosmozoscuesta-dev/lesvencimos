#!/usr/bin/env python3
"""Generate Hogar, Salud, Radio, QR, Electricidad modules + zips."""
from __future__ import annotations
import json, shutil, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "modulos"
DL = ROOT / "downloads"

CSS = """
:root{
  --fondo:#0E0E0C; --fondo-2:#161512; --fondo-3:#1C1A16;
  --tinta:#E6E1D6; --suave:#9A9488;
  --acento:#C4A15A; --acento-texto:#1A160E;
  --linea:rgba(230,225,214,0.14);
  --peligro:#C46A4A; --ok:#8F9A72; --aviso:#C4A15A;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Times New Roman",Georgia,serif;
  --sans:"Segoe UI",system-ui,-apple-system,sans-serif;
  --radio:2px;
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;min-height:100%;background:var(--fondo);color:var(--tinta);font-family:var(--sans)}
body{padding:1.15rem 1rem 3rem;max-width:36rem;margin:0 auto}
header{border-bottom:1px solid var(--linea);padding-bottom:.85rem;margin-bottom:1rem}
header h1{margin:0;font-family:var(--serif);font-size:1.55rem;font-weight:600}
header p{margin:.35rem 0 0;color:var(--suave);font-size:.72rem;letter-spacing:.12em;text-transform:uppercase}
.disclaimer{background:var(--fondo-2);border:1px solid var(--linea);border-left:3px solid var(--peligro);padding:.85rem 1rem;margin:0 0 1rem;font-size:.9rem;color:var(--suave);border-radius:var(--radio)}
.disclaimer.ok{border-left-color:var(--ok)}
.disclaimer strong{color:var(--tinta)}
.tabs{display:flex;flex-wrap:wrap;gap:.4rem;margin:0 0 1rem}
.tabs button{min-height:44px;padding:.45rem .85rem;font:600 .85rem var(--sans);border:1px solid var(--linea);border-radius:var(--radio);background:var(--fondo-3);color:var(--tinta);cursor:pointer}
.tabs button.on{background:var(--acento);color:var(--acento-texto);border-color:var(--acento)}
h2{margin:1.2rem 0 .65rem;font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;color:var(--suave);font-weight:600}
.panel{background:var(--fondo-2);border:1px solid var(--linea);border-radius:var(--radio);padding:1rem;margin-bottom:.85rem}
.card{display:block;width:100%;text-align:left;padding:.85rem 1rem;margin:0 0 .5rem;background:var(--fondo-2);border:1px solid var(--linea);border-radius:var(--radio);color:inherit;font:inherit;cursor:pointer}
.card:hover,.card:focus{border-color:var(--acento)}
.card .t{font-family:var(--serif);font-weight:600;font-size:1.05rem}
.card .m{color:var(--suave);font-size:.85rem;margin-top:.25rem}
button,.btn{min-height:48px;padding:0 1rem;font:600 .95rem var(--sans);border:1px solid var(--linea);border-radius:var(--radio);background:var(--fondo-3);color:var(--tinta);cursor:pointer}
button.primary,.btn.primary{background:var(--acento);color:var(--acento-texto);border-color:var(--acento)}
button.danger{color:var(--peligro)}
button.ghost{background:transparent}
label.field{display:block;margin:0 0 .75rem}
label.field span{display:block;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--suave);margin-bottom:.3rem}
input,select,textarea{width:100%;min-height:48px;padding:.55rem .75rem;font:inherit;background:var(--fondo-3);color:var(--tinta);border:1px solid var(--linea);border-radius:var(--radio)}
textarea{min-height:6rem;resize:vertical}
.list{display:flex;flex-direction:column;gap:.45rem}
.row{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center}
.chip{display:inline-flex;align-items:center;gap:.35rem;min-height:40px;padding:.3rem .7rem;border:1px solid var(--linea);border-radius:var(--radio);background:var(--fondo-3);font-size:.88rem}
.empty{color:var(--suave);font-size:.95rem;padding:.4rem 0}
.foot{margin-top:1.6rem;color:var(--suave);font-size:.7rem;letter-spacing:.08em;text-transform:uppercase}
.back{margin:0 0 .75rem}
.hidden{display:none!important}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:.5rem}
@media(max-width:420px){.grid2{grid-template-columns:1fr}}
.badge{display:inline-block;padding:.15rem .45rem;border:1px solid var(--linea);border-radius:var(--radio);font-size:.72rem;color:var(--acento);letter-spacing:.06em;text-transform:uppercase}
ol.steps{margin:.5rem 0 0;padding-left:1.2rem}
ol.steps li{margin:.35rem 0}
ul.ings{margin:.4rem 0;padding-left:1.1rem;color:var(--suave)}
.check-item{display:flex;align-items:center;gap:.65rem;padding:.75rem .9rem;background:var(--fondo-2);border:1px solid var(--linea);border-radius:var(--radio);cursor:pointer;width:100%;text-align:left;font:inherit;color:inherit}
.check-item.done{opacity:.6}
.check-item .box{width:22px;height:22px;border:2px solid var(--linea);border-radius:var(--radio);flex-shrink:0}
.check-item.done .box{background:var(--ok);border-color:var(--ok)}
"""

def wrap(title: str, kicker: str, body: str, extra_style: str = "", extra_head: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0E0E0C">
<title>{title} — Les vencimos</title>
{extra_head}<style>
{CSS}
{extra_style}
</style>
</head>
<body>
<header>
  <h1>{title}</h1>
  <p>{kicker}</p>
</header>
{body}
<p class="foot">Les vencimos · offline · file:// · sin Google Fonts</p>
</body>
</html>
"""

def write_zip(name: str, files: dict[str, str | bytes], leeme: str) -> None:
    staging = DL / f".staging-{name}"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    (staging / "LEEME.txt").write_text(leeme, encoding="utf-8")
    for fname, content in files.items():
        p = staging / fname
        if isinstance(content, bytes):
            p.write_bytes(content)
        else:
            p.write_text(content, encoding="utf-8")
    out = DL / f"{name}-offline.zip"
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.write(staging / "LEEME.txt", "LEEME.txt")
        for fname in files:
            z.write(staging / fname, fname)
    shutil.rmtree(staging)
    print(f"zip {out.name} ({out.stat().st_size} bytes)")


def build_hogar() -> None:
    recipes = json.loads(Path("/tmp/recipes.json").read_text(encoding="utf-8"))
    fichas = json.loads(Path("/tmp/fichas.json").read_text(encoding="utf-8"))
    tips = json.loads(Path("/tmp/tips_hogar.json").read_text(encoding="utf-8"))
    compra_def = ["Leche","Yogur","Huevos","Mantequilla","Queso","Jamón","Pollo","Merluza","Tomates","Plátanos","Naranjas","Manzanas","Pan","Aceite de oliva","Pasta","Arroz","Garbanzos","Patatas","Cebollas","Ajos","Papel de cocina","Jabón","Café","Azúcar"]
    groups = ["Frío","Huevos","Pasta","Arroz","Sopas","Pescado","Carne","Verdura","Postre","Otros"]
    zones = [{"id":"nevera","n":"Nevera"},{"id":"congelador","n":"Hielo"},{"id":"despensa","n":"Armario"},{"id":"fruta","n":"Fruta"}]
    fgroups = ["Fruta","Verdura","Carne","Pescado","Lácteos","Despensa","Pan","Condimento","Congelado","Bebida"]

    data_js = {
        "RECETAS": recipes,
        "FICHAS": fichas,
        "TIPS": tips,
        "COMPRA_DEF": compra_def,
        "GROUPS": groups,
        "ZONES": zones,
        "FGROUPS": fgroups,
    }
    body = f"""
<div class="disclaimer ok" role="note">
  <strong>Hogar offline.</strong> Recetas, nevera, lista de la compra, fichas de alimentos y consejos.
  Todo queda en este aparato (localStorage). Sin domótica.
</div>
<nav class="tabs" id="tabs" aria-label="Secciones Hogar"></nav>
<main id="app"></main>
<script>
(function(){{
  const DATA = {json.dumps(data_js, ensure_ascii=False)};
  const KEYS = {{
    compra: 'lv-hogar-compra-v1',
    nevera: 'lv-hogar-nevera-v1'
  }};
  function grupoReceta(titulo){{
    const t = (titulo||'').toLowerCase();
    if(/torrija|flan|tarta|bizcocho|natilla|macedonia|crepe|buñuelo|arroz con leche|leche frita|rosquilla|magdalena|churro|compota|pera al vino|manzana asada|natillas|brownie|galleta/.test(t)) return 'Postre';
    if(/gazpacho|salmorejo|ensalad|hummus|alioli|ajo blanco|pipirrana|escalivada|porra|remojón/.test(t)) return 'Frío';
    if(/sopa|crema de|puré|potaje|cocido|fabada|caldo|pote |gachas|fabes/.test(t)) return 'Sopas';
    if(/pasta|macarrón|lasaña|espagueti|canelón|tallarín|carbonara|boloñesa/.test(t)) return 'Pasta';
    if(/paella|risotto|arroz|fideuá/.test(t)) return 'Arroz';
    if(/merluza|salmón|calamar|bacalao|gamba|sardina|lubina|dorada|pulpo|mejillón|atún|rape|trucha|boquerón|zarzuela|marmitako/.test(t)) return 'Pescado';
    if(/pollo|albóndiga|lomo|ternera|empanad|pizza|croqueta|cerdo|conejo|cordero|hamburguesa|chorizo|carrillera|solomillo|chuleta|migas|callos|lacón/.test(t)) return 'Carne';
    if(/huevo|tortilla|revuelto/.test(t)) return 'Huevos';
    if(/patata|verdura|espinaca|pisto|berenjena|lenteja|garbanzo|alubia|judía|calabacín|coliflor|alcachofa|espárrago|guisante|haba|acelga|menestra/.test(t)) return 'Verdura';
    return 'Otros';
  }}
  function load(k, fallback){{ try{{ const v=JSON.parse(localStorage.getItem(k)||'null'); return v==null?fallback:v; }}catch(e){{ return fallback; }} }}
  function save(k,v){{ localStorage.setItem(k, JSON.stringify(v)); }}

  let tab = 'hub';
  let state = {{ grupo:null, plato:null, paso:null, fgrupo:null, ficha:null }};

  const tabs = [
    {{id:'hub', label:'Inicio'}},
    {{id:'recetas', label:'Recetas'}},
    {{id:'nevera', label:'Nevera'}},
    {{id:'super', label:'Súper'}},
    {{id:'fichas', label:'Alimentos'}},
    {{id:'tips', label:'Consejos'}}
  ];

  function setTab(id){{
    tab = id;
    if(id!=='recetas'){{ state.grupo=null; state.plato=null; state.paso=null; }}
    if(id!=='fichas'){{ state.fgrupo=null; state.ficha=null; }}
    render();
  }}

  function renderTabs(){{
    const el = document.getElementById('tabs');
    el.innerHTML = '';
    tabs.forEach(t=>{{
      const b=document.createElement('button');
      b.type='button'; b.textContent=t.label;
      if(t.id===tab || (tab==='recetas'&&t.id==='recetas') || (['hub'].indexOf(tab)>=0&&t.id==='hub'&&tab==='hub')) {{
        if(t.id===tab) b.className='on';
        else if(tab!=='hub' && t.id===tab) b.className='on';
      }}
      if(t.id===tab) b.classList.add('on');
      b.onclick=()=>setTab(t.id);
      el.appendChild(b);
    }});
  }}

  function render(){{
    renderTabs();
    const app=document.getElementById('app');
    if(tab==='hub'){{
      app.innerHTML = '<div class="grid2">'+
        [['recetas','Recetas',DATA.RECETAS.length+' platos'],
         ['nevera','Nevera','Lo que hay'],
         ['super','Súper','La lista'],
         ['fichas','Alimentos',DATA.FICHAS.length+' fichas'],
         ['tips','Consejos',DATA.TIPS.length+' ideas']].map(([id,t,m])=>
          '<button type="button" class="card" data-go="'+id+'"><div class="t">'+t+'</div><div class="m">'+m+'</div></button>'
        ).join('')+'</div>';
      app.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>setTab(b.getAttribute('data-go')));
      return;
    }}
    if(tab==='recetas') return renderRecetas(app);
    if(tab==='nevera') return renderNevera(app);
    if(tab==='super') return renderSuper(app);
    if(tab==='fichas') return renderFichas(app);
    if(tab==='tips'){{
      app.innerHTML = DATA.TIPS.map(t=>'<article class="panel"><div class="t" style="font-family:var(--serif);font-weight:600;font-size:1.1rem">'+esc(t.titulo)+'</div><p style="margin:.45rem 0 0;color:var(--suave)">'+esc(t.cuerpo)+'</p></article>').join('');
    }}
  }}

  function esc(s){{ return String(s).replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}})[c]); }}

  function renderRecetas(app){{
    if(state.plato){{
      const r = DATA.RECETAS.find(x=>x.titulo===state.plato);
      if(!r){{ state.plato=null; return renderRecetas(app); }}
      if(state.paso!=null){{
        const i=Math.max(0,Math.min(r.pasos.length-1,state.paso));
        app.innerHTML = '<div class="back"><button type="button" class="ghost" id="backPaso">← Ficha</button></div>'+
          '<div class="panel"><span class="badge">Paso '+(i+1)+' de '+r.pasos.length+'</span>'+
          '<p style="font-family:var(--serif);font-size:1.25rem;margin:.7rem 0">'+esc(r.pasos[i])+'</p>'+
          '<div class="row"><button type="button" id="prevP" '+(i<=0?'disabled':'')+'>Anterior</button>'+
          '<button type="button" class="primary" id="nextP">'+(i>=r.pasos.length-1?'Listo':'Siguiente')+'</button></div></div>';
        document.getElementById('backPaso').onclick=()=>{{state.paso=null;render();}};
        document.getElementById('prevP').onclick=()=>{{state.paso=i-1;render();}};
        document.getElementById('nextP').onclick=()=>{{ if(i>=r.pasos.length-1){{state.paso=null;state.plato=null;}} else state.paso=i+1; render(); }};
        return;
      }}
      app.innerHTML = '<div class="back"><button type="button" class="ghost" id="backG">← Grupos</button></div>'+
        '<h2 style="margin-top:0;font-family:var(--serif);font-size:1.4rem;letter-spacing:0;text-transform:none;color:var(--tinta)">'+esc(r.titulo)+'</h2>'+
        '<p class="m" style="color:var(--suave)">'+r.tiempo+' min · '+esc(r.dificultad)+' · '+r.pasos.length+' pasos</p>'+
        '<h2>Qué hace falta</h2><ul class="ings">'+r.ingredientes.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>'+
        '<h2>Cómo se hace</h2><ol class="steps">'+r.pasos.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ol>'+
        '<p style="margin-top:1rem"><button type="button" class="primary" id="cocinar">Cocinar paso a paso</button></p>';
      document.getElementById('backG').onclick=()=>{{state.plato=null;render();}};
      document.getElementById('cocinar').onclick=()=>{{state.paso=0;render();}};
      return;
    }}
    if(!state.grupo){{
      const counts={{}};
      DATA.RECETAS.forEach(r=>{{ const g=grupoReceta(r.titulo); counts[g]=(counts[g]||0)+1; }});
      app.innerHTML = '<p class="empty">'+DATA.RECETAS.length+' recetas · elige un grupo</p>'+
        DATA.GROUPS.filter(g=>counts[g]).map(g=>'<button type="button" class="card" data-g="'+g+'"><div class="t">'+g+'</div><div class="m">'+(counts[g]||0)+' recetas</div></button>').join('');
      app.querySelectorAll('[data-g]').forEach(b=>b.onclick=()=>{{state.grupo=b.getAttribute('data-g');render();}});
      return;
    }}
    const list = DATA.RECETAS.filter(r=>grupoReceta(r.titulo)===state.grupo);
    app.innerHTML = '<div class="back"><button type="button" class="ghost" id="backGroups">← Grupos</button></div><h2>'+esc(state.grupo)+'</h2>'+
      list.map(r=>'<button type="button" class="card" data-p="'+esc(r.titulo)+'"><div class="t">'+esc(r.titulo)+'</div><div class="m">'+r.tiempo+' min · '+esc(r.ingredientes.slice(0,3).join(', '))+'</div></button>').join('');
    document.getElementById('backGroups').onclick=()=>{{state.grupo=null;render();}};
    app.querySelectorAll('[data-p]').forEach(b=>b.onclick=()=>{{state.plato=b.getAttribute('data-p');render();}});
  }}

  function renderNevera(app){{
    let data = load(KEYS.nevera, {{nevera:[],congelador:[],despensa:[],fruta:[]}});
    DATA.ZONES.forEach(z=>{{ if(!Array.isArray(data[z.id])) data[z.id]=[]; }});
    app.innerHTML = DATA.ZONES.map(z=>{{
      const items = data[z.id];
      return '<section class="panel"><h2 style="margin-top:0">'+z.n+'</h2>'+
        '<div class="list" id="z-'+z.id+'">'+(items.length?items.map((it,i)=>'<div class="row" style="justify-content:space-between"><span>'+esc(it)+'</span><button type="button" class="danger" data-z="'+z.id+'" data-i="'+i+'">Quitar</button></div>').join(''):'<p class="empty">Vacío</p>')+'</div>'+
        '<div class="row" style="margin-top:.6rem"><input id="in-'+z.id+'" placeholder="Añadir…" style="flex:1"><button type="button" class="primary" data-add="'+z.id+'">Añadir</button></div></section>';
    }}).join('');
    app.querySelectorAll('[data-add]').forEach(b=>b.onclick=()=>{{
      const z=b.getAttribute('data-add'); const inp=document.getElementById('in-'+z); const v=(inp.value||'').trim();
      if(!v) return; data[z].push(v); save(KEYS.nevera,data); render();
    }});
    app.querySelectorAll('[data-z]').forEach(b=>b.onclick=()=>{{
      const z=b.getAttribute('data-z'); const i=+b.getAttribute('data-i'); data[z].splice(i,1); save(KEYS.nevera,data); render();
    }});
  }}

  function renderSuper(app){{
    let list = load(KEYS.compra, []);
    if(!list.length){{ /* seed empty ok */ }}
    app.innerHTML = '<div class="row" style="margin-bottom:.75rem"><input id="nuevo" placeholder="Qué falta…" style="flex:1"><button type="button" class="primary" id="addC">Añadir</button></div>'+
      '<div class="row" style="margin-bottom:.75rem"><button type="button" id="seed">Sugerencias típicas</button><button type="button" class="danger" id="clearDone">Limpiar marcados</button></div>'+
      '<div class="list" id="lista"></div>';
    const lista=document.getElementById('lista');
    function paint(){{
      lista.innerHTML = list.length ? list.map((it,i)=>'<button type="button" class="check-item'+(it.done?' done':'')+'" data-i="'+i+'"><span class="box"></span><span style="flex:1">'+esc(it.t)+'</span></button>').join('') : '<p class="empty">Lista vacía. Añade lo que falte.</p>';
      lista.querySelectorAll('[data-i]').forEach(b=>b.onclick=()=>{{ list[+b.getAttribute('data-i')].done=!list[+b.getAttribute('data-i')].done; save(KEYS.compra,list); paint(); }});
    }}
    paint();
    document.getElementById('addC').onclick=()=>{{
      const v=(document.getElementById('nuevo').value||'').trim(); if(!v) return;
      list.push({{t:v,done:false}}); save(KEYS.compra,list); document.getElementById('nuevo').value=''; paint();
    }};
    document.getElementById('seed').onclick=()=>{{
      DATA.COMPRA_DEF.forEach(t=>{{ if(!list.some(x=>x.t===t)) list.push({{t:t,done:false}}); }});
      save(KEYS.compra,list); paint();
    }};
    document.getElementById('clearDone').onclick=()=>{{ list=list.filter(x=>!x.done); save(KEYS.compra,list); paint(); }};
  }}

  function renderFichas(app){{
    if(state.ficha){{
      const f=DATA.FICHAS.find(x=>x.n===state.ficha);
      app.innerHTML = '<div class="back"><button type="button" class="ghost" id="bf">←</button></div>'+
        (f?('<div class="panel"><span class="badge">'+esc(f.g)+'</span><h2 style="margin:.5rem 0;font-family:var(--serif);font-size:1.35rem;letter-spacing:0;text-transform:none;color:var(--tinta)">'+esc(f.n)+'</h2>'+
        '<p><strong>Conservación:</strong> '+esc(f.tip)+'</p><p><strong>Caduca ~</strong> '+esc(f.cad)+'</p><p><strong>Combina con:</strong> '+esc(f.con)+'</p></div>'):'<p class="empty">No está</p>');
      document.getElementById('bf').onclick=()=>{{state.ficha=null;render();}};
      return;
    }}
    if(!state.fgrupo){{
      app.innerHTML = DATA.FGROUPS.map(g=>{{
        const n=DATA.FICHAS.filter(x=>x.g===g).length;
        return '<button type="button" class="card" data-fg="'+g+'"><div class="t">'+g+'</div><div class="m">'+n+' fichas</div></button>';
      }}).join('');
      app.querySelectorAll('[data-fg]').forEach(b=>b.onclick=()=>{{state.fgrupo=b.getAttribute('data-fg');render();}});
      return;
    }}
    const list=DATA.FICHAS.filter(x=>x.g===state.fgrupo);
    app.innerHTML = '<div class="back"><button type="button" class="ghost" id="bg">← Grupos</button></div>'+
      list.map(f=>'<button type="button" class="card" data-fn="'+esc(f.n)+'"><div class="t">'+esc(f.n)+'</div><div class="m">'+esc(f.tip)+'</div></button>').join('');
    document.getElementById('bg').onclick=()=>{{state.fgrupo=null;render();}};
    app.querySelectorAll('[data-fn]').forEach(b=>b.onclick=()=>{{state.ficha=b.getAttribute('data-fn');render();}});
  }}

  render();
}})();
</script>
"""
    html = wrap("Hogar", "Les vencimos · cocina y casa · offline", body)
    (MOD / "hogar.html").write_text(html, encoding="utf-8")
    leeme = """HOGAR — Les vencimos

Módulo offline: recetas, nevera, lista de la compra,
fichas de alimentos y consejos de casa.

Abre hogar.html desde Archivos (file://).
Datos en localStorage de este aparato. Sin nube. Sin domótica.

lesvencimos.com
"""
    (MOD / "LEEME-hogar.txt").write_text(leeme, encoding="utf-8")
    write_zip("hogar", {"hogar.html": html}, leeme)
    print("hogar.html", len(html))


def build_salud() -> None:
    tips = json.loads(Path("/tmp/tips_salud.json").read_text(encoding="utf-8"))
    meds_def = ["Levotiroxina","Enalapril","Omeprazol","Metformina","AAS","Atorvastatina","Paracetamol","Ibuprofeno","Amoxicilina","Vitamina D"]
    body = f"""
<div class="disclaimer" role="note">
  <strong>Aviso:</strong> recordatorio y agenda local. No sustituye indicación médica ni el prospecto.
  Urgencias: <strong>112</strong>. Complementa el módulo Medicación si lo usas aparte.
</div>
<nav class="tabs" id="tabs"></nav>
<main id="app"></main>
<script>
(function(){{
  const TIPS = {json.dumps(tips, ensure_ascii=False)};
  const MEDS_DEF = {json.dumps(meds_def, ensure_ascii=False)};
  const K = {{
    meds:'lv-salud-meds-v1',
    checks:()=>'lv-salud-check-'+new Date().toISOString().slice(0,10),
    docs:'lv-salud-docs-v1',
    reports:'lv-salud-reports-v1',
    hist:'lv-salud-hist-v1'
  }};
  function load(k, fb){{ try{{ const v=JSON.parse(localStorage.getItem(k)||'null'); return v==null?fb:v; }}catch(e){{return fb}} }}
  function save(k,v){{ localStorage.setItem(k, JSON.stringify(v)); }}
  function esc(s){{ return String(s).replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}})[c]); }}
  function uid(){{ return 's'+Date.now().toString(36)+Math.random().toString(36).slice(2,5); }}

  let tab='hub';
  const tabs=[
    {{id:'hub',label:'Inicio'}},
    {{id:'pastillas',label:'Pastillas'}},
    {{id:'medicos',label:'Médicos'}},
    {{id:'informes',label:'Informes'}},
    {{id:'historial',label:'Historial'}},
    {{id:'consejos',label:'Consejos'}}
  ];

  function setTab(id){{ tab=id; render(); }}

  function render(){{
    const tel=document.getElementById('tabs');
    tel.innerHTML='';
    tabs.forEach(t=>{{
      const b=document.createElement('button'); b.type='button'; b.textContent=t.label;
      if(t.id===tab) b.className='on'; b.onclick=()=>setTab(t.id); tel.appendChild(b);
    }});
    const app=document.getElementById('app');
    if(tab==='hub'){{
      app.innerHTML='<div class="grid2">'+[
        ['pastillas','Pastillas','Horarios y checklist de hoy'],
        ['medicos','Médicos / centros','Teléfonos y notas'],
        ['informes','Informes','Analíticas y notas locales'],
        ['historial','Historial','Qué tomaste (este aparato)'],
        ['consejos','Consejos','Hábitos suaves']
      ].map(([id,t,m])=>'<button type="button" class="card" data-go="'+id+'"><div class="t">'+t+'</div><div class="m">'+m+'</div></button>').join('')+'</div>'+
      '<p class="empty" style="margin-top:1rem">También existe el módulo suelto <strong>Medicación</strong> (más simple). Aquí está la sección Salud completa.</p>';
      app.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>setTab(b.getAttribute('data-go')));
      return;
    }}
    if(tab==='pastillas') return renderPastillas(app);
    if(tab==='medicos') return renderMedicos(app);
    if(tab==='informes') return renderInformes(app);
    if(tab==='historial') return renderHist(app);
    if(tab==='consejos'){{
      app.innerHTML=TIPS.map(t=>'<article class="panel"><div style="font-family:var(--serif);font-weight:600;font-size:1.1rem">'+esc(t.titulo)+'</div><p style="margin:.45rem 0 0;color:var(--suave)">'+esc(t.cuerpo)+'</p></article>').join('');
    }}
  }}

  function renderPastillas(app){{
    let meds=load(K.meds,[]);
    let checks=load(K.checks(),{{}});
    app.innerHTML='<h2>Hoy</h2><div class="list" id="hoy"></div><h2>Mis medicinas</h2><div class="list" id="lista"></div>'+
      '<section class="panel"><h2 style="margin-top:0">Añadir</h2>'+
      '<label class="field"><span>Nombre</span><input id="nombre" list="sug" placeholder="Ej. Metformina"></label>'+
      '<datalist id="sug">'+MEDS_DEF.map(m=>'<option value="'+esc(m)+'">').join('')+'</datalist>'+
      '<label class="field"><span>Dosis</span><input id="dosis" placeholder="Ej. 850 mg"></label>'+
      '<div class="row" style="margin-bottom:.6rem">'+[['08:00','Mañana'],['14:00','Mediodía'],['21:00','Noche']].map(([v,l])=>'<label class="chip"><input type="checkbox" value="'+v+'"> '+l+' '+v+'</label>').join('')+'</div>'+
      '<label class="field"><span>Otra hora</span><input id="otra" type="time"></label>'+
      '<button type="button" class="primary" id="add">Guardar</button></section>';

    function slots(){{
      const out=[];
      meds.forEach(m=>{{ (m.horas||[]).forEach(h=>out.push({{id:m.id+':'+h, hora:h, nombre:m.nombre, dosis:m.dosis, mid:m.id}})); }});
      out.sort((a,b)=>a.hora.localeCompare(b.hora));
      return out;
    }}
    function paint(){{
      const hoy=document.getElementById('hoy');
      const s=slots();
      hoy.innerHTML=s.length?s.map(x=>{{
        const done=!!checks[x.id];
        return '<button type="button" class="check-item'+(done?' done':'')+'" data-id="'+x.id+'"><span class="box"></span><span style="color:var(--acento);font-weight:700;min-width:3.2rem">'+x.hora+'</span><span style="flex:1"><strong>'+esc(x.nombre)+'</strong> · '+esc(x.dosis||'')+'</span></button>';
      }}).join(''):'<p class="empty">Sin tomas hoy. Añade medicinas abajo.</p>';
      hoy.querySelectorAll('[data-id]').forEach(b=>b.onclick=()=>{{
        const id=b.getAttribute('data-id');
        checks[id]=!checks[id];
        save(K.checks(),checks);
        if(checks[id]){{
          const hist=load(K.hist,[]);
          hist.unshift({{when:new Date().toISOString(), id, label:b.textContent.trim()}});
          save(K.hist, hist.slice(0,200));
        }}
        paint();
      }});
      const lista=document.getElementById('lista');
      lista.innerHTML=meds.length?meds.map(m=>'<div class="panel" style="margin:0"><div class="row" style="justify-content:space-between"><div><div style="font-family:var(--serif);font-weight:600">'+esc(m.nombre)+'</div><div class="m" style="color:var(--suave)">'+esc(m.dosis||'')+' · '+(m.horas||[]).join(', ')+'</div></div><button type="button" class="danger" data-del="'+m.id+'">Borrar</button></div></div>').join(''):'<p class="empty">Aún no hay medicinas.</p>';
      lista.querySelectorAll('[data-del]').forEach(b=>b.onclick=()=>{{ meds=meds.filter(x=>x.id!==b.getAttribute('data-del')); save(K.meds,meds); paint(); }});
    }}
    paint();
    document.getElementById('add').onclick=()=>{{
      const nombre=(document.getElementById('nombre').value||'').trim();
      if(!nombre) return;
      const dosis=(document.getElementById('dosis').value||'').trim();
      const horas=[...app.querySelectorAll('.chip input:checked')].map(i=>i.value);
      const otra=(document.getElementById('otra').value||'').trim();
      if(otra && horas.indexOf(otra)<0) horas.push(otra);
      if(!horas.length){{ alert('Elige al menos un horario'); return; }}
      horas.sort();
      meds.push({{id:uid(), nombre, dosis, horas}});
      save(K.meds,meds);
      document.getElementById('nombre').value='';
      document.getElementById('dosis').value='';
      document.getElementById('otra').value='';
      app.querySelectorAll('.chip input').forEach(i=>i.checked=false);
      paint();
    }};
  }}

  function renderMedicos(app){{
    let docs=load(K.docs,[]);
    app.innerHTML='<div class="list" id="lista"></div><section class="panel"><h2 style="margin-top:0">Añadir médico o centro</h2>'+
      '<label class="field"><span>Nombre</span><input id="n" placeholder="Dra. Pérez / Centro de salud…"></label>'+
      '<label class="field"><span>Especialidad / tipo</span><input id="e" placeholder="Médico de cabecera, cardiología…"></label>'+
      '<label class="field"><span>Teléfono 1</span><input id="t1" type="tel" placeholder="983…"></label>'+
      '<label class="field"><span>Teléfono 2</span><input id="t2" type="tel"></label>'+
      '<label class="field"><span>Horario / notas</span><textarea id="h" placeholder="Mañanas, pedir cita por app…"></textarea></label>'+
      '<button type="button" class="primary" id="add">Guardar</button></section>'+
      '<p class="empty">Urgencias Europa: <strong>112</strong>. Los números se quedan solo en este teléfono.</p>';
    function paint(){{
      const lista=document.getElementById('lista');
      lista.innerHTML=docs.length?docs.map(d=>'<article class="panel"><div style="font-family:var(--serif);font-weight:600;font-size:1.1rem">'+esc(d.nombre)+'</div>'+
        '<div style="color:var(--suave);margin:.25rem 0">'+esc(d.espe||'')+'</div>'+
        (d.tel1?('<div class="row"><a class="btn primary" href="tel:'+esc(d.tel1)+'" style="text-decoration:none">Llamar '+esc(d.tel1)+'</a>'+(d.tel2?'<a class="btn" href="tel:'+esc(d.tel2)+'" style="text-decoration:none">'+esc(d.tel2)+'</a>':'')+'</div>'):'')+
        (d.horario?('<p style="margin:.6rem 0 0;color:var(--suave)">'+esc(d.horario)+'</p>'):'')+
        '<p style="margin:.6rem 0 0"><button type="button" class="danger" data-del="'+d.id+'">Borrar</button></p></article>').join(''):'<p class="empty">Aún no hay médicos ni centros.</p>';
      lista.querySelectorAll('[data-del]').forEach(b=>b.onclick=()=>{{ docs=docs.filter(x=>x.id!==b.getAttribute('data-del')); save(K.docs,docs); paint(); }});
    }}
    paint();
    document.getElementById('add').onclick=()=>{{
      const nombre=(document.getElementById('n').value||'').trim(); if(!nombre) return;
      docs.push({{id:uid(), nombre, espe:(document.getElementById('e').value||'').trim(), tel1:(document.getElementById('t1').value||'').trim(), tel2:(document.getElementById('t2').value||'').trim(), horario:(document.getElementById('h').value||'').trim()}});
      save(K.docs,docs);
      ['n','e','t1','t2','h'].forEach(id=>document.getElementById(id).value='');
      paint();
    }};
  }}

  function renderInformes(app){{
    let reps=load(K.reports,[]);
    app.innerHTML='<div class="list" id="lista"></div><section class="panel"><h2 style="margin-top:0">Nuevo informe / nota</h2>'+
      '<label class="field"><span>Título</span><input id="t" placeholder="Analítica marzo, informe alta…"></label>'+
      '<label class="field"><span>Fecha</span><input id="f" type="date"></label>'+
      '<label class="field"><span>Texto</span><textarea id="c" placeholder="Valores, qué dijo el médico… (solo en este aparato)"></textarea></label>'+
      '<button type="button" class="primary" id="add">Guardar</button></section>';
    function paint(){{
      const lista=document.getElementById('lista');
      lista.innerHTML=reps.length?reps.map(r=>'<article class="panel"><div class="badge">'+esc(r.fecha||'sin fecha')+'</div><div style="font-family:var(--serif);font-weight:600;margin:.4rem 0">'+esc(r.titulo)+'</div><pre style="white-space:pre-wrap;font:inherit;margin:0;color:var(--suave)">'+esc(r.cuerpo||'')+'</pre><p style="margin:.6rem 0 0"><button type="button" class="danger" data-del="'+r.id+'">Borrar</button></p></article>').join(''):'<p class="empty">Sin informes aún.</p>';
      lista.querySelectorAll('[data-del]').forEach(b=>b.onclick=()=>{{ reps=reps.filter(x=>x.id!==b.getAttribute('data-del')); save(K.reports,reps); paint(); }});
    }}
    paint();
    document.getElementById('add').onclick=()=>{{
      const titulo=(document.getElementById('t').value||'').trim(); if(!titulo) return;
      reps.unshift({{id:uid(), titulo, fecha:document.getElementById('f').value||'', cuerpo:(document.getElementById('c').value||'').trim()}});
      save(K.reports,reps);
      document.getElementById('t').value=''; document.getElementById('c').value=''; paint();
    }};
  }}

  function renderHist(app){{
    const hist=load(K.hist,[]);
    app.innerHTML=hist.length?hist.map(h=>'<div class="panel" style="margin-bottom:.45rem"><div class="badge">'+esc((h.when||'').replace('T',' ').slice(0,16))+'</div><div style="margin-top:.35rem">'+esc(h.label||h.id)+'</div></div>').join('')+'<p style="margin-top:1rem"><button type="button" class="danger" id="clr">Vaciar historial</button></p>':'<p class="empty">Cuando marques una pastilla como tomada, aparecerá aquí.</p>';
    const clr=document.getElementById('clr'); if(clr) clr.onclick=()=>{{ save(K.hist,[]); render(); }};
  }}

  render();
}})();
</script>
"""
    html = wrap("Salud", "Les vencimos · pastillas, médicos, informes · offline", body)
    (MOD / "salud.html").write_text(html, encoding="utf-8")
    leeme = """SALUD — Les vencimos

Sección amplia offline: pastillas y horarios, médicos/centros
con teléfonos, informes/notas e historial local.

AVISO: no sustituye indicación médica. Urgencias: 112.
Puede complementar el módulo Medicación.

Abre salud.html desde Archivos (file://).
lesvencimos.com
"""
    (MOD / "LEEME-salud.txt").write_text(leeme, encoding="utf-8")
    write_zip("salud", {"salud.html": html}, leeme)
    print("salud.html", len(html))


def build_radio() -> None:
    stations = json.loads(Path("/tmp/stations.json").read_text(encoding="utf-8"))
    body = f"""
<div class="disclaimer ok" role="note">
  <strong>Radio offline-capable:</strong> la interfaz y la lista de emisoras viven en este HTML.
  Para <em>oír</em> el directo hace falta conexión (los streams son de las emisoras).
  Sin anuncios propios ni cuenta.
</div>
<div id="now" class="panel" style="display:none">
  <div class="badge">Sonando</div>
  <div id="nowName" style="font-family:var(--serif);font-size:1.35rem;font-weight:600;margin:.4rem 0"></div>
  <div id="nowMeta" style="color:var(--suave)"></div>
  <div class="row" style="margin-top:.75rem">
    <button type="button" class="primary" id="btnStop">Parar</button>
  </div>
</div>
<p class="empty">Toca una emisora. Puede seguir sonando si cambias de pestaña del navegador.</p>
<div class="list" id="lista"></div>
<audio id="player" preload="none"></audio>
<script>
(function(){{
  const STATIONS = {json.dumps(stations, ensure_ascii=False)};
  const player = document.getElementById('player');
  const lista = document.getElementById('lista');
  const now = document.getElementById('now');
  let current = null;
  let urlIndex = 0;

  lista.innerHTML = STATIONS.map(s=>'<button type="button" class="card" data-id="'+s.id+'"><div class="t">'+s.nom+'</div><div class="m">'+s.meta+'</div></button>').join('');

  function play(st){{
    current = st; urlIndex = 0;
    tryUrl();
    now.style.display='block';
    document.getElementById('nowName').textContent = st.nom;
    document.getElementById('nowMeta').textContent = st.meta + ' · si falla, prueba otra o revisa la red';
  }}
  function tryUrl(){{
    if(!current) return;
    const urls = current.urls || [];
    if(urlIndex >= urls.length){{
      document.getElementById('nowMeta').textContent = 'No se pudo abrir el stream. ¿Hay red?';
      return;
    }}
    player.src = urls[urlIndex];
    player.play().catch(function(){{ urlIndex++; tryUrl(); }});
  }}
  player.addEventListener('error', function(){{ urlIndex++; tryUrl(); }});

  lista.querySelectorAll('[data-id]').forEach(b=>b.onclick=()=>{{
    const st = STATIONS.find(x=>x.id===b.getAttribute('data-id'));
    if(st) play(st);
  }});
  document.getElementById('btnStop').onclick=()=>{{
    player.pause(); player.removeAttribute('src'); player.load();
    current=null; now.style.display='none';
  }};
}})();
</script>
"""
    html = wrap("Radio", "Les vencimos · emisoras · interfaz offline", body)
    (MOD / "radio.html").write_text(html, encoding="utf-8")
    leeme = """RADIO — Les vencimos

Lista de emisoras (COPE, SER, Onda Cero, Marca, Dial).
La interfaz funciona sin red; el audio en directo necesita internet.

Abre radio.html desde Archivos (file://).
lesvencimos.com
"""
    (MOD / "LEEME-radio.txt").write_text(leeme, encoding="utf-8")
    write_zip("radio", {"radio.html": html}, leeme)
    print("radio.html", len(html))


if __name__ == "__main__":
    MOD.mkdir(parents=True, exist_ok=True)
    DL.mkdir(parents=True, exist_ok=True)
    build_hogar()
    build_salud()
    build_radio()
    print("partial OK — QR and Electricidad next")
