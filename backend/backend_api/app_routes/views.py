from django.contrib.auth import authenticate, login, logout
from backend_api.app_routes.forms import SignUpForm
from backend_api.models import StandardUser, Transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import datetime

import json

@csrf_exempt
@require_POST
def user_signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = SignUpForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'accountType': data.get('accountType')})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False})

@csrf_exempt
@require_POST
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(request, username=data['username'], password=data['password'])
        try:
            user = StandardUser.objects.get(username=data['username'])
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        pass_correct = user.check_password(data['password']) if user else False
        if user and pass_correct:
            login(request, user)
            return JsonResponse({'success': True, 'accountType' : user.accountType})
    return JsonResponse({'success': False})

@csrf_exempt
@require_POST
def user_logout(request):
    try:
        logout(request)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_POST
def delete_account(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            StandardUser.objects.get(username=username).delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
@require_POST
def make_transaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            Transaction.objects.create(
                username=StandardUser.objects.get(username=data.get('username')),
                payee_name=data.get('payeeName'),
                amount=data.get('amountPayed'),
                time_of_transfer=datetime.now()
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

