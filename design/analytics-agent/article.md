# Implementing an analytics agent: from business definitions to live deployments

I've seen [Anthropic's article on self-service data analytics](https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude) doing the rounds a lot. It also provided much of the basis for an analytics agent I built. This is a technical guide to how I implemented those ideas: organising the business context, running an investigation, controlling access to the warehouse, and keeping the resulting system manageable across deployments.

The product takes a business question, queries a warehouse, investigates the results, and returns an explanation with charts, tables and the workings behind it. It has live deployments in user acceptance testing with some major retailers. I'll keep the clients and product anonymous, but describe the implementation in enough detail to make the design choices useful if you're building something similar.

One question asked during UAT was, paraphrased: “Who are the most important customers for each store?” You could rank customers by spending, recent growth, or the range of products they buy. You also need to decide how to assign someone who shops at several stores, and whether every account represents an individual customer. Those choices can produce different, defensible lists from the same data. Giving a model access to the warehouse leaves all of them to be made.

The implementation has three main layers: business definitions and policies in configuration, an investigation loop that uses them, and application code that executes tools and assembles the response. Keeping those responsibilities separate gives you room to change the model's behaviour without rebuilding everything around it.

## Define the business context as a contract

A list of tables and columns only gets you so far when you're working with an unfamiliar dataset. You also need to know what each row represents, which records are excluded, and when a particular measure is appropriate. The agent needs the same context. It can produce perfectly valid SQL using the wrong definition of a metric.

For the customer-ranking question, you need to establish what “important” means before treating the output as a repeatable ranking. Spending and growth can both be relevant, but combining them introduces choices about weighting and normalisation. Those choices need to be agreed, or presented as an exploratory method that the user can question.

I put that knowledge into configuration: table documentation, metric definitions, domain guidance and access policies. The application loads and validates those files. Keeping them separate from the investigation code gives you somewhere explicit to record a business definition, review it, and change it when necessary.

The configuration uses typed models to define the expected fields and reject unexpected ones. Table metadata records what each row represents, the scope of the data, exclusions and column definitions. Metric definitions and domain guidance describe how that data should be interpreted. Access policies define what can be queried. These are different concerns, even when they refer to the same table.

