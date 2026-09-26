# Mapa de relaciones — síntesis

Fecha: 26 sep 2026 · Europe/Madrid (UTC+2)

## Diagrama (Mermaid)

```mermaid
flowchart TB
  subgraph cocina_casa["Clúster cocina / casa"]
    H[Hogar hub]
    E[Economía]
    C[Clima]
    M[Moda]
    H -->|lv-lista-compra-v1| E
    E -->|luz € / hábitos| C
    C -->|humedad-moho causa| H
    H -->|lavado procedimiento| M
    M -->|símbolos / criterio prenda| H
  end

  subgraph sanidad["Clúster sanidad"]
    S[Salud]
    Med[Medicación]
    PA[Primeros auxilios]
    S -->|lv-medicacion-v1| Med
    PA -.->|urgencia educativa| S
  end

  subgraph resiliencia["Resiliencia / vida"]
    A[Apagón]
    El[Electricidad]
    Sup[Supervivencia]
    Cam[Campo]
    Bri[Bricolaje]
    A --> El
    A --> Sup
    El -.-> Bri
    Cam -.-> Sup
  end

  H -.->|mantén límites| El
  H -.->|mantén límites| Bri
  A -.->|nevera / meds| Med
  E -.->|patrimonio vivienda| L[Legal-casa]
  J[Jardín] -.-> Mas[Mascotas]
  G[Guías viaje] -.-> Map[Mapas]
```

## Tabla síntesis relaciones

| De | A | Tipo | Evidencia |
|----|---|------|-----------|
| Hogar | Economía | dato compartido | `lv-lista-compra-v1` |
| Hogar | Clima | contenido puente | moho/humedad vs limpieza |
| Hogar | Moda | contenido parcial | lavado ↔ cuidado |
| Hogar | Electricidad/Bricolaje | límite | mantén «llamar profesional» |
| Economía | Clima | frontera € vs confort | tabs `luz` vs lecciones clima |
| Economía | Legal-casa | puente | patrimonio / impuestos Va |
| Salud | Medicación | dato compartido | `lv-medicacion-v1` |
| Apagón | Electricidad | enlace declarado | LEEME-apagon |
| Apagón | Supervivencia | tema afín | corte / stock |
| Campo | Supervivencia | frontera outdoor/casa | LEEME-campo |
| Jardín | Mascotas | aviso toxicidad | diccionario jardín |
| Guías | Mapas | viaje ES | piloto + packs |
| Informática | Aparte Cuba | aparte | `_aparte-cuba.md` |

## Densidad por clúster

| Clúster | Núcleo denso | Satélites finos |
|---------|--------------|-----------------|
| Casa | Hogar, Economía, Jardín | Clima, Moda, Legal, Bricolaje, Electricidad |
| Salud | — | Salud, Medicación, PA, Gimnasio*, Meditación* |
| Cultura | Biblioteca, Informática | Tintas, Guitarra, Guías, QR |
| Resiliencia | — | Apagón, Supervivencia, Campo, Radio, Mapas |

\*Gimnasio/Meditación son densos pero de bienestar, no solapan datos con Salud.

*Fin mapa*
