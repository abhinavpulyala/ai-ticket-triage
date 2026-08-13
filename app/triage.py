from __future__ import annotations

import re
from collections import Counter

from app.models import Department, Priority, TicketClassification, TicketRequest

DEPARTMENT_KEYWORDS = {
    Department.billing: {
        "invoice",
        "payment",
        "charge",
        "refund",
        "billing",
        "credit",
        "receipt",
        "subscription",
    },
    Department.security: {
        "breach",
        "hacked",
        "malware",
        "phishing",
        "security",
        "suspicious",
        "compromised",
        "data leak",
    },
    Department.technical_support: {
        "error",
        "bug",
        "crash",
        "broken",
        "latency",
        "timeout",
        "integration",
        "api",
        "failed",
    },
    Department.account_access: {
        "login",
        "password",
        "locked",
        "mfa",
        "2fa",
        "account",
        "access",
        "reset",
    },
    Department.product: {
        "feature",
        "roadmap",
        "request",
        "improve",
        "dashboard",
        "reporting",
        "export",
    },
}

URGENT_TERMS = {
    "down",
    "outage",
    "blocked",
    "cannot access",
    "production",
    "breach",
    "hacked",
    "data leak",
    "urgent",
    "asap",
}

HIGH_TERMS = {"failed", "broken", "cannot", "error", "crash", "locked", "refund"}


def classify_ticket(ticket: TicketRequest) -> TicketClassification:
    text = f"{ticket.subject} {ticket.message}".lower()
    normalized = re.sub(r"\s+", " ", text)

    department_scores = Counter()
    matched_tags: set[str] = set()
    for department, keywords in DEPARTMENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in normalized:
                department_scores[department] += 1
                matched_tags.add(keyword.replace(" ", "_"))

    department = (
        department_scores.most_common(1)[0][0]
        if department_scores
        else Department.technical_support
    )

    urgent_hits = sum(1 for term in URGENT_TERMS if term in normalized)
    high_hits = sum(1 for term in HIGH_TERMS if term in normalized)

    if urgent_hits >= 2 or (urgent_hits >= 1 and ticket.customer_tier == "enterprise"):
        priority = Priority.urgent
    elif urgent_hits >= 1 or high_hits >= 2 or ticket.customer_tier == "enterprise":
        priority = Priority.high
    elif high_hits == 1 or ticket.customer_tier == "pro":
        priority = Priority.medium
    else:
        priority = Priority.low

    confidence = _confidence(department_scores, urgent_hits, high_hits)
    summary = _summarize(ticket.message)
    recommended_response = _response_template(priority, department)

    return TicketClassification(
        priority=priority,
        department=department,
        confidence=confidence,
        tags=sorted(matched_tags)[:8],
        summary=summary,
        recommended_response=recommended_response,
    )


def _confidence(scores: Counter, urgent_hits: int, high_hits: int) -> float:
    keyword_strength = min(sum(scores.values()) / 8, 0.45)
    urgency_strength = min((urgent_hits * 0.18) + (high_hits * 0.08), 0.35)
    return round(0.2 + keyword_strength + urgency_strength, 2)


def _summarize(message: str) -> str:
    first_sentence = re.split(r"(?<=[.!?])\s+", message.strip())[0]
    if len(first_sentence) <= 180:
        return first_sentence
    return first_sentence[:177].rstrip() + "..."


def _response_template(priority: Priority, department: Department) -> str:
    sla = {
        Priority.urgent: "15 minutes",
        Priority.high: "1 business hour",
        Priority.medium: "4 business hours",
        Priority.low: "1 business day",
    }[priority]
    team = department.value.replace("_", " ")
    return (
        f"Thanks for the details. I routed this to {team} with {priority.value} "
        f"priority. Our target first response is within {sla}."
    )
