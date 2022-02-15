from django.http import HttpResponse
from django.shortcuts import render


def base_response(request):
    return render(request, 'test.html')