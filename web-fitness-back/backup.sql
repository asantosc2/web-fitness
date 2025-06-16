--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.13 (Debian 15.13-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS '';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alimento; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alimento (
    id integer NOT NULL,
    nombre character varying NOT NULL,
    calorias_100g double precision NOT NULL,
    proteinas_100g double precision NOT NULL,
    carbohidratos_100g double precision NOT NULL,
    grasas_100g double precision NOT NULL,
    imagen_url character varying,
    usuario_id integer
);


ALTER TABLE public.alimento OWNER TO postgres;

--
-- Name: alimento_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.alimento_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.alimento_id_seq OWNER TO postgres;

--
-- Name: alimento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.alimento_id_seq OWNED BY public.alimento.id;


--
-- Name: comida; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comida (
    id integer NOT NULL,
    dieta_id integer NOT NULL,
    nombre character varying NOT NULL
);


ALTER TABLE public.comida OWNER TO postgres;

--
-- Name: comida_alimento; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comida_alimento (
    id integer NOT NULL,
    comida_id integer NOT NULL,
    alimento_id integer NOT NULL,
    porcion character varying NOT NULL,
    calorias double precision NOT NULL,
    proteinas double precision NOT NULL,
    carbohidratos double precision NOT NULL,
    grasas double precision NOT NULL
);


ALTER TABLE public.comida_alimento OWNER TO postgres;

--
-- Name: comida_alimento_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.comida_alimento_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comida_alimento_id_seq OWNER TO postgres;

--
-- Name: comida_alimento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.comida_alimento_id_seq OWNED BY public.comida_alimento.id;


--
-- Name: comida_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.comida_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comida_id_seq OWNER TO postgres;

--
-- Name: comida_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.comida_id_seq OWNED BY public.comida.id;


--
-- Name: dieta; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dieta (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    nombre character varying NOT NULL,
    descripcion character varying
);


ALTER TABLE public.dieta OWNER TO postgres;

--
-- Name: dieta_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dieta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dieta_id_seq OWNER TO postgres;

--
-- Name: dieta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dieta_id_seq OWNED BY public.dieta.id;


--
-- Name: ejercicio; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ejercicio (
    id integer NOT NULL,
    nombre character varying NOT NULL,
    grupo_muscular character varying NOT NULL,
    tipo_equipo character varying NOT NULL,
    descripcion character varying,
    usuario_id integer
);


ALTER TABLE public.ejercicio OWNER TO postgres;

--
-- Name: ejercicio_foto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ejercicio_foto (
    id integer NOT NULL,
    url character varying NOT NULL,
    ejercicio_id integer NOT NULL
);


ALTER TABLE public.ejercicio_foto OWNER TO postgres;

--
-- Name: ejercicio_foto_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ejercicio_foto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ejercicio_foto_id_seq OWNER TO postgres;

--
-- Name: ejercicio_foto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ejercicio_foto_id_seq OWNED BY public.ejercicio_foto.id;


--
-- Name: ejercicio_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ejercicio_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ejercicio_id_seq OWNER TO postgres;

--
-- Name: ejercicio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ejercicio_id_seq OWNED BY public.ejercicio.id;


--
-- Name: progreso; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.progreso (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    fecha date NOT NULL,
    peso double precision NOT NULL,
    comentarios character varying
);


ALTER TABLE public.progreso OWNER TO postgres;

--
-- Name: progreso_foto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.progreso_foto (
    id integer NOT NULL,
    progreso_id integer NOT NULL,
    ruta character varying NOT NULL
);


ALTER TABLE public.progreso_foto OWNER TO postgres;

--
-- Name: progreso_foto_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.progreso_foto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.progreso_foto_id_seq OWNER TO postgres;

--
-- Name: progreso_foto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.progreso_foto_id_seq OWNED BY public.progreso_foto.id;


--
-- Name: progreso_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.progreso_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.progreso_id_seq OWNER TO postgres;

--
-- Name: progreso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.progreso_id_seq OWNED BY public.progreso.id;


--
-- Name: rutina; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rutina (
    id integer NOT NULL,
    nombre character varying NOT NULL,
    descripcion character varying,
    usuario_id integer,
    fecha_creacion timestamp without time zone NOT NULL,
    es_defecto boolean NOT NULL
);


ALTER TABLE public.rutina OWNER TO postgres;

--
-- Name: rutina_ejercicio; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rutina_ejercicio (
    id integer NOT NULL,
    rutina_id integer NOT NULL,
    ejercicio_id integer NOT NULL,
    orden integer NOT NULL,
    comentarios character varying
);


ALTER TABLE public.rutina_ejercicio OWNER TO postgres;

--
-- Name: rutina_ejercicio_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rutina_ejercicio_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rutina_ejercicio_id_seq OWNER TO postgres;

--
-- Name: rutina_ejercicio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rutina_ejercicio_id_seq OWNED BY public.rutina_ejercicio.id;


--
-- Name: rutina_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rutina_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rutina_id_seq OWNER TO postgres;

--
-- Name: rutina_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rutina_id_seq OWNED BY public.rutina.id;


--
-- Name: rutina_serie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rutina_serie (
    id integer NOT NULL,
    rutina_ejercicio_id integer NOT NULL,
    numero integer NOT NULL,
    repeticiones integer NOT NULL,
    peso double precision NOT NULL
);


ALTER TABLE public.rutina_serie OWNER TO postgres;

--
-- Name: rutina_serie_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rutina_serie_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rutina_serie_id_seq OWNER TO postgres;

--
-- Name: rutina_serie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rutina_serie_id_seq OWNED BY public.rutina_serie.id;


--
-- Name: sesion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sesion (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    fecha date NOT NULL,
    rutina_id integer
);


ALTER TABLE public.sesion OWNER TO postgres;

--
-- Name: sesion_ejercicio; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sesion_ejercicio (
    id integer NOT NULL,
    sesion_id integer NOT NULL,
    ejercicio_id integer NOT NULL,
    orden integer NOT NULL,
    series integer NOT NULL,
    repeticiones integer NOT NULL,
    peso double precision NOT NULL,
    comentarios character varying
);


ALTER TABLE public.sesion_ejercicio OWNER TO postgres;

--
-- Name: sesion_ejercicio_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sesion_ejercicio_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sesion_ejercicio_id_seq OWNER TO postgres;

--
-- Name: sesion_ejercicio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sesion_ejercicio_id_seq OWNED BY public.sesion_ejercicio.id;


--
-- Name: sesion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sesion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sesion_id_seq OWNER TO postgres;

--
-- Name: sesion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sesion_id_seq OWNED BY public.sesion.id;


--
-- Name: sesion_serie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sesion_serie (
    id integer NOT NULL,
    sesion_ejercicio_id integer NOT NULL,
    numero integer NOT NULL,
    repeticiones integer NOT NULL,
    peso double precision NOT NULL
);


ALTER TABLE public.sesion_serie OWNER TO postgres;

--
-- Name: sesion_serie_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sesion_serie_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sesion_serie_id_seq OWNER TO postgres;

--
-- Name: sesion_serie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sesion_serie_id_seq OWNED BY public.sesion_serie.id;


--
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    id integer NOT NULL,
    nombre character varying NOT NULL,
    apellido character varying NOT NULL,
    email character varying NOT NULL,
    hashed_password character varying NOT NULL,
    fecha_nacimiento date NOT NULL,
    fecha_registro timestamp without time zone NOT NULL,
    is_admin boolean NOT NULL,
    token_recuperacion character varying,
    token_expira timestamp without time zone
);


