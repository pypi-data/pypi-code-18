from django.core.validators import RegexValidator


validate_dns_label = RegexValidator(r'^(?![0-9]+$)(?!-)(?![a-z0-9]+--)[a-z0-9-]{1,63}(?<!-)$',
                                    message='Invalide DNS label.',
                                    code='invalid_dns_label')
