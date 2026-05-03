const chat = document.getElementById("chat");
const input = document.getElementById("input");
const send = document.getElementById("send");

function addMessage(role, text) {
  const el = document.createElement("div");
  el.className = "msg " + role;
  el.textContent = text;
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
}

send.onclick = async () => {
  const text = input.value.trim();
  if (!text) return;
  addMessage("user", text);
  input.value = "";
  addMessage("assistant", "...");
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text }),
  });
  const data = await res.json();
  chat.lastChild.textContent = data.reply;
};