ALTER TABLE public.usuario OWNER TO postgres;

--
-- Name: usuario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.usuario_id_seq OWNER TO postgres;

--
-- Name: usuario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuario_id_seq OWNED BY public.usuario.id;


--
-- Name: alimento id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alimento ALTER COLUMN id SET DEFAULT nextval('public.alimento_id_seq'::regclass);


--
-- Name: comida id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comida ALTER COLUMN id SET DEFAULT nextval('public.comida_id_seq'::regclass);


--
-- Name: comida_alimento id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comida_alimento ALTER COLUMN id SET DEFAULT nextval('public.comida_alimento_id_seq'::regclass);


--
-- Name: dieta id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dieta ALTER COLUMN id SET DEFAULT nextval('public.dieta_id_seq'::regclass);


--
-- Name: ejercicio id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ejercicio ALTER COLUMN id SET DEFAULT nextval('public.ejercicio_id_seq'::regclass);


--
-- Name: ejercicio_foto id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ejercicio_foto ALTER COLUMN id SET DEFAULT nextval('public.ejercicio_foto_id_seq'::regclass);


--
-- Name: progreso id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progreso ALTER COLUMN id SET DEFAULT nextval('public.progreso_id_seq'::regclass);


--
-- Name: progreso_foto id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progreso_foto ALTER COLUMN id SET DEFAULT nextval('public.progreso_foto_id_seq'::regclass);


--
-- Name: rutina id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rutina ALTER COLUMN id SET DEFAULT nextval('public.rutina_id_seq'::regclass);


--
-- Name: rutina_ejercicio id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rutina_ejercicio ALTER COLUMN id SET DEFAULT nextval('public.rutina_ejercicio_id_seq'::regclass);


--
-- Name: rutina_serie id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rutina_serie ALTER COLUMN id SET DEFAULT nextval('public.rutina_serie_id_seq'::regclass);


--
-- Name: sesion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion ALTER COLUMN id SET DEFAULT nextval('public.sesion_id_seq'::regclass);


--
-- Name: sesion_ejercicio id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion_ejercicio ALTER COLUMN id SET DEFAULT nextval('public.sesion_ejercicio_id_seq'::regclass);


--
-- Name: sesion_serie id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion_serie ALTER COLUMN id SET DEFAULT nextval('public.sesion_serie_id_seq'::regclass);


--
-- Name: usuario id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);


--
-- Data for Name: alimento; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alimento (id, nombre, calorias_100g, proteinas_100g, carbohidratos_100g, grasas_100g, imagen_url, usuario_id) FROM stdin;
\.


--
-- Data for Name: comida; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comida (id, dieta_id, nombre) FROM stdin;
\.


--
-- Data for Name: comida_alimento; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comida_alimento (id, comida_id, alimento_id, porcion, calorias, proteinas, carbohidratos, grasas) FROM stdin;
\.


