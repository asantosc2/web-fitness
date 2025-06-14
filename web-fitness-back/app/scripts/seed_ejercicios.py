from sqlmodel import Session, SQLModel, create_engine
from app.models import Ejercicio

# Configurar la conexión a la base de datos
engine = create_engine("postgresql://postgres:postgres@localhost:5432/web_fitness")

# Crear las tablas en la base de datos
SQLModel.metadata.create_all(engine)

print("Base de datos inicializada correctamente.")

ejercicios_brazos = [
    {
        "nombre": "Fondos en banco",
        "grupo_muscular": "Brazos",
        "tipo_equipo": "Peso corporal",
        "descripcion": (
            "1. Siéntate en el borde de un banco con las manos a los lados y los dedos mirando al frente.\n"
            "2. Estira las piernas y apoya los talones en el suelo, deslizando el cuerpo hacia adelante.\n"
            "3. Baja lentamente doblando los codos hasta que estén en un ángulo de 90°.\n"
            "4. Empuja hacia arriba extendiendo los codos sin bloquearlos.\n"
            "5. Mantén la espalda recta y evita impulsarte con las piernas."
        ),
        "fotos": []
    },
    {
        "nombre": "Press de banca agarre cerrado",
        "grupo_muscular": "Brazos",
        "tipo_equipo": "Barra",
        "descripcion": (
            "1. Túmbate sobre un banco plano y sujeta una barra con un agarre ligeramente más estrecho que los hombros.\n"
            "2. Baja la barra lentamente hacia la parte baja del pecho manteniendo los codos pegados al cuerpo.\n"
            "3. Empuja la barra hacia arriba extendiendo los codos para activar los tríceps.\n"
            "4. Controla el descenso y evita abrir los codos en exceso.\n"
            "5. Mantén los pies firmes en el suelo y la espalda neutra."
        ),
        "fotos": []
    },
    {
        "nombre": "Curl de bíceps con barra",
        "grupo_muscular": "Brazos",
        "tipo_equipo": "Barra",
        "descripcion": (
            "1. Ponte de pie sujetando una barra con las palmas mirando al frente.\n"
            "2. Mantén los codos pegados al torso y el abdomen activado.\n"
            "3. Flexiona los codos levantando la barra hasta contraer los bíceps.\n"
            "4. Baja la barra lentamente sin bloquear los codos al final.\n"
            "5. Evita balancear el cuerpo o usar impulso."
        ),
        "fotos": []
    },
    {
        "nombre": "Curl de bíceps en polea baja",
        "grupo_muscular": "Brazos",
        "tipo_equipo": "Polea",
        "descripcion": (
            "1. Coloca una barra recta o EZ en una polea baja y sujétala con las palmas hacia arriba.\n"
            "2. De pie, con el pecho elevado y codos fijos, flexiona los brazos hasta que la barra llegue al pecho.\n"
            "3. Contrae los bíceps en la parte superior del movimiento.\n"
            "4. Baja de forma controlada manteniendo tensión constante.\n"
            "5. No arquees la espalda ni uses inercia."
        ),
        "fotos": []
    },
    {
        "nombre": "Curl de bíceps con mancuernas",
        "grupo_muscular": "Brazos",
        "tipo_equipo": "Mancuernas",
        "descripcion": (
            "1. Sujeta una mancuerna en cada mano con las palmas mirando hacia adelante.\n"
            "2. De pie o sentado, mantén los codos pegados al cuerpo y flexiona ambos brazos.\n"
            "3. Eleva las mancuernas hasta contraer los bíceps.\n"
            "4. Baja lentamente manteniendo el control.\n"
            "5. Puedes alternar los brazos o hacerlo simultáneamente."
        ),
        "fotos": []
    },
    {
        "nombre": "Extensión de tríceps en polea alta",
        "grupo_muscular": "Brazos",
        "tipo_equipo": "Polea",
        "descripcion": (
            "1. Coloca una cuerda o barra corta en la polea alta.\n"
            "2. Sujeta el accesorio con las palmas hacia abajo y los codos pegados al torso.\n"
            "3. Extiende los brazos hacia abajo hasta estirarlos completamente.\n"
            "4. Vuelve a la posición inicial con control sin mover los codos.\n"
            "5. Mantén los hombros estables y no arquees la espalda."
        ),
        "fotos": []
    },
    {
        "nombre": "Extensión de tríceps con mancuernas",
        "grupo_muscular": "Brazos",
        "tipo_equipo": "Mancuernas",
        "descripcion": (
            "1. Sujeta una mancuerna con ambas manos por encima de la cabeza.\n"
            "2. Flexiona los codos lentamente dejando caer la mancuerna detrás de la cabeza.\n"
            "3. Extiende los codos para subir la mancuerna sin mover los hombros.\n"
            "4. Mantén los codos apuntando hacia el frente durante todo el ejercicio.\n"
            "5. Ideal para trabajar la cabeza larga del tríceps."
        ),
        "fotos": []
    },
    {
        "nombre": "Curl tipo martillo con mancuernas",
        "grupo_muscular": "Brazos",
        "tipo_equipo": "Mancuernas",
        "descripcion": (
            "1. Sujeta una mancuerna en cada mano con las palmas enfrentadas (posición neutra).\n"
            "2. Flexiona los codos manteniendo esa posición hasta que las mancuernas lleguen al pecho.\n"
            "3. Contrae los bíceps y braquiales en la parte superior.\n"
            "4. Baja lentamente manteniendo la posición neutra.\n"
            "5. Evita mover los codos o balancear el cuerpo."
        ),
        "fotos": []
    },
    {
        "nombre": "Curl concentrado con mancuerna",
        "grupo_muscular": "Brazos",
        "tipo_equipo": "Mancuernas",
        "descripcion": (
            "1. Siéntate en un banco y apoya el codo sobre el muslo del mismo lado.\n"
            "2. Sujeta la mancuerna con la palma hacia arriba.\n"
            "3. Flexiona el brazo contrayendo el bíceps en la parte alta del movimiento.\n"
            "4. Baja lentamente hasta la extensión completa del brazo.\n"
            "5. Aísla el movimiento evitando involucrar los hombros."
        ),
        "fotos": []
    },
    {
        "nombre": "Rompecráneos con barra",
        "grupo_muscular": "Brazos",
        "tipo_equipo": "Barra",
        "descripcion": (
            "1. Túmbate en un banco plano sujetando una barra EZ con agarre cerrado.\n"
            "2. Baja la barra lentamente hacia la frente flexionando los codos.\n"
            "3. Mantén los codos fijos y cerca del rostro.\n"
            "4. Extiende los codos para volver a la posición inicial.\n"
            "5. Evita abrir los codos y no uses peso excesivo para no forzar los codos."
        ),
        "fotos": []
    }
]
ejercicios_espalda = [
    {
        "nombre": "Dominadas",
        "grupo_muscular": "Espalda",
        "tipo_equipo": "Peso corporal",
        "descripcion": (
            "1. Cuelga de una barra con las palmas mirando hacia adelante y los brazos completamente extendidos.\n"
            "2. Tira de tu cuerpo hacia arriba contrayendo los dorsales hasta que la barbilla supere la barra.\n"
            "3. Baja de forma controlada hasta la posición inicial.\n"
            "4. Mantén el torso firme, evitando balanceos para mayor activación muscular."
        ),
        "fotos": []
    },
    {
        "nombre": "Peso muerto (Barra)",
        "grupo_muscular": "Espalda",
        "tipo_equipo": "Barra",
        "descripcion": (
            "1. Coloca los pies al ancho de los hombros frente a una barra.\n"
            "2. Flexiona las caderas y rodillas manteniendo la espalda recta y agarra la barra.\n"
            "3. Eleva la barra estirando caderas y rodillas al mismo tiempo hasta quedar erguido.\n"
            "4. Baja controladamente manteniendo la espalda neutra.\n"
            "5. Evita curvar la espalda durante todo el recorrido."
        ),
        "fotos": []
    },
    {
        "nombre": "Remo inclinado con barra",
        "grupo_muscular": "Espalda",
        "tipo_equipo": "Barra",
        "descripcion": (
            "1. De pie, flexiona ligeramente las rodillas y el torso hacia delante.\n"
            "2. Sujeta una barra con agarre prono y brazos extendidos.\n"
            "3. Lleva la barra hacia el abdomen contrayendo los dorsales.\n"
            "4. Mantén los codos cerca del cuerpo y baja controladamente.\n"
            "5. Mantén la espalda recta durante todo el movimiento."
        ),
        "fotos": []
    },
    {
        "nombre": "Jalón en polea alta",
        "grupo_muscular": "Espalda",
        "tipo_equipo": "Polea",
        "descripcion": (
            "1. Sentado frente a una polea alta, sujeta la barra con agarre ancho.\n"
            "2. Tira de la barra hacia el pecho contrayendo los dorsales.\n"
            "3. Baja controladamente sin balancearte ni usar impulso.\n"
            "4. Mantén el pecho elevado y los codos apuntando hacia abajo."
        ),
        "fotos": []
    },
    {
        "nombre": "Remo con barra en T",
        "grupo_muscular": "Espalda",
        "tipo_equipo": "Máquina",
        "descripcion": (
            "1. Usa una barra T-bar o una barra con soporte en un extremo.\n"
            "2. Inclina el torso hacia adelante y sujeta el agarre con ambas manos.\n"
            "3. Tira del peso hacia el abdomen contrayendo la espalda.\n"
            "4. Baja de forma controlada y evita balanceos.\n"
            "5. Excelente para dar grosor a la espalda."
        ),
        "fotos": []
    },
    {
        "nombre": "Remo sentado en polea baja",
        "grupo_muscular": "Espalda",
        "tipo_equipo": "Polea",
        "descripcion": (
            "1. Siéntate en la máquina con los pies apoyados y la espalda recta.\n"
            "2. Sujeta la barra o el triángulo con ambos brazos extendidos.\n"
            "3. Tira hacia tu abdomen manteniendo los codos cerca del cuerpo.\n"
            "4. Contrae los dorsales y vuelve lentamente.\n"
            "5. No encorves la espalda al tirar."
        ),
        "fotos": []
    },
    {
        "nombre": "Face pull",
        "grupo_muscular": "Espalda",
        "tipo_equipo": "Polea",
        "descripcion": (
            "1. Coloca una cuerda en la polea alta y sujétala con ambas manos.\n"
            "2. Tira hacia tu cara separando las manos al final del recorrido.\n"
            "3. Enfócate en contraer deltoides posteriores y trapecios.\n"
            "4. Mantén los codos elevados durante todo el ejercicio."
        ),
        "fotos": []
    },
    {
        "nombre": "Buenos días (Good morning)",
        "grupo_muscular": "Espalda",
        "tipo_equipo": "Barra",
        "descripcion": (
            "1. Coloca una barra sobre la parte alta de la espalda como en una sentadilla.\n"
            "2. Flexiona las caderas hacia atrás bajando el torso con la espalda recta.\n"
            "3. Detente cuando el torso esté casi paralelo al suelo.\n"
            "4. Vuelve a subir activando glúteos y erectores espinales.\n"
            "5. Ideal para mejorar fuerza lumbar y estabilidad posterior."
        ),
        "fotos": []
    },
    {
        "nombre": "Encogimiento con mancuernas",
        "grupo_muscular": "Espalda",
        "tipo_equipo": "Mancuernas",
        "descripcion": (
            "1. Sujeta una mancuerna en cada mano con los brazos extendidos.\n"
            "2. Eleva los hombros hacia las orejas lo más alto posible.\n"
            "3. Mantén la contracción por un segundo y baja lentamente.\n"
            "4. Mantén la espalda recta y no uses impulso.\n"
            "5. Aísla perfectamente los trapecios superiores."
        ),
        "fotos": []
    },
    {
        "nombre": "Remo invertido (Inverted row)",
        "grupo_muscular": "Espalda",
        "tipo_equipo": "Peso corporal",
        "descripcion": (
            "1. Coloca una barra baja o usa una máquina Smith.\n"
            "2. Acuéstate debajo y sujeta la barra con agarre prono.\n"
            "3. Eleva tu torso hacia la barra manteniendo el cuerpo alineado.\n"
            "4. Contrae la espalda y baja lentamente.\n"
            "5. Excelente ejercicio con peso corporal para todos los niveles."
        ),
        "fotos": []
    }
]
ejercicios_pecho = [
    {
        "nombre": "Press de banca con barra",
        "grupo_muscular": "Pecho",
        "tipo_equipo": "Barra",
        "descripcion": (
            "1. Acuéstate sobre un banco plano con los pies apoyados en el suelo.\n"
            "2. Sujeta la barra con las manos ligeramente más abiertas que los hombros.\n"
            "3. Desbloquea la barra y bájala de forma controlada hasta que toque ligeramente el pecho.\n"
            "4. Empuja hacia arriba hasta estirar completamente los brazos sin bloquear los codos.\n"
            "5. Repite el movimiento manteniendo la espalda y glúteos en contacto con el banco."
        ),
    },
    {
        "nombre": "Press inclinado con mancuernas",
        "grupo_muscular": "Pecho",
        "tipo_equipo": "Mancuernas",
        "descripcion": (
            "1. Siéntate en un banco inclinado a 30-45° y recuéstate con una mancuerna en cada mano.\n"
            "2. Coloca las mancuernas al nivel del pecho con las palmas mirando hacia adelante.\n"
            "3. Empuja las mancuernas hacia arriba hasta estirar completamente los brazos.\n"
            "4. Junta ligeramente las mancuernas arriba sin que se golpeen.\n"
            "5. Baja lentamente a la posición inicial con control."
        ),
    },
    {
        "nombre": "Aperturas con mancuernas",
        "grupo_muscular": "Pecho",
        "tipo_equipo": "Mancuernas",
        "descripcion": (
            "1. Acuéstate en un banco plano con una mancuerna en cada mano.\n"
            "2. Eleva los brazos con las mancuernas por encima del pecho, ligeramente flexionados.\n"
            "3. Abre los brazos en un arco amplio hacia los lados, bajando hasta que estén al nivel del pecho.\n"
            "4. Contrae el pecho y vuelve a cerrar los brazos siguiendo el mismo arco.\n"
            "5. No bloquees los codos ni dejes que las mancuernas se toquen."
        ),
    },
    {
        "nombre": "Press inclinado en máquina Smith",
        "grupo_muscular": "Pecho",
        "tipo_equipo": "Máquina",
        "descripcion": (
            "1. Ajusta el banco a un ángulo inclinado de 30–45° dentro de la máquina Smith.\n"
            "2. Siéntate y sujeta la barra con las manos ligeramente abiertas.\n"
            "3. Desbloquea la barra y bájala de forma controlada hasta la parte superior del pecho.\n"
            "4. Empuja hacia arriba hasta estirar los brazos por completo.\n"
            "5. Controla la bajada para mantener tensión en el pecho."
        ),
    },
    {
        "nombre": "Crossover en polea",
        "grupo_muscular": "Pecho",
        "tipo_equipo": "Polea",
        "descripcion": (
            "1. Colócate en el centro de una máquina de poleas altas con una asa en cada mano.\n"
            "2. Da un paso adelante y mantén el torso inclinado ligeramente hacia adelante.\n"
            "3. Junta los brazos en un arco por delante del pecho con una ligera flexión en los codos.\n"
            "4. Aprieta el pecho al final del recorrido.\n"
            "5. Vuelve lentamente a la posición inicial sin perder tensión."
        ),
    },
    {
        "nombre": "Press en máquina",
        "grupo_muscular": "Pecho",
        "tipo_equipo": "Máquina",
        "descripcion": (
            "1. Ajusta el asiento de la máquina para que los mangos estén a la altura del pecho.\n"
            "2. Sujeta las asas con las palmas hacia adelante y pies apoyados en el suelo.\n"
            "3. Empuja las asas hacia adelante hasta extender los brazos.\n"
            "4. Mantén una ligera flexión en los codos al final.\n"
            "5. Regresa lentamente a la posición inicial controlando el movimiento."
        ),
    },
    {
        "nombre": "Fondos para pecho",
        "grupo_muscular": "Pecho",
        "tipo_equipo": "Peso corporal",
        "descripcion": (
            "1. Sujétate en unas barras paralelas con los brazos extendidos.\n"
            "2. Inclina ligeramente el torso hacia adelante.\n"
            "3. Baja el cuerpo flexionando los codos hasta sentir estiramiento en el pecho.\n"
            "4. Empuja hacia arriba hasta volver a extender los brazos.\n"
            "5. Mantén el core activado y evita movimientos bruscos."
        ),
    },
    {
        "nombre": "Press declinado con barra",
        "grupo_muscular": "Pecho",
        "tipo_equipo": "Barra",
        "descripcion": (
            "1. Acuéstate en un banco declinado con los pies bien apoyados.\n"
            "2. Sujeta la barra con un agarre ancho y retírala del soporte.\n"
            "3. Baja la barra hacia la parte baja del pecho de forma controlada.\n"
            "4. Empuja la barra hacia arriba sin bloquear completamente los codos.\n"
            "5. Controla todo el movimiento para evitar lesiones en hombros."
        ),
    },
    {
        "nombre": "Pullover con mancuerna",
        "grupo_muscular": "Pecho",
        "tipo_equipo": "Mancuernas",
        "descripcion": (
            "1. Acuéstate en un banco plano con una mancuerna entre las manos.\n"
            "2. Sujeta la mancuerna sobre el pecho con los brazos estirados.\n"
            "3. Baja la mancuerna hacia atrás en un arco por encima de la cabeza.\n"
            "4. Detén el movimiento cuando sientas el estiramiento máximo.\n"
            "5. Vuelve a la posición inicial activando el pecho y sin doblar los codos."
        ),
    },
    {
        "nombre": "Press con banda elástica",
        "grupo_muscular": "Pecho",
        "tipo_equipo": "Banda elástica",
        "descripcion": (
            "1. Ancla la banda a una superficie estable detrás de ti a la altura del pecho.\n"
            "2. Sujeta los extremos con las manos y da un paso al frente.\n"
            "3. Empuja los brazos hacia adelante simulando un press de banca.\n"
            "4. Junta las manos al frente contrayendo el pecho.\n"
            "5. Regresa lentamente a la posición inicial sin perder tensión."
        ),
    },
]
ejercicios_hombros = [
    {
        "nombre": "Elevaciones laterales con mancuernas",
        "grupo_muscular": "Hombros",
        "tipo_equipo": "Mancuernas",
        "descripcion": (
            "1. Ponte de pie con una mancuerna en cada mano a los lados.\n"
            "2. Mantén una ligera flexión en los codos y eleva los brazos lateralmente hasta que estén a la altura de los hombros.\n"
            "3. Pausa un segundo en la parte superior.\n"
            "4. Baja los brazos lentamente a la posición inicial.\n"
            "5. Mantén el torso erguido y evita balancearte."
        )
    },
    {
        "nombre": "Press militar con barra",
        "grupo_muscular": "Hombros",
        "tipo_equipo": "Barra",
        "descripcion": (
            "1. Siéntate en un banco con respaldo y coloca la barra sobre los hombros, frente a ti.\n"
            "2. Sujeta la barra con un agarre un poco más ancho que los hombros.\n"
            "3. Empuja la barra hacia arriba sobre la cabeza hasta que los brazos estén completamente extendidos.\n"
            "4. Baja la barra controladamente hasta la altura de los hombros.\n"
            "5. Mantén la espalda recta y los pies firmes en el suelo."
        )
    },
    {
        "nombre": "Face Pull con polea",
        "grupo_muscular": "Hombros",
        "tipo_equipo": "Polea",
        "descripcion": (
            "1. Ajusta la polea a la altura del rostro con una cuerda como accesorio.\n"
            "2. Agarra ambos extremos de la cuerda con las palmas enfrentadas.\n"
            "3. Tira de la cuerda hacia el rostro, separando los extremos al final del movimiento.\n"
            "4. Contrae los omóplatos al final del recorrido.\n"
            "5. Regresa lentamente a la posición inicial."
        )
    },
    {
        "nombre": "Press Arnold",
        "grupo_muscular": "Hombros",
        "tipo_equipo": "Mancuernas",
        "descripcion": (
            "1. Siéntate en un banco con respaldo y sujeta una mancuerna en cada mano a la altura del pecho, con las palmas hacia ti.\n"
            "2. Al levantar las mancuernas, rota las muñecas para que las palmas queden hacia adelante.\n"
            "3. Estira completamente los brazos por encima de la cabeza.\n"
            "4. Baja las mancuernas rotando nuevamente hasta volver a la posición inicial.\n"
            "5. Controla el movimiento en todo momento."
        )
    },
    {
        "nombre": "Encogimiento de hombros con barra",
        "grupo_muscular": "Hombros",
        "tipo_equipo": "Barra",
        "descripcion": (
            "1. Sujeta una barra con ambas manos al frente, brazos extendidos.\n"
            "2. Eleva los hombros hacia las orejas tanto como puedas.\n"
            "3. Pausa brevemente en la parte superior del movimiento.\n"
            "4. Baja los hombros lentamente.\n"
            "5. Evita girar o rotar los hombros durante el movimiento."
        )
    },
    {
        "nombre": "Elevaciones frontales con mancuernas",
        "grupo_muscular": "Hombros",
        "tipo_equipo": "Mancuernas",
        "descripcion": (
            "1. Sostén una mancuerna en cada mano al frente de tus muslos.\n"
            "2. Levanta una mancuerna al frente hasta la altura de los hombros, manteniendo el brazo recto.\n"
            "3. Baja lentamente mientras elevas la otra mancuerna.\n"
            "4. Alterna brazos en cada repetición.\n"
            "5. Mantén el torso firme y sin impulso."
        )
    },
    {
        "nombre": "Press de hombros en máquina",
        "grupo_muscular": "Hombros",
        "tipo_equipo": "Máquina",
        "descripcion": (
            "1. Ajusta el asiento para que las manijas estén a la altura de los hombros.\n"
            "2. Sujeta las manijas con un agarre firme y empuja hacia arriba hasta extender los brazos.\n"
            "3. Baja lentamente controlando el movimiento.\n"
            "4. Mantén la espalda apoyada y los pies firmes en el suelo.\n"
            "5. Evita bloquear los codos completamente."
        )
    },
    {
        "nombre": "Elevaciones laterales en máquina",
        "grupo_muscular": "Hombros",
        "tipo_equipo": "Máquina",
        "descripcion": (
            "1. Siéntate en la máquina con los brazos apoyados en las almohadillas.\n"
            "2. Empuja los brazos hacia los lados, separándolos del cuerpo.\n"
            "3. Pausa un momento al final del recorrido.\n"
            "4. Vuelve lentamente a la posición inicial.\n"
            "5. Asegúrate de no usar impulso y mantener la espalda recta."
        )
    },
    {
        "nombre": "Elevaciones posteriores en peck-deck",
        "grupo_muscular": "Hombros",
        "tipo_equipo": "Máquina",
        "descripcion": (
            "1. Siéntate en la máquina de peck-deck mirando hacia el respaldo.\n"
            "2. Sujeta las manijas y lleva los brazos hacia atrás en un movimiento de apertura.\n"
            "3. Pausa brevemente cuando los brazos estén extendidos.\n"
            "4. Regresa de forma controlada a la posición inicial.\n"
            "5. Mantén los codos ligeramente flexionados y evita empujar con el cuerpo."
        )
    },
    {
        "nombre": "Overhead Press con mancuernas",
        "grupo_muscular": "Hombros",
        "tipo_equipo": "Mancuernas",
        "descripcion": (
            "1. Sostén una mancuerna en cada mano a la altura de los hombros con las palmas hacia adelante.\n"
            "2. Empuja las mancuernas hacia arriba hasta que los brazos estén completamente extendidos.\n"
            "3. Baja lentamente hasta la posición inicial.\n"
            "4. Mantén el torso erguido y los abdominales activados.\n"
            "5. Evita arquear la espalda durante la ejecución."
        )
    },
]
ejercicios_pierna = [
    {
        "nombre": "Sentadilla con barra",
        "grupo_muscular": "Piernas",
        "tipo_equipo": "Barra",
        "descripcion": (
            "1. Coloca la barra sobre la parte alta de la espalda.\n"
            "2. Coloca los pies al ancho de los hombros, con ligera rotación externa.\n"
            "3. Baja flexionando rodillas y caderas manteniendo la espalda recta.\n"
            "4. Llega hasta que los muslos estén paralelos al suelo o más.\n"
            "5. Sube empujando con fuerza a través de los talones hasta extender caderas y rodillas."
        ),
        "fotos": []
    },
    {
        "nombre": "Prensa de piernas",
        "grupo_muscular": "Piernas",
        "tipo_equipo": "Máquina",
        "descripcion": (
            "1. Siéntate en la máquina y coloca los pies al ancho de los hombros en la plataforma.\n"
            "2. Sujeta las asas laterales para estabilizar el cuerpo.\n"
            "3. Flexiona las rodillas para bajar el peso controladamente.\n"
            "4. Empuja con fuerza hasta estirar las piernas sin bloquear completamente las rodillas.\n"
            "5. Mantén la espalda y glúteos en contacto con el respaldo."
        ),
        "fotos": []
    },
    {
        "nombre": "Peso muerto rumano",
        "grupo_muscular": "Piernas",
        "tipo_equipo": "Barra",
        "descripcion": (
            "1. De pie, sujeta la barra con un agarre prono frente a los muslos.\n"
            "2. Flexiona las caderas hacia atrás bajando la barra por delante de las piernas.\n"
            "3. Mantén la espalda recta y las rodillas ligeramente flexionadas.\n"
            "4. Baja hasta sentir el estiramiento en los isquiosurales.\n"
            "5. Vuelve a la posición inicial contrayendo los glúteos."
        ),
        "fotos": []
    },
    {
        "nombre": "Zancadas con mancuernas",
        "grupo_muscular": "Piernas",
        "tipo_equipo": "Mancuernas",
        "descripcion": (
            "1. Sujeta una mancuerna en cada mano con los brazos a los lados.\n"
            "2. Da un paso largo hacia adelante y flexiona ambas rodillas.\n"
            "3. La rodilla trasera debe acercarse al suelo sin tocarlo.\n"
            "4. Empuja con la pierna delantera para volver a la posición inicial.\n"
            "5. Alterna piernas en cada repetición o completa todas con una antes de cambiar."
        ),
        "fotos": []
    },
    {
        "nombre": "Hip thrust (elevación de cadera)",
        "grupo_muscular": "Piernas",
        "tipo_equipo": "Barra",
        "descripcion": (
            "1. Apoya la parte alta de la espalda en un banco y coloca la barra sobre las caderas.\n"
            "2. Flexiona las rodillas y apoya los pies en el suelo.\n"
            "3. Empuja las caderas hacia arriba contrayendo los glúteos al máximo.\n"
            "4. Haz una breve pausa arriba y baja lentamente.\n"
            "5. Mantén el mentón hacia el pecho y el abdomen activado."
        ),
        "fotos": []
    },
    {
        "nombre": "Extensión de piernas en máquina",
        "grupo_muscular": "Piernas",
        "tipo_equipo": "Máquina",
        "descripcion": (
            "1. Siéntate en la máquina con la espalda recta y ajusta el rodillo sobre las espinillas.\n"
            "2. Extiende las piernas hasta estirarlas completamente.\n"
            "3. Contrae los cuádriceps arriba y baja lentamente.\n"
            "4. No bloquees las rodillas en la parte final del movimiento.\n"
            "5. Controla la fase excéntrica para máxima efectividad."
        ),
        "fotos": []
    },
    {
        "nombre": "Curl femoral tumbado",
        "grupo_muscular": "Piernas",
        "tipo_equipo": "Máquina",
        "descripcion": (
            "1. Túmbate boca abajo en la máquina y ajusta el rodillo detrás de los tobillos.\n"
            "2. Flexiona las rodillas llevando los talones hacia los glúteos.\n"
            "3. Mantén la contracción un segundo y baja con control.\n"
            "4. No arquees la espalda ni levantes el abdomen del banco.\n"
            "5. Ideal para trabajar isquiosurales de forma aislada."
        ),
        "fotos": []
    },
    {
        "nombre": "Sentadilla goblet",
        "grupo_muscular": "Piernas",
        "tipo_equipo": "Mancuernas",
        "descripcion": (
            "1. Sujeta una mancuerna verticalmente frente al pecho con ambas manos.\n"
            "2. Coloca los pies al ancho de los hombros.\n"
            "3. Baja en sentadilla manteniendo el torso erguido.\n"
            "4. Llega hasta que los muslos estén paralelos o más.\n"
            "5. Empuja con los talones para volver a la posición inicial."
        ),
        "fotos": []
    },
    {
        "nombre": "Sentadilla búlgara",
        "grupo_muscular": "Piernas",
        "tipo_equipo": "Mancuernas",
        "descripcion": (
            "1. Coloca el pie trasero sobre un banco o superficie elevada.\n"
            "2. Da un paso adelante con la otra pierna.\n"
            "3. Baja el cuerpo flexionando la pierna delantera.\n"
            "4. Mantén el torso recto y no dejes que la rodilla pase los dedos del pie.\n"
            "5. Sube empujando con el talón de la pierna delantera."
        ),
        "fotos": []
    },
    {
        "nombre": "Elevación de talones de pie (gemelos)",
        "grupo_muscular": "Piernas",
        "tipo_equipo": "Máquina",
        "descripcion": (
            "1. Colócate en la máquina con los hombros bajo los pads y los pies sobre la plataforma.\n"
            "2. Baja los talones lentamente por debajo del nivel del escalón.\n"
            "3. Eleva los talones lo más alto posible contrayendo los gemelos.\n"
            "4. Mantén una pausa arriba y baja controladamente.\n"
            "5. No rebotes ni uses impulso al subir."
        ),
        "fotos": []
    }
]

ejercicios = [
    *ejercicios_brazos,
    *ejercicios_espalda,
    *ejercicios_pecho,
    *ejercicios_hombros,
    *ejercicios_pierna
]

# Insertar ejercicios en la base de datos
with Session(engine) as session:
    for ejercicio_data in ejercicios:
        ejercicio = Ejercicio(**ejercicio_data)
        session.add(ejercicio)
    session.commit()

print("Ejercicios insertados correctamente.")







