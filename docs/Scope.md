	# FLARE AI

> **Multi-Agent Scientific Intelligence Platform**\
> Transformer les recherches de la NASA sur la combustion en
> microgravité en connaissances scientifiques exploitables pour
> améliorer la sécurité incendie des futures missions spatiales.

## 1. Présentation

FLARE AI est une plateforme de recherche scientifique assistée par IA,
construite autour d'un **dashboard interactif** et d'une architecture
**multi-agents**.

Elle aide les chercheurs à explorer les expériences de combustion de la
NASA, comprendre leurs résultats, comparer les études et produire des
analyses traçables.

**Objectif principal :** résumer, classer et interpréter les résultats
de recherche afin de faire émerger des enseignements utiles à la
sécurité incendie dans les habitats spatiaux.

> L'architecture multi-agents est notre approche technique. Le dashboard
> interactif et l'analyse des résultats restent au cœur du défi NASA.
> FLARE AI est un outil d'aide à la recherche, pas un système certifié
> de prévention incendie.

## 2. Fonctionnalités principales

-   Explorer et rechercher les expériences NASA liées à la combustion en
    microgravité.
-   Extraire, nettoyer et structurer les données scientifiques
    disponibles.
-   Poser des questions à un assistant de recherche IA.
-   Analyser et comparer plusieurs expériences.
-   Produire des classements transparents et des rapports avec sources.
-   Suivre les agents, leurs tâches, leur progression et leurs résultats
    depuis le dashboard.

## 3. Architecture multi-agents

Un **Orchestrateur FLARE** reçoit la demande, planifie le travail,
distribue les tâches aux agents, vérifie leurs résultats et rassemble la
réponse.

  ---------------------------------------------------------------------
  Agent                              Responsabilité
  ---------------------------------- ----------------------------------
  Research Agent                     Rechercher les expériences,
                                     publications et données NASA
                                     pertinentes.

  Data Agent                         Extraire, nettoyer, normaliser et
                                     structurer les données sans
                                     inventer les valeurs manquantes.

  Scientific Analysis Agent          Effectuer les analyses numériques
                                     et interpréter les résultats avec
                                     prudence.

  Comparison & Ranking Agent         Comparer les expériences et
                                     classer les résultats selon des
                                     critères explicites.

  Report & Insight Agent             Générer des synthèses, rapports et
                                     enseignements avec références.
  ---------------------------------------------------------------------

Les calculs et classements doivent être vérifiables et réalisés par des
fonctions déterministes lorsque c'est possible. Chaque affirmation
scientifique doit être reliée à une source identifiable.

## 4. Dashboard

1.  **Overview** --- indicateurs, recherches récentes et activité des
    agents.
2.  **NASA Research Explorer** --- recherche, filtres et fiches des
    expériences.
3.  **Agent Control Center** --- tâches, progression, historique et
    erreurs.
4.  **AI Research Assistant** --- questions en langage naturel et
    réponses sourcées.
5.  **Comparison & Analytics** --- comparaisons, classements et
    graphiques.
6.  **Reports & Mission Insights** --- rapports, conclusions et
    implications pour les missions spatiales.

## 5. Technologies envisagées

  Partie           Technologies
  ---------------- ----------------------------------------------------
  Frontend         Next.js, React, TypeScript, Tailwind CSS, Recharts
  Backend          Python, FastAPI, Pydantic
  Orchestration    LangGraph
  IA & recherche   LLM, RAG, embeddings
  Données          Pandas, NumPy, PostgreSQL, FAISS ou pgvector
  Qualité          Pytest

Le choix final des outils peut être adapté au temps disponible et aux
ressources accessibles pendant le hackathon.

## 6. Répartition de l'équipe

### Membre 1 --- NASA Data & Scientific Research

-   Étudier les ressources NASA PSI et sélectionner les expériences
    pertinentes (ex. BASS, FLEX, SAFFIRE, ACME).
-   Collecter les publications, métadonnées et jeux de données
    disponibles.
-   Nettoyer et structurer les données, conserver les références et
    documenter les variables.
-   Développer le Research Agent, le Data Agent et les tests de
    validation.