--
-- Data for Name: dieta; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dieta (id, usuario_id, nombre, descripcion) FROM stdin;
\.


--
-- Data for Name: ejercicio; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ejercicio (id, nombre, grupo_muscular, tipo_equipo, descripcion, usuario_id) FROM stdin;
1	Fondos en banco	Brazos	Peso corporal	1. Siéntate en el borde de un banco con las manos a los lados y los dedos mirando al frente.\n2. Estira las piernas y apoya los talones en el suelo, deslizando el cuerpo hacia adelante.\n3. Baja lentamente doblando los codos hasta que estén en un ángulo de 90°.\n4. Empuja hacia arriba extendiendo los codos sin bloquearlos.\n5. Mantén la espalda recta y evita impulsarte con las piernas.	\N
2	Press de banca agarre cerrado	Brazos	Barra	1. Túmbate sobre un banco plano y sujeta una barra con un agarre ligeramente más estrecho que los hombros.\n2. Baja la barra lentamente hacia la parte baja del pecho manteniendo los codos pegados al cuerpo.\n3. Empuja la barra hacia arriba extendiendo los codos para activar los tríceps.\n4. Controla el descenso y evita abrir los codos en exceso.\n5. Mantén los pies firmes en el suelo y la espalda neutra.	\N
3	Curl de bíceps con barra	Brazos	Barra	1. Ponte de pie sujetando una barra con las palmas mirando al frente.\n2. Mantén los codos pegados al torso y el abdomen activado.\n3. Flexiona los codos levantando la barra hasta contraer los bíceps.\n4. Baja la barra lentamente sin bloquear los codos al final.\n5. Evita balancear el cuerpo o usar impulso.	\N
4	Curl de bíceps en polea baja	Brazos	Polea	1. Coloca una barra recta o EZ en una polea baja y sujétala con las palmas hacia arriba.\n2. De pie, con el pecho elevado y codos fijos, flexiona los brazos hasta que la barra llegue al pecho.\n3. Contrae los bíceps en la parte superior del movimiento.\n4. Baja de forma controlada manteniendo tensión constante.\n5. No arquees la espalda ni uses inercia.	\N
5	Curl de bíceps con mancuernas	Brazos	Mancuernas	1. Sujeta una mancuerna en cada mano con las palmas mirando hacia adelante.\n2. De pie o sentado, mantén los codos pegados al cuerpo y flexiona ambos brazos.\n3. Eleva las mancuernas hasta contraer los bíceps.\n4. Baja lentamente manteniendo el control.\n5. Puedes alternar los brazos o hacerlo simultáneamente.	\N
6	Extensión de tríceps en polea alta	Brazos	Polea	1. Coloca una cuerda o barra corta en la polea alta.\n2. Sujeta el accesorio con las palmas hacia abajo y los codos pegados al torso.\n3. Extiende los brazos hacia abajo hasta estirarlos completamente.\n4. Vuelve a la posición inicial con control sin mover los codos.\n5. Mantén los hombros estables y no arquees la espalda.	\N
7	Extensión de tríceps con mancuernas	Brazos	Mancuernas	1. Sujeta una mancuerna con ambas manos por encima de la cabeza.\n2. Flexiona los codos lentamente dejando caer la mancuerna detrás de la cabeza.\n3. Extiende los codos para subir la mancuerna sin mover los hombros.\n4. Mantén los codos apuntando hacia el frente durante todo el ejercicio.\n5. Ideal para trabajar la cabeza larga del tríceps.	\N
8	Curl tipo martillo con mancuernas	Brazos	Mancuernas	1. Sujeta una mancuerna en cada mano con las palmas enfrentadas (posición neutra).\n2. Flexiona los codos manteniendo esa posición hasta que las mancuernas lleguen al pecho.\n3. Contrae los bíceps y braquiales en la parte superior.\n4. Baja lentamente manteniendo la posición neutra.\n5. Evita mover los codos o balancear el cuerpo.	\N
9	Curl concentrado con mancuerna	Brazos	Mancuernas	1. Siéntate en un banco y apoya el codo sobre el muslo del mismo lado.\n2. Sujeta la mancuerna con la palma hacia arriba.\n3. Flexiona el brazo contrayendo el bíceps en la parte alta del movimiento.\n4. Baja lentamente hasta la extensión completa del brazo.\n5. Aísla el movimiento evitando involucrar los hombros.	\N
10	Rompecráneos con barra	Brazos	Barra	1. Túmbate en un banco plano sujetando una barra EZ con agarre cerrado.\n2. Baja la barra lentamente hacia la frente flexionando los codos.\n3. Mantén los codos fijos y cerca del rostro.\n4. Extiende los codos para volver a la posición inicial.\n5. Evita abrir los codos y no uses peso excesivo para no forzar los codos.	\N
11	Dominadas	Espalda	Peso corporal	1. Cuelga de una barra con las palmas mirando hacia adelante y los brazos completamente extendidos.\n2. Tira de tu cuerpo hacia arriba contrayendo los dorsales hasta que la barbilla supere la barra.\n3. Baja de forma controlada hasta la posición inicial.\n4. Mantén el torso firme, evitando balanceos para mayor activación muscular.	\N
12	Peso muerto (Barra)	Espalda	Barra	1. Coloca los pies al ancho de los hombros frente a una barra.\n2. Flexiona las caderas y rodillas manteniendo la espalda recta y agarra la barra.\n3. Eleva la barra estirando caderas y rodillas al mismo tiempo hasta quedar erguido.\n4. Baja controladamente manteniendo la espalda neutra.\n5. Evita curvar la espalda durante todo el recorrido.	\N
13	Remo inclinado con barra	Espalda	Barra	1. De pie, flexiona ligeramente las rodillas y el torso hacia delante.\n2. Sujeta una barra con agarre prono y brazos extendidos.\n3. Lleva la barra hacia el abdomen contrayendo los dorsales.\n4. Mantén los codos cerca del cuerpo y baja controladamente.\n5. Mantén la espalda recta durante todo el movimiento.	\N
14	Jalón en polea alta	Espalda	Polea	1. Sentado frente a una polea alta, sujeta la barra con agarre ancho.\n2. Tira de la barra hacia el pecho contrayendo los dorsales.\n3. Baja controladamente sin balancearte ni usar impulso.\n4. Mantén el pecho elevado y los codos apuntando hacia abajo.	\N
15	Remo con barra en T	Espalda	Máquina	1. Usa una barra T-bar o una barra con soporte en un extremo.\n2. Inclina el torso hacia adelante y sujeta el agarre con ambas manos.\n3. Tira del peso hacia el abdomen contrayendo la espalda.\n4. Baja de forma controlada y evita balanceos.\n5. Excelente para dar grosor a la espalda.	\N
16	Remo sentado en polea baja	Espalda	Polea	1. Siéntate en la máquina con los pies apoyados y la espalda recta.\n2. Sujeta la barra o el triángulo con ambos brazos extendidos.\n3. Tira hacia tu abdomen manteniendo los codos cerca del cuerpo.\n4. Contrae los dorsales y vuelve lentamente.\n5. No encorves la espalda al tirar.	\N
17	Face pull	Espalda	Polea	1. Coloca una cuerda en la polea alta y sujétala con ambas manos.\n2. Tira hacia tu cara separando las manos al final del recorrido.\n3. Enfócate en contraer deltoides posteriores y trapecios.\n4. Mantén los codos elevados durante todo el ejercicio.	\N
18	Buenos días (Good morning)	Espalda	Barra	1. Coloca una barra sobre la parte alta de la espalda como en una sentadilla.\n2. Flexiona las caderas hacia atrás bajando el torso con la espalda recta.\n3. Detente cuando el torso esté casi paralelo al suelo.\n4. Vuelve a subir activando glúteos y erectores espinales.\n5. Ideal para mejorar fuerza lumbar y estabilidad posterior.	\N
19	Encogimiento con mancuernas	Espalda	Mancuernas	1. Sujeta una mancuerna en cada mano con los brazos extendidos.\n2. Eleva los hombros hacia las orejas lo más alto posible.\n3. Mantén la contracción por un segundo y baja lentamente.\n4. Mantén la espalda recta y no uses impulso.\n5. Aísla perfectamente los trapecios superiores.	\N
20	Remo invertido (Inverted row)	Espalda	Peso corporal	1. Coloca una barra baja o usa una máquina Smith.\n2. Acuéstate debajo y sujeta la barra con agarre prono.\n3. Eleva tu torso hacia la barra manteniendo el cuerpo alineado.\n4. Contrae la espalda y baja lentamente.\n5. Excelente ejercicio con peso corporal para todos los niveles.	\N
21	Press de banca con barra	Pecho	Barra	1. Acuéstate sobre un banco plano con los pies apoyados en el suelo.\n2. Sujeta la barra con las manos ligeramente más abiertas que los hombros.\n3. Desbloquea la barra y bájala de forma controlada hasta que toque ligeramente el pecho.\n4. Empuja hacia arriba hasta estirar completamente los brazos sin bloquear los codos.\n5. Repite el movimiento manteniendo la espalda y glúteos en contacto con el banco.	\N
22	Press inclinado con mancuernas	Pecho	Mancuernas	1. Siéntate en un banco inclinado a 30-45° y recuéstate con una mancuerna en cada mano.\n2. Coloca las mancuernas al nivel del pecho con las palmas mirando hacia adelante.\n3. Empuja las mancuernas hacia arriba hasta estirar completamente los brazos.\n4. Junta ligeramente las mancuernas arriba sin que se golpeen.\n5. Baja lentamente a la posición inicial con control.	\N
23	Aperturas con mancuernas	Pecho	Mancuernas	1. Acuéstate en un banco plano con una mancuerna en cada mano.\n2. Eleva los brazos con las mancuernas por encima del pecho, ligeramente flexionados.\n3. Abre los brazos en un arco amplio hacia los lados, bajando hasta que estén al nivel del pecho.\n4. Contrae el pecho y vuelve a cerrar los brazos siguiendo el mismo arco.\n5. No bloquees los codos ni dejes que las mancuernas se toquen.	\N
24	Press inclinado en máquina Smith	Pecho	Máquina	1. Ajusta el banco a un ángulo inclinado de 30–45° dentro de la máquina Smith.\n2. Siéntate y sujeta la barra con las manos ligeramente abiertas.\n3. Desbloquea la barra y bájala de forma controlada hasta la parte superior del pecho.\n4. Empuja hacia arriba hasta estirar los brazos por completo.\n5. Controla la bajada para mantener tensión en el pecho.	\N
25	Crossover en polea	Pecho	Polea	1. Colócate en el centro de una máquina de poleas altas con una asa en cada mano.\n2. Da un paso adelante y mantén el torso inclinado ligeramente hacia adelante.\n3. Junta los brazos en un arco por delante del pecho con una ligera flexión en los codos.\n4. Aprieta el pecho al final del recorrido.\n5. Vuelve lentamente a la posición inicial sin perder tensión.	\N
26	Press en máquina	Pecho	Máquina	1. Ajusta el asiento de la máquina para que los mangos estén a la altura del pecho.\n2. Sujeta las asas con las palmas hacia adelante y pies apoyados en el suelo.\n3. Empuja las asas hacia adelante hasta extender los brazos.\n4. Mantén una ligera flexión en los codos al final.\n5. Regresa lentamente a la posición inicial controlando el movimiento.	\N
27	Fondos para pecho	Pecho	Peso corporal	1. Sujétate en unas barras paralelas con los brazos extendidos.\n2. Inclina ligeramente el torso hacia adelante.\n3. Baja el cuerpo flexionando los codos hasta sentir estiramiento en el pecho.\n4. Empuja hacia arriba hasta volver a extender los brazos.\n5. Mantén el core activado y evita movimientos bruscos.	\N
28	Press declinado con barra	Pecho	Barra	1. Acuéstate en un banco declinado con los pies bien apoyados.\n2. Sujeta la barra con un agarre ancho y retírala del soporte.\n3. Baja la barra hacia la parte baja del pecho de forma controlada.\n4. Empuja la barra hacia arriba sin bloquear completamente los codos.\n5. Controla todo el movimiento para evitar lesiones en hombros.	\N
29	Pullover con mancuerna	Pecho	Mancuernas	1. Acuéstate en un banco plano con una mancuerna entre las manos.\n2. Sujeta la mancuerna sobre el pecho con los brazos estirados.\n3. Baja la mancuerna hacia atrás en un arco por encima de la cabeza.\n4. Detén el movimiento cuando sientas el estiramiento máximo.\n5. Vuelve a la posición inicial activando el pecho y sin doblar los codos.	\N
30	Press con banda elástica	Pecho	Banda elástica	1. Ancla la banda a una superficie estable detrás de ti a la altura del pecho.\n2. Sujeta los extremos con las manos y da un paso al frente.\n3. Empuja los brazos hacia adelante simulando un press de banca.\n4. Junta las manos al frente contrayendo el pecho.\n5. Regresa lentamente a la posición inicial sin perder tensión.	\N
31	Elevaciones laterales con mancuernas	Hombros	Mancuernas	1. Ponte de pie con una mancuerna en cada mano a los lados.\n2. Mantén una ligera flexión en los codos y eleva los brazos lateralmente hasta que estén a la altura de los hombros.\n3. Pausa un segundo en la parte superior.\n4. Baja los brazos lentamente a la posición inicial.\n5. Mantén el torso erguido y evita balancearte.	\N
32	Press militar con barra	Hombros	Barra	1. Siéntate en un banco con respaldo y coloca la barra sobre los hombros, frente a ti.\n2. Sujeta la barra con un agarre un poco más ancho que los hombros.\n3. Empuja la barra hacia arriba sobre la cabeza hasta que los brazos estén completamente extendidos.\n4. Baja la barra controladamente hasta la altura de los hombros.\n5. Mantén la espalda recta y los pies firmes en el suelo.	\N
33	Face Pull con polea	Hombros	Polea	1. Ajusta la polea a la altura del rostro con una cuerda como accesorio.\n2. Agarra ambos extremos de la cuerda con las palmas enfrentadas.\n3. Tira de la cuerda hacia el rostro, separando los extremos al final del movimiento.\n4. Contrae los omóplatos al final del recorrido.\n5. Regresa lentamente a la posición inicial.	\N
34	Press Arnold	Hombros	Mancuernas	1. Siéntate en un banco con respaldo y sujeta una mancuerna en cada mano a la altura del pecho, con las palmas hacia ti.\n2. Al levantar las mancuernas, rota las muñecas para que las palmas queden hacia adelante.\n3. Estira completamente los brazos por encima de la cabeza.\n4. Baja las mancuernas rotando nuevamente hasta volver a la posición inicial.\n5. Controla el movimiento en todo momento.	\N
35	Encogimiento de hombros con barra	Hombros	Barra	1. Sujeta una barra con ambas manos al frente, brazos extendidos.\n2. Eleva los hombros hacia las orejas tanto como puedas.\n3. Pausa brevemente en la parte superior del movimiento.\n4. Baja los hombros lentamente.\n5. Evita girar o rotar los hombros durante el movimiento.	\N
36	Elevaciones frontales con mancuernas	Hombros	Mancuernas	1. Sostén una mancuerna en cada mano al frente de tus muslos.\n2. Levanta una mancuerna al frente hasta la altura de los hombros, manteniendo el brazo recto.\n3. Baja lentamente mientras elevas la otra mancuerna.\n4. Alterna brazos en cada repetición.\n5. Mantén el torso firme y sin impulso.	\N
37	Press de hombros en máquina	Hombros	Máquina	1. Ajusta el asiento para que las manijas estén a la altura de los hombros.\n2. Sujeta las manijas con un agarre firme y empuja hacia arriba hasta extender los brazos.\n3. Baja lentamente controlando el movimiento.\n4. Mantén la espalda apoyada y los pies firmes en el suelo.\n5. Evita bloquear los codos completamente.	\N
38	Elevaciones laterales en máquina	Hombros	Máquina	1. Siéntate en la máquina con los brazos apoyados en las almohadillas.\n2. Empuja los brazos hacia los lados, separándolos del cuerpo.\n3. Pausa un momento al final del recorrido.\n4. Vuelve lentamente a la posición inicial.\n5. Asegúrate de no usar impulso y mantener la espalda recta.	\N
39	Elevaciones posteriores en peck-deck	Hombros	Máquina	1. Siéntate en la máquina de peck-deck mirando hacia el respaldo.\n2. Sujeta las manijas y lleva los brazos hacia atrás en un movimiento de apertura.\n3. Pausa brevemente cuando los brazos estén extendidos.\n4. Regresa de forma controlada a la posición inicial.\n5. Mantén los codos ligeramente flexionados y evita empujar con el cuerpo.	\N
40	Overhead Press con mancuernas	Hombros	Mancuernas	1. Sostén una mancuerna en cada mano a la altura de los hombros con las palmas hacia adelante.\n2. Empuja las mancuernas hacia arriba hasta que los brazos estén completamente extendidos.\n3. Baja lentamente hasta la posición inicial.\n4. Mantén el torso erguido y los abdominales activados.\n5. Evita arquear la espalda durante la ejecución.	\N
41	Sentadilla con barra	Piernas	Barra	1. Coloca la barra sobre la parte alta de la espalda.\n2. Coloca los pies al ancho de los hombros, con ligera rotación externa.\n3. Baja flexionando rodillas y caderas manteniendo la espalda recta.\n4. Llega hasta que los muslos estén paralelos al suelo o más.\n5. Sube empujando con fuerza a través de los talones hasta extender caderas y rodillas.	\N
42	Prensa de piernas	Piernas	Máquina	1. Siéntate en la máquina y coloca los pies al ancho de los hombros en la plataforma.\n2. Sujeta las asas laterales para estabilizar el cuerpo.\n3. Flexiona las rodillas para bajar el peso controladamente.\n4. Empuja con fuerza hasta estirar las piernas sin bloquear completamente las rodillas.\n5. Mantén la espalda y glúteos en contacto con el respaldo.	\N
43	Peso muerto rumano	Piernas	Barra	1. De pie, sujeta la barra con un agarre prono frente a los muslos.\n2. Flexiona las caderas hacia atrás bajando la barra por delante de las piernas.\n3. Mantén la espalda recta y las rodillas ligeramente flexionadas.\n4. Baja hasta sentir el estiramiento en los isquiosurales.\n5. Vuelve a la posición inicial contrayendo los glúteos.	\N
44	Zancadas con mancuernas	Piernas	Mancuernas	1. Sujeta una mancuerna en cada mano con los brazos a los lados.\n2. Da un paso largo hacia adelante y flexiona ambas rodillas.\n3. La rodilla trasera debe acercarse al suelo sin tocarlo.\n4. Empuja con la pierna delantera para volver a la posición inicial.\n5. Alterna piernas en cada repetición o completa todas con una antes de cambiar.	\N
45	Hip thrust (elevación de cadera)	Piernas	Barra	1. Apoya la parte alta de la espalda en un banco y coloca la barra sobre las caderas.\n2. Flexiona las rodillas y apoya los pies en el suelo.\n3. Empuja las caderas hacia arriba contrayendo los glúteos al máximo.\n4. Haz una breve pausa arriba y baja lentamente.\n5. Mantén el mentón hacia el pecho y el abdomen activado.	\N
46	Extensión de piernas en máquina	Piernas	Máquina	1. Siéntate en la máquina con la espalda recta y ajusta el rodillo sobre las espinillas.\n2. Extiende las piernas hasta estirarlas completamente.\n3. Contrae los cuádriceps arriba y baja lentamente.\n4. No bloquees las rodillas en la parte final del movimiento.\n5. Controla la fase excéntrica para máxima efectividad.	\N
47	Curl femoral tumbado	Piernas	Máquina	1. Túmbate boca abajo en la máquina y ajusta el rodillo detrás de los tobillos.\n2. Flexiona las rodillas llevando los talones hacia los glúteos.\n3. Mantén la contracción un segundo y baja con control.\n4. No arquees la espalda ni levantes el abdomen del banco.\n5. Ideal para trabajar isquiosurales de forma aislada.	\N
48	Sentadilla goblet	Piernas	Mancuernas	1. Sujeta una mancuerna verticalmente frente al pecho con ambas manos.\n2. Coloca los pies al ancho de los hombros.\n3. Baja en sentadilla manteniendo el torso erguido.\n4. Llega hasta que los muslos estén paralelos o más.\n5. Empuja con los talones para volver a la posición inicial.	\N
49	Sentadilla búlgara	Piernas	Mancuernas	1. Coloca el pie trasero sobre un banco o superficie elevada.\n2. Da un paso adelante con la otra pierna.\n3. Baja el cuerpo flexionando la pierna delantera.\n4. Mantén el torso recto y no dejes que la rodilla pase los dedos del pie.\n5. Sube empujando con el talón de la pierna delantera.	\N
50	Elevación de talones de pie (gemelos)	Piernas	Máquina	1. Colócate en la máquina con los hombros bajo los pads y los pies sobre la plataforma.\n2. Baja los talones lentamente por debajo del nivel del escalón.\n3. Eleva los talones lo más alto posible contrayendo los gemelos.\n4. Mantén una pausa arriba y baja controladamente.\n5. No rebotes ni uses impulso al subir.	\N
\.


