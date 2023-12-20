from flask_mail import Message
from flask import render_template
from db_directory.accessDB import GetDailyMailCustomers, GetMonthlyMailCustomers, GetMonthlyReport
from datetime import datetime


def get_previous_month():
    current_date = datetime.now()
    previous_month = current_date.month - 1 if current_date.month > 1 else 12
    return previous_month

def daily_email(mail):
        def send_email_text(mail,to, subject, body):
            msg = Message(subject=subject, recipients=to, body=body)     
            mail.send(msg)
        
        email_customers = GetDailyMailCustomers()
        if email_customers:
            try:
                send_email_text(mail,email_customers, 'Reminder', "It's been a while since you visited us. Get fresh groceries on your door steps!")
                return "Daily reminders sent successfully."
            except Exception as e:
                return str(e)
        else : return 'No customers found to send daily reminders.'

def monthly_report(mail):
        def send_email_html(mail,to, subject, template, **kwargs):
            msg = Message(subject=subject, recipients=[to], html=render_template(template, **kwargs))
            mail.send(msg)
        month= get_previous_month()
        customers = GetMonthlyMailCustomers(month)
        if customers:
            for customer in customers:
                cid=customer["customer_id"]
                orders, total_amount = GetMonthlyReport(cid,month)
                send_email_html(mail,str(customer["email"]), 'Monthly Report', 'monthly_report.html', customer=customer, orders=orders, total_amount=total_amount)
            return "Monthly reports sent successfully."
        else:
            return 'No customers found to send monthly reports.'