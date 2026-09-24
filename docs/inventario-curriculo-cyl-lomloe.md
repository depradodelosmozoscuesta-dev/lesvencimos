# Inventario curricular oficial — Castilla y León (LOMLOE)

> Inventario de referencia para bots Profesor / lesvencimos (un bot por curso+asignatura).
> **No inventa contenidos**: bloques/saberes tomados de los decretos CyL vigentes.
> Fecha de elaboración: 2026-09-23 (Europe/Madrid).

## 1. Fuentes oficiales

### Estado (enseñanzas mínimas LOMLOE)

| Norma | Objeto | Enlace |
|---|---|---|
| Ley Orgánica 3/2020, de 29 de diciembre (LOMLOE) | Marco legal | https://www.boe.es/buscar/act.php?id=BOE-A-2020-17264 |
| Real Decreto 157/2022, de 1 de marzo | Enseñanzas mínimas Primaria | https://www.boe.es/buscar/act.php?id=BOE-A-2022-3296 |
| Real Decreto 217/2022, de 29 de marzo | Enseñanzas mínimas ESO | https://www.boe.es/buscar/act.php?id=BOE-A-2022-4975 |
| Real Decreto 243/2022, de 5 de abril | Enseñanzas mínimas Bachillerato | https://www.boe.es/buscar/act.php?id=BOE-A-2022-5521 |

### Castilla y León (currículo completo; **fuente preferente**)

| Decreto | Etapa | Publicación | PDF BOCyL | Portal Educa |
|---|---|---|---|---|
| **Decreto 38/2022**, de 29 de septiembre | Educación Primaria | BOCyL n.º 190, 30/09/2022 | https://bocyl.jcyl.es/boletines/2022/09/30/pdf/BOCYL-D-30092022-2.pdf | https://www.educa.jcyl.es/es/informacion/sistema-educativo/educacion-primaria/educacion-primaria-curriculo-ordenacion |
| **Decreto 39/2022**, de 29 de septiembre | ESO | BOCyL n.º 190, 30/09/2022 | https://bocyl.jcyl.es/boletines/2022/09/30/pdf/BOCYL-D-30092022-3.pdf | https://www.educa.jcyl.es/es/informacion/sistema-educativo/educacion-secundaria-obligatoria/educacion-secundaria-obligatoria-ordenacion-curriculo |
| **Decreto 40/2022**, de 29 de septiembre | Bachillerato | BOCyL n.º 190, 30/09/2022 | https://bocyl.jcyl.es/boletines/2022/09/30/pdf/BOCYL-D-30092022-4.pdf | https://www.educa.jcyl.es/es/informacion/sistema-educativo/bachillerato/bachillerato-decreto-ordenacion-curriculo |

**Copias locales de trabajo** (texto extraído): `/workspace/profesor-temario/fuentes/decreto{38,39,40}-*.pdf|.txt` y JSON de bloques.

### Relación Autonomía / Estado

- CyL **desarrolla y concreta** las enseñanzas mínimas estatales (saberes más detallados, optativas propias, horarios Anexo V).
- Cuando el decreto CyL detalla contenidos por curso (p. ej. Matemáticas ESO), **usar CyL**.
- Religión: oferta obligada, elección voluntaria (DA de los RD + arts. CyL). Alternativa CyL: proyectos significativos con valores/tradición/cultura de Castilla y León.
- Implantación curricular LOMLOE completa desde curso 2023-2024 (cursos pares e impares).
- **Ambiguiedad / pendientes**: no se ha localizado en esta pasada un decreto CyL posterior que derogue 38/39/40/2022; conviene revalidar periódicamente en BOCyL/Educa. Lengua Extranjera: el decreto no fija el idioma (habitualmente Inglés; 2.ª LE según centro). Oferta real de optativas depende del centro (ratios/autorización).

---

## 2. Convención de nombres de bots (español)

Formato: `{curso} {etapa} {asignatura}`

| Ejemplo | Notas |
|---|---|
| `1º ESO Matemáticas` | Obligatoria 1.º–3.º |
| `4º ESO Matemáticas A` / `4º ESO Matemáticas B` | Elección del alumnado |
| `1º Bachillerato Matemáticas I` | Modalidad Ciencias y Tecnología |
| `2º Bachillerato Matemáticas Aplicadas a las Ciencias Sociales II` | Nombre completo del decreto |
| `1º Bachillerato Matemáticas Generales` | Modalidad General |
| `3º Primaria Lengua Castellana y Literatura` | Áreas de Primaria |
| `1º ESO Lengua Extranjera (Inglés)` | Añadir idioma entre paréntesis |
| `1º ESO Religión` / `1º ESO Alternativa a la Religión` | Oferta obligada / elección |
| `1º ESO Conocimiento de las Matemáticas` | Optativa de refuerzo |

Reglas: ordinal con `º`; etapa `Primaria` | `ESO` | `Bachillerato`; asignatura = nombre oficial del decreto; en Bachillerato conservar I/II.

---

## 3. Orden de trabajo recomendado

**Recomendación: horizontal por curso (empezar y completar 1º ESO), no vertical por materia.**

Motivo: un tutor/centro obtiene antes un **curso completo usable** (todas las troncales de 1º ESO) frente a tener solo Matemáticas 1.º–4.º dejando el resto del curso vacío. Después se puede abrir la vertical de Matemáticas (2.º–4.º ESO → Bach) porque reutiliza estructura de sentidos.

### Primeros 5 bots

1. `1º ESO Matemáticas` ← **empezar aquí** (borrador de lecciones en documento aparte)
2. `1º ESO Lengua Castellana y Literatura`
3. `1º ESO Geografía e Historia`
4. `1º ESO Biología y Geología`
5. `1º ESO Tecnología y Digitalización`

Siguiente oleada 1º ESO: Lengua Extranjera (Inglés), Educación Física, Educación Plástica Visual y Audiovisual; **EPVA pack completo L01–L31/31** (Revisor Dios CONFIRMA). luego optativas frecuentes (Conocimiento de las Matemáticas / del Lenguaje / 2.ª LE) y Religión/Alternativa.