--
-- Data for Name: ejercicio_foto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ejercicio_foto (id, url, ejercicio_id) FROM stdin;
1	ejercicios/fondos_banco.png	1
2	ejercicios/curl_biceps_barra.png	3
3	ejercicios/extension_triceps_polea.png	6
4	ejercicios/dominadas.png	11
5	ejercicios/peso_muerto.png	12
6	ejercicios/remo_t.png	15
\.


--
-- Data for Name: progreso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.progreso (id, usuario_id, fecha, peso, comentarios) FROM stdin;
\.


--
-- Data for Name: progreso_foto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.progreso_foto (id, progreso_id, ruta) FROM stdin;
\.


--
-- Data for Name: rutina; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rutina (id, nombre, descripcion, usuario_id, fecha_creacion, es_defecto) FROM stdin;
1	Push Intermedio	Entrenamiento de empuje para pecho, hombros y tríceps	\N	2025-06-15 23:49:43.587947	t
\.


--
-- Data for Name: rutina_ejercicio; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rutina_ejercicio (id, rutina_id, ejercicio_id, orden, comentarios) FROM stdin;
1	1	21	1	\N
2	1	23	2	\N
3	1	31	3	\N
\.


--
-- Data for Name: rutina_serie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rutina_serie (id, rutina_ejercicio_id, numero, repeticiones, peso) FROM stdin;
1	1	1	8	0
2	1	2	8	0
3	1	3	6	0
4	2	1	10	0
5	2	2	8	0
6	2	3	8	0
7	3	1	12	0
8	3	2	12	0
9	3	3	10	0
\.


