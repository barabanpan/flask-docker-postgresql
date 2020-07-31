from flask_mail import Message
from flask import current_app, jsonify
import time

from project import celery, mail


# bind needs self
@celery.task(bind=True)
def send_three_async_emails(self, email_data):
    """Send tree emails with 5 sec interval."""
    app = current_app._get_current_object()
    for i in range(1, 4):
        time.sleep(5)

        msg = Message(subject=email_data["subject"] + f"_{i}",
                      sender=app.config['MAIL_DEFAULT_SENDER'],
                      recipients=[email_data['to']])
        msg.body = email_data['body']

        with app.app_context():
            mail.send(msg)

        self.update_state(
            state='PROGRESS',
            meta={'current': f"{i} email(s) sent."}
        )
    return {"result": "3 messages were sent."}
