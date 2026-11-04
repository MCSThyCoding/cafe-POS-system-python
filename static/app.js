/* Cafe POS front end (vanilla JS). Talks to the Flask REST API with a JWT. */
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const money = (n) => "$" + Number(n || 0).toFixed(2);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const todayStr = () => { const d = new Date(); d.setMinutes(d.getMinutes() - d.getTimezoneOffset()); return d.toISOString().slice(0, 10); };

  const state = { token: null, user: null, route: "pos", cart: [], payment: "Cash", category: "All", products: [], charts: [], reportType: "daily", reportDate: todayStr() };
  try { state.token = localStorage.getItem("cafe_token"); state.user = JSON.parse(localStorage.getItem("cafe_user") || "null"); } catch (_) {}

  // ---- API helper ---------------------------------------------------------
  async function api(path, opts = {}) {
    const headers = { "Content-Type": "application/json" };
    if (state.token) headers.Authorization = "Bearer " + state.token;
    const res = await fetch("/api" + path, { ...opts, headers, body: opts.body ? JSON.stringify(opts.body) : undefined });
    if (res.status === 401 && path !== "/login") { logout(); throw new Error("Session expired, please log in again"); }
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || "Request failed");
    }
    return res;
  }
  const getJSON = async (p) => (await api(p)).json();

  let toastTimer;
  function toast(msg, isErr = false) {
    const t = $("#toast"); t.textContent = msg; t.className = "toast" + (isErr ? " err" : "");
    clearTimeout(toastTimer); toastTimer = setTimeout(() => t.classList.add("hidden"), 3000);
  }

  // ---- Auth / shell -------------------------------------------------------
  function logout() {
    state.token = null; state.user = null; state.cart = [];
    try { localStorage.removeItem("cafe_token"); localStorage.removeItem("cafe_user"); } catch (_) {}
    show();
  }
  $("#logout").onclick = logout;

  $("#login-form").onsubmit = async (e) => {
    e.preventDefault();
    const err = $("#login-error"); err.classList.add("hidden");
    try {
      const res = await api("/login", { method: "POST", body: { username: $("#username").value, password: $("#password").value } });
      const data = await res.json();
      state.token = data.token; state.user = data.user; state.route = "pos";
      try { localStorage.setItem("cafe_token", data.token); localStorage.setItem("cafe_user", JSON.stringify(data.user)); } catch (_) {}
      $("#password").value = "";
      show();
    } catch (ex) { err.textContent = ex.message; err.classList.remove("hidden"); }
  };

  const NAV = [
    { id: "pos", label: "Point of Sale", icon: "☕", roles: ["admin", "cashier"] },
    { id: "dashboard", label: "Dashboard", icon: "▦", roles: ["admin", "cashier"] },
    { id: "inventory", label: "Inventory", icon: "📦", roles: ["admin", "cashier"] },
    { id: "reports", label: "Reports", icon: "📊", roles: ["admin"] },
  ];

  function show() {
    const loggedIn = !!(state.token && state.user);
    $("#login-view").classList.toggle("hidden", loggedIn);
    $("#app-view").classList.toggle("hidden", !loggedIn);
    if (!loggedIn) return;
    $("#who-name").textContent = state.user.full_name;
    $("#who-role").textContent = state.user.role;
    const items = NAV.filter((n) => n.roles.includes(state.user.role));
    if (!items.some((n) => n.id === state.route)) state.route = "pos";
    $("#nav").innerHTML = items.map((n) =>
      `<button class="nav-item ${n.id === state.route ? "active" : ""}" data-r="${n.id}"><span>${n.icon}</span>${n.label}</button>`).join("");
    $("#nav").querySelectorAll("button").forEach((b) => (b.onclick = () => { state.route = b.dataset.r; show(); }));
    render();
  }

  async function render() {
    state.charts.forEach((c) => c.destroy()); state.charts = [];
    const page = $("#page");
    page.innerHTML = '<p class="muted">Loading…</p>';
    try {
      await ({ pos: renderPOS, dashboard: renderDashboard, inventory: renderInventory, reports: renderReports }[state.route])(page);
    } catch (ex) { if (state.token) page.innerHTML = `<p class="error">${esc(ex.message)}</p>`; }
  }

  // ---- Cashier: Point of Sale --------------------------------------------
  async function renderPOS(page) {
    state.products = await getJSON("/products");
    const cats = ["All", ...new Set(state.products.map((p) => p.category))];
    page.innerHTML = `
      <div class="page-head"><h2>Point of Sale</h2><span class="cart-pill" id="cart-count"></span></div>
      <div class="pos">
        <div>
          <div class="chips">${cats.map((c) => `<button class="chip ${c === state.category ? "active" : ""}" data-c="${esc(c)}">${esc(c)}</button>`).join("")}</div>
          <div class="products" id="products"></div>
        </div>
        <div class="card cart" id="cart"></div>
      </div>`;
    page.querySelectorAll(".chip").forEach((b) => (b.onclick = () => { state.category = b.dataset.c; renderPOS(page); }));
    drawProducts(); drawCart();
  }

  function drawProducts() {
    const list = state.products.filter((p) => state.category === "All" || p.category === state.category);
    $("#products").innerHTML = list.map((p) => `
      <button class="product" data-id="${p.id}" ${p.stock <= 0 ? "disabled" : ""}>
        <span class="tag">${esc(p.category)}</span>
        <div class="em">${p.emoji}</div>
        <div class="nm">${esc(p.name)}</div>
        <div class="pr">${money(p.price)}</div>
        <div class="st ${p.low_stock ? "low" : ""}">${p.stock <= 0 ? "Out of stock" : p.stock + " in stock"}</div>
      </button>`).join("");
    $("#products").querySelectorAll(".product").forEach((b) => (b.onclick = () => addToCart(+b.dataset.id)));
  }

  function addToCart(id) {
    const p = state.products.find((x) => x.id === id);
    const line = state.cart.find((l) => l.id === id);
    const inCart = line ? line.qty : 0;
    if (inCart + 1 > p.stock) return toast(`Only ${p.stock} ${p.name} in stock`, true);
    if (line) line.qty++; else state.cart.push({ id, name: p.name, price: p.price, qty: 1 });
    drawCart();
  }

  function changeQty(id, delta) {
    const line = state.cart.find((l) => l.id === id); if (!line) return;
    const p = state.products.find((x) => x.id === id);
    if (delta > 0 && line.qty + 1 > p.stock) return toast(`Only ${p.stock} ${p.name} in stock`, true);
    line.qty += delta;
    if (line.qty <= 0) state.cart = state.cart.filter((l) => l.id !== id);
    drawCart();
  }

  function drawCart() {
    const count = state.cart.reduce((s, l) => s + l.qty, 0);
    const total = state.cart.reduce((s, l) => s + l.qty * l.price, 0);
    $("#cart-count").textContent = `🛒 ${count} items`;
    const box = $("#cart");
    box.innerHTML = `<h3>🛒 Current Order</h3>` + (state.cart.length ? `
      ${state.cart.map((l) => `
        <div class="cart-line">
          <div class="n">${esc(l.name)}<br><small>${money(l.price)} each</small></div>
          <div class="qty">
            <button data-d="-1" data-id="${l.id}" aria-label="Decrease">−</button><b>${l.qty}</b>
            <button data-d="1" data-id="${l.id}" aria-label="Increase">+</button>
            <button class="del" data-del="${l.id}" aria-label="Remove">🗑</button>
          </div>
        </div>`).join("")}
      <div class="total-row"><span>Total:</span><b id="cart-total">${money(total)}</b></div>
      <div class="pay">
        <button data-pay="Cash" class="${state.payment === "Cash" ? "on" : ""}">$ Cash</button>
        <button data-pay="Card" class="${state.payment === "Card" ? "on" : ""}">💳 Card</button>
      </div>
      <button class="btn btn-primary btn-block" id="complete">Complete Order</button>`
      : `<div class="cart-empty"><div class="big">🛒</div>Cart is empty</div>`);
    box.querySelectorAll("[data-d]").forEach((b) => (b.onclick = () => changeQty(+b.dataset.id, +b.dataset.d)));
    box.querySelectorAll("[data-del]").forEach((b) => (b.onclick = () => { state.cart = state.cart.filter((l) => l.id !== +b.dataset.del); drawCart(); }));
    box.querySelectorAll("[data-pay]").forEach((b) => (b.onclick = () => { state.payment = b.dataset.pay; drawCart(); }));
    const done = $("#complete"); if (done) done.onclick = completeOrder;
  }

  async function completeOrder() {
    const btn = $("#complete"); btn.disabled = true;
    try {
      const res = await api("/orders", { method: "POST", body: { payment_method: state.payment, items: state.cart.map((l) => ({ product_id: l.id, quantity: l.qty })) } });
      const o = await res.json();
      state.cart = [];
      showReceipt(o);
      state.products = await getJSON("/products"); drawProducts(); drawCart();   // stock was deducted
    } catch (ex) { toast(ex.message, true); btn.disabled = false; }
  }

  function showReceipt(o) {
    const m = $("#modal");
    m.innerHTML = `<div class="modal-box" role="dialog" aria-modal="true">
      <div class="ok">✔</div><h3>Order Completed!</h3>
      <p class="muted">Your order has been successfully processed</p>
      <div class="lbl">Order #</div><b>${o.order_id}</b>
      <div class="lbl">Payment Method:</div><b>${esc(o.payment_method)}</b>
      <div class="lbl">Total Amount:</div><div class="amt">${money(o.total)}</div>
      <button class="btn btn-primary btn-block" id="close-modal" style="margin-top:22px">New Order</button></div>`;
    m.classList.remove("hidden");
    const close = () => m.classList.add("hidden");
    $("#close-modal").onclick = close; m.onclick = (e) => { if (e.target === m) close(); };
    $("#close-modal").focus();
  }

  // ---- Dashboard (price analysis) ----------------------------------------
  const PALETTE = ["#e9a23b", "#52b788", "#4f83e8", "#a855f7", "#ef6f6c"];
  async function renderDashboard(page) {
    const d = await getJSON("/dashboard");
    page.innerHTML = `
      <div class="page-head"><h2>Dashboard</h2></div>
      ${d.low_stock.length ? `<div class="alert">⚠ Low stock: ${d.low_stock.map((x) => `${esc(x.name)} (${x.stock})`).join(", ")}</div>` : ""}
      <div class="grid4">
        ${statCard("Today's Revenue", money(d.revenue), "$", "#52b788")}
        ${statCard("Today's Orders", d.orders, "🛒", "#4f83e8")}
        ${statCard("Average Order", money(d.average_order), "↗", "#a855f7")}
        ${statCard("Total Products", d.total_products, "📦", "#e9a23b")}
      </div>
      <div class="grid2">
        <div class="card"><h3>Sales by Category</h3><div class="chart-box"><canvas id="c-cat"></canvas></div></div>
        <div class="card"><h3>Top Selling Products</h3><div class="chart-box"><canvas id="c-top"></canvas></div></div>
      </div>
      <div class="card table-card"><h3 style="padding:20px 20px 0">Recent Orders</h3>
        <table><thead><tr><th>Order ID</th><th>Customer</th><th>Total</th><th>Payment</th><th>Time</th></tr></thead>
        <tbody>${d.recent_orders.map((o) => `<tr><td>#${o.id}</td><td>${esc(o.customer)}</td><td class="price">${money(o.total)}</td><td>${esc(o.payment_method)}</td><td>${esc(o.created_at)}</td></tr>`).join("") || '<tr><td colspan="5" class="muted">No orders yet</td></tr>'}</tbody></table></div>`;
    empty("c-cat", d.sales_by_category.length, "No sales today");
    if (d.sales_by_category.length) state.charts.push(new Chart($("#c-cat"), { type: "pie", data: { labels: d.sales_by_category.map((x) => x.name), datasets: [{ data: d.sales_by_category.map((x) => x.value), backgroundColor: PALETTE }] }, options: { maintainAspectRatio: false } }));
    empty("c-top", d.top_products.length, "No sales today");
    if (d.top_products.length) state.charts.push(new Chart($("#c-top"), { type: "bar", data: { labels: d.top_products.map((x) => x.name), datasets: [{ label: "Units sold", data: d.top_products.map((x) => x.value), backgroundColor: "#e9a23b" }] }, options: { maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } } }));
  }
  const statCard = (label, val, icon, color) => `<div class="card stat"><div><small>${label}</small><div class="v">${val}</div></div><div class="ic" style="background:${color}">${icon}</div></div>`;
  function empty(canvasId, n, msg) { if (!n) $("#" + canvasId).parentElement.innerHTML = `<p class="muted">${msg}</p>`; }

  // ---- Inventory ---------------------------------------------------------
  async function renderInventory(page) {
    const items = await getJSON("/inventory");
    const isAdmin = state.user.role === "admin";
    page.innerHTML = `
      <div class="page-head"><h2>Inventory Management</h2></div>
      <input class="search" id="q" placeholder="🔍 Search products...">
      <div class="card table-card"><table>
        <thead><tr><th>Product</th><th>Category</th><th>Stock Level</th><th>Quantity</th><th>Price</th>${isAdmin ? "<th>Actions</th>" : ""}</tr></thead>
        <tbody id="inv"></tbody></table></div>`;
    const draw = () => {
      const q = $("#q").value.toLowerCase();
      $("#inv").innerHTML = items.filter((p) => p.name.toLowerCase().includes(q) || p.category.toLowerCase().includes(q)).map((p) => {
        const lvl = p.stock <= 0 ? ["out", "Out"] : p.low_stock ? ["low", "Low"] : ["good", "Good"];
        return `<tr><td>${p.emoji} ${esc(p.name)}</td><td><span class="pill">${esc(p.category)}</span></td>
          <td><span class="dot ${lvl[0]}"></span>${lvl[1]}</td><td><b>${p.stock}</b></td><td class="price">${money(p.price)}</td>
          ${isAdmin ? `<td><button class="btn btn-primary btn-sm" data-id="${p.id}">+ Add 10</button></td>` : ""}</tr>`;
      }).join("");
      $("#inv").querySelectorAll("button").forEach((b) => (b.onclick = async () => {
        try {
          const upd = await (await api(`/inventory/${b.dataset.id}/restock`, { method: "POST", body: { quantity: 10 } })).json();
          Object.assign(items.find((x) => x.id === upd.id), upd); draw(); toast(`${upd.name} restocked (+10)`);
        } catch (ex) { toast(ex.message, true); }
      }));
    };
    $("#q").oninput = draw; draw();
  }

  // ---- Admin: Reports ----------------------------------------------------
  async function renderReports(page) {
    const type = state.reportType || "daily";
    const date = state.reportDate || todayStr();
    const r = await getJSON("/reports?type=" + type + "&date=" + date);
    
    const periodLabel = type === "daily" ? "Date" : type === "monthly" ? "Month" : "Year";
    const dateInputType = type === "daily" ? "date" : type === "monthly" ? "month" : "year";
    const dateValue = type === "daily" ? r.date : type === "monthly" ? r.date + "-01" : r.date + "-01-01";
    const trendLabel = type === "daily" ? "Day of month" : type === "monthly" ? "Day of month" : "Month of year";
    
    page.innerHTML = `
      <div class="page-head"><h2>Reports &amp; Analytics</h2><button class="btn btn-primary" id="export">⬇ Export Report</button></div>
      <div class="card date-bar">
        <span>📅 Period:</span>
        <select id="report-type" class="select">
          <option value="daily" ${type === "daily" ? "selected" : ""}>Daily</option>
          <option value="monthly" ${type === "monthly" ? "selected" : ""}>Monthly</option>
          <option value="yearly" ${type === "yearly" ? "selected" : ""}>Yearly</option>
        </select>
        <span style="margin-left:12px">📅 Select ${periodLabel}:</span>
        <input type="${dateInputType}" id="date" value="${dateValue}">
      </div>
      <div class="grid4">
        <div class="card stat"><div><small>Total Revenue</small><div class="v green">${money(r.revenue)}</div></div></div>
        <div class="card stat"><div><small>Total Cost</small><div class="v red">${money(r.cost)}</div></div></div>
        <div class="card stat"><div><small>Profit</small><div class="v green">${money(r.profit)}</div></div></div>
        <div class="card stat"><div><small>Total Orders</small><div class="v blue">${r.orders}</div></div></div>
      </div>
      <div class="grid2">
        <div class="card"><h3>Revenue Trend</h3><div class="chart-box"><canvas id="c-trend"></canvas></div></div>
        <div class="card"><h3>Profit by Product</h3><div class="chart-box"><canvas id="c-profit"></canvas></div></div>
      </div>
      <div class="card table-card"><h3 style="padding:20px 20px 0">Profit Analysis (Decision Support)</h3>
        <table><thead><tr><th>Product</th><th>Category</th><th>Units</th><th>Revenue</th><th>Cost</th><th>Profit</th><th>Margin</th><th>Advice</th></tr></thead>
        <tbody>${r.products.map((p) => `<tr><td>${esc(p.name)}</td><td><span class="pill">${esc(p.category)}</span></td><td>${p.units}</td><td>${money(p.revenue)}</td><td>${money(p.cost)}</td><td class="price">${money(p.profit)}</td><td>${p.margin}%</td>
          <td class="${p.advice.startsWith("Promote") ? "advice-promote" : p.advice.startsWith("Review") ? "advice-review" : ""}">${esc(p.advice)}</td></tr>`).join("") || '<tr><td colspan="8" class="muted">No sales data</td></tr>'}</tbody></table></div>
      <div class="card table-card" style="margin-top:20px"><h3 style="padding:20px 20px 0">Reports by Category</h3>
        <table><thead><tr><th>Category</th><th>Revenue</th><th>Profit</th></tr></thead>
        <tbody>${r.categories.map((c) => `<tr><td>${esc(c.category)}</td><td>${money(c.revenue)}</td><td class="price">${money(c.profit)}</td></tr>`).join("") || '<tr><td colspan="3" class="muted">No sales data</td></tr>'}</tbody></table></div>`;
    
    $("#report-type").onchange = (e) => { 
      state.reportType = e.target.value;
      if (e.target.value === "daily") {
        state.reportDate = todayStr();
      } else if (e.target.value === "monthly") {
        state.reportDate = todayStr().slice(0, 7);
      } else {
        state.reportDate = todayStr().slice(0, 4);
      }
      render(); 
    };
    $("#date").onchange = (e) => { 
      if (e.target.value) { 
        state.reportDate = e.target.value; 
        render(); 
      } 
    };
    $("#export").onclick = async () => {
      try {
        const blob = await (await api("/reports/export?type=" + type + "&date=" + r.date)).blob();
        const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(blob), download: `report-${type}-${r.date}.txt` });
        document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(a.href);
      } catch (ex) { toast(ex.message, true); }
    };
    empty("c-trend", r.trend.length, "No revenue data");
    if (r.trend.length) state.charts.push(new Chart($("#c-trend"), { type: "line", data: { labels: r.trend.map((t) => t.day), datasets: [{ label: "Revenue", data: r.trend.map((t) => t.revenue), borderColor: "#e9a23b", backgroundColor: "#e9a23b", tension: .25 }] }, options: { maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true }, x: { title: { display: true, text: trendLabel } } } } }));
    empty("c-profit", r.products.length, "No sales data");
    if (r.products.length) state.charts.push(new Chart($("#c-profit"), { type: "bar", data: { labels: r.products.map((p) => p.name), datasets: [{ label: "Profit", data: r.products.map((p) => p.profit), backgroundColor: "#52b788" }] }, options: { maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } } }));
  }

  show();
})();