--
-- Data for Name: sesion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sesion (id, usuario_id, fecha, rutina_id) FROM stdin;
\.


--
-- Data for Name: sesion_ejercicio; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sesion_ejercicio (id, sesion_id, ejercicio_id, orden, series, repeticiones, peso, comentarios) FROM stdin;
\.


--
-- Data for Name: sesion_serie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sesion_serie (id, sesion_ejercicio_id, numero, repeticiones, peso) FROM stdin;
\.


--
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario (id, nombre, apellido, email, hashed_password, fecha_nacimiento, fecha_registro, is_admin, token_recuperacion, token_expira) FROM stdin;
1	Alejandro	Santos	a.santosc02@gmail.com	$2b$12$TeQzsOFnsnqqEGB6DL8V5eUjNMyD6aONU7rf82nDCDzvUnJja5R.e	2002-06-12	2025-06-15 23:51:57.459601	f	\N	\N
\.


--
-- Name: alimento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.alimento_id_seq', 1, false);


--
-- Name: comida_alimento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.comida_alimento_id_seq', 1, false);


--
-- Name: comida_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.comida_id_seq', 1, false);


--
-- Name: dieta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dieta_id_seq', 1, false);


--
-- Name: ejercicio_foto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ejercicio_foto_id_seq', 6, true);


