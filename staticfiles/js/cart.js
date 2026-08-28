/**
 * Doche Concessionaries — Client-Side Cart Engine
 * Persists in localStorage. Works across all pages.
 */

const CART_KEY = 'doche_cart';
const OWNER_PHONE = '2349077925555'; // WhatsApp number

// ─── Storage Helpers ──────────────────────────────────────────────
function getCart() {
  try {
    return JSON.parse(localStorage.getItem(CART_KEY)) || [];
  } catch {
    return [];
  }
}

function saveCart(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
}

function clearCart() {
  localStorage.removeItem(CART_KEY);
}

// ─── Cart Operations ─────────────────────────────────────────────
function addToCart(id, name, price, badge, imageUrl) {
  const cart = getCart();
  const existing = cart.find(item => item.id === id);
  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({ id, name, price: parseFloat(price), badge, imageUrl, qty: 1 });
  }
  saveCart(cart);
  updateCartUI();
  showCartToast(name);
}

// Helper: reads qty from an input by ID, then adds to cart
function addToCartFromCard(id, name, price, badge, imageUrl, qtyInputId) {
  const qtyInput = document.getElementById(qtyInputId);
  const qty = qtyInput ? Math.max(1, parseInt(qtyInput.value) || 1) : 1;
  const cart = getCart();
  const existing = cart.find(item => item.id === id);
  if (existing) {
    existing.qty += qty;
  } else {
    cart.push({ id, name, price: parseFloat(price), badge, imageUrl, qty });
  }
  saveCart(cart);
  updateCartUI();
  showCartToast(name);
}

// Helper: reads all product data from button's data-* attributes (no Django inline JS)
function addToCartFromDataset(btn) {
  const d = btn.dataset;
  addToCartFromCard(
    parseInt(d.id), d.name, parseFloat(d.price),
    d.badge, d.image, d.qty
  );
}

function removeFromCart(id) {
  const cart = getCart().filter(item => item.id !== id);
  saveCart(cart);
  updateCartUI();
}

function updateQty(id, delta) {
  const cart = getCart();
  const item = cart.find(item => item.id === id);
  if (item) {
    item.qty = Math.max(1, item.qty + delta);
    saveCart(cart);
    updateCartUI();
  }
}

function setQty(id, qty) {
  const qty_n = parseInt(qty, 10);
  if (isNaN(qty_n) || qty_n < 1) return;
  const cart = getCart();
  const item = cart.find(item => item.id === id);
  if (item) {
    item.qty = qty_n;
    saveCart(cart);
    updateCartUI();
  }
}

function cartTotal() {
  return getCart().reduce((sum, item) => sum + item.price * item.qty, 0);
}

function cartCount() {
  return getCart().reduce((sum, item) => sum + item.qty, 0);
}