Después: **2º ESO** (aparece Física y Química, Música; cae Biología/EPVA/TyD del horario común), **3º ESO**, **4º ESO** (Mate A/B + itinerarios), luego **Primaria** (si el producto offline lo pide) y **Bachillerato** por modalidad (priorizar Ciencias y Tecnología + Humanidades y CCSS).

---

## 4. Conteo aproximado de bots

| Ámbito | Criterio | Estimación |
|---|---|---|
| Primaria núcleos (6×8 áreas) + EvCE 6.º | Un bot por curso×área | **≈ 49** |
| Primaria Religión/Alternativa + 2.ª LE (5.º–6.º) | Si se cubren | **+10–14** |
| ESO materias comunes/obligatorias por curso | Incl. Mate A/B, EPVA/Música 3.º | **≈ 40–45** |
| ESO optativas CyL frecuentes | Refuerzo, Cultura Clásica, Digitalización, etc. | **≈ 35–50** |
| Bachillerato comunes (1.º–2.º) | Compartidas por modalidades | **≈ 10** |
| Bachillerato específicas + optativas habituales | 4 modalidades / 2 vías Artes | **≈ 50–70** |
| **Total catálogo CyL «completo razonable»** | Núcleos + optativas habituales | **≈ 180–220 bots** |
| **Fase 1 mínima útil** | Troncales ESO 1.º–4.º + Mate Bach CyT/HCCS | **≈ 55–70 bots** |

---

## 5. Educación Primaria (Decreto 38/2022)

### Organización (art. 15–16)

**Áreas en todos los cursos (1.º–6.º) — obligatorias:**

1. Ciencias de la Naturaleza
2. Ciencias Sociales
3. Educación Plástica y Visual
4. Música y Danza
5. Educación Física
6. Lengua Castellana y Literatura
7. Lengua Extranjera
8. Matemáticas

- **6.º**: además, **Educación en Valores Cívicos y Éticos** (obligatoria).
- **Autonomía de centro** (art. 15.3): Segunda Lengua Extranjera (5.º–6.º); área de profundización; área de refuerzo.
- **Religión**: oferta obligada, elección voluntaria. Quien no la curse → área de proyectos significativos (valores/tradición/cultura de CyL).

### Bloques / saberes básicos por área (nivel alto)

#### CIENCIAS DE LA NATURALEZA

- **1º**: A. Cultura científica; B. Tecnología y digitalización; C. Conciencia ecosocial
- **2º**: A. Cultura científica; B. Tecnología y digitalización; C. Conciencia ecosocial
- **3º**: A. Cultura científica; B. Tecnología y digitalización
- **4º**: A. Cultura científica; B. Tecnología y digitalización; C. Conciencia ecosocial
- **5º**: A. Cultura científica; B. Tecnología y digitalización; C. Conciencia ecosocial
- **6º**: A. Cultura científica; B. Tecnología y digitalización; C. Conciencia ecosocial

#### CIENCIAS SOCIALES

- **1º**: A. Cultura científica; B. Tecnología y digitalización; C. Sociedades y territorios
- **2º**: A. Cultura científica; B. Tecnología y digitalización; C. Sociedades y territorios
- **3º**: A. Cultura científica; B. Tecnología y digitalización; C. Sociedades y territorios
- **4º**: A. Cultura científica; B. Tecnología y digitalización; C. Sociedades y territorios
- **5º**: A. Cultura científica; B. Tecnología y digitalización; C. Sociedades y territorios
- **6º**: A. Cultura científica; B. Tecnología y digitalización; C. Sociedades y territorios

#### EDUCACIÓN PLÁSTICA Y VISUAL

- **1º**: A. Recepción, análisis y reflexión; B. Experimentación, creación y comunicación
- **2º**: A. Recepción, análisis y reflexión; B. Experimentación, creación y comunicación
- **3º**: A. Recepción, análisis y reflexión; B. Experimentación, creación y comunicación
- **4º**: A. Recepción, análisis y reflexión; B. Experimentación, creación y comunicación
- **5º**: A. Recepción, análisis y reflexión; B. Experimentación, creación y comunicación
- **6º**: A. Recepción, análisis y reflexión; B. Experimentación, creación y comunicación

#### MÚSICA Y DANZA

- **1º**: A. Recepción, análisis y reflexión; B. Experimentación, creación e interpretación
- **2º**: A. Recepción, análisis y reflexión; B. Experimentación, creación e interpretación
- **3º**: A. Recepción, análisis y reflexión; B. Experimentación, creación e interpretación
- **4º**: A. Recepción, análisis y reflexión; B. Experimentación, creación e interpretación
- **5º**: A. Recepción, análisis y reflexión; B. Experimentación, creación e interpretación
- **6º**: A. Recepción, análisis y reflexión; B. Experimentación, creación e interpretación

#### EDUCACIÓN FÍSICA

- **1º**: A. Vida activa y saludable; B. Organización y gestión de la actividad física; C. Resolución de problemas en situaciones motrices; D. Autorregulación emocional e interacción social en situaciones motrices; E. Manifestaciones de la cultura motriz; F. Interacción eficiente y sostenible con el entorno; G. Información, digitalización y comunicación
- **2º**: A. Vida activa y saludable; B. Organización y gestión de la actividad física; C. Resolución de problemas en situaciones motrices; D. Autorregulación emocional e interacción social en situaciones motrices; E. Manifestaciones de la cultura motriz; F. Interacción eficiente y sostenible con el entorno; G. Información, digitalización y comunicación
- **3º**: A. Vida activa y saludable; B. Organización y gestión de la actividad física; C. Resolución de problemas en situaciones motrices; D. Autorregulación emocional e interacción social en situaciones motrices; E. Manifestaciones de la cultura motriz; F. Interacción eficiente y sostenible con el entorno; G. Información, digitalización y comunicación
- **4º**: A. Vida activa y saludable; B. Organización y gestión de la actividad física; C. Resolución de problemas en situaciones motrices; D. Autorregulación emocional e interacción social en situaciones motrices; E. Manifestaciones de la cultura motriz; F. Interacción eficiente y sostenible con el entorno; G. Información, digitalización y comunicación
- **5º**: A. Vida activa y saludable; B. Organización y gestión de la actividad física; C. Resolución de problemas en situaciones motrices; D. Autorregulación emocional e interacción social en situaciones motrices; E. Manifestaciones de la cultura motriz; F. Interacción eficiente y sostenible con el entorno; G. Información, digitalización y comunicación
- **6º**: A. Vida activa y saludable; B. Organización y gestión de la actividad física; C. Resolución de problemas en situaciones motrices; D. Autorregulación emocional e interacción social en situaciones motrices; E. Manifestaciones de la cultura motriz; F. Interacción eficiente y sostenible con el entorno; G. Información, digitalización y comunicación