--
-- Name: ejercicio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ejercicio_id_seq', 50, true);


--
-- Name: progreso_foto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.progreso_foto_id_seq', 1, false);


--
-- Name: progreso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.progreso_id_seq', 1, false);


--
-- Name: rutina_ejercicio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rutina_ejercicio_id_seq', 3, true);


--
-- Name: rutina_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rutina_id_seq', 1, true);


--
-- Name: rutina_serie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rutina_serie_id_seq', 9, true);


--
-- Name: sesion_ejercicio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sesion_ejercicio_id_seq', 1, false);


--
-- Name: sesion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sesion_id_seq', 1, false);


--
-- Name: sesion_serie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sesion_serie_id_seq', 1, false);


--
-- Name: usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_id_seq', 1, true);


--
-- Name: alimento alimento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alimento
    ADD CONSTRAINT alimento_pkey PRIMARY KEY (id);


--
-- Name: comida_alimento comida_alimento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comida_alimento
    ADD CONSTRAINT comida_alimento_pkey PRIMARY KEY (id);


--
-- Name: comida comida_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comida
    ADD CONSTRAINT comida_pkey PRIMARY KEY (id);


--
-- Name: dieta dieta_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dieta
    ADD CONSTRAINT dieta_pkey PRIMARY KEY (id);