// ─── Format Numbers with Commas ──────────────────────────────────
function fmt(n) {
  return Number(n).toLocaleString('en-NG', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// ─── Toast Notification ──────────────────────────────────────────
function showCartToast(productName) {
  let toast = document.getElementById('cartToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'cartToast';
    toast.className = 'cart-toast';
    document.body.appendChild(toast);
  }
  toast.textContent = `✓ ${productName} added to order`;
  toast.classList.add('show');
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.remove('show'), 2800);
}

// ─── Cart Panel HTML ─────────────────────────────────────────────
function renderCartPanel() {
  const cart = getCart();
  const panel = document.getElementById('cartPanel');
  if (!panel) return;

  const itemsHtml = cart.length === 0
    ? `<div class="cart-empty">
         <div class="cart-empty-icon">🛒</div>
         <p>Your order is empty.</p>
         <a href="/products/" class="btn-primary" style="margin-top:14px;font-size:0.85rem;padding:10px 20px;">Browse Products</a>
       </div>`
    : cart.map(item => `
      <div class="cart-item" data-id="${item.id}">
        <div class="cart-item-img">
          <img src="${item.imageUrl}" alt="${item.name}" loading="lazy">
        </div>
        <div class="cart-item-info">
          <div class="cart-item-name">${item.name}</div>
          <div class="cart-item-badge">${item.badge}</div>
          <div class="cart-item-price">₦${fmt(item.price)} each</div>
          <div class="cart-qty-row">
            <button class="cart-qty-btn" onclick="updateQty(${item.id}, -1)">−</button>
            <input class="cart-qty-input" type="number" min="1" value="${item.qty}"
              onchange="setQty(${item.id}, this.value)" />
            <button class="cart-qty-btn" onclick="updateQty(${item.id}, 1)">+</button>
            <button class="cart-remove-btn" onclick="removeFromCart(${item.id})" title="Remove">🗑</button>
          </div>
          <div class="cart-item-subtotal">Subtotal: ₦${fmt(item.price * item.qty)}</div>
        </div>
      </div>`).join('');

  const total = cartTotal();
  const scheduleUrl = buildScheduleUrl();
  const whatsappUrl = buildWhatsAppUrl();

  panel.querySelector('.cart-items-wrap').innerHTML = itemsHtml;

  const footer = panel.querySelector('.cart-footer');
  footer.innerHTML = cart.length === 0 ? '' : `
    <div class="cart-total-row">
      <span>Estimated Total</span>
      <span class="cart-total-amount">₦${fmt(total)}</span>
    </div>
    <p class="cart-total-note">Final price confirmed by owner based on exact specs.</p>
    <a href="${scheduleUrl}" class="btn-primary cart-action-btn">
      📅 Schedule Delivery
    </a>
    <a href="${whatsappUrl}" target="_blank" rel="noopener" class="btn-whatsapp cart-action-btn">
      💬 Send Order via WhatsApp
    </a>
    <button class="cart-clear-btn" onclick="confirmClearCart()">Clear Order</button>
  `;
}

// ─── Build URLs ──────────────────────────────────────────────────
function buildScheduleUrl() {
  const cart = getCart();
  if (cart.length === 0) return '/booking/';
  const notes = cart.map(i => `${i.qty}x ${i.name}`).join(', ');
  return `/booking/?cart_notes=${encodeURIComponent(notes)}&cart_total=${encodeURIComponent(cartTotal())}`;
}

function buildWhatsAppUrl() {
  const cart = getCart();
  const lines = cart.map(i => `  • ${i.qty}x ${i.name} @ ₦${fmt(i.price)} = ₦${fmt(i.price * i.qty)}`).join('\n');
  const total = fmt(cartTotal());
  const msg = `Hello Doche Concessionaries! 🎂\n\nI'd like to place a *Bulk Order*:\n\n${lines}\n\n*Estimated Total: ₦${total}*\n\nPlease confirm availability and delivery date. Thank you!`;
  return `https://wa.me/${OWNER_PHONE}?text=${encodeURIComponent(msg)}`;
}

function confirmClearCart() {
  if (confirm('Clear your entire order? This cannot be undone.')) {
    clearCart();
    updateCartUI();
  }
}

// ─── Badge & Global UI Update ────────────────────────────────────
function updateCartUI() {
  const count = cartCount();

  // Update all badge elements
  document.querySelectorAll('.cart-count-badge').forEach(el => {
    el.textContent = count;
    el.style.display = count > 0 ? 'flex' : 'none';
  });

  // Re-render panel if open
  renderCartPanel();
}

// ─── Cart Panel Toggle ───────────────────────────────────────────
function toggleCart() {
  const panel = document.getElementById('cartPanel');
  const overlay = document.getElementById('cartOverlay');
  if (!panel) return;

  const isOpen = panel.classList.contains('is-open');
  if (isOpen) {
    closeCartPanel();
  } else {
    renderCartPanel();
    panel.classList.add('is-open');
    overlay.classList.add('is-visible');
    document.body.style.overflow = 'hidden';
  }
}

function closeCartPanel() {
  const panel = document.getElementById('cartPanel');
  const overlay = document.getElementById('cartOverlay');
  if (panel) panel.classList.remove('is-open');
  if (overlay) overlay.classList.remove('is-visible');
  document.body.style.overflow = '';
}

// ─── Prefill booking form from cart ─────────────────────────────
function prefillBookingFromCart() {
  const params = new URLSearchParams(window.location.search);
  const cartNotes = params.get('cart_notes');
  const cartTotal_val = params.get('cart_total');

  if (cartNotes) {
    const notesField = document.getElementById('id_quantity_notes');
    if (notesField && !notesField.value) {
      notesField.value = `BULK ORDER:\n${cartNotes}\n\nEstimated Total: ₦${fmt(cartTotal_val || 0)}`;
    }
    // Update live price estimate
    const priceEl = document.getElementById('live_price_est');
    if (priceEl && cartTotal_val) {
      priceEl.textContent = '₦' + fmt(cartTotal_val);
    }
  }
}

// ─── Inject Cart HTML into page ──────────────────────────────────
function injectCartDOM() {
  // Cart toggle button (added inside nav by base.html, but badge needs JS)
  // Cart slide panel
  if (!document.getElementById('cartPanel')) {
    const panelHtml = `
      <div id="cartOverlay" class="cart-overlay" onclick="closeCartPanel()"></div>
      <aside id="cartPanel" class="cart-panel" role="dialog" aria-label="Order Cart">
        <div class="cart-panel-header">
          <h2 class="cart-panel-title">🛒 Your Order</h2>
          <button class="cart-panel-close" onclick="closeCartPanel()" aria-label="Close cart">✕</button>
        </div>
        <div class="cart-items-wrap"></div>
        <div class="cart-footer"></div>
      </aside>`;
    document.body.insertAdjacentHTML('beforeend', panelHtml);
  }
}

// ─── Init ────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  injectCartDOM();
  updateCartUI();
  prefillBookingFromCart();

  // Escape key closes cart
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeCartPanel();
  });
});
