# Requires GTK3 runtime for windows available at https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
# Outputs pdf without styling --troubleshoot!!
from weasyprint import HTML, CSS
import os


os.environ['PATH'] += r';C:\Program Files\GTK3-Runtime Win64\bin'

html_file = HTML('invoices.html')
with open('invoices.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

base_css = CSS(string='''
    @page {
        size: A4;
        margin: 1cm;
    }
    body {
        font-family: Arial, sans-serif;
    }
''')

HTML(string=html_content).write_pdf(
    'invoice.pdf',
    stylesheets=[base_css]
)
