from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json

@api_view(["GET"])
def initialize(request):
    return JsonResponse({'foo':'bar'},safe=True)

@api_view(["GET"])
def worldmap(request):
    return JsonResponse({'foo':'bar'},safe=True)