```md
# Reference Master Map Diagram
> Visual Knowledge Architecture — Nick Pilot Project

```mermaid
graph TD

%% === Top-Level Entities ===
Nick[Nick Maroules]
ProjectRequest[ILPA Article Request]
EngagementTeam[Engagement Team]

%% === Client Context ===
Nick --> ProjectRequest
ProjectRequest --> InitialEmail[nick_project_request_ilpa_article_context.md]
ProjectRequest --> SampleEmail[nick_sample_article_reference_email.md]
SampleEmail --> SamplePDF[Asset_Mgmt_Insights_BDC_Regulatory_Reform_FINAL.pdf]

%% === ILPA Website ===
ProjectRequest --> ILPA_Web[ILPA Website Sources]
ILPA_Web --> ILPA_Reporting_Link[ilpa_reporting_template_link.md]
ILPA_Web --> ILPA_Performance_Link[ilpa_performance_template_link.md]

%% === Zip Attachment Files ===
ProjectRequest --> ZipFiles[Reference Materials (ZIP)]
ZipFiles --> ReportingZIP[/reference_materials/reporting_template/...]
ZipFiles --> PerformanceZIP[/reference_materials/performance_template/...]

%% === Engagement-Sourced Research ===
EngagementTeam --> ResearchFiles[engagement_research/ilpa_how_we_got_here.md]

%% === Meta + Strategy ===
MetaLayer --> Taxonomy[reference_taxonomy.md]
MetaLayer --> MapDiagram[reference_master_map_diagram.md]
MetaLayer --> Clarifications[open_questions_and_clarifications.md]

Strategy --> Goals[implicit_goals_and_subtext.md]
Strategy --> ArgumentPlan[article_argument_strategy.md]
Strategy --> VisualPlan[visual_strategy_vkr_plan.md]

%% === Prompt System ===
Prompts --> Prime[prompts/prime.md]
Prompts --> KickoffA[kickoff_prompt_A.md]
Prompts --> KickoffB[kickoff_prompt_B.md]

%% === Connections ===
Nick --> ILPA_Web
Nick --> ILPA_Committee[ILPA Committee]
ILPA_Committee --> ProjectRequest

ProjectRequest --> Prompts
Strategy --> Prompts
MetaLayer --> Prompts
EngagementTeam --> MetaLayer
EngagementTeam --> Strategy
```

(This diagram evolves as new files are processed and relationships mapped.)
```