--
-- Name: ejercicio_foto ejercicio_foto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ejercicio_foto
    ADD CONSTRAINT ejercicio_foto_pkey PRIMARY KEY (id);


--
-- Name: ejercicio ejercicio_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ejercicio
    ADD CONSTRAINT ejercicio_pkey PRIMARY KEY (id);


--
-- Name: progreso_foto progreso_foto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progreso_foto
    ADD CONSTRAINT progreso_foto_pkey PRIMARY KEY (id);


--
-- Name: progreso progreso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progreso
    ADD CONSTRAINT progreso_pkey PRIMARY KEY (id);


--
-- Name: rutina_ejercicio rutina_ejercicio_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rutina_ejercicio
    ADD CONSTRAINT rutina_ejercicio_pkey PRIMARY KEY (id);


--
-- Name: rutina rutina_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rutina
    ADD CONSTRAINT rutina_pkey PRIMARY KEY (id);


--
-- Name: rutina_serie rutina_serie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rutina_serie
    ADD CONSTRAINT rutina_serie_pkey PRIMARY KEY (id);


--
-- Name: sesion_ejercicio sesion_ejercicio_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion_ejercicio
    ADD CONSTRAINT sesion_ejercicio_pkey PRIMARY KEY (id);


--
-- Name: sesion sesion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion
    ADD CONSTRAINT sesion_pkey PRIMARY KEY (id);


