from django.shortcuts import render


def index(requests):
    context = {}
    return render(request, 'website/templates/index.html', context )

def about_us(requests):
    context = {}
    return render(request, 'website/templates/about.html', context )


def contact_us(requests):
    context = {}
    return render(request, 'website/templates/contacts.html', context )