from django.shortcuts import render


def index(request):
    context = {
        'index': True
    }
    return render(request, 'index/index.html', context)


def about_us(request):
    context = {
        'about_us': True
    }
    return render(request, 'index/about_us.html', context)
