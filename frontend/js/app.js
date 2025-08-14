// Base API URL — you can set this in browser console for local/prod
const API_BASE = localStorage.getItem("api_base") || "http://localhost:5000";
const API = (p) => `${API_BASE}${p}`;

const state = {
  token: localStorage.getItem("token"),
  me: null,
};

async function api(path, { method = "GET", body, auth = true } = {}) {
  const res = await fetch(API(path), {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(auth && state.token ? { "Authorization": "Bearer " + state.token } : {})
    },
    body: body ? JSON.stringify(body) : undefined
  });
  if (!res.ok) {
    const t = await res.text().catch(() => "");
    throw new Error(t || res.statusText);
  }
  return res.json();
}

function toast(msg, isError = false) {
  const el = document.querySelector(".notice");
  if (!el) return alert(msg);
  el.textContent = msg;
  el.classList.toggle("error", !!isError);
  el.style.display = "block";
  setTimeout(() => el.style.display = "none", 3000);
}

export { state, api, toast, API_BASE, API };
