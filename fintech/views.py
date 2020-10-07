from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.

def test(request):
    if request.method == 'GET':
        context = {
            "AAPL": [100, 110, 120, 130, 120, 110, 100, 120, 110],
            "MSFT": [180, 160, 150, 120, 100, 150, 140, 100, 170]
        }
        return JsonResponse(context)