**Livrables :** base de connaissances NASA, données structurées, deux
agents et documentation des sources.

### Membre 2 --- Agentic AI & Backend

-   Construire l'API FastAPI, les modèles de données et les endpoints.
-   Développer l'Orchestrateur FLARE et les workflows LangGraph.
-   Développer les agents Scientific Analysis, Comparison & Ranking et
    Report & Insight.
-   Intégrer le RAG, les outils d'analyse, la gestion des erreurs et les
    tests.

**Livrables :** backend, orchestrateur, workflows, agents d'analyse et
API documentée.

### Membre 3 --- Frontend & Integration

-   Concevoir l'identité visuelle et l'expérience utilisateur.
-   Développer les six sections du dashboard.
-   Créer l'interface de chat, le suivi des agents, les graphiques et
    l'affichage des sources.
-   Connecter le frontend à l'API, tester les parcours et préparer la
    démonstration.

**Livrables :** dashboard responsive, visualisations, interface
assistant et intégration frontend/backend.

### Travail commun

Tous les membres participent à la validation scientifique, à
l'intégration, aux tests finaux, à la présentation et à la préparation
de la soumission NASA.

## 7. Workflow principal

Exemple de demande :

> « Compare les expériences NASA sur l'extinction des flammes en
> microgravité et analyse leur pertinence pour la sécurité incendie d'un
> habitat lunaire. »

**Parcours :** Orchestrateur → Research Agent → Data Agent → Scientific
Analysis Agent → Comparison & Ranking Agent → Report & Insight Agent →
Dashboard.

Les étapes et les sources utilisées doivent rester consultables.

## 8. Structure du projet

``` text
FLARE-AI/
├── frontend/
│   ├── app/
│   ├── components/
│   └── services/
├── backend/
│   └── app/
│       ├── api/
│       ├── agents/
│       ├── workflows/
│       ├── tools/
│       ├── services/
│       ├── models/
│       ├── database/
│       └── main.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── metadata/
├── docs/
├── tests/
├── .env.example
└── README.md
```

## 9. Plan de réalisation

1.  **Fondation scientifique :** identifier les expériences et
    constituer un petit jeu de données fiable.
2.  **Agents :** développer la recherche, l'extraction et l'analyse.
3.  **Orchestration :** créer un workflow complet avec LangGraph.
4.  **Dashboard :** construire l'explorateur, l'assistant et le suivi
    des agents.
5.  **Intégration :** tester les résultats, les références, les
    visualisations et la démonstration.

### Priorités MVP

-   Un explorateur NASA fonctionnel avec des données vérifiées.
-   Un orchestrateur et au minimum trois agents opérationnels :
    Research, Scientific Analysis et Report.
-   Un workflow de recherche de bout en bout.
-   Un dashboard affichant résultats, sources et progression des agents.

## 10. Fiabilité scientifique

-   Ne jamais inventer une donnée ou une référence.
-   Signaler explicitement les données manquantes et les limites.
-   Distinguer les observations NASA des interprétations générées par
    l'IA.
-   Expliquer les critères de comparaison et de classement.
-   Conserver la traçabilité des sources et des étapes d'analyse.
-   Présenter FLARE AI comme un outil d'aide à la recherche, jamais
    comme une autorité de sécurité.

## 11. Sources de départ

-   [NASA Space Apps --- Flame in
    Freefall](https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/)
-   [NASA --- PSI Investigations by Research
    Area](https://www.nasa.gov/physical-sciences-informatics-psi/psi-investigations-by-research-area/)
-   [NASA --- Combustion
    Science](https://www.nasa.gov/glenn/glenn-expertise-space-exploration/physical-sciences-program/combustion-science/)
-   [NASA --- Researcher's Guide to
    PSI](https://www.nasa.gov/science-research/for-researchers/researchers-guide-to-physical-sciences-informatics-system/)

## 12. Sponsors & ressources

À compléter lorsque les accès, crédits ou ressources des sponsors seront
confirmés.

  Sponsor       Crédits / ressources   Accès         Utilisation prévue
  ------------- ---------------------- ------------- --------------------
  À compléter   À confirmer            À confirmer   À définir
