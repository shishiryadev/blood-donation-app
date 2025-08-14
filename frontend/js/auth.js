import { state, api, toast } from "./app.js";

function modal(html) {
  let m = document.getElementById("authModal");
  if (!m) {
    m = document.createElement("div");
    m.id = "authModal";
    m.className = "modal";
    document.body.appendChild(m);
  }
  m.innerHTML = `<div class="sheet">${html}</div>`;
  m.style.display = "flex";
  m.onclick = (e) => { if (e.target === m) m.style.display = "none"; };
}

window.openAuthModal = function (mode = "login") {
  modal(`
    <h3>${mode === "register" ? "Create account" : "Sign in"}</h3>
    <div class="notice"></div>
    <div class="row">
      ${mode === "register" ? `<input class="input" id="name" placeholder="Full name" />` : ""}
      <input class="input" id="email" placeholder="Email" />
      <input class="input" id="password" placeholder="Password" type="password" />
      ${mode === "register" ? `
        <select class="input" id="blood_type">
          ${["A+","A-","B+","B-","AB+","AB-","O+","O-"].map(b=>`<option>${b}</option>`).join("")}
        </select>
        <select class="input" id="is_donor">
          <option value="true">I'm a Donor</option>
          <option value="false">I need blood</option>
        </select>`: ""}
    </div>
    <div style="display:flex;gap:8px;margin-top:10px">
      <button class="btn primary" id="authSubmit">${mode === "register" ? "Register" : "Login"}</button>
      <button class="btn ghost" id="toggle">${mode === "register" ? "Have an account? Login" : "New here? Register"}</button>
    </div>
  `);
  document.getElementById("toggle").onclick = () => openAuthModal(mode === "register" ? "login" : "register");
  document.getElementById("authSubmit").onclick = async () => {
    try {
      if (mode === "register") {
        const body = {
          name: v("#name"), email: v("#email"), password: v("#password"),
          blood_type: v("#blood_type"), is_donor: v("#is_donor") === "true"
        };
        const r = await api("/api/auth/register", { method: "POST", body, auth: false });
        state.token = r.token;
        localStorage.setItem("token", r.token);
      } else {
        const r = await api("/api/auth/login", {
          method: "POST", auth: false,
          body: { email: v("#email"), password: v("#password") }
        });
        state.token = r.token;
        localStorage.setItem("token", r.token);
      }
      toast("Welcome!");
      location.reload();
    } catch (e) { toast(e.message || "Auth failed", true); }
  }
}

function v(sel) { return document.querySelector(sel)?.value?.trim(); }

export {}
