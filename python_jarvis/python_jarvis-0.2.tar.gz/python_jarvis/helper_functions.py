import datetime, re
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives


def convert_epoch_to_date(epoch):
    if not isinstance(epoch, long):
        return None

    return datetime.datetime.fromtimestamp(long(epoch)/1000.0)


def convert_date_to_epoch(date):
    if not isinstance(date, datetime.datetime):
        return None

    return long(date.strftime('%s'))*1000


def _validate_email(email):
    address_to_verify =email
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', address_to_verify)

    if match:
        return True
    else:
        return False


def send_email(email, message, subject):
    ## send email to user
    from_email = 'teamtrex01@gmail.com'
    to_email = email
    try:
        print "try to send email"
        email = EmailMultiAlternatives(subject, "", from_email, [to_email])
        email.attach_alternative(message, "text/html")
        email.send()
    except BadHeaderError:
        print 'Invalid header found.'
    return 0
