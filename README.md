# AI Ticket Triage

Production-style portfolio project that classifies customer support tickets by
priority, department, tags, summary, and recommended first response.

## Why this project belongs in an AI engineer portfolio

This project demonstrates an end-to-end workflow that hiring managers expect to
see from an applied AI engineer:

- API design with FastAPI
- deterministic classification logic that can later be replaced by an LLM or ML model
- browser-based demo UI
- automated tests
- Docker packaging
- GitHub Actions CI
- AWS deployment path

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install ".[dev]"
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Test

```bash
pytest
ruff check .
```

## Run with Docker

```bash
docker build -t ai-ticket-triage .
docker run -p 8000:8000 ai-ticket-triage
```

## API example

```bash
curl -X POST http://127.0.0.1:8000/classify \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Enterprise login outage",
    "message": "Our production admin account is locked and users cannot access the dashboard.",
    "customer_tier": "enterprise"
  }'
```

## AWS deployment option

The simplest AWS demo path is:

1. Push this repository to GitHub.
2. Create an AWS Elastic Beanstalk Python application.
3. Use the Dockerfile deployment option, or connect a GitHub Actions deployment workflow.
4. Add health check path `/health`.
5. Share the Elastic Beanstalk public URL in the README.

For a more advanced portfolio version, deploy the container to Amazon ECS Fargate
behind an Application Load Balancer.

## Upgrade path

Good next improvements:

- Add an OpenAI or Amazon Bedrock classifier behind a feature flag.
- Store submitted tickets in Postgres.
- Add authentication for admin review.
- Add model evaluation data and classification accuracy metrics.
- Add Terraform or AWS CDK infrastructure.
