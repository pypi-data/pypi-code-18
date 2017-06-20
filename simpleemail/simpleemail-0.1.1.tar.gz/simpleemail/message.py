from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_email_message(subject: str, sender: str, recipient: str, text: str, html: str, params: dict = dict()):
    """
    Sends an email using both an html and text version.\n
    Based originally on example from: https://docs.python.org/3/library/email-examples.html
    :param subject: Subject of the email.
    :param sender: Email address to send from.
    :param recipient: Email address to send to.
    :param text: Text version of the email.
    :param html: HTML version of the email.
    :param params: dictionary of items to replace in the message body, using square brackets.\n
                    \t Example: "[firstname]" would be replaced by "John"
    :return: Email message to send through SMTP.
    """
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    html, text = merge_params(html, text, params)
    part1 = ''
    part2 = ''
    if text:
        part1 = MIMEText(text, 'plain')
    if html:
        part2 = MIMEText(html, 'html')

    if part1:
        msg.attach(part1)
    if part2:
        msg.attach(part2)

    return msg


def merge_params(html, text, params):
    for key in params.keys():
        text = text.replace('[{}]'.format(key), params[key])
        html = html.replace('[{}]'.format(key), params[key])

    return html, text

