# FinTrack Co. — Ko‘p formatli Hisob-faktura Generatori

Bu loyiha **Python** tilida yozilgan hisob-faktura generatori bo‘lib, mijozlar tanlagan ovqat va ichimliklarni hisobga olib, turli formatlarda (PDF, Excel, HTML) hisob-fakturalar yaratadi.

---

## 🛠 Qanday ishlaydi

1. Loyiha papkasiga kiring:
```bash
cd "C:\Users\yoqub\OneDrive\Desktop\Invoice generator"

python -m venv venv
venv\Scripts\activate

2. Virtual muhit yaratish: 
pip install reportlab openpyxl

3. Kerakli kutubxonalar:
pip install reportlab openpyxl

4. Skriptni ishga tushirish:
python main.py

5. Natijada, invoices/ papkada hisob-fakturalar hosil bo‘ladi:
PDF format: invoice_<client>_<timestamp>.pdf
Excel format: invoice_<client>_<timestamp>.xlsx
HTML format: invoice_<client>_<timestamp>.html

Kerakli kutubxonalar:
reportlab — PDF fayllarni yaratish uchun
openpyxl — Excel fayllarni yaratish uchun
datetime — vaqtni saqlash va formatlash
pathlib — fayl yo‘llari bilan ishlash
