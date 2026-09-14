# Building an analytics agent

An analytics agent takes a question in ordinary language, investigates business data and returns an answer. The interesting part is what happens between the question and the answer: how the system interprets business terms, chooses an analytical approach, executes queries and decides whether it has enough evidence to respond. A useful implementation needs to make those steps flexible enough for unfamiliar questions and explicit enough to inspect when something looks wrong.

The application described here is built for retail analytics. Questions might concern differences between stores, changing sales or the most important customers in a particular location. It has a React and TypeScript frontend, a Python backend, models accessed through AWS Bedrock and a Snowflake data warehouse. The architecture separates business knowledge, agent behaviour and infrastructure integrations, allowing the same analytical workflow to support different business configurations and warehouse providers.

## The application stack

The React frontend, built with Vite, presents the conversation, investigation progress and supporting results. The Python backend manages the analysis, executes tools and assembles the response. Bedrock provides the model interface, while a warehouse adapter handles queries against Snowflake.

The code is organised around those responsibilities. The core contains the agent, configuration models, analytical rules and response contracts. Adapters handle external services such as Bedrock and the warehouse. The application layer connects those components to requests, sessions and the frontend.

A question passes through intake and clarification before reaching the analysis agent. The agent investigates through tool calls, then submits a structured result. Application code processes the evidence, constructs supported visualisations and returns the response to the frontend. Progress events provide visibility while that work is running.

## Business context and the semantic layer

Consider the question “Who are the most important customers for each store?” Before writing SQL, there are several things to establish. “Important” might mean spending, growth or breadth of purchasing. A customer might buy from several stores, and an account might represent an individual or an entire business. Different interpretations can produce different rankings while every query involved runs successfully.

The semantic layer records the knowledge needed to interpret the data. It contains table documentation, column definitions, metric definitions and exclusions, alongside domain guidance about how the data should be used. Table documentation describes what a row represents and which population a table covers. Metric definitions explain how a measure is calculated. Domain guidance supplies the analytical context: when a measure is useful, which distinctions matter and what needs care when making a comparison.

These definitions live in configuration files that the application loads and validates using Pydantic models. Validation catches missing or unexpected fields; the business meaning still needs to be correct. Keeping this material separate from the investigation code makes definitions easier to review and allows different deployments to supply their own business knowledge.

The agent initially receives a compact description of the available tables. A `load_table_metadata` tool retrieves detailed documentation for a selected table, and the agent is instructed to read it before querying. Reference and skill tools make further analytical guidance available when needed. This staged approach keeps the initial context manageable while allowing the agent to retrieve specific instructions during an investigation.

Documentation can resolve an ambiguity when the business already has an agreed rule. Where no definition exists, clarification or an explicit interpretation is still necessary. For the customer-ranking question, the documentation might establish how accounts are assigned to stores without defining what makes a customer important. The system needs to recognise that remaining decision.

## Bedrock and the investigation loop

The backend uses Bedrock’s Converse interface to send the model its instructions, conversation and available tool definitions. Each tool has a schema describing the arguments it accepts. When the model requests an operation, the backend executes the corresponding application function and returns the result to the conversation.

The main investigation runs through a single agent. It can inspect metadata, query the warehouse, perform calculations in Python and request additional guidance. Each result becomes context for the next decision, allowing the investigation to develop as evidence arrives.

For the customer-ranking question, an initial query might identify the highest-spending accounts. Those results could justify checking whether the accounts buy across several stores, examining unusually active accounts or considering whether category breadth adds anything useful to the ranking. The next step depends on what the earlier queries reveal.

The principal tool interfaces are:

| Tool | Purpose |
|---|---|
| `load_table_metadata` | Retrieve detailed documentation for a selected table. |
| `run_sql` | Submit SQL for policy checking and warehouse execution. |
| `run_python` | Calculate over gathered evidence when a code interpreter is configured. |
| Reference and skill tools | Retrieve additional analytical or domain guidance. |
| `submit_final_analysis` | Submit the answer, findings, caveats and selected supporting result. |

The application owns execution and the tool budgets. Each investigation has limits on queries, Python runs and tool rounds. Independent calls can execute concurrently, with budget reservations protected by a lock so simultaneous calls cannot each consume the same remaining allowance. Operations that depend on an earlier result require another round.

The agent completes the investigation by calling `submit_final_analysis`. Its arguments follow a JSON schema generated from a Pydantic model. That gives the backend a defined structure to validate and process, rather than leaving it to identify the answer, caveats and supporting evidence within an unrestricted text response.

## Query controls and evidence

Before proposed SQL reaches the warehouse, it passes through a parser and policy checks. These restrict execution to a single read-only statement, enforce access to approved tables and fields, and apply result limits. The model cannot waive those checks by explaining that a query would be useful.

