# AI Engineer Portfolio Roadmap

Build 4 to 6 small applications that each prove a different production skill.
Each project should include a working demo, clear README, tests, Dockerfile, and
deployment notes.

## Project 1: AI Ticket Triage

Classifies support tickets by urgency, department, tags, summary, and response
guidance.

What it proves:

- API design
- lightweight AI-style decisioning
- test coverage
- Docker and CI
- AWS web app deployment

## Project 2: Resume and Job Match Analyzer

Compares a resume against a job description and returns skill gaps, match score,
and suggested resume bullets.

What it proves:

- document parsing
- prompt engineering
- explainable scoring
- private user-data handling

## Project 3: RAG Knowledge Base Assistant

Lets users upload documents, indexes them, and answers questions with citations.

What it proves:

- embeddings
- vector search
- retrieval-augmented generation
- source attribution

## Project 4: Forecasting Dashboard

Uses historical business data to forecast demand, revenue, or support volume.

What it proves:

- data cleaning
- time-series modeling
- charts and decision support

## Project 5: Agentic Workflow Automator

Turns a user goal into steps, calls tools, tracks status, and produces a final
artifact.

What it proves:

- agent design
- tool calling
- state management
- failure handling

## Suggested GitHub workflow

For each project:

1. Create a dedicated GitHub repository.
2. Use a clear README with demo link, architecture, local setup, tests, and roadmap.
3. Add screenshots or a short GIF.
4. Add GitHub Actions for tests and linting.
5. Add Dockerfile and deployment notes.
6. Tag the first stable version as `v1.0.0`.

## Suggested AWS path

Start simple, then grow:

1. Elastic Beanstalk for first web app demos.
2. ECS Fargate for containerized production-style deployments.
3. RDS Postgres when a project needs persistent data.
4. S3 for document or file upload projects.
5. CloudWatch for logs and metrics.
6. CDK or Terraform once you are comfortable deploying manually.