#### LENGUA CASTELLANA Y LITERATURA

- **1º**: A. Las lenguas y sus hablantes; B. Comunicación; C. Educación literaria; D. Reflexión sobre la lengua y sus usos en el marco de propuestas de producción y
- **2º**: A. Las lenguas y sus hablantes; B. Comunicación; C. Educación literaria; D. Reflexión sobre la lengua y sus usos en el marco de propuestas de producción y
- **3º**: A. Las lenguas y sus hablantes; B. Comunicación; C. Educación literaria; D. Reflexión sobre la lengua y sus usos en el marco de propuestas de producción y
- **4º**: A. Las lenguas y sus hablantes; B. Comunicación; C. Educación literaria; D. Reflexión sobre la lengua y sus usos en el marco de propuestas de producción y
- **5º**: A. Las lenguas y sus hablantes; B. Comunicación; C. Educación literaria; D. Reflexión sobre la lengua y sus usos en el marco de propuestas de producción y
- **6º**: A. Las lenguas y sus hablantes; B. Comunicación; C. Educación literaria; D. Reflexión sobre la lengua y sus usos en el marco de propuestas de producción y

#### LENGUA EXTRANJERA

- **1º**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad
- **2º**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad
- **3º**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad
- **4º**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad
- **5º**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad
- **6º**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad

#### MATEMÁTICAS

- **1º**: A. Sentido numérico; B. Sentido de la medida; C. Sentido espacial; D. Sentido algebraico; E. Sentido estocástico; F. Sentido socioafectivo
- **2º**: A. Sentido numérico; B. Sentido de la medida; C. Sentido espacial; D. Sentido algebraico; E. Sentido estocástico; F. Sentido socioafectivo
- **3º**: A. Sentido numérico; B. Sentido de la medida; C. Sentido espacial; D. Sentido algebraico; E. Sentido estocástico; F. Sentido socioafectivo
- **4º**: A. Sentido numérico; B. Sentido de la medida; C. Sentido espacial; D. Sentido algebraico; E. Sentido estocástico; F. Sentido socioafectivo
- **5º**: A. Sentido numérico; B. Sentido de la medida; C. Sentido espacial; D. Sentido algebraico; E. Sentido estocástico; F. Sentido socioemocional
- **6º**: A. Sentido numérico; B. Sentido de la medida; C. Sentido espacial; D. Sentido algebraico; E. Sentido estocástico; F. Sentido socioafectivo

#### EDUCACIÓN EN VALORES CÍVICOS Y ÉTICOS

- **Obligatoria en 6.º**. Bloques según decreto:
- **6º**: A. Autoconocimiento y autonomía moral; B. Sociedad, justicia y democracia; C. Desarrollo sostenible y ética ambiental

---

## 6. ESO (Decreto 39/2022)

### 6.1 Organización por curso (arts. 15–17)

#### 1º ESO — materias que cursa todo el alumnado (**obligatorias**)

| # | Materia | Tipo |
|---|---|---|
| 1 | Biología y Geología | Obligatoria |
| 2 | Educación Física | Obligatoria |
| 3 | Educación Plástica, Visual y Audiovisual | Obligatoria |
| 4 | Geografía e Historia | Obligatoria |
| 5 | Lengua Castellana y Literatura | Obligatoria |
| 6 | Lengua Extranjera | Obligatoria |
| 7 | Matemáticas | Obligatoria |
| 8 | Tecnología y Digitalización | Obligatoria |

**Optativa (elegir 1):** Conocimiento de las Matemáticas | Conocimiento del Lenguaje | Segunda Lengua Extranjera.  
Refuerzo instrumental (si carencias): Conocimiento de las Matemáticas o del Lenguaje.  
+ Tutoría; Religión (elección) / Alternativa CyL.

#### 2º ESO — obligatorias

| # | Materia | Tipo |
|---|---|---|
| 1 | Educación Física | Obligatoria |
| 2 | Física y Química | Obligatoria |
| 3 | Geografía e Historia | Obligatoria |
| 4 | Lengua Castellana y Literatura | Obligatoria |
| 5 | Lengua Extranjera | Obligatoria |
| 6 | Matemáticas | Obligatoria |
| 7 | Música | Obligatoria |

**Además:** Cultura Clásica (**obligatoria en 2.º** según art. 15.2.b) **y** una optativa entre: Conocimiento de las Matemáticas | Conocimiento del Lenguaje | Segunda Lengua Extranjera.  
+ Tutoría; Religión/Alternativa.

#### 3º ESO — obligatorias

| # | Materia | Tipo |
|---|---|---|
| 1 | Biología y Geología | Obligatoria |
| 2 | Educación en Valores Cívicos y Éticos | Obligatoria |
| 3 | Educación Física | Obligatoria |
| 4 | Física y Química | Obligatoria |
| 5 | Geografía e Historia | Obligatoria |
| 6 | Lengua Castellana y Literatura | Obligatoria |
| 7 | Lengua Extranjera | Obligatoria |
| 8 | Matemáticas | Obligatoria |
| 9 | Música **o** Educación Plástica, Visual y Audiovisual | Obligatoria (elección) |
| 10 | Tecnología y Digitalización | Obligatoria |

**Optativa (1):** Conocimiento de las Matemáticas | Conocimiento del Lenguaje | Control y Robótica | Iniciación a la Actividad Emprendedora y Empresarial | Resolución de Problemas | Segunda Lengua Extranjera | Taller de Artes Plásticas | Taller de Expresión Musical.

