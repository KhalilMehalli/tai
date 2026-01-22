--
-- PostgreSQL database dump
--

\restrict MckzwsTn4xhsRFqr6lw7L6fTGShW35nl7FvRXVWMDVr5vM6AMT9qQn5IUsu7qZy

-- Dumped from database version 14.20 (Ubuntu 14.20-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.20 (Ubuntu 14.20-0ubuntu0.22.04.1)

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
-- Name: language; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.language AS ENUM (
    'C',
    'JAVA',
    'PYTHON',
    'CCP'
);


--
-- Name: progressstatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.progressstatus AS ENUM (
    'NOT_STARTED',
    'IN_PROGRESS',
    'VALIDATED'
);


--
-- Name: submissionstatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.submissionstatus AS ENUM (
    'SUCCESS',
    'FAILURE',
    'PENDING'
);


--
-- Name: userrole; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.userrole AS ENUM (
    'STUDENT',
    'TEACHER'
);


--
-- Name: visibility; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.visibility AS ENUM (
    'PUBLIC',
    'PRIVATE'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: course; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.course (
    id integer NOT NULL,
    name character varying NOT NULL,
    unit_id integer NOT NULL,
    visibility public.visibility NOT NULL,
    difficulty integer NOT NULL,
    "position" integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    description text NOT NULL
);


--
-- Name: course_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.course_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: course_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.course_id_seq OWNED BY public.course.id;


--
-- Name: exercise; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.exercise (
    id integer NOT NULL,
    course_id integer NOT NULL,
    name character varying NOT NULL,
    description text NOT NULL,
    visibility public.visibility NOT NULL,
    language public.language NOT NULL,
    difficulty integer NOT NULL,
    "position" integer NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: exercise_file; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.exercise_file (
    id integer NOT NULL,
    exercise_id integer NOT NULL,
    name character varying NOT NULL,
    template_without_marker text NOT NULL,
    extension character varying NOT NULL,
    is_main boolean NOT NULL,
    editable boolean NOT NULL,
    "position" integer NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: exercise_file_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.exercise_file_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: exercise_file_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.exercise_file_id_seq OWNED BY public.exercise_file.id;


--
-- Name: exercise_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.exercise_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: exercise_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.exercise_id_seq OWNED BY public.exercise.id;


--
-- Name: exercise_marker; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.exercise_marker (
    id integer NOT NULL,
    exercise_file_id integer NOT NULL,
    marker_id character varying NOT NULL,
    solution_content text NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: exercise_marker_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.exercise_marker_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: exercise_marker_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.exercise_marker_id_seq OWNED BY public.exercise_marker.id;


--
-- Name: exercise_progress; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.exercise_progress (
    id integer NOT NULL,
    user_id integer NOT NULL,
    exercise_id integer NOT NULL,
    status public.progressstatus NOT NULL,
    attempts_count integer,
    started_at timestamp with time zone DEFAULT now(),
    last_activity timestamp with time zone
);


--
-- Name: exercise_progress_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.exercise_progress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: exercise_progress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.exercise_progress_id_seq OWNED BY public.exercise_progress.id;


--
-- Name: hint; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hint (
    id integer NOT NULL,
    exercise_id integer NOT NULL,
    unlock_after_attempts integer NOT NULL,
    body text NOT NULL,
    "position" integer NOT NULL
);


--
-- Name: hint_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.hint_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hint_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hint_id_seq OWNED BY public.hint.id;


--
-- Name: hint_view; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hint_view (
    id integer NOT NULL,
    user_id integer NOT NULL,
    hint_id integer NOT NULL,
    viewed_at timestamp with time zone DEFAULT now()
);


--
-- Name: hint_view_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.hint_view_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hint_view_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hint_view_id_seq OWNED BY public.hint_view.id;


--
-- Name: submission_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.submission_history (
    id integer NOT NULL,
    user_id integer NOT NULL,
    exercise_id integer NOT NULL,
    status public.submissionstatus NOT NULL,
    submitted_at timestamp with time zone DEFAULT now()
);


--
-- Name: submission_history_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.submission_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: submission_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.submission_history_id_seq OWNED BY public.submission_history.id;


--
-- Name: submission_marker; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.submission_marker (
    id integer NOT NULL,
    submission_id integer NOT NULL,
    exercise_file_id integer NOT NULL,
    marker_id character varying NOT NULL,
    content text NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: submission_marker_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.submission_marker_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: submission_marker_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.submission_marker_id_seq OWNED BY public.submission_marker.id;


--
-- Name: submission_result; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.submission_result (
    id integer NOT NULL,
    submission_id integer NOT NULL,
    test_case_id integer NOT NULL,
    status public.submissionstatus NOT NULL,
    actual_output text NOT NULL,
    error_log text
);


--
-- Name: submission_result_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.submission_result_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: submission_result_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.submission_result_id_seq OWNED BY public.submission_result.id;


--
-- Name: test_case; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.test_case (
    id integer NOT NULL,
    exercise_id integer NOT NULL,
    argv text,
    expected_output text NOT NULL,
    "position" integer NOT NULL,
    comment text
);


--
-- Name: test_case_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.test_case_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: test_case_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.test_case_id_seq OWNED BY public.test_case.id;


--
-- Name: unit; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.unit (
    id integer NOT NULL,
    name character varying,
    description text NOT NULL,
    author_id integer,
    visibility public.visibility NOT NULL,
    difficulty integer NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: unit_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.unit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: unit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.unit_id_seq OWNED BY public.unit.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    firstname character varying NOT NULL,
    lastname character varying NOT NULL,
    email character varying NOT NULL,
    mdp_hash character varying NOT NULL,
    role public.userrole NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: course id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course ALTER COLUMN id SET DEFAULT nextval('public.course_id_seq'::regclass);


--
-- Name: exercise id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise ALTER COLUMN id SET DEFAULT nextval('public.exercise_id_seq'::regclass);


--
-- Name: exercise_file id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_file ALTER COLUMN id SET DEFAULT nextval('public.exercise_file_id_seq'::regclass);


--
-- Name: exercise_marker id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_marker ALTER COLUMN id SET DEFAULT nextval('public.exercise_marker_id_seq'::regclass);


--
-- Name: exercise_progress id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_progress ALTER COLUMN id SET DEFAULT nextval('public.exercise_progress_id_seq'::regclass);


--
-- Name: hint id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hint ALTER COLUMN id SET DEFAULT nextval('public.hint_id_seq'::regclass);


--
-- Name: hint_view id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hint_view ALTER COLUMN id SET DEFAULT nextval('public.hint_view_id_seq'::regclass);


--
-- Name: submission_history id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.submission_history ALTER COLUMN id SET DEFAULT nextval('public.submission_history_id_seq'::regclass);


--
-- Name: submission_marker id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.submission_marker ALTER COLUMN id SET DEFAULT nextval('public.submission_marker_id_seq'::regclass);


--
-- Name: submission_result id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.submission_result ALTER COLUMN id SET DEFAULT nextval('public.submission_result_id_seq'::regclass);


--
-- Name: test_case id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.test_case ALTER COLUMN id SET DEFAULT nextval('public.test_case_id_seq'::regclass);


--
-- Name: unit id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.unit ALTER COLUMN id SET DEFAULT nextval('public.unit_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
787cb8d1b77c
\.


--
-- Data for Name: course; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.course (id, name, unit_id, visibility, difficulty, "position", created_at, description) FROM stdin;
7	Les bases	3	PUBLIC	5	1	2026-01-17 16:55:00.417887+01	Python 
6	Premier cours	2	PUBLIC	2	1	2026-01-17 15:56:29.78688+01	Java java java java
1	Les bases	1	PUBLIC	1	0	2025-12-06 16:40:51.095602+01	Les bases de la programmation C 
4	Test 2	1	PUBLIC	2	3	2026-01-14 10:38:01.862856+01	Test modification depuis le front
2	Test	1	PUBLIC	3	1	2026-01-13 19:54:15.298003+01	Creation de cours depuis le front
14	Démo cours	7	PUBLIC	1	1	2026-01-22 13:44:25.507792+01	démo démo 2
\.


--
-- Data for Name: exercise; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.exercise (id, course_id, name, description, visibility, language, difficulty, "position", created_at) FROM stdin;
2	1	Afficher les n premières lignes d'un fichier	Vous devez completer la fonction "afficher_lignes", qui comme son nom l'indique ,va afficher les n premières lignes du fichier data.txt	PUBLIC	C	1	0	2025-12-06 17:28:03.915547+01
3	1	Test	Test	PUBLIC	C	1	0	2025-12-12 09:02:35.74337+01
6	1	Multiplication	Exercice avec  2 TODO à remplir	PRIVATE	C	1	0	2025-12-18 12:45:08.267532+01
7	1	Multiplication	Exercice avec  2 TODO à remplir	PUBLIC	C	1	0	2025-12-18 12:45:52.721959+01
8	2	Test Exo	Salut salut	PUBLIC	C	1	0	2026-01-14 12:06:57.240173+01
13	6	Addition	Addition en Java	PUBLIC	JAVA	3	0	2026-01-17 16:52:34.965492+01
14	7	Addition	Addition en python	PUBLIC	PYTHON	1	0	2026-01-17 16:58:07.942475+01
9	2	Test 2 Exo	qsc	PUBLIC	C	1	0	2026-01-14 12:07:53.809079+01
15	4	Test modifié depuis pgAdmin	Test après avoir implémenter la modification d'exercice ......	PUBLIC	C	5	0	2026-01-20 10:15:03.718767+01
10	4	Test 3	a	PUBLIC	C	1	0	2026-01-14 12:14:16.441271+01
1	1	Addition	Pendant ce cours, vous devrez réaliser une addition	PUBLIC	C	3	0	2025-12-06 16:54:14.051921+01
18	14	démo java	java démo	PUBLIC	JAVA	1	0	2026-01-22 13:45:12.864212+01
\.


--
-- Data for Name: exercise_file; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.exercise_file (id, exercise_id, name, template_without_marker, extension, is_main, editable, "position", created_at) FROM stdin;
8	3	main		c	t	t	0	2025-12-12 09:02:35.74337+01
9	3	file1	Salut	c	f	t	1	2025-12-12 09:02:35.74337+01
16	6	main	#include <stdio.h>\n#include <stdlib.h>\n#include "fonction.h"\n\nint main(char argc, char ** argv) {\n    int a = atoi(argv[1]);\n    int b = atoi(argv[2]);\n    int c = multiplication(a, b); \n    printf("%d", c);\n    return 0;\n}	c	t	t	0	2025-12-18 12:45:08.267532+01
17	6	fonction	#include <stdio.h>\n#include "fonction.h"\n\nint multiplication(int a, int b){\n// TODO: a\n\n// END TODO: a\n// Return le result\n// TODO: b\n\n// END TODO: b\n}\n	c	f	t	1	2025-12-18 12:45:08.267532+01
18	6	fonction	#ifndef FONCTION_H\n#define FONCTION_H\n\nint multiplication(int a, int b);\n#endif\n\n\n	h	f	t	2	2025-12-18 12:45:08.267532+01
19	7	main	#include <stdio.h>\n#include <stdlib.h>\n#include "fonction.h"\n\nint main(char argc, char ** argv) {\n    int a = atoi(argv[1]);\n    int b = atoi(argv[2]);\n    int c = multiplication(a, b); \n    printf("%d", c);\n    return 0;\n}	c	t	t	0	2025-12-18 12:45:52.721959+01
20	7	fonction	#include <stdio.h>\n#include "fonction.h"\n\nint multiplication(int a, int b){\n// TODO: a\n\n// END TODO: a\n// Return le result\n// TODO: b\n\n// END TODO: b\n}\n	c	f	t	1	2025-12-18 12:45:52.721959+01
21	7	fonction	#ifndef FONCTION_H\n#define FONCTION_H\n\nint multiplication(int a, int b);\n#endif\n\n\n	h	f	t	2	2025-12-18 12:45:52.721959+01
31	14	main	import sys\nimport fonction  \n\nif __name__ == "__main__":\n    if len(sys.argv) < 3:\n        print("Usage: python main.py <nombre1> <nombre2>")\n        sys.exit(0)\n\n    a = int(sys.argv[1])\n    b = int(sys.argv[2])\n    \n    c = fonction.addition(a, b)\n    \n    print(f"{c}", end="")	py	t	f	0	2026-01-17 16:58:07.942475+01
32	14	fonction	def addition(a, b):\n    # TODO: 1\n\n    # END TODO: 1	py	f	t	1	2026-01-17 16:58:07.942475+01
36	9	main	Test	c	t	t	0	2026-01-19 10:28:12.503882+01
37	8	main	Salut	c	t	t	0	2026-01-19 10:28:20.855817+01
55	15	main	#include <stdio.h>\n\nint main(){\nprintf("5");\n\n}	c	t	t	0	2026-01-20 12:30:12.478792+01
56	15	file2	#include <stdio.h>\n\n// TODO: "test"\n\n// END TODO: "test"	c	f	t	1	2026-01-20 12:30:12.478792+01
57	10	main		c	t	t	0	2026-01-20 13:58:22.542868+01
69	1	main	#include <stdio.h>\n#include <stdlib.h>\n#include "fonction.h"\n\nint main(char argc, char ** argv) {\n    int a = atoi(argv[1]);\n    int b = atoi(argv[2]);\n    int c = addition(a, b);\n    printf("%d", c);\n    return 0;\n}	c	t	t	0	2026-01-21 08:39:54.65439+01
70	1	fonction	#include <stdio.h>\n#include "fonction.h"\n\nint addition(int a, int b){\n// TODO: "1"\n\n// END TODO: "1"\n}	c	f	t	1	2026-01-21 08:39:54.65439+01
71	1	fonction	#ifndef FONCTION_H\n#define FONCTION_H\n\n\nint addition(int a, int b);\n\n#endif	h	f	f	2	2026-01-21 08:39:54.65439+01
80	2	main	#include <stdio.h>\n#include <stdlib.h>\n#include "fonction.h"\n\nint main(int argc, char **argv) {\n    if (argc < 2) return 1;\n\n    int n = atoi(argv[1]); \n    afficher_lignes(n, "data.txt"); \n\n    return 0;\n}	c	t	f	0	2026-01-21 15:45:50.305886+01
81	2	fonction	#include <stdio.h>\n#include <stdlib.h>\n#include "fonction.h"\n\nvoid afficher_lignes(int n, char *nom_fichier) {\n    \n    // Ouverture du fichier en lecture seule ("r" = read) \n    FILE *f = fopen(nom_fichier, "r");\n\n    if (f == NULL) return;\n\n    char buffer[256];\n    int i = 0;\n\n    // while (i < n && fgets(buffer, 256, f) != NULL) { printf("%s", buffer); i++; }\n    // TODO: 1\n\n    // END TODO: 1\n\n    fclose(f);\n}	c	f	t	1	2026-01-21 15:45:50.305886+01
82	2	fonction	#ifndef FONCTION_H\n#define FONCTION_H\n\nvoid afficher_lignes(int n, char *nom_fichier);\n\n#endif	h	f	f	2	2026-01-21 15:45:50.305886+01
83	2	data	Ligne 1 : azerty\nLigne 2 : _-_\nLigne 3 : *****\nLigne 4 : 123\nLigne 5 : zqsd	txt	f	f	3	2026-01-21 15:45:50.305886+01
84	13	Main	public class Main {\n    public static void main(String[] args) {\n        if (args.length < 2) {\n            System.out.println("Usage: java Main <nombre1> <nombre2>");\n            return;\n        }\n\n        int a = Integer.parseInt(args[0]);\n        int b = Integer.parseInt(args[1]);\n        \n        int c = Fonction.addition(a, b);\n        \n        System.out.printf("%d", c); \n    }\n}	java	t	f	0	2026-01-21 15:48:56.259382+01
85	13	Fonction	public class Fonction {\n    \n    public static int addition(int a, int b) {\n        // TODO: a\n\n        // END TODO: a\n    }\n}	java	f	t	1	2026-01-21 15:48:56.259382+01
89	18	Main	public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello World!");\n    }\n}	java	t	t	0	2026-01-22 13:46:50.016064+01
90	18	file2	Salut	java	f	t	1	2026-01-22 13:46:50.016064+01
\.


--
-- Data for Name: exercise_marker; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.exercise_marker (id, exercise_file_id, marker_id, solution_content, created_at) FROM stdin;
5	17	a	\n   int c = a*b;\n	2025-12-18 12:45:08.267532+01
6	17	b	\n   return c;\n	2025-12-18 12:45:08.267532+01
7	20	a	\n   int c = a*b;\n	2025-12-18 12:45:52.721959+01
8	20	b	\n   return c;\n	2025-12-18 12:45:52.721959+01
11	32	1	\n    \n    return a + b\n    	2026-01-17 16:58:07.942475+01
13	56	"test"	\nint function_test(){\nprintf("5");\n\n}\n	2026-01-20 12:30:12.478792+01
17	70	"1"	\n   return a + b;\n	2026-01-21 08:39:54.65439+01
18	81	1	\n    while (i < n && fgets(buffer, 256, f) != NULL) {\n        printf("%s", buffer);\n        i++;\n    }\n    	2026-01-21 15:45:50.305886+01
19	85	a	\n        \n        return a + b;         \n        	2026-01-21 15:48:56.259382+01
\.


--
-- Data for Name: exercise_progress; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.exercise_progress (id, user_id, exercise_id, status, attempts_count, started_at, last_activity) FROM stdin;
3	1	7	VALIDATED	19	2025-12-18 12:47:24.185502+01	2026-01-21 10:18:38.9164+01
5	1	13	VALIDATED	5	2026-01-17 16:53:02.708345+01	2026-01-21 10:23:07.240959+01
6	1	14	VALIDATED	25	2026-01-17 16:58:21.705381+01	2026-01-21 10:24:00.89623+01
2	1	2	VALIDATED	33	2025-12-17 14:44:54.405944+01	2026-01-21 16:06:50.219893+01
1	1	1	VALIDATED	54	2025-12-17 14:44:06.393337+01	2026-01-21 17:14:51.322508+01
\.


--
-- Data for Name: hint; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.hint (id, exercise_id, unlock_after_attempts, body, "position") FROM stdin;
4	3	1	Salut	0
5	6	3	return c	0
6	6	1	c = a * b	1
7	7	3	return c	0
8	7	1	c = a * b	1
12	14	10	C'est encore moins compliqué	0
19	15	1	Indice modifié via le front	0
24	1	1	C'est pas compliqué	0
26	2	1	Pensé à bien afficher le contenue de la ligne à chaque tour de boucle	0
27	2	3	while (i < n && fgets(buffer, 256, f) != NULL)	1
28	13	3	C'est pas compliqué !!!!	0
35	18	2	NO	0
36	18	1	Yes	1
\.


--
-- Data for Name: hint_view; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.hint_view (id, user_id, hint_id, viewed_at) FROM stdin;
\.


--
-- Data for Name: submission_history; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.submission_history (id, user_id, exercise_id, status, submitted_at) FROM stdin;
2	1	1	FAILURE	2025-12-17 14:39:28.42667+01
57	1	7	SUCCESS	2025-12-18 12:47:24.185502+01
5	1	1	SUCCESS	2025-12-17 14:44:06.393337+01
6	1	2	FAILURE	2025-12-17 14:44:54.405944+01
7	1	2	FAILURE	2025-12-17 14:45:13.980652+01
8	1	2	FAILURE	2025-12-17 14:45:14.273492+01
9	1	2	FAILURE	2025-12-17 14:46:46.424115+01
10	1	2	SUCCESS	2025-12-17 14:47:56.865942+01
11	1	2	FAILURE	2025-12-17 14:48:22.055551+01
12	1	2	SUCCESS	2025-12-17 14:48:32.897341+01
13	1	1	SUCCESS	2025-12-17 15:22:56.554587+01
14	1	1	FAILURE	2025-12-17 15:23:23.415122+01
15	1	1	FAILURE	2025-12-17 16:14:34.75471+01
16	1	1	FAILURE	2025-12-17 16:14:55.332733+01
17	1	1	FAILURE	2025-12-17 16:17:35.673853+01
18	1	1	FAILURE	2025-12-17 16:30:46.235593+01
19	1	1	FAILURE	2025-12-17 16:31:10.213955+01
20	1	1	FAILURE	2025-12-17 16:31:21.021941+01
21	1	1	FAILURE	2025-12-17 16:32:07.124459+01
22	1	1	FAILURE	2025-12-17 16:32:15.662104+01
23	1	1	FAILURE	2025-12-17 16:32:54.285222+01
25	1	1	FAILURE	2025-12-17 16:33:31.036102+01
26	1	1	FAILURE	2025-12-17 16:34:04.356172+01
27	1	1	FAILURE	2025-12-17 16:34:13.181717+01
28	1	1	FAILURE	2025-12-17 16:34:45.83698+01
29	1	1	FAILURE	2025-12-17 16:35:15.357207+01
30	1	1	FAILURE	2025-12-17 16:35:40.325339+01
31	1	1	FAILURE	2025-12-17 16:37:14.900235+01
32	1	1	FAILURE	2025-12-17 16:39:45.750937+01
33	1	1	FAILURE	2025-12-17 16:40:56.391751+01
34	1	1	FAILURE	2025-12-17 16:41:10.452833+01
35	1	1	FAILURE	2025-12-17 16:42:07.956939+01
36	1	1	FAILURE	2025-12-17 16:45:53.083307+01
37	1	1	FAILURE	2025-12-17 16:46:06.557213+01
38	1	1	FAILURE	2025-12-17 16:46:32.604161+01
39	1	1	FAILURE	2025-12-17 16:46:57.021358+01
40	1	1	FAILURE	2025-12-17 16:48:25.996167+01
41	1	1	FAILURE	2025-12-17 16:49:09.085339+01
42	1	1	FAILURE	2025-12-17 16:58:12.001165+01
43	1	1	FAILURE	2025-12-17 16:58:17.260239+01
44	1	1	FAILURE	2025-12-17 17:25:59.954323+01
45	1	1	FAILURE	2025-12-17 17:26:08.100636+01
46	1	1	FAILURE	2025-12-17 17:26:21.81731+01
47	1	1	SUCCESS	2025-12-17 17:26:32.052254+01
48	1	1	SUCCESS	2025-12-17 17:26:32.194283+01
49	1	1	SUCCESS	2025-12-17 17:26:32.339419+01
50	1	1	FAILURE	2025-12-18 12:08:37.363664+01
51	1	1	FAILURE	2025-12-18 12:08:45.505843+01
52	1	1	FAILURE	2025-12-18 12:08:52.166446+01
53	1	1	SUCCESS	2025-12-18 12:08:57.685151+01
54	1	1	SUCCESS	2025-12-18 12:09:06.326282+01
55	1	7	FAILURE	2025-12-18 12:46:46.03278+01
56	1	7	FAILURE	2025-12-18 12:47:09.518229+01
60	1	7	FAILURE	2025-12-18 12:50:07.470694+01
63	1	7	FAILURE	2025-12-18 12:52:51.247629+01
64	1	7	FAILURE	2025-12-18 12:53:02.707585+01
65	1	7	FAILURE	2025-12-18 12:53:10.324951+01
66	1	7	FAILURE	2025-12-18 12:53:20.253092+01
67	1	7	FAILURE	2025-12-18 12:53:33.557195+01
68	1	7	FAILURE	2025-12-18 12:54:43.959478+01
74	1	1	FAILURE	2025-12-31 10:17:49.286264+01
75	1	1	SUCCESS	2025-12-31 10:18:10.798985+01
76	1	2	SUCCESS	2026-01-10 10:39:23.868125+01
77	1	2	SUCCESS	2026-01-10 10:39:40.009529+01
78	1	2	FAILURE	2026-01-10 10:39:50.220484+01
79	1	2	FAILURE	2026-01-10 10:40:37.456323+01
80	1	2	FAILURE	2026-01-10 10:40:55.130931+01
81	1	2	FAILURE	2026-01-10 10:41:04.015817+01
82	1	2	FAILURE	2026-01-10 10:41:10.150401+01
83	1	2	SUCCESS	2026-01-10 10:41:15.301729+01
85	1	2	SUCCESS	2026-01-10 10:41:46.430501+01
86	1	2	SUCCESS	2026-01-10 10:42:01.126952+01
87	1	2	SUCCESS	2026-01-10 10:42:03.016312+01
88	1	1	SUCCESS	2026-01-16 14:35:59.712746+01
89	1	1	FAILURE	2026-01-16 14:36:15.569859+01
105	1	14	SUCCESS	2026-01-19 09:27:13.438994+01
106	1	14	FAILURE	2026-01-19 09:27:19.213414+01
95	1	13	FAILURE	2026-01-17 16:52:54.106263+01
96	1	13	SUCCESS	2026-01-17 16:53:02.708345+01
97	1	13	SUCCESS	2026-01-17 16:53:06.628233+01
98	1	14	SUCCESS	2026-01-17 16:58:21.705381+01
99	1	14	SUCCESS	2026-01-17 16:58:31.972516+01
100	1	14	SUCCESS	2026-01-17 16:58:42.900591+01
101	1	14	FAILURE	2026-01-17 16:58:56.190457+01
102	1	14	FAILURE	2026-01-17 16:59:16.700849+01
103	1	14	SUCCESS	2026-01-17 16:59:36.017431+01
104	1	14	FAILURE	2026-01-17 16:59:40.932614+01
107	1	14	FAILURE	2026-01-19 09:27:25.298286+01
108	1	14	FAILURE	2026-01-19 09:27:38.601933+01
109	1	14	FAILURE	2026-01-19 09:29:03.968524+01
112	1	14	SUCCESS	2026-01-19 09:29:41.935735+01
113	1	1	FAILURE	2026-01-19 10:15:33.397999+01
114	1	1	SUCCESS	2026-01-19 10:15:58.922735+01
115	1	1	SUCCESS	2026-01-19 10:17:47.77629+01
117	1	2	SUCCESS	2026-01-19 10:19:00.200528+01
118	1	1	FAILURE	2026-01-20 10:09:26.127818+01
119	1	1	FAILURE	2026-01-20 10:09:32.324042+01
120	1	1	FAILURE	2026-01-20 10:09:40.371001+01
121	1	1	SUCCESS	2026-01-20 10:09:49.04595+01
122	1	2	FAILURE	2026-01-20 10:10:23.658509+01
123	1	2	SUCCESS	2026-01-20 10:11:05.29828+01
124	1	2	SUCCESS	2026-01-20 10:11:07.906858+01
125	1	1	FAILURE	2026-01-20 11:53:15.85034+01
126	1	1	FAILURE	2026-01-20 11:53:16.348928+01
127	1	1	FAILURE	2026-01-20 11:53:19.085349+01
128	1	7	SUCCESS	2026-01-20 13:59:12.713875+01
129	1	7	FAILURE	2026-01-20 13:59:20.89103+01
130	1	7	FAILURE	2026-01-20 13:59:41.254245+01
131	1	7	FAILURE	2026-01-20 13:59:50.021555+01
132	1	7	FAILURE	2026-01-20 13:59:51.117815+01
133	1	7	FAILURE	2026-01-20 13:59:52.180893+01
134	1	7	FAILURE	2026-01-20 14:00:06.203868+01
135	1	1	SUCCESS	2026-01-20 14:27:37.592762+01
136	1	1	FAILURE	2026-01-20 14:27:45.374327+01
137	1	1	SUCCESS	2026-01-20 14:27:55.042231+01
138	1	1	FAILURE	2026-01-20 14:28:59.215376+01
139	1	1	SUCCESS	2026-01-20 14:29:22.346117+01
140	1	7	FAILURE	2026-01-20 14:30:00.26476+01
141	1	7	SUCCESS	2026-01-20 14:30:24.652006+01
142	1	2	FAILURE	2026-01-20 14:31:06.915205+01
143	1	2	SUCCESS	2026-01-20 14:31:11.941731+01
144	1	2	FAILURE	2026-01-20 14:31:26.4354+01
145	1	1	FAILURE	2026-01-20 14:38:09.414236+01
146	1	1	SUCCESS	2026-01-20 14:38:30.733868+01
147	1	1	FAILURE	2026-01-20 14:38:38.480119+01
148	1	1	FAILURE	2026-01-20 14:39:09.030715+01
149	1	1	SUCCESS	2026-01-20 14:39:12.709307+01
150	1	1	SUCCESS	2026-01-20 14:39:13.100553+01
152	1	2	SUCCESS	2026-01-20 14:40:16.724215+01
153	1	2	FAILURE	2026-01-20 14:40:34.814063+01
154	1	7	FAILURE	2026-01-20 14:40:59.134+01
155	1	7	SUCCESS	2026-01-20 14:41:08.757474+01
156	1	1	FAILURE	2026-01-20 14:44:40.047397+01
157	1	13	SUCCESS	2026-01-20 14:47:11.938924+01
158	1	13	FAILURE	2026-01-20 14:47:17.412963+01
159	1	14	SUCCESS	2026-01-20 14:47:32.746971+01
160	1	14	SUCCESS	2026-01-20 14:47:42.005743+01
162	1	14	FAILURE	2026-01-20 14:47:54.741586+01
164	1	14	SUCCESS	2026-01-20 14:48:16.269725+01
166	1	14	SUCCESS	2026-01-20 14:48:19.645107+01
168	1	14	FAILURE	2026-01-20 14:48:24.845853+01
161	1	14	SUCCESS	2026-01-20 14:47:48.75457+01
163	1	14	SUCCESS	2026-01-20 14:48:06.956772+01
165	1	14	SUCCESS	2026-01-20 14:48:19.387984+01
167	1	14	SUCCESS	2026-01-20 14:48:19.83699+01
169	1	1	FAILURE	2026-01-21 10:04:11.386463+01
170	1	1	SUCCESS	2026-01-21 10:04:40.589651+01
171	1	1	FAILURE	2026-01-21 10:04:52.780433+01
172	1	1	FAILURE	2026-01-21 10:05:09.828903+01
173	1	2	SUCCESS	2026-01-21 10:07:46.975568+01
174	1	2	SUCCESS	2026-01-21 10:08:05.924557+01
175	1	2	FAILURE	2026-01-21 10:08:12.002573+01
176	1	2	FAILURE	2026-01-21 10:09:00.88487+01
177	1	7	SUCCESS	2026-01-21 10:10:29.201855+01
178	1	7	FAILURE	2026-01-21 10:10:37.212408+01
179	1	7	SUCCESS	2026-01-21 10:18:38.679419+01
184	1	13	SUCCESS	2026-01-21 10:23:05.973254+01
185	1	14	SUCCESS	2026-01-21 10:23:29.362198+01
186	1	14	FAILURE	2026-01-21 10:24:00.77773+01
187	1	2	SUCCESS	2026-01-21 15:15:55.68753+01
188	1	2	FAILURE	2026-01-21 16:06:29.623313+01
189	1	2	SUCCESS	2026-01-21 16:06:50.115322+01
190	1	1	SUCCESS	2026-01-21 16:55:41.162668+01
191	1	1	FAILURE	2026-01-21 17:14:51.196799+01
\.


--
-- Data for Name: submission_marker; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.submission_marker (id, submission_id, exercise_file_id, marker_id, content, created_at) FROM stdin;
159	160	32	1	                      return a+b	2026-01-20 14:47:42.005743+01
161	162	32	1	                      return a+bsdvsd	2026-01-20 14:47:54.741586+01
163	164	32	1	   return a+b ;vsvsd	2026-01-20 14:48:16.269725+01
165	166	32	1	   return a+b ;vsvsd	2026-01-20 14:48:19.645107+01
167	168	32	1	   return a+b sdv;vsvsd	2026-01-20 14:48:24.845853+01
168	169	70	"1"	  retur a +b	2026-01-21 10:04:11.386463+01
170	171	70	"1"	  return a +b +8;	2026-01-21 10:04:52.780433+01
176	177	20	a	    int c = a*b;	2026-01-21 10:10:29.201855+01
177	177	20	b	   return c;	2026-01-21 10:10:29.201855+01
183	185	32	1	  return a+b;	2026-01-21 10:23:29.362198+01
186	188	81	1	      // while (i < n && fgets(buffer, 256, f) != NULL) { printf("%s", buffer); i++; }	2026-01-21 16:06:29.623313+01
187	189	81	1	      while (i < n && fgets(buffer, 256, f) != NULL) { printf("%s", buffer); i++; }	2026-01-21 16:06:50.115322+01
188	190	70	"1"	   return a+b;	2026-01-21 16:55:41.162668+01
189	191	70	"1"		2026-01-21 17:14:51.196799+01
51	55	20	a	int t = a *c;	2025-12-18 12:46:46.03278+01
52	55	20	b	return t	2025-12-18 12:46:46.03278+01
53	56	20	a	int t = a *c;	2025-12-18 12:47:09.518229+01
54	56	20	b	return t;	2025-12-18 12:47:09.518229+01
55	57	20	a	int t = a *b;	2025-12-18 12:47:24.185502+01
56	57	20	b	return t;	2025-12-18 12:47:24.185502+01
57	60	20	a		2025-12-18 12:50:07.470694+01
58	60	20	b		2025-12-18 12:50:07.470694+01
59	63	20	a		2025-12-18 12:52:51.247629+01
60	63	20	b		2025-12-18 12:52:51.247629+01
61	64	20	a		2025-12-18 12:53:02.707585+01
62	64	20	b		2025-12-18 12:53:02.707585+01
63	65	20	a		2025-12-18 12:53:10.324951+01
64	65	20	b	;	2025-12-18 12:53:10.324951+01
65	66	20	a		2025-12-18 12:53:20.253092+01
66	66	20	b	;	2025-12-18 12:53:20.253092+01
67	67	20	a		2025-12-18 12:53:33.557195+01
68	67	20	b	zef	2025-12-18 12:53:33.557195+01
69	68	20	a		2025-12-18 12:54:43.959478+01
70	68	20	b	}	2025-12-18 12:54:43.959478+01
90	98	32	1	    return a + b	2026-01-17 16:58:21.705381+01
91	99	32	1	    return a + b;	2026-01-17 16:58:31.972516+01
92	100	32	1	    return a + b;zadaz	2026-01-17 16:58:42.900591+01
93	101	32	1	    return a +	2026-01-17 16:58:56.190457+01
94	102	32	1	    return a + c	2026-01-17 16:59:16.700849+01
95	103	32	1	    return a + b	2026-01-17 16:59:36.017431+01
96	104	32	1	    return a + b + 2	2026-01-17 16:59:40.932614+01
97	105	32	1	return a+b	2026-01-19 09:27:13.438994+01
98	106	32	1	return a+b + a	2026-01-19 09:27:19.213414+01
99	107	32	1	return a+//	2026-01-19 09:27:25.298286+01
100	108	32	1	return a+ ;	2026-01-19 09:27:38.601933+01
101	109	32	1	ert	2026-01-19 09:29:03.968524+01
102	112	32	1	return a +b	2026-01-19 09:29:41.935735+01
158	159	32	1	return a+b	2026-01-20 14:47:32.746971+01
160	161	32	1	                      return a+b;	2026-01-20 14:47:48.75457+01
117	128	20	a	    int c = a*b;	2026-01-20 13:59:12.713875+01
118	128	20	b	    return c;	2026-01-20 13:59:12.713875+01
119	129	20	a	    int c = a*b;	2026-01-20 13:59:20.89103+01
120	129	20	b	    return b;	2026-01-20 13:59:20.89103+01
121	130	20	a	    int c = a*b;	2026-01-20 13:59:41.254245+01
122	130	20	b	    return b;	2026-01-20 13:59:41.254245+01
123	131	20	a	    int c = a*b;	2026-01-20 13:59:50.021555+01
124	131	20	b	    return b;	2026-01-20 13:59:50.021555+01
125	132	20	a	    int c = a*b;	2026-01-20 13:59:51.117815+01
126	132	20	b	    return b;	2026-01-20 13:59:51.117815+01
127	133	20	a	    int c = a*b;	2026-01-20 13:59:52.180893+01
128	133	20	b	    return b;	2026-01-20 13:59:52.180893+01
129	134	20	a	    int c = a*b;	2026-01-20 14:00:06.203868+01
130	134	20	b	    return a;	2026-01-20 14:00:06.203868+01
162	163	32	1	                      return a+b ;	2026-01-20 14:48:06.956772+01
164	165	32	1	   return a+b ;vsvsd	2026-01-20 14:48:19.387984+01
166	167	32	1	   return a+b ;vsvsd	2026-01-20 14:48:19.83699+01
169	170	70	"1"	  return a +b;	2026-01-21 10:04:40.589651+01
171	172	70	"1"	  return 2;	2026-01-21 10:05:09.828903+01
136	140	20	a	  c = a*b;	2026-01-20 14:30:00.26476+01
137	140	20	b	   return c;	2026-01-20 14:30:00.26476+01
138	141	20	a	  int c = a*b;	2026-01-20 14:30:24.652006+01
139	141	20	b	   return c;	2026-01-20 14:30:24.652006+01
178	178	20	a	    int c = a*b;	2026-01-21 10:10:37.212408+01
179	178	20	b	   return b;	2026-01-21 10:10:37.212408+01
180	179	20	a	 int c = a*b;	2026-01-21 10:18:38.679419+01
181	179	20	b	 return c;	2026-01-21 10:18:38.679419+01
151	154	20	a	  int c = a+b;	2026-01-20 14:40:59.134+01
152	154	20	b	    return c;	2026-01-20 14:40:59.134+01
153	155	20	a	  int c = a*b;	2026-01-20 14:41:08.757474+01
154	155	20	b	    return c;	2026-01-20 14:41:08.757474+01
184	186	32	1	  return a+bsfsdf;	2026-01-21 10:24:00.77773+01
\.


--
-- Data for Name: submission_result; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.submission_result (id, submission_id, test_case_id, status, actual_output, error_log) FROM stdin;
219	128	11	SUCCESS	25	
220	128	12	SUCCESS	2	
357	188	37	FAILURE		
358	188	38	SUCCESS		
359	188	39	FAILURE		
360	188	40	FAILURE		
361	189	37	SUCCESS	Ligne 1 : azerty\nLigne 2 : _-_	
362	189	38	SUCCESS		
363	189	39	SUCCESS	Ligne 1 : azerty\nLigne 2 : _-_\nLigne 3 : *****\nLigne 4 : 123\nLigne 5 : zqsd	
364	189	40	SUCCESS	Ligne 1 : azerty	
365	190	35	SUCCESS	2	
366	190	36	SUCCESS	-1	
367	191	35	FAILURE	1	
368	191	36	SUCCESS	-1	
221	128	13	SUCCESS	10000	
225	130	11	FAILURE	5	
226	130	12	SUCCESS	2	
227	130	13	FAILURE	100	
231	132	11	FAILURE	5	
232	132	12	SUCCESS	2	
233	132	13	FAILURE	100	
237	134	11	FAILURE	5	
238	134	12	FAILURE	1	
239	134	13	FAILURE	100	
246	141	11	SUCCESS	25	
247	141	12	SUCCESS	2	
248	141	13	SUCCESS	10000	
274	154	11	FAILURE	10	
275	154	12	FAILURE	3	
276	154	13	FAILURE	200	
299	162	25	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmp4tng6q3y/main.py", line 12, in <module>\n    c = fonction.addition(a, b)\n  File "/tmp/tmp4tng6q3y/fonction.py", line 2, in addition\n    return a+bsdvsd\nNameError: name 'bsdvsd' is not defined\n
303	164	23	SUCCESS	2	
304	164	24	SUCCESS	60	
305	164	25	SUCCESS	30	
309	166	23	SUCCESS	2	
310	166	24	SUCCESS	60	
311	166	25	SUCCESS	30	
315	168	23	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpdrxaxwii/main.py", line 2, in <module>\n    import fonction  \n  File "/tmp/tmpdrxaxwii/fonction.py", line 2\n    return a+b sdv;vsvsd\n               ^^^\nSyntaxError: invalid syntax\n
316	168	24	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpdrxaxwii/main.py", line 2, in <module>\n    import fonction  \n  File "/tmp/tmpdrxaxwii/fonction.py", line 2\n    return a+b sdv;vsvsd\n               ^^^\nSyntaxError: invalid syntax\n
77	57	11	SUCCESS	25	
78	57	12	SUCCESS	2	
79	57	13	SUCCESS	10000	
80	60	11	FAILURE	5	
81	60	12	FAILURE	1	
82	60	13	FAILURE	100	
83	63	11	FAILURE	5	
84	63	12	FAILURE	1	
85	63	13	FAILURE	100	
86	64	11	FAILURE	5	
87	64	12	FAILURE	1	
88	64	13	FAILURE	100	
89	65	11	FAILURE	5	
90	65	12	FAILURE	1	
91	65	13	FAILURE	100	
92	66	11	FAILURE	5	
93	66	12	FAILURE	1	
94	66	13	FAILURE	100	
222	129	11	FAILURE	5	
223	129	12	SUCCESS	2	
224	129	13	FAILURE	100	
228	131	11	FAILURE	5	
229	131	12	SUCCESS	2	
230	131	13	FAILURE	100	
234	133	11	FAILURE	5	
235	133	12	SUCCESS	2	
236	133	13	FAILURE	100	
277	155	11	SUCCESS	25	
278	155	12	SUCCESS	2	
279	155	13	SUCCESS	10000	
317	168	25	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpdrxaxwii/main.py", line 2, in <module>\n    import fonction  \n  File "/tmp/tmpdrxaxwii/fonction.py", line 2\n    return a+b sdv;vsvsd\n               ^^^\nSyntaxError: invalid syntax\n
339	178	11	FAILURE	5	
340	178	12	SUCCESS	2	
341	178	13	FAILURE	100	
342	179	11	SUCCESS	25	
343	179	12	SUCCESS	2	
344	179	13	SUCCESS	10000	
291	160	23	SUCCESS	2	
292	160	24	SUCCESS	60	
293	160	25	SUCCESS	30	
297	162	23	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmp4tng6q3y/main.py", line 12, in <module>\n    c = fonction.addition(a, b)\n  File "/tmp/tmp4tng6q3y/fonction.py", line 2, in addition\n    return a+bsdvsd\nNameError: name 'bsdvsd' is not defined\n
298	162	24	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmp4tng6q3y/main.py", line 12, in <module>\n    c = fonction.addition(a, b)\n  File "/tmp/tmp4tng6q3y/fonction.py", line 2, in addition\n    return a+bsdvsd\nNameError: name 'bsdvsd' is not defined\n
318	170	35	SUCCESS	2	
319	170	36	SUCCESS	-1	
322	172	35	SUCCESS	2	
323	172	36	FAILURE	2	
154	98	23	SUCCESS	2	
155	98	24	SUCCESS	60	
156	98	25	SUCCESS	30	
157	99	23	SUCCESS	2	
158	99	24	SUCCESS	60	
159	99	25	SUCCESS	30	
160	100	23	SUCCESS	2	
161	100	24	SUCCESS	60	
162	100	25	SUCCESS	30	
163	101	23	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmph7000jof/main.py", line 2, in <module>\n    import fonction  \n  File "/tmp/tmph7000jof/fonction.py", line 2\n    return a +\n              ^\nSyntaxError: invalid syntax\n
164	101	24	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmph7000jof/main.py", line 2, in <module>\n    import fonction  \n  File "/tmp/tmph7000jof/fonction.py", line 2\n    return a +\n              ^\nSyntaxError: invalid syntax\n
165	101	25	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmph7000jof/main.py", line 2, in <module>\n    import fonction  \n  File "/tmp/tmph7000jof/fonction.py", line 2\n    return a +\n              ^\nSyntaxError: invalid syntax\n
166	102	23	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpvoe_suni/main.py", line 12, in <module>\n    c = fonction.addition(a, b)\n  File "/tmp/tmpvoe_suni/fonction.py", line 2, in addition\n    return a + c\nNameError: name 'c' is not defined\n
167	102	24	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpvoe_suni/main.py", line 12, in <module>\n    c = fonction.addition(a, b)\n  File "/tmp/tmpvoe_suni/fonction.py", line 2, in addition\n    return a + c\nNameError: name 'c' is not defined\n
168	102	25	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpvoe_suni/main.py", line 12, in <module>\n    c = fonction.addition(a, b)\n  File "/tmp/tmpvoe_suni/fonction.py", line 2, in addition\n    return a + c\nNameError: name 'c' is not defined\n
169	103	23	SUCCESS	2	
170	103	24	SUCCESS	60	
171	103	25	SUCCESS	30	
172	104	23	FAILURE	4	
173	104	24	FAILURE	62	
174	104	25	FAILURE	32	
175	105	23	SUCCESS	2	
176	105	24	SUCCESS	60	
177	105	25	SUCCESS	30	
178	106	23	FAILURE	3	
179	106	24	FAILURE	110	
180	106	25	FAILURE	110	
181	107	23	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpc4u7i9h4/main.py", line 2, in <module>\n    import fonction  \n  File "/tmp/tmpc4u7i9h4/fonction.py", line 2\n    return a+//\n             ^^\nSyntaxError: invalid syntax\n
182	107	24	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpc4u7i9h4/main.py", line 2, in <module>\n    import fonction  \n  File "/tmp/tmpc4u7i9h4/fonction.py", line 2\n    return a+//\n             ^^\nSyntaxError: invalid syntax\n
183	107	25	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpc4u7i9h4/main.py", line 2, in <module>\n    import fonction  \n  File "/tmp/tmpc4u7i9h4/fonction.py", line 2\n    return a+//\n             ^^\nSyntaxError: invalid syntax\n
184	108	23	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpkr0q19wp/main.py", line 2, in <module>\n    import fonction  \n  File "/tmp/tmpkr0q19wp/fonction.py", line 2\n    return a+ ;\n              ^\nSyntaxError: invalid syntax\n
185	108	24	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpkr0q19wp/main.py", line 2, in <module>\n    import fonction  \n  File "/tmp/tmpkr0q19wp/fonction.py", line 2\n    return a+ ;\n              ^\nSyntaxError: invalid syntax\n
186	108	25	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpkr0q19wp/main.py", line 2, in <module>\n    import fonction  \n  File "/tmp/tmpkr0q19wp/fonction.py", line 2\n    return a+ ;\n              ^\nSyntaxError: invalid syntax\n
187	109	23	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpganb9a9i/main.py", line 12, in <module>\n    c = fonction.addition(a, b)\n  File "/tmp/tmpganb9a9i/fonction.py", line 2, in addition\n    ert\nNameError: name 'ert' is not defined\n
188	109	24	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpganb9a9i/main.py", line 12, in <module>\n    c = fonction.addition(a, b)\n  File "/tmp/tmpganb9a9i/fonction.py", line 2, in addition\n    ert\nNameError: name 'ert' is not defined\n
189	109	25	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpganb9a9i/main.py", line 12, in <module>\n    c = fonction.addition(a, b)\n  File "/tmp/tmpganb9a9i/fonction.py", line 2, in addition\n    ert\nNameError: name 'ert' is not defined\n
190	112	23	SUCCESS	2	
191	112	24	SUCCESS	60	
192	112	25	SUCCESS	30	
288	159	23	SUCCESS	2	
289	159	24	SUCCESS	60	
290	159	25	SUCCESS	30	
294	161	23	SUCCESS	2	
295	161	24	SUCCESS	60	
296	161	25	SUCCESS	30	
300	163	23	SUCCESS	2	
301	163	24	SUCCESS	60	
302	163	25	SUCCESS	30	
306	165	23	SUCCESS	2	
307	165	24	SUCCESS	60	
308	165	25	SUCCESS	30	
312	167	23	SUCCESS	2	
313	167	24	SUCCESS	60	
314	167	25	SUCCESS	30	
320	171	35	FAILURE	10	
321	171	36	FAILURE	7	
336	177	11	SUCCESS	25	
337	177	12	SUCCESS	2	
338	177	13	SUCCESS	10000	
348	185	23	SUCCESS	2	
349	185	24	SUCCESS	60	
350	185	25	SUCCESS	30	
351	186	23	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpm5g6_szk/main.py", line 12, in <module>\n    c = fonction.addition(a, b)\n  File "/tmp/tmpm5g6_szk/fonction.py", line 2, in addition\n    return a+bsfsdf;\nNameError: name 'bsfsdf' is not defined\n
352	186	24	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpm5g6_szk/main.py", line 12, in <module>\n    c = fonction.addition(a, b)\n  File "/tmp/tmpm5g6_szk/fonction.py", line 2, in addition\n    return a+bsfsdf;\nNameError: name 'bsfsdf' is not defined\n
353	186	25	FAILURE		Traceback (most recent call last):\n  File "/tmp/tmpm5g6_szk/main.py", line 12, in <module>\n    c = fonction.addition(a, b)\n  File "/tmp/tmpm5g6_szk/fonction.py", line 2, in addition\n    return a+bsfsdf;\nNameError: name 'bsfsdf' is not defined\n
\.


--
-- Data for Name: test_case; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.test_case (id, exercise_id, argv, expected_output, "position", comment) FROM stdin;
8	6	5 5	25	0	
9	6	1 2	2	1	
10	6	100 100	10000	2	
11	7	5 5	25	0	
12	7	1 2	2	1	
13	7	100 100	10000	2	
23	14	1 1	2	0	
24	14	50 10	60	1	
25	14	80 -50	30	2	
35	1	1 1	2	0	
36	1	-1 0	-1	1	
37	2	2	Ligne 1 : azerty\nLigne 2 : _-_	0	
38	2	0		1	
39	2	5	Ligne 1 : azerty\nLigne 2 : _-_\nLigne 3 : *****\nLigne 4 : 123\nLigne 5 : zqsd	2	
40	2	1	Ligne 1 : azerty	3	
41	13	10 5	15	0	
42	13	-50 50	0	1	
43	13	895 105	1000	2	
44	13	1 1	2	3	
\.


--
-- Data for Name: unit; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.unit (id, name, description, author_id, visibility, difficulty, created_at) FROM stdin;
3	Module Python	Apprentissage du langage Python	1	PUBLIC	1	2026-01-17 16:54:29.121389+01
2	Module Java 	Apprentissage du langage Java 	1	PUBLIC	1	2026-01-17 15:55:50.258126+01
1	Module C 	Apprentissage du langage C	1	PUBLIC	4	2025-12-06 16:40:03.414646+01
7	Démo module	démo démo 2	1	PUBLIC	1	2026-01-22 13:44:00.599255+01
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."user" (id, firstname, lastname, email, mdp_hash, role, created_at) FROM stdin;
1	Khalil	Mehalli	khalilmehalli@gmail.com	hash_temporaire	TEACHER	2025-12-06 16:38:46.435262+01
\.


--
-- Name: course_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.course_id_seq', 14, true);


--
-- Name: exercise_file_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.exercise_file_id_seq', 90, true);


--
-- Name: exercise_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.exercise_id_seq', 18, true);


--
-- Name: exercise_marker_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.exercise_marker_id_seq', 19, true);


--
-- Name: exercise_progress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.exercise_progress_id_seq', 6, true);


--
-- Name: hint_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.hint_id_seq', 36, true);


--
-- Name: hint_view_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.hint_view_id_seq', 1, false);


--
-- Name: submission_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.submission_history_id_seq', 191, true);


--
-- Name: submission_marker_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.submission_marker_id_seq', 189, true);


--
-- Name: submission_result_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.submission_result_id_seq', 368, true);


--
-- Name: test_case_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.test_case_id_seq', 44, true);


--
-- Name: unit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.unit_id_seq', 7, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_id_seq', 1, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: course course_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course
    ADD CONSTRAINT course_pkey PRIMARY KEY (id);


--
-- Name: exercise_file exercise_file_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_file
    ADD CONSTRAINT exercise_file_pkey PRIMARY KEY (id);


--
-- Name: exercise_marker exercise_marker_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_marker
    ADD CONSTRAINT exercise_marker_pkey PRIMARY KEY (id);


--
-- Name: exercise exercise_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise
    ADD CONSTRAINT exercise_pkey PRIMARY KEY (id);


--
-- Name: exercise_progress exercise_progress_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_progress
    ADD CONSTRAINT exercise_progress_pkey PRIMARY KEY (id);


--
-- Name: hint hint_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hint
    ADD CONSTRAINT hint_pkey PRIMARY KEY (id);


--
-- Name: hint_view hint_view_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hint_view
    ADD CONSTRAINT hint_view_pkey PRIMARY KEY (id);


--
-- Name: submission_history submission_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.submission_history
    ADD CONSTRAINT submission_history_pkey PRIMARY KEY (id);


--
-- Name: submission_marker submission_marker_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.submission_marker
    ADD CONSTRAINT submission_marker_pkey PRIMARY KEY (id);


--
-- Name: submission_result submission_result_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.submission_result
    ADD CONSTRAINT submission_result_pkey PRIMARY KEY (id);


--
-- Name: test_case test_case_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.test_case
    ADD CONSTRAINT test_case_pkey PRIMARY KEY (id);


--
-- Name: exercise_marker unique_marker_per_file; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_marker
    ADD CONSTRAINT unique_marker_per_file UNIQUE (exercise_file_id, marker_id);


--
-- Name: unit unit_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.unit
    ADD CONSTRAINT unit_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: ix_course_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_course_id ON public.course USING btree (id);


--
-- Name: ix_exercise_file_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_exercise_file_id ON public.exercise_file USING btree (id);


--
-- Name: ix_exercise_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_exercise_id ON public.exercise USING btree (id);


--
-- Name: ix_exercise_marker_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_exercise_marker_id ON public.exercise_marker USING btree (id);


--
-- Name: ix_exercise_progress_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_exercise_progress_id ON public.exercise_progress USING btree (id);


--
-- Name: ix_hint_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_hint_id ON public.hint USING btree (id);


--
-- Name: ix_hint_view_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_hint_view_id ON public.hint_view USING btree (id);


--
-- Name: ix_submission_history_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_submission_history_id ON public.submission_history USING btree (id);


--
-- Name: ix_submission_marker_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_submission_marker_id ON public.submission_marker USING btree (id);


--
-- Name: ix_submission_result_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_submission_result_id ON public.submission_result USING btree (id);


--
-- Name: ix_test_case_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_test_case_id ON public.test_case USING btree (id);


--
-- Name: ix_unit_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_unit_id ON public.unit USING btree (id);


--
-- Name: ix_user_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);


--
-- Name: ix_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_id ON public."user" USING btree (id);


--
-- Name: course course_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course
    ADD CONSTRAINT course_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.unit(id) ON DELETE CASCADE;


--
-- Name: exercise exercise_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise
    ADD CONSTRAINT exercise_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.course(id) ON DELETE CASCADE;


--
-- Name: exercise_file exercise_file_exercise_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_file
    ADD CONSTRAINT exercise_file_exercise_id_fkey FOREIGN KEY (exercise_id) REFERENCES public.exercise(id) ON DELETE CASCADE;


--
-- Name: exercise_marker exercise_marker_exercise_file_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_marker
    ADD CONSTRAINT exercise_marker_exercise_file_id_fkey FOREIGN KEY (exercise_file_id) REFERENCES public.exercise_file(id) ON DELETE CASCADE;


--
-- Name: exercise_progress exercise_progress_exercise_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_progress
    ADD CONSTRAINT exercise_progress_exercise_id_fkey FOREIGN KEY (exercise_id) REFERENCES public.exercise(id) ON DELETE CASCADE;


--
-- Name: exercise_progress exercise_progress_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_progress
    ADD CONSTRAINT exercise_progress_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: hint hint_exercise_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hint
    ADD CONSTRAINT hint_exercise_id_fkey FOREIGN KEY (exercise_id) REFERENCES public.exercise(id) ON DELETE CASCADE;


--
-- Name: hint_view hint_view_hint_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hint_view
    ADD CONSTRAINT hint_view_hint_id_fkey FOREIGN KEY (hint_id) REFERENCES public.hint(id) ON DELETE CASCADE;


--
-- Name: hint_view hint_view_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hint_view
    ADD CONSTRAINT hint_view_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: submission_history submission_history_exercise_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.submission_history
    ADD CONSTRAINT submission_history_exercise_id_fkey FOREIGN KEY (exercise_id) REFERENCES public.exercise(id) ON DELETE CASCADE;


--
-- Name: submission_history submission_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.submission_history
    ADD CONSTRAINT submission_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: submission_marker submission_marker_exercise_file_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.submission_marker
    ADD CONSTRAINT submission_marker_exercise_file_id_fkey FOREIGN KEY (exercise_file_id) REFERENCES public.exercise_file(id) ON DELETE CASCADE;


--
-- Name: submission_marker submission_marker_submission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.submission_marker
    ADD CONSTRAINT submission_marker_submission_id_fkey FOREIGN KEY (submission_id) REFERENCES public.submission_history(id) ON DELETE CASCADE;


--
-- Name: submission_result submission_result_submission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.submission_result
    ADD CONSTRAINT submission_result_submission_id_fkey FOREIGN KEY (submission_id) REFERENCES public.submission_history(id) ON DELETE CASCADE;


--
-- Name: submission_result submission_result_test_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.submission_result
    ADD CONSTRAINT submission_result_test_case_id_fkey FOREIGN KEY (test_case_id) REFERENCES public.test_case(id) ON DELETE CASCADE;


--
-- Name: test_case test_case_exercise_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.test_case
    ADD CONSTRAINT test_case_exercise_id_fkey FOREIGN KEY (exercise_id) REFERENCES public.exercise(id) ON DELETE CASCADE;


--
-- Name: unit unit_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.unit
    ADD CONSTRAINT unit_author_id_fkey FOREIGN KEY (author_id) REFERENCES public."user"(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

\unrestrict MckzwsTn4xhsRFqr6lw7L6fTGShW35nl7FvRXVWMDVr5vM6AMT9qQn5IUsu7qZy