Access policy and business guidance serve different purposes. A query can be permitted yet analytically inappropriate: it might compare incompatible periods, use the wrong customer population or aggregate at an unsuitable level. The semantic layer guides those choices, while the execution controls determine what may run.

Queries and their results are retained as evidence. That makes it possible to inspect which data supported an answer and follow the investigation beyond its final explanation. When a result is questioned, the useful detail is often in a filter, join or aggregation that the prose has summarised away.

The agent also declares whether a query follows documented business guidance or includes its own interpretation. The response preserves that distinction, including where an investigation uses an agreed definition for one finding and an inferred approach for another. This is a model-supplied declaration, so it needs to be read alongside the evidence. It can nevertheless expose a missing definition or an assumption worth revisiting.

## Warehouse portability

Snowflake is accessed through a warehouse adapter rather than directly from the agent’s orchestration code. The repository also contains BigQuery and Databricks adapters implementing the same execution interface. Each accepts a query request and returns a common `QueryResult` containing column metadata, rows, execution information and any error.

That shared result format allows evidence handling, chart construction and response assembly to operate independently of the provider. A table returned from Snowflake reaches those components in the same application-level structure as one returned from BigQuery or Databricks.

SQL still needs to reflect the target warehouse. The configured provider supplies guidance on object naming, identifier quoting, date functions and row limits. The SQL parser and policy checks use the corresponding dialect as well. Warehouse portability therefore depends on both the shared execution contract and provider-specific query handling.

Connecting a different warehouse also requires the appropriate credentials, policies and business metadata. The shared architecture means those changes can be concentrated around the connection and configuration while the investigation workflow and response handling remain consistent.

## Structured responses and the frontend

Pydantic contracts define the information passed through the backend, including query results, analysis outputs, chart specifications and the final response. These contracts allow the application to validate the shape of data before passing it to other components. They also give the frontend a predictable representation of an answer and its supporting material.

The React interface renders those components as conversation content, tables, charts and disclosures. Charts use Recharts, with the backend supplying specifications derived from returned data and supported rendering capabilities. The model can propose what a chart should communicate, while application code determines how that proposal becomes a supported visual.

Different questions merit different amounts of supporting material. A short factual answer may need little explanation, while a comparison across stores could benefit from a chart, a detailed table and access to the query. The structured response keeps those components available without requiring every answer to present them in the same way.

During execution, progress events show the activity behind the investigation. Afterwards, the supporting work remains accessible alongside the answer. Saved conversations and exports can use the same defined response fields, preserving the relationship between the explanation and its evidence.

## Deployment and tracing

Each backend deployment is bound to one client configuration and deployment stack. Requests specifying a different client or stack are rejected. The model operates within the deployment’s configured context; selecting another client environment is not one of its responsibilities.

Requests carry a correlation identifier through the application, and warehouse queries are annotated with that context. This connects an answer to its application logs and warehouse query history, providing a route from a reported problem to the operations that produced it.

The separation between core behaviour, adapters and application wiring also helps contain changes. Updating a business definition belongs in configuration. Changing warehouse connection behaviour belongs in the adapter. Adjusting the investigation’s instructions or tool use belongs in the agent. Those boundaries make it easier to understand which parts of the system a change should affect.

## Testing the system

Automated tests cover configuration validation, query controls, orchestration, evidence handling and chart behaviour. Replay cases supply known tool calls and warehouse results, making it possible to check whether a code change has altered how an investigation is processed or assembled into a response.

Analytical evaluation also needs to examine the decisions the model makes on real questions. Did it consult the relevant documentation? Did it choose suitable data and comparisons? Were its assumptions reasonable, and does the conclusion follow from the results? A replay can verify the handling of a prescribed sequence, but assessing the choice of sequence requires reviewing the investigation itself.

User acceptance testing contributes questions grounded in how the business actually operates. These are useful for finding gaps in the semantic layer as well as weaknesses in the analysis. A technically coherent answer may still reveal that the system has misunderstood a term with a specific meaning to the people using it.

## Keeping questions under review

The application supports pinning an answered question and checking whether the underlying data has changed. During an investigation, the agent can propose small checks based on SQL it actually ran. The application validates and executes those checks to establish a baseline.

Subsequent checks run without a model call. A change in the data can trigger a decision about whether to perform a fresh investigation, with full reruns capped. Failed checks are recorded separately from unchanged results, so an execution failure cannot be mistaken for evidence that nothing has moved.

This extends the usefulness of an investigation beyond the initial answer. The system retains the definitions, queries and results that explain how it reached a conclusion, then uses some of that work to decide when the question may deserve another look. Those records also make the application easier to maintain: a disputed answer, a revised business definition or a change of model can be examined against the work the system actually performed.
