from flask import current_app as app
from application.models import *
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from flask import render_template

mail = Mail(app)

def monthly_report():
    with app.app_context():
        for customer in Customer.query.all():
            last_month_start_date = datetime.now() - timedelta(days=datetime.now().day)
            last_month_start_date = last_month_start_date.replace(day=1)

            # Filter orders of the last month for the current customer
            orders = (
                OrderDetails.query.filter_by(customer_id=customer.id)
                .filter(OrderDetails.order_date >= last_month_start_date)
                .all()
            )

            total_amount = total(orders)
            for order in orders:
                order_items = OrdersItems.query.filter_by(order_id=order.id).all()
                order['order_items'] = order_items
            send_email_html(str(customer.email), 'Monthly Report', 'monthly_report.html', customer=customer, orders=orders, total_amount=total_amount)

def daily_email():
     with app.app_context():
        none_login_customers = Customer.query.filter_by(last_login=None).all()
        not_logged_in_24hrs = Customer.query.filter(
            Customer.last_login - datetime.now() >= timedelta(days=1)
        ).all()
        email_customers = none_login_customers + not_logged_in_24hrs
        for customer in email_customers:
            send_email_text(str(customer.email), 'Reminder', "It's been a while since you visited us. Get fresh groceries on your door steps!")


def send_email_html(to, subject, template, **kwargs):
        msg = Message(subject, recipients=[to], html=render_template(template, **kwargs))
        mail.send(msg)
def send_email_text(to, subject, body):
        msg = Message(subject, recipients=[to], body=body)     
        mail.send(msg)

def total(orders):
        total_amount = 0
        for order in orders:
            total_amount += order.total_price
        return total_amount