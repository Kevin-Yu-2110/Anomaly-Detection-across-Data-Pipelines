from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from backend_api.reg_auth.forms import SignUpForm
from backend_api.models import StandardUser
from django.http import JsonResponse

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'accountType' : request.POST.get('accountType')})
    else:
        form = SignUpForm()
    return JsonResponse({'success': False})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({'success': True, 'accountType' : request.POST.get('accountType')})
    else:
        form = AuthenticationForm()
    return JsonResponse({'success': False, 'accountType' : request.POST.get('accountType')})

def delete_account(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            StandardUser.objects.get(username=username).delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

