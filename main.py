from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer
from reportlab.lib.styles import getSampleStyleSheet

MENU = {
    "Burger": 8.5,"Pizza": 12.0,"Pasta": 10.0,"Salad": 6.0,
    "Sushi": 15.0,"Steak": 20.0,"Sandwich": 7.0,"Fries": 3.5,
    "Soup": 5.0,"Ice Cream": 4.0,"Cola": 2.0,"Water": 1.5,
    "Juice": 3.0, "Coffee": 2.5,"Tea": 2.0
}

class TaxMixin:
    TAX_RATE = 0.10  # 10%

    def apply_tax(self, subtotal):
        return round(subtotal * (1 + self.TAX_RATE), 2)

class InvoiceGenerator(ABC):
    def __init__(self, client_name, items):
        self.client_name = client_name
        self.items = items
        self.created_at = datetime.now()

    def calculate_total(self):
        subtotal = sum(i['price'] for i in self.items)
        if isinstance(self, TaxMixin):
            return self.apply_tax(subtotal)
        return round(subtotal, 2)

    @abstractmethod
    def generate_invoice(self, output_dir: Path):
        pass

class PDFInvoiceGenerator(TaxMixin, InvoiceGenerator):
    def generate_invoice(self, output_dir: Path):
        output_dir.mkdir(exist_ok=True)
        filepath = output_dir / f"invoice_{self.client_name}_{self.created_at:%Y%m%d_%H%M%S}.pdf"

        doc = SimpleDocTemplate(str(filepath))
        styles = getSampleStyleSheet()
        story = [
            Paragraph(f"Invoice for: {self.client_name}", styles['Title']),
            Paragraph(f"Created: {self.created_at:%Y-%m-%d %H:%M:%S}", styles['Normal']),
            Spacer(1,12)
        ]
        data = [["Product","Price"]] + [[i['name'], f"{i['price']:.2f}"] for i in self.items] + [["Total", f"{self.calculate_total():.2f}"]]
        table = Table(data)
        story.append(table)
        doc.build(story)
        return filepath

class ExcelInvoiceGenerator(TaxMixin, InvoiceGenerator):
    def generate_invoice(self, output_dir: Path):
        output_dir.mkdir(exist_ok=True)
        filepath = output_dir / f"invoice_{self.client_name}_{self.created_at:%Y%m%d_%H%M%S}.xlsx"

        wb = Workbook()
        ws = wb.active
        ws.append(["Product","Price"])
        for i in self.items:
            ws.append([i['name'], i['price']])
        ws.append(["Total", self.calculate_total()])
        ws.append(["Created", self.created_at.strftime("%Y-%m-%d %H:%M:%S")])
        wb.save(filepath)
        return filepath

class HTMLInvoiceGenerator(TaxMixin, InvoiceGenerator):
    def generate_invoice(self, output_dir: Path):
        output_dir.mkdir(exist_ok=True)
        filepath = output_dir / f"invoice_{self.client_name}_{self.created_at:%Y%m%d_%H%M%S}.html"
        items_html = "".join(f"<tr><td>{i['name']}</td><td>{i['price']:.2f}</td></tr>" for i in self.items)
        html_content = f"""
        <html><body>
        <h1>Invoice for {self.client_name}</h1>
        <p>Created: {self.created_at:%Y-%m-%d %H:%M:%S}</p>
        <table border="1">
        <tr><th>Product</th><th>Price</th></tr>
        {items_html}
        <tr><td>Total (+10% tax)</td><td>{self.calculate_total():.2f}</td></tr>
        </table>
        </body></html>
        """
        filepath.write_text(html_content, encoding="utf-8")
        return filepath

class InvoiceManager:
    def __init__(self, generator: InvoiceGenerator, invoices_dir: Path):
        self.generator = generator
        self.invoices_dir = invoices_dir

    def export_invoice(self):
        return self.generator.generate_invoice(self.invoices_dir)

class InvoiceFactory:
    @staticmethod
    def get_generator(fmt, client_name, items):
        fmt = fmt.lower()
        if fmt == "pdf": return PDFInvoiceGenerator(client_name, items)
        if fmt in ("excel","xlsx"): return ExcelInvoiceGenerator(client_name, items)
        if fmt == "html": return HTMLInvoiceGenerator(client_name, items)
        raise ValueError(f"Unsupported format: {fmt}")

if __name__=="__main__":
    out_dir = Path.cwd() / "invoices"

    print("Menyu:")
    for k, v in MENU.items():
        print(f"{k}: ${v}")

    items = []
    while True:
        choice = input("Mahsulot yoki ichimlik tanlang (yoki 'stop'): ")
        if choice.lower() == "stop":
            break
        if choice not in MENU:
            print("Menyu mavjud emas, qaytadan tanlang!")
            continue
        items.append({"name": choice, "price": MENU[choice]})
        print(f"{choice} qo'shildi - ${MENU[choice]}")

    if not items:
        print("Buyurtma yo'q. Dastur tugadi.")
    else:
        client = input("Mijoz nomi: ")
        for fmt in ["pdf","excel","html"]:
            gen = InvoiceFactory.get_generator(fmt, client, items)
            mgr = InvoiceManager(gen, out_dir)
            try:
                path = mgr.export_invoice()
                print(f"{fmt.upper()} invoice created: {path}")
            except Exception as e:
                print(f"Failed to create {fmt} invoice: {e}")
