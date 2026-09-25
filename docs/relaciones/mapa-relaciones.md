# Mapa sintético de relaciones

Unifica `inventario.md`, `solapes.md`, `huecos.md`, `puentes.md`.  
29 módulos únicos · 5 aliases · Cuba aparte · Ruleta/red/juego fuera de alcance.

---

## Diagrama (Mermaid)

```mermaid
flowchart TB
  subgraph nucleo["Núcleo asistente offline"]
    AST[Asistente / Estantería / Añadir módulo]
  end

  subgraph clusterHEC["Clúster Hogar-Economía-Clima"]
    HOG[Hogar]
    ECO[Economía]
    CLI[Clima]
    HOG <-.lista/menú.-> ECO
    ECO <-.energía €.-> CLI
    HOG <-.humedad/moho.-> CLI
  end

  subgraph verde["Verde / vivo"]
    JAR[Jardín]
    CAM[Campo]
    MAS[Mascotas]
    JAR --- CAM
    JAR --- MAS
  end

  subgraph salud["Salud cuerpo"]
    SAL[Salud]
    MED[Medicación]
    AUX[Primeros auxilios]
    GYM[Gimnasio]
    MDT[Meditación]
    SAL -.duplicado pastillas.-> MED
    AUX --- SAL
  end

  subgraph resili["Resiliencia"]
    APA[Apagón]
    SUP[Supervivencia]
    ELE[Electricidad]
    BRI[Bricolaje]
    APA --- ELE
    APA --- SUP
    SUP --- CAM
    APA --- AUX
  end

  subgraph casa_legal["Casa formal"]
    LEG[Legal-casa]
    LEG --- ECO
    LEG --- HOG
    LEG --- MAS
  end

  subgraph ropa["Ropa"]
    MOD[Moda]
    MOD --- HOG
    MOD --- ECO
  end

  subgraph tools["Herramientas"]
    CAJ[Caja fuerte]
    QR[QR]
    RAD[Radio]
    CAL[Calculadora]
    INF[Informática]
    INF --- CAJ
    INF --- QR
    QR --> AST
  end

  subgraph viaje["Viaje"]
    MAP[Mapas]
    GUI[Guías viaje]
    MAP --- GUI
  end

  subgraph cultura["Cultura / estudio"]
    BIB[Biblioteca]
    GUI_T[Guitarra]
    TE[Tinta escritura]
    TD[Tinta estudio]
    PROF[[Profesor — fuera pack]]
    TE -.frontera.-> PROF
    INF -.frontera.-> PROF
  end

  subgraph aparte["Aparte Cuba"]
    CUB[Alarma / Central Cuba]
  end

  AST --> HOG
  AST --> ECO
  AST --> SAL
  AST --> APA
  HOG --- JAR
  RAD --- APA
  INF -.-> CUB
```

---

## Tabla clúster × módulo

| Clúster | Módulos | Solape fuerte | Hueco / tensión | Puente prioritario |
|---|---|---|---|---|
| Hogar-€-Clima | Hogar, Economía, Clima | Compra/menú; termostato/€ | Doble lista compra | P1 lista unificada; P3 hábitos energía |
| Verde | Jardín, Campo, Mascotas | Toxicidad; supervivencia plantas | Vet en apagón | Deep-link toxicidad |
| Salud | Salud, Medicación, Auxilios, Gym, Medita | Pastillas duplicadas | Fuente de verdad | P2 Medicación→Salud |
| Resiliencia | Apagón, Supervivencia, Campo, Elec, Radio | Corte luz / agua / 112 | Radio no offline audio | Hub Resiliencia 3 chips |
| Legal-€ | Legal, Economía, Hogar | Derramas, vivienda | IRPF no cubierto | Derrama→gasto |
| Ropa | Moda, Hogar, Economía | Lavado/manchas | — | Etiqueta `lavado` |
| Herramientas | Info, Caja, QR, Radio, Calc | Secretos / catálogo | Cuba en Info vs home | QR ids canónicos |
| Viaje | Mapas, Guías | Ciudad Va | Guías esqueleto en modulos/ | CTA pack cruzado |
| Cultura | Biblio, Guitarra, Tintas, Info | Frontera Profesor | Plantilla 1 KB en modulos | No mezclar estantes |

---

## Conteos

- HTML en `modulos/`: 34  
- Únicos: **29**  
- Aliases: **5**  
- LEEME: 28 (+ vida sin HTML)  
- Docs carpeta: HOGAR-INDICE, _aparte-cuba  

## Top 5 solapes
1. Hogar ↔ Economía (compra/menú/nevera)  
2. Economía ↔ Clima (energía/confort)  
3. Moda ↔ Hogar (lavado/manchas)  
4. Salud ↔ Medicación (pastillas)  
5. Apagón ↔ Electricidad ↔ Supervivencia  

## Top 5 huecos
1. Fontanería / gas / pintura (LEEME-vida)  
2. Lista compra no unificada  
3. Duplicado Salud/Medicación  
4. Guías viaje esqueleto en modulos/  
5. Agenda personal inexistente en estantería  

## 3 puentes prioritarios
1. Lista compra Hogar↔Economía  
2. Medicación como fuente → Salud  
3. Hábitos energía Clima↔Economía  

*Fin mapa.*
