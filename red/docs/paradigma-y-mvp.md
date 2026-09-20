# Nuevo Internet — Paradigma y MVP

## Analogía (para qué existe)
Esta red es **la bicicleta / el coche para ir de un sitio a otro**: lo básico, universal, que no se le niega a nadie — comunicación, gestiones, información limpia, lugares de la ciudad.

El internet comercial es **el que sale el domingo a la carretera “como profesional”**: quiere el pack completo (streaming, juegos, exceso). Que lo use quien lo quiera. Aquí no se imita ese capricho; se ofrece lo esencial y limpio.

## Para qué sirve (alcance de uso)
Red **ligera** pensada para seguir vivo socialmente y administrativamente cuando falle o no exista el internet comercial pesado.

**Sí (prioridad):**
- Comunicarte (mensajes, voz breve si cabe)
- Mantenerte al día (noticias / avisos de bajo peso)
- Compras y pagos simples (catálogos, pedidos, confirmaciones)
- Documentos y gestiones (texto, PDFs ligeros, trámites)
- Ficheros de trabajo de KBs–pocos MBs: código, procesadores/editores, imágenes, modelos 3D de biblioteca
- Imágenes modestas (comprimidas; no álbumes 4K masivos)
- Prensa y revistas “limpias”: texto + imágenes fijas; publicidad solo estática embebida (sin vídeo, sin pop-ups, sin trackers invasivos)

**No (fuera de alcance):**
- Vídeo de un giga, streaming continuo, juegos online
- Sustituir la web multimedia completa el día uno

Implicación de diseño: mensajes y ficheros ligeros primero; transferencias con cola, cifrado y reanudación si el enlace se parte; objetivo práctico ~hasta unos MB por envío (decenas de MB tolerables con paciencia).

## Motivación
Piloto geográfico: **Valladolid**, luego federación con otros municipios.

El internet actual concentra poder en nubes y plataformas. Ante fallos, censura o dependencia de Big Tech/IA, hace falta una red que siga funcionando en local y en comunidad, sin un dueño central.

## Paradigma (principios no negociables)

1. **Soberanía del usuario** — Identidad, datos y nodos bajo control propio.
2. **Peer-to-peer primero** — Servidores centrales opcionales, nunca obligatorios.
3. **Cifrado por defecto** — E2E; confianza por claves, no por un proveedor.
4. **Funciona sin el internet comercial** — Mesh/local primero; ISP/satélite solo como puente.
5. **Código abierto y auditable**
6. **Alcance acotado** — Comunicación + gestiones + docs/noticias, no multimedia pesada.
7. **Sin direcciones / URLs** — La interfaz es una pantalla de **lugares** (biblioteca, hospital, ayuntamiento, centro comercial, prensa…). Se navega con el dedo por enlaces y secciones. El usuario no escribe páginas web; los identificadores técnicos quedan ocultos.

### Interfaz: lugares, mapa y búsqueda (sin URLs)
- Pantalla principal = **mapa / directorio de Valladolid** (biblioteca, hospital, ayuntamiento, centro comercial, prensa…).
- Navegación a toques por lugares y secciones.
- **Buscador** por nombre (“hospital”, “biblioteca”) que te dice dónde está y te lleva — no es una barra de URLs.
- Sin teclear dominios. Identificadores técnicos ocultos.
- **Metáfora física:** prensa = hojas que pasas; banco/gestiones = mostrador y servicios; no portales web raros.

### Despliegue geográfico
1. **Piloto: Valladolid** (red ciudadana local).
2. Otros pueblos/ciudades montan **su** red (misma idea, datos propios).
3. **Federación**: redes autónomas conectadas entre sí; se comparten solo datos importantes (avisos críticos, directorios esenciales), no todo el ruido de la web.
4. Convivencia: el internet comercial sigue disponible; esta red es la alternativa limpia y el respaldo si aquel cae.

## MVP — Qué construimos primero

**Objetivo:** 2–5 nodos en casa/barrio que permitan:
1. Chat / avisos E2E
2. Compartir documentos de texto (y PDFs ligeros)
3. Opcional: imagen comprimida
…sin internet comercial. Compras/gestiones vienen en la fase siguiente (catálogo + pedido + identidad).

### Componentes del MVP
| Pieza | Descripción |
|-------|-------------|
| Nodo | Mini-PC / Raspberry Pi que enruta y almacena en local |
| Identidad | Par de claves por usuario/dispositivo |
| Descubrimiento | Vecinos en LAN/mesh |
| Mensajería | Chat y avisos E2E |
| Documentos | Publicar/obtener texto y ficheros ligeros entre pares |
| Cliente | App/kiosko táctil: lugares → secciones → docs (sin URLs) |

### Criterios de éxito
- [ ] Chat local vivo aunque caiga el ISP
- [ ] Un documento de texto llega de A a B cifrado
- [ ] Una imagen pequeña (&lt; ~200–500 KB) opcional funciona
- [ ] Instalación &lt; 1 h con guía