#### 4º ESO (art. 16)

**Comunes obligatorias:** Educación Física; Geografía e Historia; Lengua Castellana y Literatura; Lengua Extranjera; **Matemáticas A o Matemáticas B**.

**Elegir 2** entre: Biología y Geología; Economía y Emprendimiento; Física y Química; Latín.

**Elegir 1** entre: Digitalización; Expresión Artística; Formación y Orientación Personal y Profesional; Música; Segunda Lengua Extranjera; Tecnología.

**Optativa (1)** entre: Conocimiento de las Matemáticas; Conocimiento del Lenguaje; Cultura Científica; Cultura Clásica; Educación Financiera; Formación para la Empresa y el Empleo; Geografía Económica; Laboratorio de Ciencias; Lengua y Cultura Gallega*; Literatura Universal; Programación Informática; Taller de Artes Escénicas; Taller de Filosofía.  
\* Solo centros del programa de lengua gallega. Lengua y Cultura China: previa solicitud.

### 6.2 Bloques / saberes por materia (Anexo III)

#### BIOLOGÍA Y GEOLOGÍA

- **1º ESO**: A. Proyecto científico; B. Geosfera; C. Atmósfera e hidrosfera; D. La célula; E. Seres vivos; F. Ecología y sostenibilidad
- **3º ESO**: A. Proyecto científico; B. Geología; C. La célula; D. Cuerpo humano; E. Hábitos saludables; F. Salud y enfermedad
- **4º ESO**: A. Proyecto científico; B. La célula; C. Genética y evolución; D. Geología; E. La Tierra en el universo

#### CONOCIMIENTO DE LAS MATEMÁTICAS

- **1º ESO**: A. Sentido numérico; B. Sentido de la medida; C. Sentido espacial; D. Sentido algebraico
- **2º ESO**: A. Sentido numérico; B. Sentido de la medida; C. Sentido espacial; D. Sentido algebraico; E. Sentido estocástico
- **3º ESO**: A. Sentido numérico; B. Sentido espacial; C. Sentido algebraico; D. Sentido estocástico
- **4º ESO**: A. Sentido numérico; B. Sentido de la medida; C. Sentido espacial; D. Sentido algebraico; E. Sentido estocástico

#### CONOCIMIENTO DEL LENGUAJE

- **1º ESO**: A. Comunicación; B. Educación literaria; C. Reflexión sobre la lengua
- **2º ESO**: A. Comunicación; B. Educación literaria; C. Reflexión sobre la lengua
- **3º ESO**: A. Comunicación; B. Educación Literaria; C. Reflexión sobre la lengua
- **4º ESO**: A. Comunicación; B. Educación literaria; C. Reflexión sobre la lengua

#### CONTROL Y ROBÓTICA

- **3º ESO**: A. Fundamentos de los sistemas automáticos de control; B. Fundamentos de electrónica aplicados a la robótica; C. Programación asociada a Control y Robótica

#### CULTURA CIENTÍFICA

- **(según curso de oferta)**: A. Procedimientos de trabajo; B. La Tierra: características y curiosidades; C. La vida en la Tierra; D. Medio ambiente e impactos ambientales; E. Nuevas Tecnologías de la Información y Comunicación; F. Proyecto de investigación

#### CULTURA CLÁSICA

- **2º ESO**: A. La actualidad de la civilización clásica; B. Lenguas clásicas y plurilingüismo; C. Educación artística y literaria; D. Legado y patrimonio
- **4º ESO**: A. Las antiguas civilizaciones de Grecia y Roma; B. Lenguas clásicas y plurilingüismo; C. Educación artística y literaria; D. Legado y patrimonio

#### DIGITALIZACIÓN

- **(según curso de oferta)**: A. Dispositivos digitales, sistemas operativos y de comunicación; B. Digitalización del entorno personal de aprendizaje; C. Seguridad y bienestar digital; D. Ciudadanía digital crítica

#### ECONOMÍA Y EMPRENDIMIENTO

- **(según curso de oferta)**: A. El perfil de la persona emprendedora, iniciativa y creatividad; B. El entorno como fuente de ideas y oportunidades; C. Recursos para llevar a cabo un proyecto emprendedor; D. La realización del proyecto emprendedor

#### EDUCACIÓN EN VALORES CÍVICOS Y ÉTICOS

- **(según curso de oferta)**: A. Autoconocimiento y autonomía moral; B. Sociedad, justicia y democracia, y Derecho; C. Sostenibilidad y ética ambiental

#### EDUCACIÓN FINANCIERA

- **(según curso de oferta)**: A. La economía y las finanzas personales; B. La Macroeconomía y las finanzas en un mundo global; C. Aspectos financieros de la economía regional en el contexto global

#### EDUCACIÓN FÍSICA

- **1º ESO**: A. Vida activa y saludable; B. Organización y gestión de la actividad física; C. Resolución de problemas en situaciones motrices; D. Autorregulación emocional e interacción social en situaciones motrices; E. Manifestaciones de la cultura motriz; F. Interacción eficiente y sostenible con el entorno
- **2º ESO**: A. Vida activa y saludable; B. Organización y gestión de la actividad física; C. Resolución de problemas en situaciones motrices; D. Autorregulación emocional e interacción social en situaciones motrices; E. Manifestaciones de la cultura motriz; F. Interacción eficiente y sostenible con el entorno
- **3º ESO**: A. Vida activa y saludable; B. Organización y gestión de la actividad física; C. Resolución de problemas en situaciones motrices; D. Autorregulación emocional e interacción social en situaciones motrices; E. Manifestaciones de la cultura motriz; F. Interacción eficiente y sostenible con el entorno
- **4º ESO**: A. Vida activa y saludable; B. Organización y gestión de la actividad física; C. Resolución de problemas en situaciones motrices; D. Autorregulación emocional e interacción social en situaciones motrices; E. Manifestaciones de la cultura motriz; F. Interacción eficiente y sostenible con el entorno

#### EDUCACIÓN PLÁSTICA, VISUAL Y AUDIOVISUAL

