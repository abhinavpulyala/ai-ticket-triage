from app.models import Department, Priority, TicketRequest
from app.triage import classify_ticket


def test_enterprise_outage_is_urgent_account_access():
    ticket = TicketRequest(
        subject="Enterprise login outage",
        customer_tier="enterprise",
        message=(
            "Our production admin account is locked and multiple users cannot "
            "access the dashboard. This is urgent."
        ),
    )

    result = classify_ticket(ticket)

    assert result.priority == Priority.urgent
    assert result.department == Department.account_access
    assert "locked" in result.tags


def test_billing_refund_routes_to_billing():
    ticket = TicketRequest(
        subject="Refund request",
        message="I was charged twice on my subscription invoice and need a refund.",
    )

    result = classify_ticket(ticket)

    assert result.department == Department.billing
    assert result.priority in {Priority.medium, Priority.high}
