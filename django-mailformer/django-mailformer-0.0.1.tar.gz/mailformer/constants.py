STATUS = {
    1: 'NEW',
    2: 'PROCESSING',
    3: 'RETRY',
    4: 'ERROR',
    5: 'SENT',
    6: 'INVALID',
}

URL_NAME = {
    'form': 'mailformer-form',
    'success': 'mailformer-success',
}

TEMPLATES = {
    'email': 'mailformer/email.txt',
    'form': 'mailformer/mailformer-form.html',
    'success': 'mailformer/mailformer-success.html'
}

STATUS_ = {value: key for key, value in STATUS.items()}
