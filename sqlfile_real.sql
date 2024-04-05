--
-- PostgreSQL database dump
--

-- Dumped from database version 13.12 (Debian 13.12-1.pgdg120+1)
-- Dumped by pg_dump version 15.4

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
-- Name: public; Type: SCHEMA; Schema: -; Owner: user
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO "user";

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Orders; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."Orders" (
    "ID_order" uuid NOT NULL,
    "ID_user" uuid,
    "ID_product" uuid,
    "Quantity" integer,
    "Date" timestamp without time zone
);


ALTER TABLE public."Orders" OWNER TO "user";

--
-- Name: Products; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."Products" (
    "ID" uuid NOT NULL,
    "Name" character varying,
    "Price" double precision,
    "Description" character varying,
    "Quantity" integer,
    "Image" character varying,
    "Icons" character varying
);


ALTER TABLE public."Products" OWNER TO "user";

--
-- Name: User_Cart; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."User_Cart" (
    "ID_user" uuid NOT NULL,
    "ID_product" uuid NOT NULL,
    "Quantity" integer
);


ALTER TABLE public."User_Cart" OWNER TO "user";

--
-- Name: User_Data_Invoicing; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."User_Data_Invoicing" (
    "ID" uuid NOT NULL,
    "User_ID" uuid,
    "Name" character varying,
    "Last_Name" character varying,
    "CF" character varying,
    "Address" character varying,
    "Billing_Address" character varying
);


ALTER TABLE public."User_Data_Invoicing" OWNER TO "user";

--
-- Name: Users; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."Users" (
    "ID" uuid NOT NULL,
    "Username" character varying,
    "Pass" character varying
);


ALTER TABLE public."Users" OWNER TO "user";

--
-- Data for Name: Orders; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public."Orders" ("ID_order", "ID_user", "ID_product", "Quantity", "Date") FROM stdin;
053f6df4-3d49-4d8a-9679-eebe9d0ee494	34bd8a5f-1ff5-404b-9791-1d58ded5862d	d02b03e5-3ee2-445f-ba46-bb6c4198d24d	1	2024-04-04 16:33:01.563068
e5f49ea4-0749-4ec2-9223-ce4e8dfb5200	34bd8a5f-1ff5-404b-9791-1d58ded5862d	d02b03e5-3ee2-445f-ba46-bb6c4198d24d	1	2024-04-04 16:36:41.138147
d1372875-7dd3-4ccd-9a72-558a25f69bbe	34bd8a5f-1ff5-404b-9791-1d58ded5862d	d02b03e5-3ee2-445f-ba46-bb6c4198d24d	1	2024-04-04 16:37:13.49639
9795336e-603f-4f02-b8d6-ee2e042bc9a6	34bd8a5f-1ff5-404b-9791-1d58ded5862d	d02b03e5-3ee2-445f-ba46-bb6c4198d24d	1	2024-04-04 16:38:41.466235
eb4b3ec0-bdd4-4478-96ac-15a0ab0cf530	34bd8a5f-1ff5-404b-9791-1d58ded5862d	d02b03e5-3ee2-445f-ba46-bb6c4198d24d	1	2024-04-04 16:46:02.482347
2d6576b0-8336-4399-b8a8-3f49c795e699	34bd8a5f-1ff5-404b-9791-1d58ded5862d	d02b03e5-3ee2-445f-ba46-bb6c4198d24d	1	2024-04-04 16:46:34.777416
4359cbdd-1c55-4f4b-98cf-bba8be6ef9bd	34bd8a5f-1ff5-404b-9791-1d58ded5862d	d02b03e5-3ee2-445f-ba46-bb6c4198d24d	2	2024-04-04 16:49:33.095415
46868f27-b23d-4f2b-a589-81c350c1f81d	34bd8a5f-1ff5-404b-9791-1d58ded5862d	d02b03e5-3ee2-445f-ba46-bb6c4198d24d	9	2024-04-05 09:11:29.03956
83d5ec3a-c700-4294-8bf6-a6b7d59de90e	34bd8a5f-1ff5-404b-9791-1d58ded5862d	67c251dc-a082-4314-9f01-db70702aa1a2	1	2024-04-05 15:42:45.413783
\.


--
-- Data for Name: Products; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public."Products" ("ID", "Name", "Price", "Description", "Quantity", "Image", "Icons") FROM stdin;
67c251dc-a082-4314-9f01-db70702aa1a2	Sciarpa	13.99	Sciarpa a quadri	8	images/sciarpa a quadri.jpeg	icons/squared scarf icon.jpg
cfdf55a8-0ee3-4da2-a0f9-5ccf722dee27	Pantaloni	10.5	Pantaloni beige	10	images/pantaloni beige.jpeg	icons/beige trousers icon.jpg
d02b03e5-3ee2-445f-ba46-bb6c4198d24d	Scarpe	11	Scarpe nere	5	images/scarpe.jpg	icons/shoe icon.jpg
f9e7316a-9c78-407b-bd3b-75119ef51321	Jeans	19.99	Jeans blu	4	images/jeans blu.jpeg	icons/jeans icon.jpg
\.


--
-- Data for Name: User_Cart; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public."User_Cart" ("ID_user", "ID_product", "Quantity") FROM stdin;
\.


--
-- Data for Name: User_Data_Invoicing; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public."User_Data_Invoicing" ("ID", "User_ID", "Name", "Last_Name", "CF", "Address", "Billing_Address") FROM stdin;
\.


--
-- Data for Name: Users; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public."Users" ("ID", "Username", "Pass") FROM stdin;
34bd8a5f-1ff5-404b-9791-1d58ded5862d	TheVoyager	ironclad2
909b029b-ad81-44d1-b596-7115e7914619	Ad.Str	gkesitD
\.


--
-- Name: User_Cart Carrello_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."User_Cart"
    ADD CONSTRAINT "Carrello_pkey" PRIMARY KEY ("ID_user", "ID_product");


--
-- Name: Orders Ordinit_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."Orders"
    ADD CONSTRAINT "Ordinit_pkey" PRIMARY KEY ("ID_order");


--
-- Name: Products Prodotti_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."Products"
    ADD CONSTRAINT "Prodotti_pkey" PRIMARY KEY ("ID");


--
-- Name: User_Data_Invoicing User_Data_Invoicing_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."User_Data_Invoicing"
    ADD CONSTRAINT "User_Data_Invoicing_pkey" PRIMARY KEY ("ID");


--
-- Name: Users Utenti_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Utenti_pkey" PRIMARY KEY ("ID");


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: user
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