- **1º ESO**: A. Patrimonio artístico y cultural. Apreciación estética y análisis; B. Elementos formales de la imagen y del lenguaje visual. La expresión gráfica; C. Expresión artística y gráfico-plástica. Técnicas y procedimientos; D. Imagen y comunicación visual y audiovisual
- **3º ESO**: A. Patrimonio artístico y cultural. Apreciación estética y análisis; B. Elementos formales de la imagen y del lenguaje visual. La expresión gráfica; C. Expresión artística y gráfico-plástica. Técnicas y procedimientos; D. Imagen y comunicación visual y audiovisual

#### EXPRESIÓN ARTÍSTICA

- **(según curso de oferta)**: A. Técnicas gráfico-plásticas; B. Fotografía, lenguaje visual, audiovisual y multimedia; C. Patrimonio artístico y cultural

#### FÍSICA Y QUÍMICA

- **2º ESO**: A. Las destrezas científicas básicas; B. La materia; C. La energía; D. La interacción
- **3º ESO**: A. Las destrezas científicas básicas; B. La materia; C. La energía; D. La interacción; E. El cambio
- **4º ESO**: A. Las destrezas científicas básicas; B. La materia; C. La energía; D. La interacción; E. El cambio

#### FORMACIÓN PARA LA EMPRESA Y EL EMPLEO

- **(según curso de oferta)**: A. Mundo laboral y oportunidades de empleo; B. La empresa y la iniciativa empresarial; C. Finanzas dentro de la empresa

#### FORMACIÓN Y ORIENTACIÓN PERSONAL Y PROFESIONAL

- **4º ESO**: A. El ser humano y el conocimiento de uno mismo; B. Aprendizaje y desarrollo: habilidades personales y sociales. Formación y orientación; C. Orientación hacia la formación académica y profesional. Exploración del entorno; D. Proyecto personal, académico-profesional y aproximación a la búsqueda activa de

#### GEOGRAFÍA E HISTORIA

- **1º ESO**: A. Retos del mundo actual; B. Sociedades y territorios; C. Compromiso Cívico
- **2º ESO**: A. Retos del mundo actual; B. Sociedades y territorios; C. Compromiso cívico
- **3º ESO**: A. Retos del mundo actual; B. Sociedades y territorios; C. Compromiso cívico local y global
- **4º ESO**: A. Retos del mundo actual; B. Sociedades y territorios; C. Compromiso cívico, local y global

#### GEOGRAFÍA ECONÓMICA

- **(según curso de oferta)**: A. Retos del mundo actual; B. Sociedades y territorios

#### INICIACIÓN A LA ACTIVIDAD EMPRENDEDORA Y EMPRESARIAL

- **(según curso de oferta)**: A. Habilidades emprendedoras básicas; B. Finanzas básicas; C. Retos sociales a los que se enfrenta la ciudadanía global

#### LABORATORIO DE CIENCIAS

- **(según curso de oferta)**: A. El trabajo en el laboratorio; B. Física; C. Química; D. Biología; E. Geología; F. La Tierra en el Universo

#### LATÍN

- **(según curso de oferta)**: A. El presente de la civilización latina; B. Latín y plurilingüismo; C. El texto latino y la traducción; D. Legado y patrimonio

#### LENGUA CASTELLANA Y LITERATURA

- **1º ESO**: A. Las lenguas y sus hablantes; B. Comunicación; C. Educación Literaria; D. Reflexión sobre la lengua
- **2º ESO**: A. Las lenguas y sus hablantes; B. Comunicación; C. Educación literaria; D. Reflexión sobre la lengua
- **3º ESO**: A. Las lenguas y sus hablantes; B. Comunicación; C. Educación literaria; D. Reflexión sobre la lengua
- **4º ESO**: A. Las lenguas y sus hablantes; B. Comunicación; C. Educación literaria; D. Reflexión sobre la lengua

#### LENGUA EXTRANJERA

- **1º ESO**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad
- **2º ESO**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad
- **3º ESO**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad
- **4º ESO**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad

#### LENGUA Y CULTURA CHINA

- **1º ESO**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad
- **2º ESO**: B. Plurilingüismo; C. Interculturalidad
- **3º ESO**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad
- **4º ESO**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad

#### LITERATURA UNIVERSAL

- **(según curso de oferta)**: A. Lectura colectiva y elaboración guiada de una interpretación de los clásicos de la; B. Lectura autónoma de obras relevantes del patrimonio universal desarrollando las; C. Estrategias de selección, análisis, interpretación, recreación y valoración crítica de

#### MATEMÁTICAS

- **1º ESO**: A. Sentido numérico; B. Sentido de la medida; C. Sentido espacial; D. Sentido algebraico; E. Sentido socioafectivo
- **2º ESO**: A. Sentido numérico; B. Sentido de la medida; C. Sentido espacial; D. Sentido algebraico; E. Sentido estocástico; F. Sentido socioafectivo
- **3º ESO**: A. Sentido numérico; B. Sentido espacial; C. Sentido algebraico; D. Sentido estocástico; E. Sentido socioafectivo
- **4º ESO Matemáticas A**: A. Sentido numérico; B. Sentido de la medida; C. Sentido espacial; D. Sentido algebraico; E. Sentido estocástico; F. Sentido socioafectivo
- **4º ESO Matemáticas B**: A. Sentido numérico; B. Sentido de la medida; C. Sentido espacial; D. Sentido algebraico; E. Sentido estocástico; F. Sentido socioafectivo

#### MÚSICA

- **2º ESO**: A. Escucha y percepción; B. Interpretación, improvisación y creación escénica; C. Contextos y culturas
- **3º ESO**: A. Escucha y percepción; B. Interpretación, improvisación y creación escénica; C. Contextos y culturas
- **4º ESO**: A. Escucha y percepción; B. Interpretación, improvisación y creación escénica; C. Contextos y culturas

#### PROGRAMACIÓN INFORMÁTICA

- **(según curso de oferta)**: A. Introducción a la programación; B. Entornos de programación gráfica por bloques; C. Lenguajes de programación mediante código

