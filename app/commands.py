import os
import click
from datetime import datetime, timedelta
from flask.cli import with_appcontext
from app import db
from app.models import Case
from twilio.rest import Client as TwilioClient
from flask import current_app

@click.command('send_reminders')
@with_appcontext
def send_reminders():
    """Send SMS reminders for cases with hearings tomorrow."""
    # Calculate tomorrow's date
    tomorrow = datetime.now().date() + timedelta(days=1)

    # Find cases
    cases = Case.query.filter(Case.next_hearing_date == tomorrow).all()

    if not cases:
        print("No hearings found for tomorrow.")
        return

    # Twilio setup
    account_sid = current_app.config.get('TWILIO_SID')
    auth_token = current_app.config.get('TWILIO_AUTH_TOKEN')
    from_number = current_app.config.get('TWILIO_FROM_NUMBER')

    if not account_sid or not auth_token or not from_number:
        print("Twilio configuration missing. Please set TWILIO_SID, TWILIO_AUTH_TOKEN, and TWILIO_FROM_NUMBER.")
        return

    client = TwilioClient(account_sid, auth_token)

    for case in cases:
        if case.client and case.client.phone_number:
            message_body = (
                f"Reminder: You have a hearing tomorrow ({case.next_hearing_date}) for case "
                f"{case.case_number}: {case.case_title} at {case.court_name}."
            )
            try:
                message = client.messages.create(
                    body=message_body,
                    from_=from_number,
                    to=case.client.phone_number
                )
                print(f"Sent SMS to {case.client.name} ({case.client.phone_number}): {message.sid}")
            except Exception as e:
                print(f"Failed to send SMS to {case.client.name}: {e}")
        else:
            print(f"Skipping case {case.case_number}: Client phone number missing.")
