# 💳 FlowPay — Projet Analytics Engineering

Pipeline de données complète pour une plateforme de paiement fictive (type Stripe / Payplug) — de la génération des données brutes jusqu'au dashboard financier, en passant par la modélisation dbt et Snowflake.

**Auteure :** [Dyhia Rehoune](https://www.linkedin.com/in/dyhia-rehoune) | **GitHub :** [d-rehoune/saas_finance_project](https://github.com/d-rehoune/saas_finance_project)

---

## 🎯 Contexte métier

**FlowPay** est une solution de paiement pour e-commerçants (boutiques Shopify, Etsy, etc.) qui leur permet d'encaisser leurs clients et de gérer leur trésorerie.

FlowPay propose 3 plans tarifaires :

| Plan | Frais fixes | Commission | Cible |
|------|-------------|------------|-------|
| Essential | 0€ / mois | 2.9% + 0.30€ | Petits vendeurs |
| Business | 49€ / mois | 1.5% + 0.15€ | Boutiques établies |
| Custom | 299€ / mois | 0.8% | Grosses enseignes |

### Métriques clés suivies

- **GMV (Gross Merchandise Volume)** — montant total des ventes transitant par la plateforme
- **Net Take Rate** — pourcentage que FlowPay conserve après commissions bancaires
- **Default Rate** — taux de transactions frauduleuses ou en chargeback
- **LTV (Lifetime Value)** — valeur cumulée générée par chaque boutique dans le temps
- **ARPU (Average Revenue Per User)** — revenu moyen mensuel par boutique

---

## 🏗️ Architecture

```
Python (génération)
        │
        ▼
   seeds/ (CSV)
        │
        ▼
  Snowflake RAW
        │
        ▼
   dbt staging        ← nettoyage, typage, renommage
        │
        ▼
dbt intermediate      ← jointures, agrégations mensuelles, cycle de vie client
        │
        ▼
    dbt marts         ← métriques finales (revenue, chargeback, ltv)
        │
        ▼
    Power BI          ← dashboard cockpit FlowPay
```

---

## 🛠️ Stack technique

| Outil | Rôle |
|-------|------|
| Python + Pandas | Génération des données simulées |
| Snowflake | Data Warehouse |
| dbt (dbt-snowflake) | Transformation et modélisation |
| dbt_utils | Utilitaires dbt (date_spine) |
| Git / GitHub | Versioning |
| Power BI | Visualisation |

---

## 📁 Structure du projet

```
saas_finance_project/
│
├── seeds/                          # Données brutes (CSV)
│   ├── raw_customers.csv           # 150 boutiques e-commerce
│   ├── raw_subscriptions.csv       # Contrats FlowPay
│   └── raw_transactions.csv        # ~643 000 transactions (non versionné)
│
├── models/
│   ├── staging/                    # Matérialisés en views
│   │   ├── _stg_sources.yml        # Déclaration des sources RAW
│   │   ├── _stg_tests.yml          # Tests de qualité staging
│   │   ├── stg_customers.sql
│   │   ├── stg_subscriptions.sql
│   │   ├── stg_transactions.sql
│   │   └── stg_calendar.sql
│   │
│   ├── intermediate/               # Matérialisés en tables
│   │   ├── int_transactions_enriched.sql
│   │   ├── int_monthly_revenue.sql
│   │   └── int_customer_activity.sql
│   │
│   └── marts/                      # Matérialisés en tables
│       ├── _marts_tests.yml         # Tests de qualité marts
│       ├── mart_revenue.sql
│       ├── mart_chargeback.sql
│       └── mart_ltv.sql
│
├── generate_saas_data.py           # Script de génération des données
├── packages.yml                    # Dépendances dbt
├── dbt_project.yml                 # Configuration dbt
└── README.md
```

---

## 📊 Modèles dbt

### Staging
Nettoyage et typage des données brutes. Matérialisés en **views**.

| Modèle | Description |
|--------|-------------|
| `stg_customers` | Boutiques e-commerce avec typage des dates |
| `stg_subscriptions` | Contrats FlowPay avec taux de commission |
| `stg_transactions` | Transactions avec flags (is_success, is_chargeback) |
| `stg_calendar` | Table calendrier jour par jour (2024 → 2026) |

### Intermediate
Jointures et agrégations complexes. Matérialisés en **tables**.

| Modèle | Description |
|--------|-------------|
| `int_transactions_enriched` | Jointure centrale : transactions + client + abonnement |
| `int_monthly_revenue` | Agrégation mensuelle du revenu par boutique |
| `int_customer_activity` | Cycle de vie et historique cumulé par boutique |

### Marts
Métriques finales prêtes pour le dashboard. Matérialisés en **tables**.

| Modèle | Métriques clés |
|--------|----------------|
| `mart_revenue` | GMV, Net Take Rate, revenu transactionnel + abonnement |
| `mart_chargeback` | Default Rate, chargeback impact, pertes par boutique |
| `mart_ltv` | LTV cumulative, ARPU, tenure, Negative Churn |

---

## 🧪 Tests dbt

27 tests automatisés couvrant :

- Unicité des clés primaires (`unique`)
- Absence de valeurs nulles (`not_null`)
- Intégrité référentielle entre tables (`relationships`)
- Valeurs acceptées pour les colonnes catégorielles (`accepted_values`)

```bash
dbt test
# Done. PASS=27 WARN=0 ERROR=0
```

---

## 🚀 Reproduire le projet

### Prérequis

- Python 3.9+
- Un compte Snowflake
- dbt-snowflake installé (`pip install dbt-snowflake`)

### Étapes

```bash
# 1. Cloner le repo
git clone https://github.com/d-rehoune/saas_finance_project.git
cd saas_finance_project

# 2. Générer les données
python generate_saas_data.py

# 3. Configurer le profil dbt (~/.dbt/profiles.yml)
# Renseigner les credentials Snowflake

# 4. Installer les packages dbt
dbt deps

# 5. Charger les seeds dans Snowflake
dbt seed

# 6. Lancer les transformations
dbt run

# 7. Vérifier la qualité des données
dbt test
```

---

## 📈 Dashboard Power BI

*Screenshot à venir*

Le dashboard expose les métriques suivantes :
- Évolution du GMV mensuel par plan
- Net Take Rate par boutique
- Taux de chargeback et impact sur le revenu net
- Courbes de LTV et Negative Churn

---

## 💡 Points forts du projet

- **Données réalistes** — simulation de la Negative Churn (+2% de volume/mois), chargebacks, croissance organique
- **Architecture en couches** — staging / intermediate / marts conformes aux bonnes pratiques dbt
- **Tests de qualité** — 27 tests automatisés sur les données
- **Métriques FinTech** — GMV, Take Rate, LTV, ARPU, Default Rate