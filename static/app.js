const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const messages = document.querySelector("#chat-messages");
const suggestions = document.querySelectorAll(".suggestion");

function addMessage(text, sender) {
  const row = document.createElement("div");
  row.className = `message-row ${sender}-row`;

  if (sender === "bot") {
    const avatar = document.createElement("span");
    avatar.className = "mini-avatar";
    avatar.setAttribute("aria-hidden", "true");
    avatar.textContent = "✳";
    row.append(avatar);
  }

  const wrap = document.createElement("div");
  wrap.className = "bubble-wrap";
  const bubble = document.createElement("div");
  bubble.className = `bubble ${sender}-bubble`;
  bubble.textContent = text;
  wrap.append(bubble);

  const time = document.createElement("span");
  time.className = "message-time";
  time.textContent = sender === "bot" ? "Careline · just now" : "You · just now";
  wrap.append(time);
  row.append(wrap);
  messages.append(row);
  messages.scrollTop = messages.scrollHeight;
}

async function sendMessage(text) {
  const message = text.trim();
  if (!message) return;

  addMessage(message, "user");
  input.value = "";
  input.disabled = true;
  form.querySelector("button").disabled = true;

  try {
    const response = await fetch("/demo/reply", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "The demo could not answer.");
    addMessage(data.reply, "bot");
  } catch (error) {
    addMessage(error.message || "Unable to reach the demo. Please try again.", "bot");
  } finally {
    input.disabled = false;
    form.querySelector("button").disabled = false;
    input.focus();
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(input.value);
});

suggestions.forEach((button) => {
  button.addEventListener("click", () => sendMessage(button.dataset.message || ""));
});
