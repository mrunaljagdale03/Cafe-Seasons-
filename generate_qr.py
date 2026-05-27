import os
import segno

BASE_URL = "http://192.168.1.10:5000"

os.makedirs("qr_codes", exist_ok=True)

for table in range(1, 11):
    url = f"{BASE_URL}/?table={table}"
    qr = segno.make(url)

    qr.save(
        f"qr_codes/table_{table}_qr.svg",
        scale=10,
        border=4
    )

print("QR codes created successfully in qr_codes folder.")