#### RESOLUCIÓN DE PROBLEMAS

- **(según curso de oferta)**: A. La resolución de problemas como proceso; B. Lógica y estrategia; C. Modelos matemáticos

#### SEGUNDA LENGUA EXTRANJERA

- **1º ESO**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad
- **2º ESO**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad
- **3º ESO**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad
- **4º ESO**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad

#### TALLER DE ARTES ESCÉNICAS

- **(según curso de oferta)**: A. El personaje; B. El espacio; C. La acción; D. El texto; E. Medios expresivos no específicos; F. El montaje; G. Las técnicas de trabajo

#### TALLER DE ARTES PLÁSTICAS

- **(según curso de oferta)**: A. El proyecto creativo; D. Técnicas digitales aplicables para la expresión artística; B. Técnicas de Expresión Bidimensionales; C. Técnicas de Expresión Tridimensionales

#### TALLER DE EXPRESIÓN MUSICAL

- **(según curso de oferta)**: A. Técnica vocal, instrumental y de expresión corporal; B. Creación musical; C. Actitudes para la práctica e interpretación musical

#### TALLER DE FILOSOFÍA

- **(según curso de oferta)**: A. La Filosofía y el pensamiento crítico; B. El ser humano, el conocimiento y la realidad; C. La acción

#### TECNOLOGÍA

- **(según curso de oferta)**: A. Proceso de resolución de problemas. Estrategias y técnicas:; B. Operadores tecnológicos; C. Pensamiento computacional, automatización y robótica; D. Tecnología Sostenible

#### TECNOLOGÍA Y DIGITALIZACIÓN

- **1º ESO**: A. Proceso de resolución de problemas; B. Comunicación y difusión de ideas; C. Pensamiento computacional, programación y robótica; D. Digitalización del entorno personal de aprendizaje
- **3º ESO**: A. Proceso de resolución de problemas; B. Comunicación y difusión de ideas; C. Pensamiento computacional, programación y robótica; D. Digitalización del entorno personal de aprendizaje; E. Tecnología sostenible

---

## 7. Bachillerato (Decreto 40/2022)

### Modalidades (art. 14)

- **Artes** → vías: Artes Plásticas, Imagen y Diseño | Música y Artes Escénicas
- **Ciencias y Tecnología**
- **General**
- **Humanidades y Ciencias Sociales**

Tipos de materias: **comunes**, **específicas de modalidad**, **optativas**. Religión: oferta obligada / elección (arts. 15–21).

### Materias comunes (todas las modalidades)

| Curso | Comunes |
|---|---|
| 1º | Educación Física; Filosofía; Lengua Castellana y Literatura I; Lengua Extranjera I |
| 2º | Historia de España; Historia de la Filosofía; Lengua Castellana y Literatura II; Lengua Extranjera II |

### Ciencias y Tecnología (art. 17) — resumen

- **1º**: específica ancla **Matemáticas I** + 2 entre BGCA; Dibujo Técnico I; Física y Química; Tecnología e Ingeniería I. Optativas según decreto (Anatomía Aplicada, Economía, FyQ si no elegida, Cultura Científica, Religión, 2.ª LE I, TIC I…).
- **2º**: ancla **Matemáticas II** o **Matemáticas Aplicadas a las CCSS II** + 2 entre Biología; Dibujo Técnico II; Física; Geología y Ciencias Ambientales; Química; Tecnología e Ingeniería II (+ optativas).

### Humanidades y Ciencias Sociales (art. 19) — resumen

- **1º**: ancla **Latín I** o **Matemáticas Aplicadas a las CCSS I** + 2 entre Economía; Griego I; Historia del Mundo Contemporáneo; Latín I / Mate CCSS I (si no ancla); Literatura Universal.
- **2º**: ancla **Latín II** o **Mate CCSS II** + 2 entre Empresa y Diseño de Modelos de Negocio; Geografía; Griego II; Historia del Arte; Latín II / Mate CCSS II.

### General (art. 18) — resumen

- **1º**: ancla **Matemáticas Generales** + 2 específicas (oferta del centro; incluye obligatoriamente Economía, Emprendimiento y Actividad Empresarial en la oferta).
- **2º**: ancla **Ciencias Generales** + 2 (oferta con Movimientos Culturales y Artísticos obligatorio en oferta).

### Artes — ver arts. 15–16 del Decreto 40/2022 (Dibujo Artístico I/II u otras anclas según vía; volumen, proyectos, análisis musical, etc.).

### Bloques / saberes (Anexo III) — materias principales

#### MATEMÁTICAS

- **1º Bach**: A. Sentido numérico; B. Sentido de la medida; C. Sentido espacial; D. Sentido algebraico; E. Sentido estocástico; F. Sentido socioafectivo
- **2º Bach**: A. Sentido numérico; B. Sentido de la medida; C. Sentido espacial; D. Sentido algebraico; E. Sentido estocástico; F. Sentido socioafectivo

#### MATEMÁTICAS APLICADAS A LAS CIENCIAS SOCIALES

- **1º Bach**: A. Sentido numérico; B. Sentido de la medida; C. Sentido algebraico; D. Sentido estocástico; E. Sentido socioafectivo
- **2º Bach**: A. Sentido numérico; B. Sentido de la medida; C. Sentido algebraico; D. Sentido Estocástico; E. Sentido socioafectivo

#### MATEMÁTICAS GENERALES

- **I/II según decreto**: A. Sentido numérico; B. Sentido de la medida; C. Sentido espacial; D. Sentido algebraico y pensamiento computacional; E. Sentido estocástico; F. Sentido socioafectivo

#### FÍSICA

- **I/II según decreto**: A. Campo gravitatorio; B. Campo electromagnético; C. Vibraciones y ondas; D. Física relativista, cuántica, nuclear y de partículas

#### QUÍMICA

- **I/II según decreto**: A. Enlace químico y estructura de la materia; B. Reacciones químicas; C. Química orgánica

#### FÍSICA Y QUÍMICA

- **I/II según decreto**: A. Enlace químico y estructura de la materia; B. Reacciones químicas; C. Química orgánica; D. Cinemática; E. Estática y dinámica; F. Energía

