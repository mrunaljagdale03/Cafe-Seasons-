# Seasons Cafe Nashik - Updated QR Menu & Ordering System

This updated version includes:

- Customer scan menu without login
- Add to cart with quantity
- Proper bill preview after checkout
- Payment methods:
  - Pay at Counter
  - UPI Online Payment
  - Card at Counter
  - Cash at Counter
- UPI payment section for online payment
- Order confirmation page with full bill
- Admin dashboard shows:
  - Order items
  - Table number
  - Total bill
  - Payment method
  - Payment status
  - Order status
- Admin can update payment status manually
- Admin can print bill

## Run Steps

1. Start XAMPP MySQL.
2. Import `database.sql` in phpMyAdmin if not already imported.
3. Install packages:

```bash
pip install -r requirements.txt
```

4. Run:

```bash
python app.py
```

Customer side:

```text
http://127.0.0.1:5000/?table=1
```

Admin side:

```text
http://127.0.0.1:5000/admin
```

Login:

```text
admin
admin123
```

## Change Real UPI ID

Open `app.py` and update:

```python
"upi_id": "seasoncafe@upi"
```

Also open `static/js/script.js` and update:

```javascript
const upiId = "seasoncafe@upi";
```

Use the real cafe UPI ID here.
