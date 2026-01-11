let state = {};
const container = document.getElementById("step-container");
const agentMsg = document.getElementById("agent-message");
const confidenceEl = document.getElementById("confidence");

function renderStep() {
  container.innerHTML = "";
  const step = state.step;

  if(step === "select_date") {
    const input = document.createElement("input");
    input.type = "date";
    input.id = "date-input";
    const btn = document.createElement("button");
    btn.textContent = "Next";
    btn.onclick = () => submitStep(document.getElementById("date-input").value);
    container.append(input, btn);
  }

  else if(step === "select_participants") {
    const input = document.createElement("input");
    input.type = "text";
    input.placeholder = "Comma separated names";
    input.id = "participants-input";
    const btn = document.createElement("button");
    btn.textContent = "Next";
    btn.onclick = () => submitStep(document.getElementById("participants-input").value.split(","));
    container.append(input, btn);
  }

  else if(step === "confirm") {
    const summary = document.createElement("div");
    summary.innerHTML = `<p>Date: ${state.date}</p><p>Participants: ${state.participants.join(", ")}</p>`;
    const btn = document.createElement("button");
    btn.textContent = "Confirm";
    btn.onclick = () => submitStep(null);
    container.append(summary, btn);
  }

  else if(step === "completed") {
    container.innerHTML = "<h2>Task Completed!</h2>";
  }
}

async function submitStep(input) {
  const res = await fetch("http://127.0.0.1:5000/next_step", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input })
  });
  const data = await res.json();
  state = data.state;
  agentMsg.textContent = `Agent: ${data.message}`;
  confidenceEl.textContent = `Confidence: ${Math.round(data.confidence*100)}%`;

  renderStep();

  if(state.error) {
    const errorEl = document.createElement("div");
    errorEl.id = "error";
    errorEl.textContent = state.error;
    container.appendChild(errorEl);
  }
}

// Initialize
submitStep(null);