### Servicio excepcional: depósito en nodo (dead drop)
Para ficheros grandes (~1 GB) de forma puntual: reservar espacio en un nodo (cita/cuota), subir el archivo cifrado, un solo destinatario con clave lo descarga, y al terminar o caducar se borra. No es tráfico habitual del mesh; es aparcar y recoger.

### Canal: prensa limpia (periódicos / revistas / avisos)
Gratis para el lector. Formato **hojas digitales** (pasar página, como el papel), no webs enrevesadas. Paquetes firmados en el nodo. Sin autoplay, sin pop-ups, sin trackers. Publicidad a cargo del medio: banner estático o **una hoja entera de anuncio**. Se sincroniza entre nodos; se lee en local.

### Fase 2 (después del MVP)
Compras (catálogo + pedido), gestiones (formularios firmados), tablón de prensa limpia y avisos comunitarios, puente satelital opcional entre islas, UI de citas/cuotas para depósitos grandes.


## Modelo de negocio
**Solo extras de uso** (envíos / almacenamiento excepcional). **Prohibido** hacer negocio con el directorio ciudadano: ninguna tienda ni sitio aparece más grande o mejor colocado por pagar. La información de lugares es pública e igualitaria.

**Gratis (universal / no negociable):** mensajería, mapa y lugares (todos iguales), gestiones esenciales (p. ej. banco como mostrador), avisos críticos, **prensa completa** (el medio se financia con anuncios estáticos/hoja completa, no cobrando al lector aquí), transferencia ligera entre personas.

**De pago (solo tuyo):** envío/depósito de ficheros grandes con cita, más cuota de disco, sync prioritaria, y equivalentes — nunca ranking de tiendas ni muro al periódico.

**Gancho:** privacidad 100% y red que sigue si cae el internet comercial.


## Ecosistema financiero (visión futura)
**No sustituye al euro** (sueldos y economía oficial siguen en euros). Son **vales / resguardos digitales de plata**: cambias euros por plata en custodia y llevas el vale en lugar del metal. Equivalencia vale ↔ plata ↔ referencia en euros. Sirve para pagos internos (envíos premium, trueque local) con respaldo tangible — no es “banco central” ni moneda de curso legal.

**No es fase MVP.** Custodiar valor de terceros y emitir vales canjeables implica reglas (entidad, auditoría de reservas, condiciones de canje, marco legal aplicable). Hasta entonces, sostén operativo solo con cuotas de envíos/almacenamiento excepcional.



## Casa, dirección rotativa y timbre (estructura social)
No son páginas web: cada persona tiene una **casa** (espacio privado suyo).

- **Dirección privada**: identificador de contacto que **rota** con el tiempo (la casa “cambia de sitio”) para dificultar acecho/permanencia.
- **Timbre**: alguien pide contacto → el dueño **acepta o rechaza**. Sin aceptación, no hay acceso a la casa.
- **Tras aceptar**: se revela/usa solo la dirección **actual** (efímera), no una URL fija pública.
- **Alarma**: el usuario puede marcar vigilancia/aviso sobre un contacto o intento; salta notificación local en la red.
- Encaje UI: en el mapa de Valladolid hay lugares cívicos; las **casas** son personales y no aparecen como escaparate público igualitario de comercios — son privadas.

Implementación por fases: primero modelo de datos + API stub (casa, rotación, peticiones pending/accepted/rejected, alarmas); luego rotación real de claves/dirección y UI de timbre.

## MVP v0.1 — plan concreto
**Incluye:** app táctil mapa/lugares + buscador; 2 nodos LAN con mDNS; chat E2E; ficheros ligeros; funciona sin ISP.

**Excluye (después):** prensa-hojas, depósito 1GB, vales plata, federación municipios.

**Hardware:** 2× Raspberry Pi 5 (8GB) + SSD (o mini-PC Linux); AP/LAN local; cliente en móvil/tablet/táctil.

**Stack:** servicio nodo (Go o Rust) + SQLite; mDNS; identidad Ed25519; cifrado Noise/libsodium; cliente PWA táctil local.

**Orden:** (1) maqueta lugares Valladolid en un nodo (2) 2º nodo + mDNS (3) identidad + chat E2E (4) ficheros con resume (5) test cortando ISP.

## Siguiente paso inmediato
Arrancar esqueleto del nodo + maqueta de lugares de Valladolid en código.

---
*Borrador vivo — alcance de uso fijado: comunicación, compras, actualidad, docs/gestiones, imágenes ligeras.*


## Formato de documento: `.pucela`
Archivo de datos propio de la red (no HTML). Contenido permitido: **letras/texto**, **sonido**, **imágenes fijas** (sin vídeo).
Cerrojo: cifrado/firma; apertura en la app oficial en la red.
**Fotos:** hay tope de calidad/tamaño, pero **no se rechazan** — la app **recomprime/redimensiona sola** hasta que entren.
Futuro (después del formato): “páginas” de mercado/tienda y de personas (no HTML clásico), cada una con su asistente y servicios dentro, sobre casas/.pucela.
