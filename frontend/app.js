const API_BASE = "https://w9ygca0mk4.execute-api.eu-north-1.amazonaws.com/prod";
const result = document.getElementById("result");
 
document.getElementById("ticketForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.currentTarget;
  const button = document.getElementById("submitBtn");
  const data = Object.fromEntries(new FormData(form).entries());
  button.disabled = true;
  result.textContent = "Submitting...";
  try {
    const response = await fetch(`${API_BASE}/tickets`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data)
    });
    const body = await response.json();
    if (!response.ok) throw new Error(body.message || "Ticket submission failed");
    result.textContent = `Ticket created successfully. Your ticket ID is ${body.ticketId}.`;
    form.reset();
  } catch (err) {
    result.textContent = `Error: ${err.message}`;
  } finally {
    button.disabled = false;
  }
});
 
document.getElementById("trackForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const id = new FormData(e.currentTarget).get("ticketId").trim();
  const box = document.getElementById("trackResult");
  box.textContent = "Checking...";
  try {
    const response = await fetch(`${API_BASE}/tickets/${encodeURIComponent(id)}`);
    const body = await response.json();
    if (!response.ok) throw new Error(body.message || "Ticket not found");
    box.textContent = `Status: ${body.status} | Subject: ${body.subject}`;
  } catch (err) { box.textContent = `Error: ${err.message}`; }
});
 
document.getElementById("refreshBtn").addEventListener("click", async () => {
  const box = document.getElementById("ticketList");
  box.textContent = "Loading...";
  try {
    const response = await fetch(`${API_BASE}/tickets`);
    const body = await response.json();
    if (!response.ok) throw new Error(body.message || "Unable to load tickets");
    box.replaceChildren();
    (body.items || []).forEach(ticket => {
      const card = document.createElement("div");
      card.className = "ticket";
      const title = document.createElement("strong");
      title.textContent = `${ticket.ticketId} — ${ticket.subject}`;
      const detail = document.createElement("p");
      detail.textContent = `${ticket.name} | ${ticket.email} | ${ticket.status}`;
      card.append(title, detail);
      box.append(card);
    });
  } catch (err) { box.textContent = `Error: ${err.message}`; }
});
