let cart = JSON.parse(localStorage.getItem("seasonsCart")) || [];

function saveCart() {
    localStorage.setItem("seasonsCart", JSON.stringify(cart));
    updateCartUI();
}

function addToCart(id, name, price) {
    const item = cart.find(x => x.id == id);
    if (item) {
        item.quantity += 1;
    } else {
        cart.push({ id, name, price: parseFloat(price), quantity: 1 });
    }
    saveCart();
    openCart();
}

function updateQuantity(id, change) {
    const item = cart.find(x => x.id == id);
    if (!item) return;
    item.quantity += change;
    if (item.quantity <= 0) {
        cart = cart.filter(x => x.id != id);
    }
    saveCart();
}

function getCartTotal() {
    return cart.reduce((sum, item) => sum + (Number(item.price) * Number(item.quantity)), 0);
}

function updateCartUI() {
    const cartItems = document.getElementById("cart-items");
    const cartTotal = document.getElementById("cart-total");
    const cartCount = document.getElementById("cart-count");

    let total = 0;
    let count = 0;

    if (cartItems) cartItems.innerHTML = "";

    cart.forEach(item => {
        const subtotal = Number(item.price) * Number(item.quantity);
        total += subtotal;
        count += Number(item.quantity);

        if (cartItems) {
            cartItems.innerHTML += `
                <div class="cart-item">
                    <h6>${item.name}</h6>
                    <div class="d-flex justify-content-between align-items-center">
                        <span>₹${Number(item.price).toFixed(2)} × ${item.quantity}</span>
                        <div>
                            <button class="qty-btn" onclick="updateQuantity('${item.id}', -1)">-</button>
                            <span class="mx-2">${item.quantity}</span>
                            <button class="qty-btn" onclick="updateQuantity('${item.id}', 1)">+</button>
                        </div>
                    </div>
                    <b>₹${subtotal.toFixed(2)}</b>
                </div>
            `;
        }
    });

    if (cartTotal) cartTotal.innerText = total.toFixed(2);
    if (cartCount) cartCount.innerText = count;
}

function openCart() {
    document.getElementById("cartDrawer")?.classList.add("open");
    document.getElementById("overlay")?.classList.add("show");
    updateCartUI();
}

function closeCart() {
    document.getElementById("cartDrawer")?.classList.remove("open");
    document.getElementById("overlay")?.classList.remove("show");
}

function filterCategory(category, btn) {
    document.querySelectorAll(".cat-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");

    document.querySelectorAll(".menu-card-wrapper").forEach(card => {
        card.style.display = category === "All" || card.dataset.category === category ? "block" : "none";
    });
}

function togglePaymentBox() {
    const method = document.getElementById("payment_method")?.value;
    const paymentBox = document.getElementById("paymentBox");
    const upiAmount = document.getElementById("upiAmount");
    const upiPayLink = document.getElementById("upiPayLink");

    if (!paymentBox) return;

    const total = getCartTotal().toFixed(2);

    if (method === "UPI Online Payment") {
        paymentBox.style.display = "block";
        if (upiAmount) upiAmount.innerText = total;

        // Replace this UPI ID with actual cafe UPI ID in production.
        const upiId = "seasoncafe@upi";
        const upiName = "Sea Sons Cafe N Restro";
        const upiUrl = `upi://pay?pa=${encodeURIComponent(upiId)}&pn=${encodeURIComponent(upiName)}&am=${total}&cu=INR`;

        if (upiPayLink) upiPayLink.href = upiUrl;
    } else {
        paymentBox.style.display = "none";
    }
}

function loadCheckout() {
    const box = document.getElementById("checkout-cart");
    if (!box) return;

    if (cart.length === 0) {
        box.innerHTML = `<div class="alert alert-warning">Your cart is empty. Please go back and add items.</div>`;
        const form = document.getElementById("checkoutForm");
        if (form) form.style.display = "none";
        return;
    }

    let total = 0;
    let html = `
        <div class="bill-preview">
            <h5>Bill Preview</h5>
            <div class="bill-row bill-head">
                <span>Item</span>
                <span>Total</span>
            </div>
    `;

    cart.forEach(item => {
        const subtotal = Number(item.price) * Number(item.quantity);
        total += subtotal;
        html += `
            <div class="bill-row">
                <span>${item.name}<br><small>₹${Number(item.price).toFixed(2)} × ${item.quantity}</small></span>
                <strong>₹${subtotal.toFixed(2)}</strong>
            </div>
        `;
    });

    html += `
            <div class="bill-row grand-row">
                <span>Grand Total</span>
                <strong>₹${total.toFixed(2)}</strong>
            </div>
        </div>
    `;

    box.innerHTML = html;

    const grandTotal = document.getElementById("grandTotal");
    if (grandTotal) grandTotal.innerText = total.toFixed(2);

    togglePaymentBox();

    document.getElementById("checkoutForm").addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            customer_name: document.getElementById("customer_name").value,
            phone: document.getElementById("phone").value,
            table_no: document.getElementById("table_no").value,
            payment_method: document.getElementById("payment_method").value,
            cart
        };

        const response = await fetch("/place_order", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            window.location.href = `/success/${result.order_id}`;
        } else {
            alert(result.message);
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    updateCartUI();

    if (document.getElementById("checkoutForm")) {
        loadCheckout();
    }
});
