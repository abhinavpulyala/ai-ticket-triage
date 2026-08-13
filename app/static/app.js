const form = document.querySelector("#ticket-form");
const sampleButtons = document.querySelectorAll(".sample");
const inputs = {
  subject: document.querySelector("#subject"),
  message: document.querySelector("#message"),
  customerTier: document.querySelector("#customer_tier"),
};
const fields = {
  priority: document.querySelector("#priority"),
  confidence: document.querySelector("#confidence"),
  department: document.querySelector("#department"),
  summary: document.querySelector("#summary"),
  tags: document.querySelector("#tags"),
  response: document.querySelector("#response"),
};

const samples = {
  outage: {
    subject: "Enterprise login outage",
    customer_tier: "enterprise",
    message:
      "Our production admin account is locked and multiple users cannot access the dashboard. This is blocking our morning operations and needs urgent help.",
  },
  billing: {
    subject: "Charged twice for subscription",
    customer_tier: "standard",
    message:
      "I was charged twice on my subscription invoice this month. Please review the payment and issue a refund for the duplicate charge.",
  },
  security: {
    subject: "Suspicious account activity",
    customer_tier: "pro",
    message:
      "We received a phishing email and now see suspicious account activity. We are worried the account may be compromised.",
  },
  feature: {
    subject: "Dashboard export request",
    customer_tier: "standard",
    message:
      "Can you add a feature to export dashboard reporting data as a CSV? Our team needs it for monthly leadership reports.",
  },
};

sampleButtons.forEach((button) => {
  button.addEventListener("click", () => {
    sampleButtons.forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    loadSample(button.dataset.sample);
    classifyCurrentTicket();
  });
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  await classifyCurrentTicket();
});

loadSample("outage");
classifyCurrentTicket();

function loadSample(key) {
  const sample = samples[key];
  inputs.subject.value = sample.subject;
  inputs.message.value = sample.message;
  inputs.customerTier.value = sample.customer_tier;
}

async function classifyCurrentTicket() {
  const payload = {
    subject: inputs.subject.value.trim(),
    message: inputs.message.value.trim(),
    customer_tier: inputs.customerTier.value,
  };

  fields.priority.textContent = "Working";
  fields.priority.className = "badge";
  fields.department.textContent = "--";
  fields.summary.textContent = "Reading the ticket and finding routing signals...";
  fields.response.textContent = "--";
  fields.tags.textContent = "--";

  try {
    const result = await fetch("/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!result.ok) {
      fields.priority.textContent = "Error";
      fields.summary.textContent = "Please check the ticket fields and try again.";
      return;
    }

    const data = await result.json();
    fields.priority.textContent = data.priority;
    fields.priority.className = `badge ${data.priority}`;
    fields.confidence.textContent = `Confidence ${Math.round(data.confidence * 100)}%`;
    fields.department.textContent = data.department.replaceAll("_", " ");
    fields.summary.textContent = data.summary;
    fields.response.textContent = data.recommended_response;
    fields.tags.innerHTML = data.tags.length
      ? data.tags.map((tag) => `<span>${tag.replaceAll("_", " ")}</span>`).join("")
      : "none";
  } catch {
    fields.priority.textContent = "Connection issue";
    fields.priority.className = "badge high";
    fields.confidence.textContent = "Confidence --";
    fields.department.textContent = "--";
    fields.summary.textContent =
      "The page is open, but it cannot reach the local app server. Start or refresh the server, then try again.";
    fields.response.textContent = "--";
    fields.tags.textContent = "--";
  }
}
