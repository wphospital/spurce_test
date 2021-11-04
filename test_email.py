from sprucepy.notifier import Email, get_recipient_emails, get_recipients, get_recipient_attrs
import click
import datetime as dt
import yaml
import os
from pytz import timezone


def _today():
    return dt.date.today()


def _today_pretty():
    return _today().strftime('%a %B %d, %Y')


def _yesterday():
    return dt.date.today() - dt.timedelta(days=1)


def _yesterday_pretty():
    return _yesterday().strftime('%a %B %d, %Y')


def _now():
    return dt.datetime.now().astimezone(timezone('America/New_York'))


def _now_pretty():
    return _now().strftime('%a %B %d, %Y %H:%M %Z')


@click.command()
@click.option('--email_subject', default='Extracted data')
@click.option('--smtpserver')
def main(
    email_subject,
    smtpserver
):
    task_id = os.getenv('TASK_ID')
    run_id = os.getenv('RUN_ID')

    if smtpserver is None:
        smptserver = os.getenv('smptserver', 'SMTPRelay.montefiore.org')

    default_smtp = f' (default)' if os.getenv('smptserver') is None else ''

    # Email subject
    # email_subject = 'Extracted data'

    now = _now_pretty()

    # Email body
    email_body = f'''
    <html>
        <head>
        </head>
        <body>
            <p>Hello,</p>
            <p>
                This is a test email from Spruce!
                This email was generated <b>{now}</b>.

                Sent using {smtpserver}{default_smtp}.
            </p>
            <p>
                Please email <a href="mailto: jsege@wphospital.org">Jon Sege</a>
                or <a href="mailto: mzelenetz@wphospital.org">Michael Zelenetz</a>
                with any questions.
            </p>
            <div style="width:100%;background-color:#343a40;color:white;padding-left:20px;margin-top:50px">
                <p><i>Generated by WPH Analytics</i></p>
            </div>
        </div>
        </body>
    </html>
    '''

    recipients = get_recipients(task_id, 'output')
    emails = get_recipient_emails(recipients)

    e = Email(
        recipients=emails,
        body=email_body,
        from_email='noreply@wphospital.org',
        subject=email_subject,
        body_type='html',
        run=run_id,
        category='output',
        object='task',
        server=smtpserver
    )

    e.build_and_send()


if __name__ == '__main__':
    main()
