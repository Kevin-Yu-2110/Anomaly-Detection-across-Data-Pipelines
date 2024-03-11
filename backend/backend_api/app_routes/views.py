from django.contrib.auth import login, logout
from backend_api.app_routes.forms import SignUpForm
from rest_framework_simplejwt.tokens import RefreshToken
from backend_api.models import StandardUser, Transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from datetime import datetime, timedelta
import json
import jwt

JWT_KEY = "3fRKDzIVo2m6sPhDkhNU9URS8nT0hTTYRbeCd3iVHyeBFuUf7mAY6n5sJ2MiinE7Jem0QzYbHVla8FtqIb4xHt1GmdWgOQDa"

def generate_jwt(username, password):
    expiration = datetime.utcnow() + timedelta(days=1)
    payload = {'username' : username, 'password' : password, 'exp' : expiration}
    token = jwt.encode(payload, JWT_KEY, algorithm='HS256')
    return token

def validate_attached_token(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        decoded_token = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        impacted_user = json.loads(request.body).get('username')
        requesting_user = decoded_token.get('username')
        return impacted_user == requesting_user
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

@csrf_exempt
@require_POST
def user_signup(request):
    data = json.loads(request.body)
    form = SignUpForm(data)
    if form.is_valid():
        form.save()
        # Generate JSON Web Token for User-Auth
        token = generate_jwt(data['username'], data['password1'])
        login(request, StandardUser.objects.get(username=data['username']))
        return JsonResponse({'success': True, 'accountType': data.get('accountType'), 'token' : token})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})

@csrf_exempt
@require_POST
def user_login(request):
    data = json.loads(request.body)
    # if user does not exist, return failure
    try:
        user = StandardUser.objects.get(username=data['username'])
    except:
        return JsonResponse({'success': False, 'error' : 'Invalid Credentials'})        
    # validate password
    if user.check_password(data['password']):
        # Generate JSON Web Token for User-Auth
        token = generate_jwt(data['username'], data['password'])
        login(request, user)
        return JsonResponse({'success': True, 'accountType' : user.accountType, 'token' : token})
    return JsonResponse({'success': False, 'error' : 'Invalid Credentials'})

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
    if not validate_attached_token(request):
        return JsonResponse({'success': False, 'error': 'Invalid session token'})
    try:
        data = json.loads(request.body)
        username = data.get('username')
        StandardUser.objects.get(username=username).delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_POST
def make_transaction(request):    
    try:
        data = json.loads(request.body)
        Transaction.objects.create(
            username=StandardUser.objects.get(username=data.get('username')),
            payee_name=data.get('payeeName'),
            amount=data.get('amountPayed'),
            time_of_transfer=datetime.now()
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