--
-- Name: sesion_serie sesion_serie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion_serie
    ADD CONSTRAINT sesion_serie_pkey PRIMARY KEY (id);


--
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);


--
-- Name: ix_usuario_token_recuperacion; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_usuario_token_recuperacion ON public.usuario USING btree (token_recuperacion);


--
-- Name: alimento alimento_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alimento
    ADD CONSTRAINT alimento_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);


--
-- Name: comida_alimento comida_alimento_alimento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comida_alimento
    ADD CONSTRAINT comida_alimento_alimento_id_fkey FOREIGN KEY (alimento_id) REFERENCES public.alimento(id);


--
-- Name: comida_alimento comida_alimento_comida_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comida_alimento
    ADD CONSTRAINT comida_alimento_comida_id_fkey FOREIGN KEY (comida_id) REFERENCES public.comida(id);


--
-- Name: comida comida_dieta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comida
    ADD CONSTRAINT comida_dieta_id_fkey FOREIGN KEY (dieta_id) REFERENCES public.dieta(id);


--
-- Name: dieta dieta_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dieta
    ADD CONSTRAINT dieta_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);


--
-- Name: ejercicio_foto ejercicio_foto_ejercicio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ejercicio_foto
    ADD CONSTRAINT ejercicio_foto_ejercicio_id_fkey FOREIGN KEY (ejercicio_id) REFERENCES public.ejercicio(id);


--
-- Name: ejercicio ejercicio_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ejercicio
    ADD CONSTRAINT ejercicio_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);


--
-- Name: progreso_foto progreso_foto_progreso_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progreso_foto
    ADD CONSTRAINT progreso_foto_progreso_id_fkey FOREIGN KEY (progreso_id) REFERENCES public.progreso(id);


--
-- Name: progreso progreso_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.progreso
    ADD CONSTRAINT progreso_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);


--
-- Name: rutina_ejercicio rutina_ejercicio_ejercicio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rutina_ejercicio
    ADD CONSTRAINT rutina_ejercicio_ejercicio_id_fkey FOREIGN KEY (ejercicio_id) REFERENCES public.ejercicio(id);


--
-- Name: rutina_ejercicio rutina_ejercicio_rutina_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rutina_ejercicio
    ADD CONSTRAINT rutina_ejercicio_rutina_id_fkey FOREIGN KEY (rutina_id) REFERENCES public.rutina(id);


--
-- Name: rutina_serie rutina_serie_rutina_ejercicio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rutina_serie
    ADD CONSTRAINT rutina_serie_rutina_ejercicio_id_fkey FOREIGN KEY (rutina_ejercicio_id) REFERENCES public.rutina_ejercicio(id);


--
-- Name: rutina rutina_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rutina
    ADD CONSTRAINT rutina_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);


--
-- Name: sesion_ejercicio sesion_ejercicio_ejercicio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion_ejercicio
    ADD CONSTRAINT sesion_ejercicio_ejercicio_id_fkey FOREIGN KEY (ejercicio_id) REFERENCES public.ejercicio(id);


--
-- Name: sesion_ejercicio sesion_ejercicio_sesion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion_ejercicio
    ADD CONSTRAINT sesion_ejercicio_sesion_id_fkey FOREIGN KEY (sesion_id) REFERENCES public.sesion(id);


--
-- Name: sesion sesion_rutina_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion
    ADD CONSTRAINT sesion_rutina_id_fkey FOREIGN KEY (rutina_id) REFERENCES public.rutina(id);


--
-- Name: sesion_serie sesion_serie_sesion_ejercicio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion_serie
    ADD CONSTRAINT sesion_serie_sesion_ejercicio_id_fkey FOREIGN KEY (sesion_ejercicio_id) REFERENCES public.sesion_ejercicio(id);


--
-- Name: sesion sesion_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion
    ADD CONSTRAINT sesion_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuario(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


--
-- PostgreSQL database dump complete
--