#### BIOLOGÍA

- **I/II según decreto**: A. Biomoléculas; B. Genética molecular; C. Biología celular; D. Metabolismo; E. Biotecnología; F. Inmunología

#### BIOLOGÍA, GEOLOGÍA Y CIENCIAS AMBIENTALES

- **I/II según decreto**: A. Proyecto científico; B. Ecología y sostenibilidad; C. Historia de la Tierra y la vida; D. La dinámica y composición terrestres; E. Fisiología e histología animal; F. Fisiología e histología vegetal; G. Los microorganismos y formas acelulares

#### CIENCIAS GENERALES

- **I/II según decreto**: A. Construyendo ciencia; B. Un universo de materia y energía; C. El sistema Tierra; D. Biología para el siglo XXI; E. Las fuerzas que nos mueven

#### LENGUA CASTELLANA Y LITERATURA

- **I/II según decreto**: A. Las lenguas y sus hablantes; B. Comunicación; C. Educación literaria; D. Reflexión sobre la lengua

#### LENGUA EXTRANJERA

- **I/II según decreto**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad

#### FILOSOFÍA

- **I/II según decreto**: A. La filosofía y el ser humano; B. Conocimiento y realidad; C. Acción y creación

#### HISTORIA DE ESPAÑA

- **I/II según decreto**: A. Sociedades en el tiempo; B. Retos del mundo actual; C. Compromiso cívico

#### HISTORIA DE LA FILOSOFÍA

- **I/II según decreto**: A. Del origen de la filosofía en Grecia de hasta el fin de la antigüedad; B. De la Edad Media a la Modernidad europea; C. De la modernidad a la postmodernidad

#### EDUCACIÓN FÍSICA

- **I/II según decreto**: A. Vida activa y saludable; B. Organización y gestión de la actividad física; C. Resolución de problemas en situaciones motrices; D. Autorregulación emocional e interacción social en situaciones motrices; E. Manifestaciones de la cultura motriz; F. Interacción eficiente y sostenible con el entorno

#### ECONOMÍA

- **I/II según decreto**: A. Las decisiones económicas; B. La realidad económica. Herramientas para entender el mundo con una visión; C. La realidad económica. Herramientas para entender el mundo con una visión; D. Las políticas económicas; E. Los retos de la economía española en un contexto globalizado

#### EMPRESA Y DISEÑO DE MODELOS DE NEGOCIO

- **I/II según decreto**: A. La empresa y su entorno; B. El modelo de negocio y de gestión; C. Herramientas para innovar en modelos de negocio y de gestión; D. Estrategia empresarial y métodos de análisis de la realidad empresarial: estudio

#### GEOGRAFÍA

- **I/II según decreto**: A. España, Europa y la Globalización; B. La sostenibilidad del medio físico en España; C. La ordenación del territorio en el enfoque ecosocial

#### HISTORIA DEL MUNDO CONTEMPORÁNEO

- **I/II según decreto**: C. Compromiso cívico; B. Plurilingüismo; D. La antigua Roma; E. Legado y patrimonio; A. Traducción

#### HISTORIA DEL ARTE

- **I/II según decreto**: A. Aproximación y funciones de la Historia del Arte; B. El arte a lo largo de la historia; C. Dimensión individual y social del arte; D. Realidad, espacio y territorio en el arte

#### GRIEGO

- **I/II según decreto**: A. El texto: comprensión y traducción; B. Plurilingüismo; C. Educación literaria; E. Legado y patrimonio; D. La antigua Grecia

#### GRIEGO

- **I/II según decreto**: A. El texto: comprensión y traducción; B. Plurilingüismo; C. Educación literaria; E. Legado y patrimonio; D. La antigua Grecia

#### DIBUJO TÉCNICO

- **I/II según decreto**: A. Fundamentos geométricos; B. Geometría proyectiva; C. Normalización y documentación gráfica de proyectos; D. Sistemas CAD

#### TECNOLOGÍA E INGENIERÍA

- **I/II según decreto**: A. Proyectos de investigación y desarrollo; B. Materiales y fabricación; C. Sistemas mecánicos; D. Sistemas eléctricos y electrónicos; F. Sistemas automáticos; G. Tecnología sostenible; E. Sistemas informáticos emergentes

#### TECNOLOGÍAS DE LA INFORMACIÓN Y LA COMUNICACIÓN

- **2º Bach**: A. Proyecto TIC. Publicación y difusión de contenidos; B. Digitalización del entorno personal de aprendizaje; C. Programación

#### GEOLOGÍA Y CIENCIAS AMBIENTALES

- **I/II según decreto**: A. Experimentación en Geología y Ciencias Ambientales; B. Estructura interna terrestre, tectónica de placas y geodinámica interna; C. Minerales, los componentes de las rocas; D. Rocas ígneas, sedimentarias y metamórficas; E. Procesos geológicos externos; F. Geología histórica; G. Capas fluidas de la Tierra; H. Ecología, humanidad y medio ambiente; I. Gestión sostenible de los recursos naturales

#### PSICOLOGÍA

- **I/II según decreto**: A. La psicología como ciencia; B. Fundamentos biológicos de la conducta; C. Los procesos cognitivos básicos: percepción, atención y memoria; D. Procesos cognitivos superiores: aprendizaje, inteligencia y pensamiento; E. La construcción del ser humano. Motivación, personalidad y afectividad; F. Psicología social y de las organizaciones

#### CULTURA CIENTÍFICA

- **I/II según decreto**: A. Ciencia y sociedad; B. Biomedicina y calidad de vida; C. Revolución genética; D. Desarrollo tecnológico, materiales y medio ambiente; E. El universo; F. Proyecto de investigación

#### ANÁLISIS MUSICAL

- **I/II según decreto**: B. La forma musical; A. Técnicas de análisis musical

#### ANATOMÍA APLICADA

- **I/II según decreto**: A. Organización básica del cuerpo humano; B. Sistema de aporte y utilización de energía y excreción; C. Sistema cardiopulmonar; D. Sistemas de recepción, coordinación y regulación; E. Sistema locomotor; F. Aparatos reproductores; G. Características del movimiento, expresión y comunicación corporal; H. Elementos comunes

