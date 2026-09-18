# Business Operations & E-commerce Intelligence Agent

An AI-powered analytics agent that connects a Large Language Model to business data through the **Model Context Protocol (MCP)**.

The project explores how AI agents can support a Data Analyst workflow by translating natural-language business questions into data exploration, SQL analysis, anomaly investigation, and evidence-based insights.

The agent can inspect the available database schema, understand business context, generate read-only SQL queries, investigate performance changes, and drill down into potential root causes.

> Portfolio project built with synthetic data and inspired by real-world business operations and e-commerce analytics scenarios.

---

## Project Goal

The goal of this project is to experiment with an AI-assisted analytical workflow:

**Business Question → Data Exploration → SQL → Investigation → Insight**

Instead of asking an analyst to manually write every query, the user can start with a higher-level business question such as:

> **What are the most significant changes in our e-commerce performance this month, what is driving them, what is their financial impact, and which findings require further investigation?**

The agent can then explore the database, generate SQL queries, compare periods, investigate relevant dimensions, and return findings supported by the underlying data.

The analyst remains responsible for validating the results, interpreting business context, distinguishing correlation from causation, and deciding which findings require deeper investigation.

---

## Architecture

### Local development

```text
Claude Desktop
      │
      ▼
Model Context Protocol (MCP)
      │
      ▼
Python MCP Server
      │
      ▼
PostgreSQL
      │
      ▼
Synthetic Business Data
```

### Remote deployment

```text
Claude
   │
   │ HTTPS
   ▼
Remote MCP Server
   │
   ▼
Cloud PostgreSQL
```

The MCP server and PostgreSQL database are deployed to the cloud, allowing the analytical agent to operate independently of the local development machine.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Claude Desktop | Conversational interface for interacting with the analytical agent |
| MCP (Model Context Protocol) | Connects the LLM with analytical tools and business data |
| Python | MCP server and backend logic |
| PostgreSQL | Analytical database |
| SQL | Data exploration, aggregation and investigation |
| Docker | Local PostgreSQL environment and containerization |
| Railway | Cloud deployment of the MCP server and PostgreSQL database |
| Git / GitHub | Version control and deployment workflow |
| pytest | Automated testing of database and MCP functionality |
| ChatGPT | Assisted development and generation of controlled synthetic business scenarios |

---

## Data Model

The project currently contains two analytical domains.

### E-commerce Analytics

Synthetic e-commerce data includes:

- customers
- sessions
- behavioral events
- products
- orders
- order items
- customer payments
- returns
- marketing channels
- campaigns
- marketing spend

This enables analysis of:

- revenue and order trends
- conversion funnels
- customer behavior
- acquisition channels
- marketing efficiency
- product performance
- discounts
- payment failures
- returns
- device and browser performance

### Business Operations / Procure-to-Pay

The operations dataset includes:

- business units
- cost centers
- suppliers
- purchase orders
- invoices
- supplier payments
- budgets

This domain is designed for analysis such as:

- spend monitoring
- budget vs. actual analysis
- supplier performance
- invoice anomalies
- purchase-order compliance
- payment analysis
- operational variance investigation

---

## Synthetic Anomalies

The dataset intentionally contains hidden business and technical patterns.

Examples include:

- abnormal changes in marketing spend
- unusual discount behavior
- payment failures concentrated in a specific device/browser segment
- increased product returns in selected categories
- operational and financial variance patterns

The agent is not explicitly told where these anomalies exist.

The objective is to evaluate whether it can move from a broad business question to:

**Signal Detection → Investigation → Segmentation → Evidence → Financial Impact**

---

## MCP Tools

The current MCP server exposes three core analytical tools.

### `list_tables`

Discovers the tables available in the analytical database.

### `describe_table`

Returns table structure together with business-level semantic descriptions.

This helps the agent understand what the data represents before generating SQL.

### `run_sql`

Executes read-only analytical SQL queries.

The SQL layer includes safeguards such as:

- read-only transactions
- query timeout
- row limits
- restrictions on data-modification statements

---

## Example Investigation

A user can start with a broad analytical question:

> **What are the most significant changes in our e-commerce performance this month, what is driving them, what is their financial impact, and which findings require further investigation?**

The agent may then investigate:

```text
Business Performance
        │
        ├── Revenue
        ├── Orders
        ├── Conversion
        ├── Average Order Value
        └── Profitability
                │
                ▼
        Segment Investigation
                │
        ├── Marketing Channel
        ├── Product / Category
        ├── Customer Segment
        ├── Device
        ├── Browser
        └── Geography
                │
                ▼
          Funnel Investigation
                │
        ├── Product View
        ├── Add to Cart
        ├── Checkout
        ├── Payment
        └── Purchase
                │
                ▼
        Potential Root Cause
```

This allows the agent to progressively move from a high-level KPI change toward more specific evidence.

---

## Semantic Layer

Database comments are used as a lightweight semantic layer.

They explain business concepts such as:

- the difference between revenue and cash payments
- how orders should be interpreted
- how marketing attribution should be handled
- the meaning of supplier risk
- how returns affect business performance
- which records should or should not be included in specific calculations

This reduces the risk of generating technically valid SQL based on incorrect business assumptions.

---

## Testing

The project includes automated tests for:

- database connectivity
- schema discovery
- table descriptions
- SQL execution
- read-only SQL validation

Run the test suite with:

```bash
pytest
```

---

## Running Locally

### 1. Create the environment file

```bash
cp .env.example .env
```

### 2. Start PostgreSQL

```bash
docker compose up -d
```

### 3. Create a Python virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -e ".[dev]"
```

### 5. Generate synthetic e-commerce data

```bash
python db/seed_ecommerce.py
```

### 6. Run tests

```bash
pytest
```

### 7. Start the MCP server

```bash
python -m server.main
```

---

## Remote MCP

The project also supports **Streamable HTTP**, allowing the MCP server to run remotely rather than only through a local `stdio` connection.

The current deployment architecture is:

```text
Claude
   ↓
HTTPS
   ↓
MCP Server (Railway)
   ↓
PostgreSQL (Railway)
```

This allows another user to connect their Claude client to the remote analytical agent without running the project or database locally.

The public testing endpoint is intentionally not included in this repository while authentication and access controls are being developed.

---

## Current Limitations

This is an experimental portfolio project rather than a production analytics platform.

Current limitations include:

- synthetic rather than production business data
- LLM-generated analytical hypotheses still require human validation
- SQL correctness does not guarantee correct business interpretation
- correlation should not automatically be interpreted as causation
- data-quality issues can affect analytical conclusions
- authentication and access control for public MCP usage are still being developed
- more advanced anomaly detection and analytical tools are planned

---

## Future Development

Planned areas of experimentation include:

- automated anomaly detection
- root-cause investigation workflows
- financial-impact estimation
- contribution-margin analysis
- supplier and procurement intelligence
- automated management reports
- data-quality monitoring
- additional MCP analytical tools
- authentication and controlled remote access
- dashboards and visualization
- integration with additional enterprise and web analytics data sources

---

## Why This Project

The project explores a simple question:

> **What changes when an AI assistant can not only answer questions, but also investigate the underlying business data?**

The goal is not to replace analytical judgment.

It is to explore how AI agents can reduce the mechanical part of data exploration while keeping business understanding, validation, critical thinking, and decision-making with the analyst.