The documentation is available in stages, following the same principle as the on-demand references in [Anthropic's skills approach](https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude). The agent starts with a compact description of the tables and can request the full documentation for whichever ones it needs. That includes column definitions, exclusions and rules about when to use them. Its instructions require it to read that detail before querying a table, so it has a chance to resolve those questions before writing SQL.

You still need to check whether it follows that instruction. The documentation helps it decide what to query; separate checks in the application determine whether that query is allowed to run.

## Give the investigation a bounded tool loop

In an earlier version, I split the investigation between a planner and a set of workers, each with a bounded task. As the models improved, I decided to move to a simpler arrangement for the main analysis: one agent with tools to query the warehouse, run calculations in Python, and load additional guidance. It can inspect a result and decide what to do next.

The fixed plan was awkward for the more open-ended questions I wanted it to handle. With the customer-ranking example, an initial spending analysis might lead you to check purchases across stores, investigate unusually active accounts, or reconsider whether category breadth usefully separates the customers at the top. The agent needs to be able to make that sort of adjustment as it gathers evidence, while keeping the chosen ranking method explicit.

I kept intake and clarification ahead of the investigation, and put limits around how much work the analysis agent can do. It has a budget for queries, Python runs and tool rounds, and it finishes by submitting a structured response containing its answer, findings and caveats. Other model calls still have roles in the product, but the investigation itself belongs to one agent.

The main interfaces are small enough to describe directly:

| Interface | Responsibility |
|---|---|
| `load_table_metadata` | Return detailed documentation for a selected table. |
| `run_sql` | Execute proposed SQL through warehouse policies and record the result. |
| `run_python` | Run calculations over evidence already gathered, when a code interpreter is configured. |
| Reference and skill tools | Load additional analytical guidance when needed. |
| `submit_final_analysis` | Submit the structured answer, findings, caveats and selected supporting result. |

The application owns the tool session and its counters. Independent tool calls can execute concurrently, with budgets reserved under a lock so simultaneous calls cannot each spend the same remaining allowance. The results go back to the agent for its next decision. If a query depends on a previous result, that dependency naturally requires another round.

I kept the output format consistent between the two approaches. That let me change the investigation without having to rebuild the interface, saved history or evidence displays around it. The earlier implementation is still available for comparison.

## Enforce execution policy and retain the evidence

Before a query reaches the warehouse, it passes through a SQL parser and policy checks. Those restrict it to a single read-only statement, check access to approved tables and fields, and apply result limits. These are application controls, so the model doesn't get to waive them because a query seems useful.

An allowed query can still make a poor comparison. You need to be able to look at how an answer was reached, whether you're developing the agent or using it to make a decision. The queries and results behind an investigation are retained, with supporting material available alongside the answer.

Charts follow a similar principle. The model can suggest what a visual should communicate, while the application builds it from the returned data using defined chart rules. That gives the agent some say in how it presents a finding, with the actual rendering tied to the available columns and supported chart types.

Anthropic also describes [showing the source behind an answer in a provenance footer](https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude). In this product, the distinction is whether the agent followed a documented business rule or made an interpretation of its own. I added a declaration for that when it runs a query. If it reports using its own judgement in part of an answer, the interface keeps that qualification visible alongside any documented rules it used elsewhere.

You can't treat the declaration as independent verification, because it comes from the same model. It does, however, give you something specific to question. Was that interpretation reasonable? Is there a definition missing from the documentation? Should the analysis be rerun with a different assumption? Those are useful conversations to make possible in the interface.

## Keep deployment boundaries explicit

The same product code needs to work with different business configurations. I separated the analysis logic from the warehouse and model adapters, with the API and deployment wiring outside that core. The warehouse adapter returns a common query-result structure, so response handling does not have to know which provider executed the query.

Each backend deployment is bound to one client configuration and deployment stack. Requests that specify a different client or stack are rejected. This makes the boundary explicit in the application; selecting a client is not a decision delegated to the model.

Operating across deployments also means being able to trace a reported problem. Requests carry a correlation identifier, and warehouse queries are annotated with that context. That gives you a way to connect an answer to its application logs and warehouse query history when you need to inspect what happened.

Execution budgets and bounded concurrency address individual investigations. Establishing capacity for a larger user population also requires measuring concurrent demand, warehouse performance and model limits. The current UAT deployments provide an environment for that work; they do not, by themselves, establish a throughput benchmark.

## Test application behaviour and analytical judgement separately

Tests cover the configuration, query controls, orchestration and chart behaviour. Replay cases pass known tool calls and warehouse results through the investigation, letting you check that a change hasn't broken how evidence is retained or how a result becomes a response.

Checking a prescribed sequence doesn't tell you whether the model will choose a sensible sequence for a new question. For that, you need to review actual investigations: what it queried, which assumptions it made, and whether the conclusion follows. That is an important part of what I want to establish through user acceptance testing, alongside whether people find the product useful enough to return to.

## Recheck the data before rerunning the analysis

I also built a way to pin an answered question and keep it under review. The agent can propose small checks based on SQL it actually ran during the investigation. The application validates those checks and runs them to establish a baseline; subsequent checks can then run without calling the model. If the data moves, that can trigger a decision about whether a fresh investigation is worthwhile.

This lets you revisit useful questions without paying for a full analysis every time you check the data. Full reruns are capped, and failed checks appear separately from unchanged results, so a broken query doesn't quietly look like nothing has happened.

If you're implementing a similar system, keep a complete investigation inspectable from the outset: the definitions it consulted, the queries it ran, the results it used and the answer it returned. Those records give you something concrete to work with when a user questions a result, a business definition changes, or you want to compare a new model with the existing one.
