/* Les vencimos — base de medicinas con prospecto RESUMIDO (offline)
 * Información general orientativa. NO sustituye prospecto oficial ni indicación médica.
 * Urgencias: 112. Sin recomendaciones personalizadas de dosis/tratamiento.
 * v20261002b
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
  }
];
  root.LV_MEDS_DB = LV_MEDS_DB;
  root.LV_MEDS_DISCLAIMER = LV_MEDS_DISCLAIMER;
})(typeof window !== 'undefined' ? window : this);
