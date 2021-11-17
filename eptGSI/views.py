from django.shortcuts import render, redirect
#from .models import 
from django.db import transaction, IntegrityError
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Q


def index(request):
    return render(request, 'eptGSI/index.html')