#### ARTES ESCÉNICAS

- **I/II según decreto**: A. Patrimonio escénico; B. Expresión y comunicación escénica; D. Representación y escenificación; E. Recepción en las artes escénicas; C. Interpretación

#### CORO Y TÉCNICA VOCAL

- **I/II según decreto**: A. Análisis; B. Técnica vocal; C. Práctica de conjunto

#### CULTURA AUDIOVISUAL

- **I/II según decreto**: A. Hitos y contemporaneidad de la fotografía y el audiovisual. Formatos; B. Elementos formales y capacidad expresiva de la imagen fotográfica y el; C. Narrativa audiovisual; D. La producción audiovisual. Técnicas y procedimientos

#### DIBUJO ARTÍSTICO

- **I/II según decreto**: A. Concepto e historia del dibujo; B. La expresión gráfica y sus recursos elementales; D. La luz, el claroscuro y el color; F. Proyectos gráficos colaborativos; C. Dibujo y espacio; E. La figura humana

#### DIBUJO TÉCNICO APLICADO A LAS ARTES PLÁSTICAS Y AL DISEÑO

- **I/II según decreto**: A. Geometría, arte y entorno; B. Sistemas de representación del espacio aplicado; C. Normalización y diseño de proyectos; D. Herramientas digitales para el diseño

#### DISEÑO

- **I/II según decreto**: A. Concepto, historia y campos del diseño; B. El diseño: configuración formal y metodología; C. Diseño gráfico; D. Diseño tridimensional

#### ECONOMÍA, EMPRENDIMIENTO Y ACTIVIDAD EMPRESARIAL

- **I/II según decreto**: A. Economía; B. Emprendimiento; C. Actividad empresarial

#### FUNDAMENTOS ARTÍSTICOS

- **I/II según decreto**: A. Los fundamentos del arte; B. Visión, realidad y representación; C. El arte clásico y sus proyecciones; D. Arte y expresión; E. Naturaleza, sociedad y comunicación en el arte; F. Metodologías y estrategias

#### FUNDAMENTOS DE ADMINISTRACIÓN Y GESTIÓN

- **I/II según decreto**: A. La innovación e idea de negocio. El proyecto de empresa; B. Decisiones para iniciar un proyecto emprendedor global en un contexto local; C. Estudio y diseño de las áreas funcionales de la empresa; D. Comunicación y presentación del proyecto emprendedor

#### HISTORIA DE LA MÚSICA Y DE LA DANZA

- **I/II según decreto**: A. Percepción visual y auditiva; B. Contextos de creación; C. Investigación, opinión crítica y difusión; D. Experimentación activa

#### LENGUAJE Y PRÁCTICA MUSICAL

- **I/II según decreto**: A. Lenguaje musical; B. Práctica musical

#### LITERATURA DRAMÁTICA

- **I/II según decreto**: A. Construcción, guiada y compartida, de la interpretación de algunos textos relevantes; B. Recepción autónoma de obras relevantes de la literatura dramática y participación en

#### LITERATURA UNIVERSAL

- **I/II según decreto**: A. Construcción guiada y compartida de la interpretación de algunos clásicos de la; B. Lectura autónoma de obras relevantes del patrimonio universal desarrollando las

#### MOVIMIENTOS CULTURALES Y ARTÍSTICOS

- **I/II según decreto**: A. Aspectos generales; B. Naturaleza, arte y cultura; C. El arte dentro del arte; D. El arte en los espacios urbanos; E. Lenguajes artísticos contemporáneos

#### PROYECTOS ARTÍSTICOS

- **I/II según decreto**: A. Nociones básicas sobre la creación artística y el patrimonio; B. La creatividad. Entornos de trabajo creativos; C. Gestión de proyectos artísticos

#### SEGUNDA LENGUA EXTRANJERA

- **I/II según decreto**: A. Comunicación; B. Plurilingüismo; C. Interculturalidad

#### TÉCNICAS DE EXPRESIÓN GRÁFICO-PLÁSTICA

- **I/II según decreto**: A. Aspectos generales; B. Técnicas de dibujo; C. Técnicas de pintura; D. Técnicas de grabado y estampación; E. Técnicas mixtas y alternativas; F. Proyectos gráfico-plásticos

#### VOLUMEN

- **I/II según decreto**: A. Técnicas y materiales de configuración; B. Elementos de configuración formal y espacial; C. Análisis de la representación tridimensional; D. El volumen en el proceso de diseño

---

## 8. Notas para expansión a lecciones

- Los **bloques/sentidos** del Anexo III son la unidad de inventariado; las lecciones se derivan de los ítems numerados bajo cada bloque (conteo, cantidad, operaciones…).
- El sentido **socioafectivo** es transversal: no suele ser una UD aislada, sino integrado.
- CyL a menudo **adelanta o detalla** saberes respecto al mínimo estatal (p. ej. Tales/Pitágoras aparecen en contenidos de 1º ESO Matemáticas CyL).
- Documento hermano: `01-eso-matematicas-lecciones-borrador.md` (borrador pendiente de OK de Jorge).

## 9. Ambiguidades abiertas

1. **Idioma de Lengua Extranjera / 2.ª LE**: no fijado en el decreto; bots deben parametrizar idioma.
2. **Oferta real de optativas y modalidades**: depende del centro; el inventario lista el marco legal completo.
3. **Religión**: currículos confesionales (BOE) vs alternativa CyL de proyectos; bot «Alternativa a la Religión» es específico CyL.
4. **Actualizaciones post-2022**: revalidar BOCyL antes de escribir contenido largo; PDFs fuente en `profesor-temario/fuentes/`.
5. **Primaria**: bloques de CN/CS CyL usan etiquetas «Cultura científica / Tecnología y digitalización / …» (estructura propia CyL sobre el RD 157/2022).

### Publicación completa (Les vencimos)

- **1º ESO Educación Plástica, Visual y Audiovisual**: pack completo L01–L31/31 (hub + ZIP offline). Revisor Dios CONFIRMA (0 críticos).
