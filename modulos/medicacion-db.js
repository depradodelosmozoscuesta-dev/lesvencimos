/* Les vencimos — base de medicinas con prospecto RESUMIDO (offline)
 * Información general orientativa. NO sustituye prospecto oficial ni indicación médica.
 * Urgencias: 112. Sin recomendaciones personalizadas de dosis/tratamiento.
 * v20261002c
 */
(function (root) {
  'use strict';
  var LV_MEDS_DISCLAIMER = "Información general orientativa offline. No sustituye el prospecto oficial del envase ni la indicación de un profesional sanitario. Ante duda, consulta médico o farmacéutico. Urgencias: 112.";
  var LV_MEDS_DB = [
  {
    "id": "paracetamol",
    "nombre": "Paracetamol",
    "marca": "Gelocatil, Efferalgan, Termalgin…",
    "presentacion": "Comprimidos / sobres 500 mg o 1 g",
    "usos": "Alivio de dolor leve o moderado y de la fiebre (dolor de cabeza, muscular, dental, resfriado).",
    "como": "Vía oral. Puede tomarse con o sin comida. Respeta el intervalo y el máximo del prospecto del envase; no acumules con otros productos que también lleven paracetamol.",
    "avisos": "No uses varios medicamentos con paracetamol a la vez. Si tienes problemas de hígado, consume alcohol con frecuencia o estás embarazada/lactando, consulta antes. No es un diagnóstico: si el dolor o la fiebre no mejoran, ve al médico.",
    "efectos": [
      "Molestias digestivas poco frecuentes",
      "Reacciones alérgicas raras",
      "Daño hepático si se supera la dosis del prospecto"
    ],
    "categoria": "analgesico"
  },
  {
    "id": "ibuprofeno",
    "nombre": "Ibuprofeno",
    "marca": "Neobrufen, Espidifen, Dalsy…",
    "presentacion": "Comprimidos / sobres 200–600 mg; suspensión pediátrica",
    "usos": "Dolor e inflamación leves o moderados; fiebre. Dolor menstrual, muscular, dental, cefalea.",
    "como": "Vía oral, preferible con comida o leche para proteger el estómago. No es pauta médica: sigue el prospecto del envase o lo que te haya dicho tu médico.",
    "avisos": "Evita si tienes úlcera, sangrado digestivo, insuficiencia renal/cardíaca graves o alergia a AINE. No combines con otros antiinflamatorios sin consejo. Embarazo (sobre todo último trimestre): consulta. Hipertensión o anticoagulantes: pregunta al médico/farmacéutico.",
    "efectos": [
      "Molestia gástrica",
      "Acidez",
      "Mareo",
      "Riesgo de úlcera o sangrado con uso prolongado o dosis altas"
    ],
    "categoria": "analgesico"
  },
  {
    "id": "aas-analgesico",
    "nombre": "Ácido acetilsalicílico (analgésico)",
    "marca": "Aspirina, AAS…",
    "presentacion": "Comprimidos 500 mg (analgésico); también existe 100 mg (otro uso)",
    "usos": "Dolor leve y fiebre en adultos. La presentación de 100 mg se usa en prevención cardiovascular solo bajo indicación médica.",
    "como": "Vía oral, con comida. No uses en niños o adolescentes con fiebre/viral (riesgo de síndrome de Reye) salvo indicación expresa.",
    "avisos": "No si alergia a salicilatos, úlcera activa, hemofilia o tratamiento con anticoagulantes sin control médico. Embarazo: consulta. No confundas 500 mg con 100 mg.",
    "efectos": [
      "Acidez",
      "Molestia gástrica",
      "Mayor facilidad de sangrado",
      "Zumbido de oídos a dosis altas"
    ],
    "categoria": "analgesico"
  },
  {
    "id": "naproxeno",
    "nombre": "Naproxeno",
    "marca": "Antalgin, Naprosyn…",
    "presentacion": "Comprimidos 250–500 mg",
    "usos": "Dolor e inflamación (muscular, articular, menstrual) cuando un profesional o el prospecto lo indican.",
    "como": "Vía oral, con comida. Intervalos según prospecto del envase o indicación médica.",
    "avisos": "Misma familia que ibuprofeno (AINE): cuidado con estómago, riñón, corazón, embarazo y anticoagulantes. No combines AINE por tu cuenta.",
    "efectos": [
      "Acidez",
      "Molestia digestiva",
      "Cefalea",
      "Riesgo de úlcera con uso prolongado"
    ],
    "categoria": "analgesico"
  },
  {
    "id": "metamizol",
    "nombre": "Metamizol (dipirona)",
    "marca": "Nolotil…",
    "presentacion": "Cápsulas 575 mg; ampollas (uso hospitalario/prescripción)",
    "usos": "Dolor intenso o fiebre cuando otros analgésicos no bastan; en España suele requerir prescripción.",
    "como": "Solo según indiquen médico y prospecto. Vía oral en cápsulas; no inventes dosis.",
    "avisos": "Asociado a agranulocitosis (poco frecuente pero grave): fiebre, dolor de garganta o infecciones → atención urgente. Alergias, embarazo, médula ósea: solo con control médico. No es OTC libre en muchas situaciones.",
    "efectos": [
      "Hipotensión (sobre todo inyectable)",
      "Reacciones alérgicas",
      "Alteraciones sanguíneas raras pero graves"
    ],
    "categoria": "analgesico"
  },
  {
    "id": "omeprazol",
    "nombre": "Omeprazol",
    "marca": "Mopral, Losec, genéricos…",
    "presentacion": "Cápsulas gastrorresistentes 20 mg (también 40 mg con receta)",
    "usos": "Acidez, reflujo y protección gástrica cuando así lo indique el médico o el uso autorizado en automedicación breve.",
    "como": "Vía oral, preferible por la mañana en ayunas, tragar entero (no masticar la bolita gastrorresistente). Duración: sigue prospecto o médico; no alargues por tu cuenta.",
    "avisos": "Si necesitas antiácido muchos días, hay síntomas de alarma (vómito con sangre, heces negras, pérdida de peso) o eres mayor y tomas muchos fármacos: consulta. Interacciones posibles (clopidogrel, algunos antirretrovirales, etc.).",
    "efectos": [
      "Dolor de cabeza",
      "Gases o diarrea",
      "Con uso muy prolongado: posibles déficits (B12, magnesio) — lo valora el médico"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "pantoprazol",
    "nombre": "Pantoprazol",
    "marca": "Anagastra, genéricos…",
    "presentacion": "Comprimidos gastrorresistentes 20–40 mg",
    "usos": "Reflujo y úlcera/protección gástrica bajo criterio médico (a menudo con receta).",
    "como": "Vía oral, enteros, suele ser en ayunas. Solo la pauta que te indiquen.",
    "avisos": "Igual que otros IBP: síntomas de alarma y uso largo → médico. Informa de todos los medicamentos que tomas.",
    "efectos": [
      "Cefalea",
      "Diarrea o estreñimiento",
      "Molestia abdominal"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "famotidina",
    "nombre": "Famotidina",
    "marca": "Pepcid, genéricos…",
    "presentacion": "Comprimidos 20–40 mg",
    "usos": "Acidez y ardor de estómago; reduce la producción de ácido (anti-H2).",
    "como": "Vía oral, con o sin comida, según prospecto.",
    "avisos": "Si la acidez es frecuente o hay signos de alarma digestiva, no te automediques de forma prolongada.",
    "efectos": [
      "Cefalea",
      "Mareo",
      "Estreñimiento o diarrea"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "almagato",
    "nombre": "Almagato",
    "marca": "Almax…",
    "presentacion": "Comprimidos masticables / suspensión",
    "usos": "Alivio rápido de la acidez y molestia de estómago (antiácido de contacto).",
    "como": "Vía oral, tras las comidas o cuando aparezca el ardor, según prospecto. Separar de otros fármacos (puede restar absorción).",
    "avisos": "No sustituye estudio si el ardor es constante. Insuficiencia renal grave: consulta. Deja horas respecto a hierro, antibióticos, etc.",
    "efectos": [
      "Estreñimiento o heces blandas",
      "Sensación de llenado"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "magaldrato",
    "nombre": "Magaldrato",
    "marca": "Bocasept, genéricos…",
    "presentacion": "Comprimidos / sobres",
    "usos": "Acidez y reflujo leve como antiácido.",
    "como": "Vía oral tras comidas o al notar ardor; sigue el envase.",
    "avisos": "Separa de otros medicamentos. Problemas de riñón: pregunta al farmacéutico.",
    "efectos": [
      "Alteración del ritmo intestinal"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "simeticona",
    "nombre": "Simeticona",
    "marca": "Aero-Red, Flatus…",
    "presentacion": "Cápsulas / gotas / masticables",
    "usos": "Gases, hinchazón y flatulencia.",
    "como": "Vía oral, a menudo tras comidas, según prospecto. Actúa en el intestino; no se absorbe de forma relevante.",
    "avisos": "Si hay dolor intenso, vómitos o cambio de ritmo intestinal, consulta (no es solo «gases»).",
    "efectos": [
      "Suelen ser mínimos",
      "Molestia digestiva ocasional"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "loperamida",
    "nombre": "Loperamida",
    "marca": "Fortasec, Imodium…",
    "presentacion": "Cápsulas / comprimidos 2 mg",
    "usos": "Diarrea aguda ocasional del adulto (sintomático).",
    "como": "Vía oral según prospecto. Hidrátate (suero de rehidratación). No es tratamiento de la causa.",
    "avisos": "No uses si hay fiebre alta, sangre en heces, diarrea del viajero grave o en niños pequeños sin consejo. No superes la dosis del envase. Embarazo/lactancia: consulta.",
    "efectos": [
      "Estreñimiento",
      "Dolor abdominal",
      "Sequedad de boca",
      "Mareo"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "lactulosa",
    "nombre": "Lactulosa",
    "marca": "Duphalac…",
    "presentacion": "Jarabe / sobres",
    "usos": "Estreñimiento; también usos especiales bajo control médico (encefalopatía hepática).",
    "como": "Vía oral; puede tardar 1–2 días en hacer efecto. Bebe suficiente líquido.",
    "avisos": "Dolor abdominal intenso, obstrucción sospechada o uso crónico sin diagnóstico: médico. Diabéticos: mira el contenido en azúcares del prospecto.",
    "efectos": [
      "Gases",
      "Hinchazón",
      "Diarrea si te pasas de cantidad"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "macrogol",
    "nombre": "Macrogol (PEG)",
    "marca": "Movicol, Casenlax…",
    "presentacion": "Sobres para disolver en agua",
    "usos": "Estreñimiento en adultos (y presentaciones pediátricas según prospecto/médico).",
    "como": "Disolver en agua y beber. Hidratación adecuada. Efecto en 1–2 días a menudo.",
    "avisos": "No si sospecha de obstrucción intestinal. Uso prolongado: valora causa con profesional.",
    "efectos": [
      "Hinchazón",
      "Náuseas",
      "Diarrea si exceso"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "plantago",
    "nombre": "Ispágula / Plantago ovata",
    "marca": "Plantaben, Cenat…",
    "presentacion": "Sobres de polvo / granulado",
    "usos": "Estreñimiento y regulación del tránsito (fibra formadora de bolo).",
    "como": "Mezclar con abundante agua y beber de inmediato; luego más líquido. No tomar seco.",
    "avisos": "Sin agua suficiente puede empeorar. Separar de otros fármacos. Obstrucción o dolor agudo: no.",
    "efectos": [
      "Gases al inicio",
      "Hinchazón"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "domperidona",
    "nombre": "Domperidona",
    "marca": "Motilium…",
    "presentacion": "Comprimidos 10 mg",
    "usos": "Náuseas y vómitos; a menudo con receta y tiempo limitado por seguridad cardiaca.",
    "como": "Solo según médico/prospecto. Vía oral antes de las comidas si así se indica.",
    "avisos": "Riesgo de alteraciones del ritmo cardiaco: no combines con ciertos fármacos; cardiopatía → médico. Uso corto. Embarazo: consulta.",
    "efectos": [
      "Sequedad de boca",
      "Cefalea",
      "Alteraciones hormonales poco frecuentes",
      "Efectos cardiacos raros"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "loratadina",
    "nombre": "Loratadina",
    "marca": "Clarityne, Soften…",
    "presentacion": "Comprimidos 10 mg; jarabe",
    "usos": "Rinitis alérgica, estornudos, picor, urticaria leve.",
    "como": "Vía oral, una vez al día según prospecto. Poco sedante en la mayoría de personas.",
    "avisos": "Si hay dificultad respiratoria grave o hinchazón de cara/labios: urgencias 112. Embarazo/hígado: consulta. No sustituye el tratamiento de anafilaxia.",
    "efectos": [
      "Sequedad de boca",
      "Cefalea",
      "Somnolencia ocasional"
    ],
    "categoria": "alergia"
  },
  {
    "id": "cetirizina",
    "nombre": "Cetirizina",
    "marca": "Zyrtec, Alerfil…",
    "presentacion": "Comprimidos 10 mg; gotas/jarabe",
    "usos": "Alergia respiratoria y cutánea (picor, rinitis, urticaria).",
    "como": "Vía oral según prospecto. Puede producir algo más de somnolencia que loratadina en algunas personas.",
    "avisos": "Cuidado al conducir si te da sueño. Insuficiencia renal: ajusta solo con consejo profesional. Reacción grave → 112.",
    "efectos": [
      "Somnolencia",
      "Sequedad de boca",
      "Fatiga"
    ],
    "categoria": "alergia"
  },
  {
    "id": "desloratadina",
    "nombre": "Desloratadina",
    "marca": "Aerius, genéricos…",
    "presentacion": "Comprimidos 5 mg; jarabe",
    "usos": "Síntomas de alergia (rinitis, picor, urticaria).",
    "como": "Vía oral según prospecto; suele ser una toma al día.",
    "avisos": "Igual que otros antihistamínicos: síntomas graves de alergia no se tratan solo con pastilla → 112.",
    "efectos": [
      "Cefalea",
      "Sequedad de boca",
      "Fatiga"
    ],
    "categoria": "alergia"
  },
  {
    "id": "bilastina",
    "nombre": "Bilastina",
    "marca": "Bilaxten, Ibinol…",
    "presentacion": "Comprimidos 20 mg",
    "usos": "Rinitis alérgica y urticaria.",
    "como": "Vía oral en ayunas (sin comida alrededor, según prospecto): la comida reduce absorción.",
    "avisos": "Respeta la ventana sin alimentos del prospecto. Conducir si no hay somnolencia. Embarazo: consulta.",
    "efectos": [
      "Cefalea",
      "Somnolencia ocasional",
      "Molestia abdominal"
    ],
    "categoria": "alergia"
  },
  {
    "id": "dimenhidrinato",
    "nombre": "Dimenhidrinato",
    "marca": "Biodramina…",
    "presentacion": "Comprimidos / masticables / chicles",
    "usos": "Mareo de viaje (cinetosis) y náuseas asociadas.",
    "como": "Vía oral, a menudo antes del viaje según prospecto. Produce sueño: no conduzcas si te afecta.",
    "avisos": "Glaucoma, próstata, asma: pregunta. Alcohol y sedantes: potencian sueño. Niños: solo presentaciones y edades del envase.",
    "efectos": [
      "Somnolencia",
      "Sequedad de boca",
      "Visión borrosa ocasional"
    ],
    "categoria": "alergia"
  },
  {
    "id": "dextrometorfano",
    "nombre": "Dextrometorfano",
    "marca": "Romilar, Bisolvon antitusivo…",
    "presentacion": "Jarabe / comprimidos",
    "usos": "Tos seca irritativa ocasional del adulto.",
    "como": "Vía oral según prospecto. No mezcles varios antitusivos.",
    "avisos": "Tos con mucha mucosidad, tos de semanas, sangre o dificultad respiratoria → médico. Interacciona con algunos antidepresivos (IMAO/ISRS): pregunta. No abuses (riesgo neurológico a dosis altas).",
    "efectos": [
      "Somnolencia",
      "Mareo",
      "Molestia digestiva"
    ],
    "categoria": "respiratorio"
  },
  {
    "id": "guaifenesina",
    "nombre": "Guaifenesina",
    "marca": "Robitussin, mucolíticos combinados…",
    "presentacion": "Jarabe",
    "usos": "Tos productiva: ayuda a fluidificar la mucosidad (expectorante).",
    "como": "Vía oral; bebe agua. Sigue el prospecto.",
    "avisos": "Tos persistente o con alarma → médico. Mira si el jarabe lleva otros principios (descongestivos, antitusivos).",
    "efectos": [
      "Náuseas",
      "Molestia estomacal"
    ],
    "categoria": "respiratorio"
  },
  {
    "id": "acetilcisteina",
    "nombre": "Acetilcisteína",
    "marca": "Flumil, Rinofluimucil (otras formas)…",
    "presentacion": "Sobres / comprimidos efervescentes 200–600 mg",
    "usos": "Mucosidad espesa en resfriados/bronquitis leves; también uso hospitalario en otras indicaciones.",
    "como": "Vía oral disuelto en agua, según prospecto. Disuelve bien el efervescente.",
    "avisos": "Úlcera activa: precaución. Si hay dificultad respiratoria importante o asma mal controlado: médico. No es antibiótico.",
    "efectos": [
      "Náuseas",
      "Ardor",
      "Olor azufrado del preparado"
    ],
    "categoria": "respiratorio"
  },
  {
    "id": "carbocisteina",
    "nombre": "Carbocisteína",
    "marca": "Mucolitico, Actithiol…",
    "presentacion": "Jarabe / cápsulas",
    "usos": "Fluidificar secreciones bronquiales en resfriado o bronquitis leve.",
    "como": "Vía oral según prospecto; buena hidratación.",
    "avisos": "Úlcera gastroduodenal: consulta. Síntomas graves o prolongados → profesional.",
    "efectos": [
      "Molestia digestiva",
      "Náuseas"
    ],
    "categoria": "respiratorio"
  },
  {
    "id": "xilometazolina",
    "nombre": "Xilometazolina (nasal)",
    "marca": "Otrivin, Rhinomer descongestivo…",
    "presentacion": "Spray / gotas nasales",
    "usos": "Congestión nasal de resfriado o rinitis por pocos días.",
    "como": "Vía nasal. Uso corto (pocos días): el abuso rebota y congestiona más.",
    "avisos": "No alargues más de lo que diga el prospecto (suele ser ≤3–5 días). Hipertensión, corazón, hipertiroidismo, glaucoma: pregunta. Niños: solo presentación adecuada.",
    "efectos": [
      "Sequedad nasal",
      "Picor",
      "Congestión de rebote si se abusa"
    ],
    "categoria": "respiratorio"
  },
  {
    "id": "suero-fisiologico",
    "nombre": "Suero fisiológico / agua de mar nasal",
    "marca": "Sterimar, Rhinomer limpio…",
    "presentacion": "Spray isotónico o hipertónico",
    "usos": "Limpieza e hidratación de fosas nasales; congestión leve.",
    "como": "Vía nasal según instrucciones del envase. Seguro en uso habitual si es solo suero.",
    "avisos": "Si el producto lleva fármaco descongestivo, aplica las reglas de ese principio. Envases: evita contaminar la boquilla.",
    "efectos": [
      "Escurrimiento",
      "Picor leve"
    ],
    "categoria": "respiratorio"
  },
  {
    "id": "vitamina-c",
    "nombre": "Vitamina C (ácido ascórbico)",
    "marca": "Redoxon, Cebion…",
    "presentacion": "Comprimidos efervescentes / masticables 500–1000 mg",
    "usos": "Aporte de vitamina C; estados carenciales o dieta pobre en frutas/verduras. No «cura» el resfriado por sí sola.",
    "como": "Vía oral, con agua. Efervescentes: disolver bien.",
    "avisos": "Dosis muy altas: diarrea y piedras renales en susceptibles. Cálculos de riñón o problemas renales: consulta. No sustituye alimentación.",
    "efectos": [
      "Acidez",
      "Diarrea a dosis altas"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "vitamina-d",
    "nombre": "Vitamina D (colecalciferol)",
    "marca": "Deltius, Vitamina D3 Kern…",
    "presentacion": "Gotas / cápsulas / ampollas bebibles (dosis según envase)",
    "usos": "Déficit de vitamina D, salud ósea; a menudo tras analítica e indicación médica.",
    "como": "Vía oral según prospecto o pauta del médico. No te automediques con dosis altas «de carga».",
    "avisos": "Exceso = toxicidad (hipercalcemia). Piedras, sarcoidosis, hiperparatiroidismo: solo con control. Embarazo: lo indica el profesional.",
    "efectos": [
      "Náuseas si exceso",
      "Sed",
      "Confusión en intoxicación — urgencias"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "vitamina-b12",
    "nombre": "Vitamina B12 (cianocobalamina / metilcobalamina)",
    "marca": "Optovite, genéricos…",
    "presentacion": "Comprimidos; ampollas (a menudo prescritas)",
    "usos": "Déficit de B12 (dieta vegana mal planificada, absorción, anemia perniciosa) bajo criterio médico.",
    "como": "Oral o inyectable según indiquen. No improvises inyecciones.",
    "avisos": "La causa del déficit debe valorarla un profesional. No sustituye estudio de anemia.",
    "efectos": [
      "Acné o erupción rara",
      "Molestia en el punto de inyección"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "acido-folico",
    "nombre": "Ácido fólico (vitamina B9)",
    "marca": "Afolic, genéricos…",
    "presentacion": "Comprimidos 5 mg (y dosis menores en polivitamínicos)",
    "usos": "Prevención de defectos del tubo neural en gestación planificada; anemias carenciales según médico.",
    "como": "Vía oral. En embarazo: sigue la pauta de tu matrona/médico (suele empezarse antes de concebir).",
    "avisos": "No enmascara déficit de B12: si hay anemia, estudia ambas. Epilepsia y algunos fármacos: interacciones.",
    "efectos": [
      "Molestia digestiva leve",
      "Reacciones alérgicas raras"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "hierro",
    "nombre": "Hierro oral (ferroso / ferrimanitol)",
    "marca": "Tardyferon, Ferogradumet, Ferro sanol…",
    "presentacion": "Comprimidos / sobres; distintas sales y dosis",
    "usos": "Anemia ferropénica o prevención cuando lo indique el médico tras analítica.",
    "como": "Vía oral; a menudo lejos del café/té/lácteos. Vitamina C puede ayudar a absorber; sigue prospecto. Las heces pueden oscurecerse (normal).",
    "avisos": "No tomes hierro «por si acaso» sin análisis: el exceso es tóxico (sobre todo en niños: mantén lejos). Úlcera, colitis: consulta. Intoxicación infantil = urgencia.",
    "efectos": [
      "Estreñimiento o diarrea",
      "Náuseas",
      "Dolor de estómago",
      "Heces negras"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "calcio-vitd",
    "nombre": "Calcio (+ vitamina D)",
    "marca": "Calcium Sandoz, Ideos, Natecal…",
    "presentacion": "Comprimidos masticables / efervescentes",
    "usos": "Aporte de calcio; osteoporosis o déficit bajo consejo profesional.",
    "como": "Vía oral; algunos se mastican. Separar de hierro y de ciertos antibióticos (quinolonas, tetraciclinas).",
    "avisos": "Hipercalcemia, piedras renales graves: no sin control. Mira si ya tomas vitamina D aparte para no duplicar.",
    "efectos": [
      "Estreñimiento",
      "Gases",
      "Sed si exceso de calcio"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "complejo-b",
    "nombre": "Complejo vitamínico B",
    "marca": "Benerva compleja, Supradyn B…",
    "presentacion": "Comprimidos",
    "usos": "Aporte de vitaminas del grupo B en dietas pobres o mayor necesidad; no sustituye diagnóstico de déficit.",
    "como": "Vía oral con agua, según envase.",
    "avisos": "Orina muy amarilla puede ser normal (riboflavina). Dosis mega: no aportan más y pueden molestar. Embarazo: elige preparados indicados.",
    "efectos": [
      "Náuseas",
      "Coloración intensa de orina"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "magnesio",
    "nombre": "Magnesio",
    "marca": "Magnesio Pharma, Magnogene…",
    "presentacion": "Comprimidos / sobres",
    "usos": "Aporte de magnesio; calambres o déficit cuando lo aconsejen; también laxante suave según sal.",
    "como": "Vía oral con agua. Sales distintas (lactato, citrato…) tienen tolerancias distintas.",
    "avisos": "Insuficiencia renal: peligro de acumulación — solo con consejo. Diarrea si te pasas.",
    "efectos": [
      "Diarrea",
      "Hinchazón"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "melatonina",
    "nombre": "Melatonina",
    "marca": "Cinfa Noche, Aquilea Sueño…",
    "presentacion": "Comprimidos 1–1,9 mg (complemento); dosis mayores a menudo con control",
    "usos": "Ayuda ocasional a conciliar el sueño / jet lag según el producto autorizado.",
    "como": "Vía oral por la noche, según prospecto. No es hipnótico fuerte.",
    "avisos": "No conduzcas si te queda sueño. Enfermedad autoinmune, embarazo, epilepsia: consulta. No combines con alcohol. Insomnio crónico → profesional (no solo pastilla).",
    "efectos": [
      "Somnolencia diurna",
      "Cefalea",
      "Sueños vívidos"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "ibuprofeno-gel",
    "nombre": "Ibuprofeno gel / crema",
    "marca": "Salvat, genéricos…",
    "presentacion": "Gel tópico 50 mg/g",
    "usos": "Dolor muscular o articular localizado (golpes, sobrecarga) en adultos.",
    "como": "Aplicar capa fina en la zona intacta; lavarse las manos. No usar bajo vendaje oclusivo fuerte salvo indicación.",
    "avisos": "No en heridas abiertas ni mucosas. Alergia a AINE: precaución (absorción menor pero existe). Embarazo avanzado: consulta.",
    "efectos": [
      "Enrojecimiento local",
      "Picor",
      "Fotosensibilidad rara"
    ],
    "categoria": "topico"
  },
  {
    "id": "hidrocortisona",
    "nombre": "Hidrocortisona crema (baja potencia)",
    "marca": "Crema de hidrocortisona 1 %…",
    "presentacion": "Crema / pomada 1 %",
    "usos": "Picor e inflamación leve de la piel (picaduras, eccema leve) por pocos días.",
    "como": "Capa fina en zona afectada, piel intacta, poco tiempo. Cara, pliegues y niños: solo con consejo.",
    "avisos": "No en infecciones cutáneas (hongos, impétigo) sin diagnóstico. Uso largo = afinamiento de piel. No en ojos.",
    "efectos": [
      "Sequedad",
      "Ardor inicial",
      "Con abuso: piel fina, vasos visibles"
    ],
    "categoria": "topico"
  },
  {
    "id": "clorhexidina",
    "nombre": "Clorhexidina",
    "marca": "Cristalmina, Hibiscrub (otras formas)…",
    "presentacion": "Solución antiséptica / colutorio (distintas concentraciones)",
    "usos": "Desinfección de piel sana o heridas superficiales; colutorios bucales según producto.",
    "como": "Uso externo o bucal según el envase. No tragar el colutorio. No mezclar a ciegas con otros antisépticos.",
    "avisos": "Ojos y oídos profundos: cuidado (algunas soluciones no sirven para oído perforado). Alergia rara pero posible. Heridas profundas/graves → sanitarios.",
    "efectos": [
      "Irritación local",
      "Manchas en dientes con colutorio prolongado"
    ],
    "categoria": "topico"
  },
  {
    "id": "povidona-yodada",
    "nombre": "Povidona yodada",
    "marca": "Betadine…",
    "presentacion": "Solución / jabón / pomada",
    "usos": "Antiséptico de piel y heridas superficiales.",
    "como": "Uso externo según envase. Dejar secar. Mancha la ropa.",
    "avisos": "Alergia al yodo, tiroides, embarazo/lactancia prolongada: consulta. No grandes superficies en bebés sin consejo. Ojos: productos específicos.",
    "efectos": [
      "Irritación",
      "Tinción de la piel"
    ],
    "categoria": "topico"
  },
  {
    "id": "vaselina-lanolina",
    "nombre": "Vaselina / emolientes",
    "marca": "Vaselina pura, Cold cream…",
    "presentacion": "Pomada / bálsamo",
    "usos": "Piel seca, labios agrietados, protección de barrera.",
    "como": "Aplicar en piel limpia. Uso externo.",
    "avisos": "No en heridas infectadas como único tratamiento. Si hay alergia a lanolina, elige vaselina simple.",
    "efectos": [
      "Grasa en la ropa",
      "Foliculitis rara si se ocluye mucho"
    ],
    "categoria": "topico"
  },
  {
    "id": "sueroral",
    "nombre": "Sales de rehidratación oral",
    "marca": "Sueroral, Oralsuite…",
    "presentacion": "Sobres para disolver en agua",
    "usos": "Deshidratación leve por diarrea o vómitos (reponer agua y electrolitos).",
    "como": "Disolver exactamente en el volumen de agua del prospecto. Beber a sorbos. No diluir «a ojo».",
    "avisos": "Vómitos incoercibles, sangre, letargo, niños pequeños, ancianos frágiles → atención sanitaria. No sustituye suero intravenoso cuando hace falta.",
    "efectos": [
      "Náuseas si se bebe muy rápido"
    ],
    "categoria": "otro"
  },
  {
    "id": "glucosa-oral",
    "nombre": "Gel / tabletas de glucosa",
    "marca": "Glucogel, Dextrosa…",
    "presentacion": "Gel bucal / tabletas masticables",
    "usos": "Hipoglucemia en personas con diabetes que ya tienen un plan enseñado por su equipo sanitario.",
    "como": "Según el plan de tu educador/médico. Si hay pérdida de conciencia: no administer por boca — 112.",
    "avisos": "Solo si la persona está consciente y puede tragar. No improvises en quien no es diabético conocido sin consejo.",
    "efectos": [
      "Hiperglucemia de rebote si se abusa"
    ],
    "categoria": "otro"
  },
  {
    "id": "lagrimas-artificiales",
    "nombre": "Lágrimas artificiales",
    "marca": "Systane, Viscofresh, Artific…",
    "presentacion": "Colirio monodosis o multidosis",
    "usos": "Ojo seco, molestia por pantallas, ambiente seco.",
    "como": "Vía oftálmica: no tocar el ojo con el gotero. Monodosis: desechar tras uso si así lo indica.",
    "avisos": "Dolor intenso, pérdida de visión, ojo rojo con secreción: oftalmólogo/urgencias. Si usas lentillas, mira compatibilidad del producto.",
    "efectos": [
      "Visión borrosa breve tras la gota",
      "Picor leve"
    ],
    "categoria": "otro"
  },
  {
    "id": "benzidamina",
    "nombre": "Benzidamina (bucal)",
    "marca": "Tantum Verde…",
    "presentacion": "Spray / colutorio / pastillas",
    "usos": "Alivio de dolor e inflamación de garganta o boca (sintomático).",
    "como": "Bucal según prospecto; no tragar el colutorio salvo que el envase lo permita.",
    "avisos": "Si hay fiebre alta, dificultad para tragar/respirar o placas: médico (puede hacer falta otro tratamiento). Uso corto.",
    "efectos": [
      "Entumecimiento bucal",
      "Irritación"
    ],
    "categoria": "otro"
  },
  {
    "id": "pastillas-garganta",
    "nombre": "Pastillas para la garganta (varios)",
    "marca": "Strepsils, Angileptol…",
    "presentacion": "Pastillas para chupar (antiséptico + a veces anestésico suave)",
    "usos": "Alivio sintomático de irritación de garganta.",
    "como": "Chupar despacio; no masticar a lo loco. Mira alérgenos (miel, mentol, etc.).",
    "avisos": "No sustituye valoración si la faringitis es intensa o dura muchos días. Niños pequeños: riesgo de atragantamiento — presentaciones adecuadas.",
    "efectos": [
      "Hormigueo",
      "Irritación leve"
    ],
    "categoria": "otro"
  },
  {
    "id": "carbón-activado",
    "nombre": "Carbón activado",
    "marca": "Carbonet, Carbón medicinal…",
    "presentacion": "Cápsulas / comprimidos",
    "usos": "Algunas intoxicaciones agudas en entorno sanitario; a veces flatulencia (evidencia limitada).",
    "como": "En intoxicación: solo bajo indicación de profesionales / 112 / toxicología. No lo uses por tu cuenta en envenenamientos.",
    "avisos": "No para todo veneno (alcohol, metales, ácidos…). Puede anular otros fármacos si se toma cerca. Urgencia real → 112.",
    "efectos": [
      "Heces negras",
      "Estreñimiento o vómito"
    ],
    "categoria": "otro"
  },
  {
    "id": "metformina",
    "nombre": "Metformina",
    "marca": "Dianben, genéricos…",
    "presentacion": "Comprimidos 850 mg / 1000 mg (y otras dosis)",
    "usos": "Diabetes tipo 2 y a veces prediabetes / SOP, siempre con prescripción y control.",
    "como": "Vía oral con las comidas según pauta de tu médico. No cambies la dosis por tu cuenta.",
    "avisos": "Riesgo raro de acidosis láctica (vómitos intensos, hiperventilación, malestar extremo → urgencias). Contrastes yodados, cirugía, diarrea grave: sigue instrucciones médicas. Alcohol excesivo: evita.",
    "efectos": [
      "Diarrea",
      "Náuseas",
      "Sabor metálico",
      "Molestia abdominal al inicio"
    ],
    "categoria": "cronico"
  },
  {
    "id": "enalapril",
    "nombre": "Enalapril",
    "marca": "Renitec, genéricos…",
    "presentacion": "Comprimidos 5–20 mg",
    "usos": "Hipertensión e insuficiencia cardiaca bajo prescripción.",
    "como": "Vía oral a la hora que indique tu médico. Control de tensión y analíticas según te citen.",
    "avisos": "Puede subir el potasio y afectar al riñón. Embarazo: contraindicado — avisa si quedas embarazada. Mareo al levantarte: cuidado. No suspendas brusco sin consejo.",
    "efectos": [
      "Tos seca",
      "Mareo",
      "Hipotensión",
      "Hiperpotasemia"
    ],
    "categoria": "cronico"
  },
  {
    "id": "atorvastatina",
    "nombre": "Atorvastatina",
    "marca": "Cardyl, Zarator, genéricos…",
    "presentacion": "Comprimidos 10–80 mg",
    "usos": "Colesterol alto y prevención cardiovascular con prescripción.",
    "como": "Vía oral, a menudo por la noche o cuando diga el médico. Dieta y ejercicio siguen siendo la base.",
    "avisos": "Dolor muscular intenso, orina oscura o debilidad → médico (raro: afectación muscular). Interacciones con algunos antibióticos/antifúngicos y pomelo. Embarazo: no.",
    "efectos": [
      "Molestia digestiva",
      "Dolor muscular leve",
      "Elevación de enzimas hepáticas"
    ],
    "categoria": "cronico"
  },
  {
    "id": "levotiroxina",
    "nombre": "Levotiroxina",
    "marca": "Eutirox, Levothroid…",
    "presentacion": "Comprimidos (dosis en µg: 25, 50, 75, 100…)",
    "usos": "Hipotiroidismo y otros usos tiroideos con control endocrino/médico.",
    "como": "Vía oral en ayunas, lejos del café, calcio y hierro (separar horas). Misma marca/dosis salvo que te cambien con control.",
    "avisos": "Demasiada = palpitaciones, nerviosismo; poca = cansancio, frío. Analíticas periódicas. Embarazo: suele necesitar ajuste — avisa ya.",
    "efectos": [
      "Palpitaciones si exceso",
      "Insomnio si exceso",
      "Caída de pelo al inicio del ajuste"
    ],
    "categoria": "cronico"
  },
  {
    "id": "amoxicilina",
    "nombre": "Amoxicilina",
    "marca": "Clamoxyl, genéricos…",
    "presentacion": "Cápsulas / sobres / suspensión (500 mg, 875 mg, etc.)",
    "usos": "Infecciones bacterianas sensibles; solo con receta. No vale para virus (resfriado común).",
    "como": "Vía oral a intervalos regulares según la receta. Termina el tratamiento que te hayan indicado; no guardes «por si acaso» sin criterio.",
    "avisos": "Alergia a penicilinas = no. Diarrea intensa o con sangre durante/después → médico (colitis). Resistencias: no te automediques con sobras.",
    "efectos": [
      "Diarrea",
      "Náuseas",
      "Candidiasis",
      "Erupción (valorar alergia)"
    ],
    "categoria": "cronico"
  },
  {
    "id": "amoxicilina-clavulanico",
    "nombre": "Amoxicilina / ácido clavulánico",
    "marca": "Augmentine, genéricos…",
    "presentacion": "Comprimidos 875/125 mg; suspensión",
    "usos": "Infecciones bacterianas cuando el médico elige este espectro; con receta.",
    "como": "Con comida para mejor tolerancia, según receta.",
    "avisos": "Igual que amoxicilina + más molestia hepática/digestiva posible. Alergia a penicilina: no. No automedicación.",
    "efectos": [
      "Diarrea",
      "Náuseas",
      "Candidiasis",
      "Alteración de transaminasas"
    ],
    "categoria": "cronico"
  },
  {
    "id": "aas-100",
    "nombre": "Ácido acetilsalicílico 100 mg",
    "marca": "Adiro, AAS 100…",
    "presentacion": "Comprimidos 100 mg",
    "usos": "Prevención de eventos cardiovasculares solo si te lo ha indicado un médico.",
    "como": "Vía oral, a menudo con comida, a la hora pautada. No es el mismo uso que la aspirina 500 mg para el dolor.",
    "avisos": "Sangrado, úlcera, anticoagulantes, cirugía próxima: tu médico debe saberlo. No empieces por tu cuenta «para el corazón».",
    "efectos": [
      "Acidez",
      "Mayor sangrado",
      "Moratones"
    ],
    "categoria": "cronico"
  },
  {
    "id": "salbutamol",
    "nombre": "Salbutamol (inhalador)",
    "marca": "Ventolin, genéricos…",
    "presentacion": "Inhalador de rescate (aerosol / polvo)",
    "usos": "Alivio rápido de broncoespasmo en asma/EPOC según plan prescrito.",
    "como": "Inhalado con la técnica que te enseñaron. Espaciador si te lo indicaron. No es el único tratamiento del asma persistente.",
    "avisos": "Si necesitas el rescate muy a menudo o no alivia → urgencias / médico (ataque grave). Temblores y subida de ritmo son posibles. Revisa caducidad y técnica.",
    "efectos": [
      "Temblor",
      "Taquicardia",
      "Nerviosismo"
    ],
    "categoria": "cronico"
  },
  {
    "id": "budesonida-nasal",
    "nombre": "Budesonida nasal",
    "marca": "Rhinocort, genéricos…",
    "presentacion": "Spray nasal corticosteroide",
    "usos": "Rinitis alérgica persistente; a menudo con consejo farmacéutico/médico.",
    "como": "Vía nasal; tarda días en notarse el máximo efecto. Técnica: hacia el lateral de la fosa, no al tabique.",
    "avisos": "Heridas nasales, infecciones locales: consulta. Uso largo: revisión. No es descongestivo inmediato tipo xilometazolina.",
    "efectos": [
      "Sequedad nasal",
      "Sangrado leve",
      "Irritación de garganta"
    ],
    "categoria": "alergia"
  },
  {
    "id": "colecalciferol-ampolla",
    "nombre": "Vitamina D3 ampolla bebible",
    "marca": "Deltius 25.000 UI…",
    "presentacion": "Ampollas bebibles de alta dosis",
    "usos": "Corrección de déficit importante bajo pauta médica (no es la misma que el complemento diario bajo).",
    "como": "Solo la pauta que te den tras analítica. Beber tal cual o como indique el prospecto.",
    "avisos": "No repitas ampollas «porque sí»: riesgo de intoxicación. Piedras o calcio alto: control estricto.",
    "efectos": [
      "Náuseas",
      "Sed",
      "Confusión si intoxicación"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "paracetamol-codeina",
    "nombre": "Paracetamol + codeína",
    "marca": "Cod-efferalgan, genéricos…",
    "presentacion": "Comprimidos (analgesia combinada; suele requerir control)",
    "usos": "Dolor más intenso cuando lo prescribe un profesional. Contiene opioide débil.",
    "como": "Solo pauta médica. No conduzcas si te sedan. No combines con otros depresores ni alcohol.",
    "avisos": "Estreñimiento, sueño, dependencia potencial. No en niños para tos/dolor sin criterio estricto. Respeta el máximo de paracetamol del total diario.",
    "efectos": [
      "Somnolencia",
      "Estreñimiento",
      "Náuseas",
      "Mareo"
    ],
    "categoria": "analgesico"
  },
  {
    "id": "paracetamol-pediatrico",
    "nombre": "Paracetamol (suspensión / gotas pediátricas)",
    "marca": "Apiretal, Febrectal, Gelocatil infantil…",
    "presentacion": "Suspensión oral o gotas (concentración según envase; medir solo con el dosificador del producto)",
    "usos": "Alivio de fiebre o dolor en niños cuando un pediatra o el prospecto del envase lo contemplan.",
    "como": "Vía oral. Usa solo el dosificador del envase. La cantidad depende de peso/edad según el prospecto — no improvises ni uses cucharas de cocina. Ante duda: pediatra o farmacéutico.",
    "avisos": "Consulta siempre al pediatra en lactantes, fiebre alta/prolongada, vómitos, letargo o si el niño no mejora. No combines varios productos con paracetamol. No es un diagnóstico ni una pauta prescrita.",
    "efectos": [
      "Molestias digestivas poco frecuentes",
      "Reacciones alérgicas raras",
      "Riesgo hepático si se supera lo indicado en el prospecto"
    ],
    "categoria": "pediatria"
  },
  {
    "id": "ibuprofeno-pediatrico",
    "nombre": "Ibuprofeno (suspensión pediátrica)",
    "marca": "Dalsy, Junifen, Neobrufen infantil…",
    "presentacion": "Suspensión oral (concentración según envase; dosificador incluido)",
    "usos": "Fiebre o dolor con componente inflamatorio en niños, solo según prospecto o pediatra.",
    "como": "Vía oral, preferible con algo de comida. Mide solo con el dosificador del envase. No inventes cantidades.",
    "avisos": "No en deshidratación, vómitos intensos, problemas renales o alergia a AINE sin criterio médico. En niños pequeños o síntomas de alarma: consulta pediatra.",
    "efectos": [
      "Molestia gástrica",
      "Acidez",
      "Mareo",
      "Mayor riesgo digestivo si se usa mal o mucho tiempo"
    ],
    "categoria": "pediatria"
  },
  {
    "id": "simeticona-gotas",
    "nombre": "Simeticona gotas (gases del bebé)",
    "marca": "Aero-Red gotas, Flatuben, genéricos…",
    "presentacion": "Gotas orales (concentración según envase)",
    "usos": "Alivio sintomático de gases y cólicos leves cuando el pediatra o el prospecto lo contemplan.",
    "como": "Vía oral según prospecto del envase. No sustituye valoración si el bebé llora mucho, no come o tiene fiebre.",
    "avisos": "Si hay vómitos, diarrea, fiebre, sangre en heces o decaimiento: pediatra urgente. No es tratamiento de alergia ni de infección.",
    "efectos": [
      "Suele tolerarse bien",
      "Molestia digestiva rara"
    ],
    "categoria": "pediatria"
  },
  {
    "id": "sueroral-pediatrico",
    "nombre": "Sales de rehidratación oral (uso infantil)",
    "marca": "Sueroral, Farmasierra, genéricos…",
    "presentacion": "Sobres para disolver en agua (seguir la dilución exacta del envase)",
    "usos": "Reponer líquidos y sales en diarrea o vómitos leves, según pediatra o prospecto.",
    "como": "Disuelve exactamente como indica el envase. Ofrece a sorbos. No sustituyas por bebidas azucaradas caseras.",
    "avisos": "Si el niño no orina, está muy dormido, vomita todo, tiene sangre en heces o signos de deshidratación grave → urgencias/pediatra. Bebés muy pequeños: siempre criterio profesional.",
    "efectos": [
      "Náuseas si se bebe demasiado rápido",
      "Hinchazón leve"
    ],
    "categoria": "pediatria"
  },
  {
    "id": "suero-nasal-pediatrico",
    "nombre": "Suero fisiológico nasal pediátrico",
    "marca": "Sterimar Baby, Fisiomer, monodosis…",
    "presentacion": "Spray o monodosis de suero isotónico",
    "usos": "Limpieza suave de fosas nasales en congestión por resfriado o mocos.",
    "como": "Según prospecto (suele ser en posición adecuada, sin forzar). No introduzcas objetos en la nariz.",
    "avisos": "Si hay dificultad respiratoria, fiebre alta o el bebé no come: pediatra. No uses descongestionantes vasoconstrictores en lactantes sin indicación expresa.",
    "efectos": [
      "Escozor leve pasajero",
      "Estornudos"
    ],
    "categoria": "pediatria"
  },
  {
    "id": "oxido-zinc-panal",
    "nombre": "Pasta / pomada de óxido de zinc (pañal)",
    "marca": "Bepanthol pomada, Pasta Lassar, Mustela…",
    "presentacion": "Pomada o pasta tópica",
    "usos": "Protección e hidratación de la zona del pañal ante rozaduras leves.",
    "como": "Aplicar en piel limpia y seca según prospecto. Cambios de pañal frecuentes ayudan más que cualquier crema.",
    "avisos": "Si hay ampollas, pus, fiebre o no mejora: pediatra (puede ser infección). Evita productos con corticoide potente sin indicación.",
    "efectos": [
      "Manchas en ropa",
      "Irritación rara si hay alergia a un componente"
    ],
    "categoria": "pediatria"
  },
  {
    "id": "lactasa-gotas",
    "nombre": "Lactasa (gotas / enzima)",
    "marca": "Lactaid, Dilactasa, genéricos…",
    "presentacion": "Gotas o comprimidos masticables (según envase)",
    "usos": "Ayuda a digerir la lactosa en personas con intolerancia, cuando el prospecto lo indica (también hay presentaciones infantiles).",
    "como": "Según prospecto (a menudo añadir a la leche o tomar con lácteos). No cura alergia a la proteína de la leche.",
    "avisos": "Distingue intolerancia a lactosa de alergia a leche (esta última puede ser grave). En bebés: solo con criterio pediátrico. No sustituye dieta indicada por profesional.",
    "efectos": [
      "Suele tolerarse bien",
      "Molestia digestiva rara"
    ],
    "categoria": "pediatria"
  },
  {
    "id": "crema-hidratante-infantil",
    "nombre": "Crema / loción hidratante infantil",
    "marca": "Mustela, A-Derma, LetiAT4, genéricos…",
    "presentacion": "Crema o loción emoliente",
    "usos": "Hidratación de piel seca o tendencia atópica leve, como cuidado diario.",
    "como": "Aplicar en piel limpia según prospecto. En dermatitis de verdad, el pediatra o dermatólogo marcan el plan.",
    "avisos": "Si hay infección, costras amarillas o empeora: consulta. Evita perfumes fuertes en piel muy sensible.",
    "efectos": [
      "Grietas si no se hidrata",
      "Irritación por fragancias en piel atópica"
    ],
    "categoria": "pediatria"
  },
  {
    "id": "cetirizina-gotas-pedia",
    "nombre": "Cetirizina (gotas / solución pediátrica)",
    "marca": "Virlix, Zyrtec, genéricos…",
    "presentacion": "Gotas o solución oral (edad mínima y cantidad: solo prospecto o pediatra)",
    "usos": "Alivio de síntomas alérgicos (rinitis, urticaria) en niños cuando el producto está autorizado para esa edad.",
    "como": "Vía oral según prospecto. No uses antihistamínicos «por si acaso» ni en lactantes sin criterio.",
    "avisos": "Puede dar sueño. Edad mínima estricta según envase. Ante dificultad respiratoria o anafilaxia: 112. Consulta pediatra antes en niños pequeños.",
    "efectos": [
      "Somnolencia",
      "Sequedad de boca",
      "Irritabilidad ocasional"
    ],
    "categoria": "pediatria"
  },
  {
    "id": "antiseptico-piel-pedia",
    "nombre": "Antiséptico suave para piel (uso infantil)",
    "marca": "Clorhexidina diluida, suero + limpieza, productos pediátricos…",
    "presentacion": "Solución o toallitas según envase",
    "usos": "Limpieza de heridas superficiales leves en niños, según prospecto.",
    "como": "Limpiar con suavidad; no fricciones agresivas. Cubre si el pediatra o el farmacéutico lo aconsejan.",
    "avisos": "Heridas profundas, mordeduras, quemaduras extensas o signos de infección → profesional. No uses alcohol fuerte en grandes superficies en bebés.",
    "efectos": [
      "Escozor leve",
      "Irritación si se usa en exceso"
    ],
    "categoria": "pediatria"
  },
  {
    "id": "losartan",
    "nombre": "Losartán",
    "marca": "Cozaar, genéricos…",
    "presentacion": "Comprimidos (dosis según envase/prescripción)",
    "usos": "Tratamiento de la tensión arterial alta y otras indicaciones bajo prescripción médica.",
    "como": "Solo la pauta que te haya indicado tu médico. Vía oral, a menudo a la misma hora. No cambies ni dejes el fármaco por tu cuenta.",
    "avisos": "Embarazo: contraindicado en muchas situaciones — consulta. Controla tensión según te indiquen. Mareo al levantarte, hinchazón o tos: coméntalo. Interacciones posibles (potasio, AINE, etc.).",
    "efectos": [
      "Mareo",
      "Cansancio",
      "Alteraciones de potasio (las valora el médico)"
    ],
    "categoria": "cronico"
  },
  {
    "id": "amlodipino",
    "nombre": "Amlodipino",
    "marca": "Norvas, Astudal, genéricos…",
    "presentacion": "Comprimidos (dosis según prescripción)",
    "usos": "Hipertensión y algunas formas de angina, solo con indicación médica.",
    "como": "Pauta médica. Vía oral. No improvises dosis ni combines con zumo de pomelo si te lo han restringido.",
    "avisos": "Hinchazón de tobillos frecuente. Mareo o palpitaciones: consulta. Embarazo/lactancia: criterio médico. No suspendas de golpe sin consejo.",
    "efectos": [
      "Edema en tobillos",
      "Enrojecimiento facial",
      "Dolor de cabeza",
      "Palpitaciones"
    ],
    "categoria": "cronico"
  },
  {
    "id": "ramipril",
    "nombre": "Ramipril",
    "marca": "Acercomp, genéricos…",
    "presentacion": "Cápsulas / comprimidos (prescripción)",
    "usos": "Hipertensión, protección cardiovascular en pacientes seleccionados — solo médico.",
    "como": "Sigue exactamente la pauta prescrita. Suele tomarse vía oral a hora regular.",
    "avisos": "Tos seca posible (coméntala). Embarazo: no. Control de riñón y potasio según analíticas. Angioedema (hinchazón de cara/lengua): urgencias.",
    "efectos": [
      "Tos",
      "Mareo",
      "Cansancio",
      "Hiperpotasemia (control analítico)"
    ],
    "categoria": "cronico"
  },
  {
    "id": "bisoprolol",
    "nombre": "Bisoprolol",
    "marca": "Emconcor, genéricos…",
    "presentacion": "Comprimidos (prescripción)",
    "usos": "Control de tensión, frecuencia cardiaca o insuficiencia cardiaca según indicación médica.",
    "como": "Solo pauta médica. No lo dejes bruscamente: el médico indica cómo ajustar.",
    "avisos": "Puede enmascarar síntomas de hipoglucemia en diabéticos. Asma/EPOC, bradicardia o bloqueos: solo con criterio estricto. Fatiga al ejercicio: coméntalo.",
    "efectos": [
      "Cansancio",
      "Manos frías",
      "Sueño",
      "Bradicardia si exceso — lo valora el médico"
    ],
    "categoria": "cronico"
  },
  {
    "id": "simvastatina",
    "nombre": "Simvastatina",
    "marca": "Zocor, genéricos…",
    "presentacion": "Comprimidos (prescripción)",
    "usos": "Reducción de colesterol y riesgo cardiovascular bajo control médico.",
    "como": "Pauta médica (a menudo nocturna). Evita zumo de pomelo si te lo indican.",
    "avisos": "Dolor muscular intenso, orina oscura o debilidad: consulta pronto (raro pero importante). Interacciones con algunos antibióticos y antifúngicos. Embarazo: no.",
    "efectos": [
      "Molestia muscular",
      "Alteración de analíticas hepáticas",
      "Digestivo leve"
    ],
    "categoria": "cronico"
  },
  {
    "id": "gliclazida",
    "nombre": "Gliclazida",
    "marca": "Diamicron, genéricos…",
    "presentacion": "Comprimidos (prescripción; diabetes tipo 2)",
    "usos": "Ayuda a controlar la glucosa en diabetes tipo 2 cuando el médico lo prescribe.",
    "como": "Solo pauta médica, alineada con dieta y controles. No «compenses» comidas saltándote o duplicando tomas por tu cuenta.",
    "avisos": "Riesgo de hipoglucemia (temblor, sudor, confusión): actúa según te hayan enseñado y consulta. Alcohol y ayunos aumentan el riesgo. Embarazo: otro manejo.",
    "efectos": [
      "Hipoglucemia",
      "Aumento de peso posible",
      "Molestia digestiva"
    ],
    "categoria": "cronico"
  },
  {
    "id": "clopidogrel",
    "nombre": "Clopidogrel",
    "marca": "Plavix, genéricos…",
    "presentacion": "Comprimidos (prescripción; antiagregante)",
    "usos": "Prevención de eventos trombóticos en pacientes seleccionados — solo médico.",
    "como": "Pauta estricta. No lo suspendas antes de una cirugía sin que lo sepan médico y cirujano.",
    "avisos": "Aumenta el sangrado. Avisa siempre que tomas antiagregante. Úlcera, AINE o anticoagulantes: control. Alergias raras.",
    "efectos": [
      "Moretones",
      "Sangrado de encías",
      "Molestia digestiva",
      "Hemorragia (urgencia si es importante)"
    ],
    "categoria": "cronico"
  },
  {
    "id": "furosemida",
    "nombre": "Furosemida",
    "marca": "Seguril, genéricos…",
    "presentacion": "Comprimidos / ampollas (prescripción; diurético)",
    "usos": "Eliminar retención de líquidos en insuficiencia cardiaca u otras indicaciones médicas.",
    "como": "Solo pauta médica. Suele aumentar la orina; el médico fija horario y controles de electrolitos.",
    "avisos": "Deshidratación, mareo, bajada de potasio o sodio: control analítico. No compenses bebiendo «a ciegas» ni tomes suplementos de potasio sin indicación.",
    "efectos": [
      "Aumento de orina",
      "Calambres",
      "Mareo",
      "Alteración de sales (lo vigila el médico)"
    ],
    "categoria": "cronico"
  },
  {
    "id": "insulina-info",
    "nombre": "Insulina (información general)",
    "marca": "Distintos tipos y marcas (rápida, basal, mezclas…)",
    "presentacion": "Plumas / viales inyectables (solo con prescripción y educación diabetológica)",
    "usos": "Tratamiento de la diabetes cuando el médico lo indica. Hay muchos tipos: no son intercambiables a la ligera.",
    "como": "Solo la técnica, tipo y horario que te hayan enseñado. Conservación según prospecto (nevera/temperatura ambiente según producto). Nunca compartas agujas.",
    "avisos": "Hipoglucemia es la urgencia más frecuente: ten un plan. No cambies de tipo ni de marca sin criterio. Embarazo, enfermedad aguda o ejercicio intenso: consulta tu equipo. Esta ficha NO enseña a pinchar ni a calcular dosis.",
    "efectos": [
      "Hipoglucemia",
      "Lipodistrofia en zona de inyección",
      "Aumento de peso posible"
    ],
    "categoria": "cronico"
  },
  {
    "id": "ibp-largo-plazo",
    "nombre": "IBP a largo plazo (omeprazol y similares)",
    "marca": "Omeprazol, pantoprazol, esomeprazol…",
    "presentacion": "Cápsulas/comprimidos (automedicación breve o pauta médica prolongada)",
    "usos": "Acidez/reflujo; a veces protección gástrica crónica bajo control.",
    "como": "Si lo usas muchos meses, debe haber un plan médico (necesidad, dosis mínima, revisiones).",
    "avisos": "No alargues indefinidamente «por costumbre» sin revisión. Síntomas de alarma (sangre, pérdida de peso, disfagia): estudio. Interacciones y déficits posibles a muy largo plazo.",
    "efectos": [
      "Cefalea",
      "Gases",
      "Con uso muy largo: posibles déficits — lo valora el médico"
    ],
    "categoria": "cronico"
  },
  {
    "id": "butilescopolamina",
    "nombre": "Butilescopolamina (butilbromuro de escopolamina)",
    "marca": "Buscapina, genéricos…",
    "presentacion": "Comprimidos / grageas (también inyectable hospitalario)",
    "usos": "Alivio de espasmos digestivos o menstruales cuando el prospecto o el médico lo indican.",
    "como": "Vía oral según prospecto. No es el tratamiento de un abdomen agudo grave.",
    "avisos": "Si el dolor es intenso, con fiebre, vómito continuo o abdomen duro → urgencias. Glaucoma, retención urinaria, miastenia: consulta. Puede dar sequedad y visión borrosa.",
    "efectos": [
      "Boca seca",
      "Estreñimiento",
      "Visión borrosa",
      "Taquicardia ocasional"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "diosmectita",
    "nombre": "Diosmectita (smectita)",
    "marca": "Smecta, genéricos…",
    "presentacion": "Sobres para suspensión oral",
    "usos": "Alivio sintomático de diarrea aguda leve en adultos/niños según prospecto.",
    "como": "Disolver y tomar según envase. Mantén hidratación (sales si procede).",
    "avisos": "Diarrea con sangre, fiebre alta o deshidratación: médico. Puede reducir absorción de otros fármacos: separa tomas según prospecto. Niños: criterio pediátrico.",
    "efectos": [
      "Estreñimiento",
      "Heces más claras"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "racecadotrilo",
    "nombre": "Racecadotrilo",
    "marca": "Tiorfan, genéricos…",
    "presentacion": "Cápsulas / sobres (según edad autorizada)",
    "usos": "Tratamiento sintomático de la diarrea aguda junto a rehidratación, según prospecto o médico.",
    "como": "Vía oral según envase. La base es hidratarse bien.",
    "avisos": "No sustituye valoración si hay sangre, fiebre alta o diarrea prolongada. Edad mínima según producto. Embarazo: consulta.",
    "efectos": [
      "Dolor de cabeza",
      "Erupción rara",
      "Náuseas"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "alginato-antiacido",
    "nombre": "Alginato + antiácido (tipo Gaviscon)",
    "marca": "Gaviscon, Algiscon, genéricos…",
    "presentacion": "Comprimidos masticables / suspensión",
    "usos": "Ardor y reflujo ocasional formando una «balsa» protectora, según prospecto.",
    "como": "Suele tomarse tras comidas o al acostarse según envase. Mastica bien si son comprimidos.",
    "avisos": "Si necesitas antiácido a diario muchas semanas o hay alarma (sangre, disfagia, pérdida de peso): médico. Hipertensión/sodio: mira composición. Embarazo: muchas veces se usa, pero confirma.",
    "efectos": [
      "Náuseas",
      "Estreñimiento o diarrea según componente"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "bisacodilo",
    "nombre": "Bisacodilo",
    "marca": "Dulcolax, genéricos…",
    "presentacion": "Comprimidos gastrorresistentes / supositorios",
    "usos": "Estreñimiento ocasional a corto plazo según prospecto.",
    "como": "Vía oral o rectal según presentación. No es un hábito diario ideal.",
    "avisos": "Uso prolongado puede empeorar el estreñimiento. Dolor intenso, sangre o sospecha de obstrucción: médico. Embarazo/niños: consulta.",
    "efectos": [
      "Cólicos",
      "Diarrea",
      "Malestar abdominal"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "glicerina-supositorio",
    "nombre": "Glicerina (supositorios / microenemas)",
    "marca": "Verolax, Micralax, glicerina…",
    "presentacion": "Supositorios o microenemas",
    "usos": "Alivio local del estreñimiento ocasional.",
    "como": "Uso rectal según prospecto. Hidratación y fibra suelen ser la base a medio plazo.",
    "avisos": "No uses a diario de forma crónica sin consejo. Sangre, dolor intenso o no hay deposición: médico.",
    "efectos": [
      "Escozor local",
      "Cólico leve"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "saccharomyces",
    "nombre": "Saccharomyces boulardii (probiótico levadura)",
    "marca": "Ultra-Levura, genéricos…",
    "presentacion": "Cápsulas / sobres",
    "usos": "Complemento en diarrea asociada a antibióticos u otros contextos según prospecto.",
    "como": "Vía oral según envase. Separar de antifúngicos si te lo indican.",
    "avisos": "Inmunodeprimidos o vías centrales: riesgo raro de fungemia — solo con criterio médico. No sustituye rehidratación ni estudio de diarrea grave.",
    "efectos": [
      "Gases",
      "Hinchazón leve"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "carbon-vegetal-digest",
    "nombre": "Carbón vegetal (gases / digestivo)",
    "marca": "Carbón vegetal activado (dosis digestivas OTC)",
    "presentacion": "Comprimidos / cápsulas",
    "usos": "Alivio sintomático de gases y flatulencia ocasional (distinto del uso de urgencias por intoxicación).",
    "como": "Según prospecto OTC. Puede ennegrecer las heces.",
    "avisos": "Reduce absorción de fármacos y anticonceptivos orales: separa tomas. Intoxicación aguda: 112 / toxicología, no automedicación casera. Embarazo: consulta.",
    "efectos": [
      "Estreñimiento",
      "Heces negras",
      "Náuseas"
    ],
    "categoria": "digestivo"
  },
  {
    "id": "clotrimazol-crema",
    "nombre": "Clotrimazol crema",
    "marca": "Canesten, genéricos…",
    "presentacion": "Crema tópica 1% (también óvulos en otra ficha)",
    "usos": "Infecciones fúngicas superficiales de la piel (pie de atleta, tiña) según prospecto.",
    "como": "Aplicar en zona limpia y seca según envase, completar el tiempo indicado aunque mejore antes.",
    "avisos": "Si no mejora, hay pus o afecta uñas/cuero cabelludo extensamente: médico. Evita mucosas oculares. Embarazo: consulta para uso vaginal.",
    "efectos": [
      "Escozor local",
      "Enrojecimiento",
      "Irritación"
    ],
    "categoria": "topico"
  },
  {
    "id": "miconazol-crema",
    "nombre": "Miconazol crema",
    "marca": "Daktarin, genéricos…",
    "presentacion": "Crema / gel tópico",
    "usos": "Hongos cutáneos superficiales y algunas candidiasis de pliegues, según prospecto.",
    "como": "Capa fina según envase. Mantén la zona seca.",
    "avisos": "Interacción posible con anticoagulantes orales si hay mucha superficie: pregunta. Si no mejora o empeora: médico.",
    "efectos": [
      "Irritación local",
      "Quemazón"
    ],
    "categoria": "topico"
  },
  {
    "id": "aciclovir-labial",
    "nombre": "Aciclovir crema (labial)",
    "marca": "Zovirax labial, genéricos…",
    "presentacion": "Crema para herpes labial",
    "usos": "Acortar/aliviar brotes de herpes labial cuando se inicia pronto, según prospecto.",
    "como": "Aplicar en la zona al notar hormigueo, según envase. Lavarse las manos; no compartir.",
    "avisos": "No cura de forma definitiva ni evita todos los brotes. Herpes ocular o inmunodepresión: médico urgente. Embarazo: consulta.",
    "efectos": [
      "Sequedad",
      "Escozor leve"
    ],
    "categoria": "topico"
  },
  {
    "id": "diclofenaco-gel",
    "nombre": "Diclofenaco gel / spray",
    "marca": "Voltaren Emulgel, genéricos…",
    "presentacion": "Gel o spray tópico",
    "usos": "Alivio local de dolor muscular o articular leve-moderado.",
    "como": "Aplicar en zona intacta según prospecto. No uses oclusión fuerte ni en heridas abiertas.",
    "avisos": "Aunque es tópico, es AINE: cuidado si te han restringido AINE, embarazo o piel dañada. No combines muchos AINE. Fotosensibilidad posible.",
    "efectos": [
      "Enrojecimiento",
      "Picor",
      "Erupción"
    ],
    "categoria": "topico"
  },
  {
    "id": "calamina",
    "nombre": "Loción de calamina",
    "marca": "Calamina, genéricos…",
    "presentacion": "Loción tópica",
    "usos": "Alivio sintomático de picor y escozor leves (picaduras, irritaciones).",
    "como": "Agitar y aplicar según prospecto en piel limpia.",
    "avisos": "No en mucosas ni heridas profundas. Si hay infección, fiebre o reacción generalizada: médico. Mancha la ropa.",
    "efectos": [
      "Sequedad",
      "Irritación rara"
    ],
    "categoria": "topico"
  },
  {
    "id": "permetrina-piojos",
    "nombre": "Permetrina (piojos / escabiosis según producto)",
    "marca": "Srepiol, Nix, genéricos…",
    "presentacion": "Crema o loción a concentración según indicación del envase",
    "usos": "Tratamiento de pediculosis (piojos) u otras indicaciones del prospecto concreto.",
    "como": "Sigue el tiempo de contacto y aclarado del envase al pie de la letra. Lava ropa de cama/peines según instrucciones.",
    "avisos": "No uses concentraciones de otro uso. Edad mínima y embarazo: prospecto/profesional. Picor puede continuar días tras matar piojos: no es fallo inmediato.",
    "efectos": [
      "Picor",
      "Enrojecimiento",
      "Escozor del cuero cabelludo"
    ],
    "categoria": "topico"
  },
  {
    "id": "protector-solar",
    "nombre": "Protector solar (FPS)",
    "marca": "ISDIN, La Roche-Posay, Avène, genéricos…",
    "presentacion": "Crema / spray / fluido FPS 30–50+",
    "usos": "Prevención de quemadura solar y daño actínico; parte del cuidado diario en muchas personas.",
    "como": "Cantidad generosa, renovar según prospecto (agua, sudor, tiempo). No sustituye sombra ni ropa.",
    "avisos": "Quemadura intensa, ampollas o golpe de calor: valoración. Alergia a filtros: prueba y consulta. Bebés: criterio pediátrico y sombra prioritaria.",
    "efectos": [
      "Ojos irritados si espray",
      "Foliculitis rara",
      "Manchas en ropa"
    ],
    "categoria": "topico"
  },
  {
    "id": "minoxidil-topico",
    "nombre": "Minoxidil tópico",
    "marca": "Regaine, genéricos…",
    "presentacion": "Solución o espuma (concentración según envase)",
    "usos": "Tratamiento de algunos tipos de alopecia androgenética en adultos, según prospecto.",
    "como": "Aplicar en cuero cabelludo seco según envase. La respuesta tarda meses; al dejarlo puede revertirse.",
    "avisos": "No en menores sin criterio. Problemas cardiacos, embarazo/lactancia: consulta. Irritación intensa o crecimiento no deseado en otras zonas: para y pregunta. No es milagroso en todas las alopecias.",
    "efectos": [
      "Picor",
      "Caspa",
      "Caída inicial temporal",
      "Hipertricosis en otras zonas si escurre"
    ],
    "categoria": "topico"
  },
  {
    "id": "astringente-aluminio",
    "nombre": "Solución / pasta astringente (aluminio)",
    "marca": "Productos astringentes de farmacia / fórmulas suaves…",
    "presentacion": "Solución o pasta según producto",
    "usos": "Alivio de maceración leve en pliegues o rozaduras, según prospecto.",
    "como": "Aplicar en piel limpia según envase; seca bien la zona.",
    "avisos": "Infección evidente (pus, fiebre): médico. No en mucosas profundas sin indicación.",
    "efectos": [
      "Sequedad",
      "Irritación"
    ],
    "categoria": "topico"
  },
  {
    "id": "ambroxol",
    "nombre": "Ambroxol",
    "marca": "Mucosan, genéricos…",
    "presentacion": "Jarabe / comprimidos",
    "usos": "Facilitar la expulsión de moco en catarros con tos productiva, según prospecto.",
    "como": "Vía oral según envase. Bebe líquidos. No combines mucolíticos y antitusígenos a ciegas.",
    "avisos": "Tos con sangre, disnea o dura más de 1–2 semanas: médico. Úlcera activa o embarazo: consulta. Reacciones cutáneas graves raras: suspende y urgencias.",
    "efectos": [
      "Náuseas",
      "Diarrea",
      "Alteración del gusto"
    ],
    "categoria": "respiratorio"
  },
  {
    "id": "pseudoefedrina",
    "nombre": "Pseudoefedrina (descongestionante oral)",
    "marca": "En compuestos resfriados (varios); control de dispensación en España",
    "presentacion": "Comprimidos / sobres (a menudo combinada; suele haber control en farmacia)",
    "usos": "Alivio temporal de congestión nasal en resfriado o rinitis, según prospecto.",
    "como": "Vía oral respetando máximo e intervalos del envase. No uses varios productos con el mismo principio.",
    "avisos": "Hipertensión, corazón, glaucoma, próstata, hipertiroidismo, IMAO: consulta o evita. Nerviosismo, insomnio. Embarazo: criterio profesional. No en niños pequeños según envase.",
    "efectos": [
      "Insomnio",
      "Nerviosismo",
      "Taquicardia",
      "Subida de tensión"
    ],
    "categoria": "respiratorio"
  },
  {
    "id": "fenilefrina-oral",
    "nombre": "Fenilefrina (en compuestos resfriados)",
    "marca": "Varios anticatarrales combinados…",
    "presentacion": "Comprimidos / sobres combinados",
    "usos": "Descongestión nasal sintomática a corto plazo según prospecto del compuesto.",
    "como": "Sigue el envase del producto concreto (a menudo lleva también analgésico).",
    "avisos": "Cuidado con tensión, corazón y combinación con otros descongestionantes. Lee todos los principios del sobre. Embarazo/niños: prospecto.",
    "efectos": [
      "Nerviosismo",
      "Dolor de cabeza",
      "Insomnio"
    ],
    "categoria": "respiratorio"
  },
  {
    "id": "fluticasona-nasal",
    "nombre": "Fluticasona spray nasal",
    "marca": "Flixonase, Avamys (otros), genéricos…",
    "presentacion": "Spray nasal (algunas presentaciones OTC / otras con consejo)",
    "usos": "Rinitis alérgica: reducir inflamación local según prospecto.",
    "como": "Técnica de spray según envase; constancia. No es descongestionante «de un minuto».",
    "avisos": "Heridas nasales, infecciones o uso prolongado: revisa con profesional. Visión o sangrado nasal persistente: consulta. Niños: edad autorizada.",
    "efectos": [
      "Sequedad nasal",
      "Sangrado leve",
      "Irritación de garganta"
    ],
    "categoria": "respiratorio"
  },
  {
    "id": "oximetazolina",
    "nombre": "Oximetazolina (nasal)",
    "marca": "Respons, Utabon Adultos, genéricos…",
    "presentacion": "Spray / gotas nasales",
    "usos": "Descongestión nasal rápida a muy corto plazo.",
    "como": "Según prospecto. Máximo pocos días seguidos (riesgo de efecto rebote).",
    "avisos": "No alargues: rinitis medicamentosa. Hipertensión/corazón: cuidado. Niños: solo productos y edades autorizadas. Embarazo: consulta.",
    "efectos": [
      "Ardor nasal",
      "Sequedad",
      "Congestión de rebote si se abusa"
    ],
    "categoria": "respiratorio"
  },
  {
    "id": "pastillas-miel-limon",
    "nombre": "Pastillas / jarabes demulcentes (miel-limón, etc.)",
    "marca": "Varios OTC de garganta y tos irritativa…",
    "presentacion": "Pastillas para chupar / jarabes suaves",
    "usos": "Alivio sintomático de irritación de garganta y tos seca leve.",
    "como": "Chupar / tomar según envase. Hidratación y humedad ambiental ayudan.",
    "avisos": "Miel no en menores de 1 año. Tos con ahogo, fiebre alta o tos que dura: médico. Diabéticos: mira azúcares.",
    "efectos": [
      "Náuseas raras",
      "Caries si abuso de azucaradas"
    ],
    "categoria": "respiratorio"
  },
  {
    "id": "mentol-balsamo",
    "nombre": "Bálsamos / ungüentos mentolados",
    "marca": "Vicks VapoRub, genéricos…",
    "presentacion": "Ungüento tópico aromático",
    "usos": "Sensación de alivio en resfriado (aplicación cutánea según prospecto).",
    "como": "Pecho/espalda según envase. No aplicar en fosas nasales de lactantes ni ingerir.",
    "avisos": "Prohibido en cara/nariz de bebés (riesgo respiratorio). Irritación cutánea posible. No sustituye valoración de disnea.",
    "efectos": [
      "Irritación de piel",
      "Lagrimeo si cerca de ojos"
    ],
    "categoria": "respiratorio"
  },
  {
    "id": "clotrimazol-ovulos",
    "nombre": "Clotrimazol óvulos / crema vaginal",
    "marca": "Canesten óvulos, genéricos…",
    "presentacion": "Óvulos o crema intravaginal",
    "usos": "Candidiasis vaginal no complicada según prospecto, cuando los síntomas son típicos y ya conocidos.",
    "como": "Según envase (a menudo al acostarse). Completa el ciclo indicado.",
    "avisos": "Primera vez, embarazo, fiebre, dolor bajo, flujo maloliente o no mejora: médico (puede no ser cándida). Interacción con látex: mira prospecto.",
    "efectos": [
      "Escozor local",
      "Flujo al expulsar el óvulo"
    ],
    "categoria": "femenina"
  },
  {
    "id": "miconazol-ovulos",
    "nombre": "Miconazol vaginal",
    "marca": "Gyno-Daktarin, genéricos…",
    "presentacion": "Óvulos / crema vaginal",
    "usos": "Infección vaginal por hongos según prospecto.",
    "como": "Aplicación vaginal según envase.",
    "avisos": "Misma cautela que otros antifúngicos vaginales: síntomas atípicos → consulta. Embarazo: profesional. Puede dañar preservativos de látex.",
    "efectos": [
      "Irritación",
      "Picor inicial"
    ],
    "categoria": "femenina"
  },
  {
    "id": "hialuronico-vaginal",
    "nombre": "Gel / óvulos de ácido hialurónico (sequedad)",
    "marca": "Varios hidratantes vaginales OTC…",
    "presentacion": "Gel o óvulos hidratantes",
    "usos": "Alivio de sequedad vaginal y molestia por falta de lubricación, según prospecto.",
    "como": "Según envase. No trata infecciones ni ETS.",
    "avisos": "Sangrado, dolor intenso u olor fuerte: médico. Embarazo/postparto: pregunta. Distingue hidratante de tratamiento hormonal (este último es médico).",
    "efectos": [
      "Escozor leve",
      "Secreción pasajera"
    ],
    "categoria": "femenina"
  },
  {
    "id": "lubricante-intimo",
    "nombre": "Lubricante íntimo (base agua / silicona)",
    "marca": "Varios OTC…",
    "presentacion": "Gel lubricante",
    "usos": "Reducir fricción y molestia en relaciones o uso de dispositivos, según producto.",
    "como": "Según envase. Compatibilidad con preservativos: lee la etiqueta (aceites pueden dañar látex).",
    "avisos": "Irritación persistente: consulta. No sustituye preservativo frente a ETS. Infección activa: profesional.",
    "efectos": [
      "Irritación por fragancias",
      "Pegajosidad"
    ],
    "categoria": "femenina"
  },
  {
    "id": "test-embarazo",
    "nombre": "Test de embarazo (orina)",
    "marca": "Clearblue, Predictor, genéricos de farmacia…",
    "presentacion": "Tira / dispositivo de orina",
    "usos": "Detección orientativa de hCG en orina tras retraso menstrual.",
    "como": "Sigue el tiempo y la línea de control del envase. Mejor con primera orina de la mañana si el prospecto lo dice.",
    "avisos": "Falsos negativos tempranos posibles. Resultado positivo o duda: confirma con profesional. Medicamentos de fertilidad con hCG pueden interferir.",
    "efectos": [
      "No es un fármaco; resultado ambiguo — repite o consulta"
    ],
    "categoria": "femenina"
  },
  {
    "id": "hierro-embarazo-info",
    "nombre": "Hierro en embarazo (información)",
    "marca": "Ferrosos / ferrimanitol según pauta…",
    "presentacion": "Comprimidos / sobres (a menudo prescritos tras analítica)",
    "usos": "Corregir o prevenir anemia ferropénica en gestación cuando el médico/matrona lo indican.",
    "como": "Solo la pauta del equipo de embarazo. A menudo mejor con estómago adecuado y separado de algunos alimentos/fármacos según te digan.",
    "avisos": "No te automediques dosis altas: exceso de hierro es peligroso. Estreñimiento frecuente: coméntalo. Esta ficha no sustituye controles de embarazo.",
    "efectos": [
      "Náuseas",
      "Estreñimiento",
      "Heces oscuras"
    ],
    "categoria": "femenina"
  },
  {
    "id": "arandano-rojo",
    "nombre": "Arándano rojo (vaccinium) complemento",
    "marca": "Varios complementos OTC…",
    "presentacion": "Cápsulas / sobres / zumo (concentración variable)",
    "usos": "Complemento tradicionalmente usado en higiene urinaria; evidencia mixta. No sustituye antibiótico si hay infección.",
    "como": "Según envase del complemento. Hidratación abundante es clave.",
    "avisos": "Ardor al orinar, fiebre, sangre o dolor lumbar: médico (posible ITU). Interacciones con anticoagulantes posibles en extractos. Embarazo: pregunta.",
    "efectos": [
      "Molestia gástrica",
      "Diarrea si zumo muy azucarado"
    ],
    "categoria": "urologia"
  },
  {
    "id": "d-manosa",
    "nombre": "D-manosa",
    "marca": "Complementos varios…",
    "presentacion": "Sobres / cápsulas",
    "usos": "Complemento usado por algunas personas en el contexto de molestias urinarias leves; no es antibiótico.",
    "como": "Según envase. Bebe agua. Si hay infección real, el médico decide el tratamiento.",
    "avisos": "No retrases la consulta si hay fiebre, dolor intenso o embarazo. Diabéticos: mira aporte de azúcares. Evidencia limitada.",
    "efectos": [
      "Hinchazón",
      "Diarrea leve"
    ],
    "categoria": "urologia"
  },
  {
    "id": "fosfomicina-info",
    "nombre": "Fosfomicina trometamol (información)",
    "marca": "Monurol, genéricos…",
    "presentacion": "Sobre de dosis única (prescripción habitual en cistitis no complicada)",
    "usos": "Antibiótico de toma única en cistitis seleccionadas — solo con criterio médico/farmacéutico según protocolo.",
    "como": "Solo si te lo indican. Disolver y tomar según prospecto, a menudo en ayunas nocturno.",
    "avisos": "No automedicación repetida. Pielonefritis, hombre, embarazo, catéter o recidivas: otro manejo. Resistencias y alergias importan.",
    "efectos": [
      "Diarrea",
      "Náuseas",
      "Cefalea"
    ],
    "categoria": "urologia"
  },
  {
    "id": "tamsulosina-info",
    "nombre": "Tamsulosina (información)",
    "marca": "Omnic, genéricos…",
    "presentacion": "Cápsulas de liberación (prescripción; próstata)",
    "usos": "Facilitar el vaciado urinario en hiperplasia prostática sintomática bajo control médico.",
    "como": "Pauta médica. Suele tomarse siempre igual respecto a comidas según envase.",
    "avisos": "Mareo al levantarse. Cirugía de cataratas: avisa (síndrome de iris flácido). No compartas con otras personas.",
    "efectos": [
      "Mareo",
      "Eyaculación retrógrada",
      "Congestión nasal"
    ],
    "categoria": "urologia"
  },
  {
    "id": "higiene-perianal",
    "nombre": "Higiene / baños de asiento (cuidado perianal)",
    "marca": "Productos de higiene suaves, agua tibia…",
    "presentacion": "Cuidado no farmacológico / jabones suaves",
    "usos": "Alivio de molestia perianal leve (hemorroides externas irritadas, etc.) como medida de confort.",
    "como": "Agua tibia, secar sin frotar. Fibras e hidratación ayudan al estreñimiento asociado.",
    "avisos": "Sangre abundante, dolor intenso, fiebre o bulto que no reduce: médico. Cremas con anestésicos/corticoides: solo según prospecto y poco tiempo.",
    "efectos": [
      "Irritación por jabones perfumados"
    ],
    "categoria": "urologia"
  },
  {
    "id": "hipromelosa",
    "nombre": "Hipromelosa (lágrimas artificiales)",
    "marca": "Artific, Viscofresh, genéricos…",
    "presentacion": "Colirio / monodosis",
    "usos": "Alivio de ojo seco e irritación leve por ambiente o pantallas.",
    "como": "Según prospecto. Si el envase es multidosis con conservante, respeta caducidad tras apertura.",
    "avisos": "Dolor intenso, pérdida de visión, ojo rojo con secreción o traumatismo: urgencias/oftalmólogo. Lentes de contacto: mira compatibilidad.",
    "efectos": [
      "Visión borrosa breve tras instilar",
      "Escozor leve"
    ],
    "categoria": "oftalmologia"
  },
  {
    "id": "hialuronico-ocular",
    "nombre": "Ácido hialurónico ocular",
    "marca": "Hylo, Thealoz Duo (combinados), genéricos…",
    "presentacion": "Colirio lubricante",
    "usos": "Lubricación más duradera en ojo seco, según prospecto.",
    "como": "Instilar según envase. Monodosis: desechar tras uso si así lo indica.",
    "avisos": "Misma alerta de síntomas graves que otras lágrimas. Infección: no solo lubricar.",
    "efectos": [
      "Visión borrosa momentánea",
      "Pegajosidad leve"
    ],
    "categoria": "oftalmologia"
  },
  {
    "id": "ketotifeno-colirio",
    "nombre": "Ketotifeno colirio (antialérgico)",
    "marca": "Zaditen, genéricos…",
    "presentacion": "Colirio",
    "usos": "Alivio de síntomas de conjuntivitis alérgica (picor, lagrimeo) según prospecto.",
    "como": "Según envase. Quítate lentillas si el prospecto lo pide y espera para ponértelas.",
    "avisos": "Ojo rojo doloroso con visión borrosa: no es «solo alergia» → profesional. Niños: edad autorizada. Embarazo: consulta.",
    "efectos": [
      "Escozor",
      "Visión borrosa breve",
      "Sequedad"
    ],
    "categoria": "oftalmologia"
  },
  {
    "id": "suero-ocular-monodosis",
    "nombre": "Suero fisiológico ocular (monodosis)",
    "marca": "Fisiológico monodosis farmacia…",
    "presentacion": "Monodosis estériles",
    "usos": "Lavado suave o alivio de irritación leve / cuerpo extraño superficial tras valoración.",
    "como": "Según técnica del envase. No reutilices monodosis abiertas si el prospecto lo prohíbe.",
    "avisos": "Cuerpo extraño clavado, químico o pérdida visual: urgencias, no improvises. Evita colirios vasoconstrictores de «ojo rojo» de forma habitual.",
    "efectos": [
      "Escozor leve"
    ],
    "categoria": "oftalmologia"
  },
  {
    "id": "pomada-lubricante-ocular",
    "nombre": "Pomada oftálmica lubricante",
    "marca": "Lubricantes nocturnos varios…",
    "presentacion": "Pomada estéril oftálmica",
    "usos": "Ojo seco nocturno o protección de la superficie ocular según prospecto.",
    "como": "Aplicar según envase (a menudo por la noche: borra la visión).",
    "avisos": "No conduzcas tras aplicarla. Infección o herida: oftalmólogo. Caducidad tras apertura.",
    "efectos": [
      "Visión borrosa",
      "Pegajosidad"
    ],
    "categoria": "oftalmologia"
  },
  {
    "id": "lagrimas-vision-general",
    "nombre": "Lágrimas artificiales (visión general)",
    "marca": "Varias marcas de farmacia…",
    "presentacion": "Colirios lubricantes con o sin conservante",
    "usos": "Síntomas leves de ojo seco; complemento de hábitos (parpadear, humidificar, pausas de pantalla).",
    "como": "Según envase. Si usas varios colirios, separa unos minutos.",
    "avisos": "Uso diario continuo sin mejora → oftalmólogo. Conservantes pueden molestar si instilas muy a menudo: valora monodosis.",
    "efectos": [
      "Escozor",
      "Visión borrosa breve"
    ],
    "categoria": "oftalmologia"
  },
  {
    "id": "omega3",
    "nombre": "Omega-3 (EPA/DHA)",
    "marca": "Varios complementos de pescado o algas…",
    "presentacion": "Cápsulas / perlas",
    "usos": "Complemento dietético graso; no sustituye medicación cardiovascular prescrita.",
    "como": "Según envase, a menudo con comida. Mira equivalencia EPA/DHA.",
    "avisos": "Anticoagulantes o cirugía: consulta (puede influir en coagulación a dosis altas). Alergia a pescado: elige fuente adecuada. Embarazo: criterio profesional.",
    "efectos": [
      "Eructos a pescado",
      "Molestia gástrica",
      "Diarrea"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "zinc-suplemento",
    "nombre": "Zinc (complemento)",
    "marca": "Varios…",
    "presentacion": "Comprimidos / cápsulas",
    "usos": "Aporte de zinc cuando la dieta es insuficiente o lo indica un profesional.",
    "como": "Según envase; no abuses de dosis altas prolongadas.",
    "avisos": "Exceso crónico puede alterar cobre e inmunidad. Náuseas en ayunas. Interacciones con algunos antibióticos (separar).",
    "efectos": [
      "Náuseas",
      "Sabor metálico",
      "Molestia gástrica"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "probiotico-adulto",
    "nombre": "Probiótico (combinaciones adultas)",
    "marca": "Lactobacillus/Bifidobacterium varios…",
    "presentacion": "Cápsulas / sobres",
    "usos": "Complemento de microbiota en contextos de diarrea o tras antibióticos según prospecto del producto.",
    "como": "Según envase; a veces separar del antibiótico unas horas.",
    "avisos": "Inmunodepresión grave: consulta. No sustituye diagnóstico de diarrea inflamatoria. Calidad varía entre marcas.",
    "efectos": [
      "Gases",
      "Hinchazón inicial"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "multivitaminico",
    "nombre": "Multivitamínico adulto",
    "marca": "Supradyn, Centrum, genéricos…",
    "presentacion": "Comprimidos efervescentes / cápsulas",
    "usos": "Complemento cuando la dieta puede ser incompleta; no sustituye alimentación ni tratamientos.",
    "como": "Según envase. No combines varios multimix (riesgo de exceso de A/D/hierro).",
    "avisos": "Embarazo: usa el preparado indicado (ácido fólico específico). Hierro/vitamina A en exceso: peligroso. Analíticas si hay síntomas.",
    "efectos": [
      "Orina más amarilla (riboflavina)",
      "Náuseas",
      "Estreñimiento si lleva hierro"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "colageno",
    "nombre": "Colágeno (hidrolizado) complemento",
    "marca": "Varios…",
    "presentacion": "Polvo / comprimidos",
    "usos": "Complemento popular para piel/articulaciones; evidencia variable. No es un fármaco antiartrósico prescrito.",
    "como": "Según envase, a menudo disuelto.",
    "avisos": "Alergia a fuente (pescado/bovino). Enfermedad renal grave: consulta. No sustituye fisioterapia ni analgésicos indicados.",
    "efectos": [
      "Saciedad",
      "Molestia digestiva",
      "Sabor"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "valeriana",
    "nombre": "Valeriana",
    "marca": "Valerianadis, genéricos de planta…",
    "presentacion": "Comprimidos / cápsulas / infusiones",
    "usos": "Tradicionalmente usada para nerviosismo leve o dificultad para dormir, según prospecto de planta.",
    "como": "Según envase. No conduzcas si te sedas.",
    "avisos": "No combinar a la ligera con alcohol, hipnóticos o ansiolíticos. Embarazo/lactancia/niños: consulta. Insomnio crónico: profesional (puede haber otra causa).",
    "efectos": [
      "Somnolencia",
      "Sueños vívidos",
      "Molestia gástrica"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "passiflora",
    "nombre": "Passiflora (pasionaria)",
    "marca": "Complementos/plantas varios…",
    "presentacion": "Comprimidos / infusión",
    "usos": "Uso tradicional en nerviosismo leve según prospecto.",
    "como": "Según envase.",
    "avisos": "Sedación posible. Interacciones con sedantes. Embarazo: consulta. No sustituye tratamiento de ansiedad diagnosticada.",
    "efectos": [
      "Somnolencia",
      "Mareo leve"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "coenzima-q10",
    "nombre": "Coenzima Q10",
    "marca": "Varios complementos…",
    "presentacion": "Cápsulas",
    "usos": "Complemento; a veces comentado junto a estatinas, sin sustituir la medicación prescrita.",
    "como": "Según envase, preferible con comida grasa.",
    "avisos": "Anticoagulantes: consulta. Cirugía: informa. Evidencia mixta según objetivo. Embarazo: pregunta.",
    "efectos": [
      "Insomnio ocasional",
      "Molestia gástrica"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "onagra",
    "nombre": "Aceite de onagra",
    "marca": "Complementos varios…",
    "presentacion": "Perlas",
    "usos": "Uso tradicional en molestias cíclicas leves; evidencia limitada.",
    "como": "Según envase.",
    "avisos": "Epilepsia o anticoagulantes: consulta. Embarazo: no sin criterio. No sustituye valoración ginecológica.",
    "efectos": [
      "Náuseas",
      "Cefalea",
      "Heces blandas"
    ],
    "categoria": "vitamina"
  },
  {
    "id": "curcuma",
    "nombre": "Cúrcuma / curcumina complemento",
    "marca": "Varios…",
    "presentacion": "Cápsulas / polvo",
    "usos": "Complemento alimenticio; no sustituye antiinflamatorios prescritos ni diagnóstico.",
    "como": "Según envase.",
    "avisos": "Cálculos biliares, anticoagulantes o cirugía: consulta. Dosis altas: molestia hepática rara — para si hay síntomas. Embarazo: pregunta.",
    "efectos": [
      "Reflujo",
      "Diarrea",
      "Sabor"
    ],
    "categoria": "vitamina"
  }
];
  root.LV_MEDS_DB = LV_MEDS_DB;
  root.LV_MEDS_DISCLAIMER = LV_MEDS_DISCLAIMER;
})(typeof window !== 'undefined' ? window : this);
