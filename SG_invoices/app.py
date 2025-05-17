from flask import Flask, render_template
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta


app = Flask(__name__)


@app.route('/')
def hello_world():
    today = datetime.today().strftime("%B %d, %Y").replace(" 0", " ")
    invoice_number = 567
    sender_addr = {
        'company_name': 'Tani Saba Holdings',
        'addr1': '8663-00300',
        'addr2': 'Nairobi, Kenya'
    }
    recipients_addr = {
        'company_name': 'Supra Group',
        'person_name': 'Tani Saba',
        'person_email': 'gute_melden@gmail.com'
    }
    items = [
        {
            'title': 'Devops Consulting',
            'charge': 3000.00
        }, {
            'title': 'Data Lake',
            'charge': 4500.00
        }, {
            'title': 'Cloud Setup',
            'charge': 5500.00
        }
    ]
    due_date = (datetime.today() + relativedelta(months=2)
                ).strftime("%B %d, %Y").replace(" 0", " ")
    total = sum([i['charge'] for i in items])
    return render_template('invoices.html', date=today, sender_addr=sender_addr, recipients_addr=recipients_addr, items=items, total=total, invoice_number=invoice_number, due_date=due_date)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
