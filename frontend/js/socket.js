import { state, toast } from "./app.js";

const sioUrl = localStorage.getItem("socket_base") || "http://localhost:5000";
const socket = io(sioUrl, { transports: ["websocket", "polling"] });

socket.on("connect", () => {
  if (state.me?.id) socket.emit("join", { user_id: state.me.id });
});

socket.on("receive_alert", (data) => {
  toast(`ALERT: ${data.message || "Emergency need!"}`);
});

socket.on("match_notification", (data) => {
  toast(`New match: ${data.message || "A donor accepted your request."}`);
});

socket.on("joined", (_) => { /* joined room ack */ });

window.sendEmergencyAlert = function () {
  const msg = prompt(
    "Describe the emergency (blood type, units, hospital):",
    "Urgent: O+ needed at City Hospital"
  );
  if (!msg) return;
  socket.emit("send_alert", { message: msg });
}

export {}
