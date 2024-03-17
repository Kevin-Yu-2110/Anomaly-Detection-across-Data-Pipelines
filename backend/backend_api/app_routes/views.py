from django.contrib.auth import login, logout
from backend_api.app_routes.forms import SignUpForm
from backend_api.models import StandardUser, Transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from email.message import EmailMessage
from django.http import JsonResponse
from datetime import datetime, timedelta
from functools import wraps
import json
import jwt
import smtplib

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

def auth_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not validate_attached_token(request):
            return JsonResponse({'success': False, 'error': "Failed to authenticate"})
        return func(request, *args, **kwargs)
    return wrapper

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
@auth_required
def user_logout(request):
    try:
        logout(request)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_POST
@auth_required
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
def reset_request(request):
    data = json.loads(request.body)
    email = data['email']
    try:
        user = StandardUser.objects.get(email=email)
    except:
        return JsonResponse({'success': False, 'error' : 'User with email does not exist'})   
    if StandardUser.objects.filter(email=email).exists():
        # send email with otp
        msg = EmailMessage()
        msg.set_content(user.otp)
        msg['Subject'] = "OTP for password reset"
        msg['From'] = "pearproject3900@gmail.com"
        msg['To'] = email
        mail_server = smtplib.SMTP("smtp.gmail.com", 587)
        mail_server.starttls()
        mail_server.login(msg['From'], "obed iylr awsd trqg")
        mail_server.send_message(msg)
        mail_server.quit
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'cant find email'})
    
@csrf_exempt
@require_POST
def reset_password(request):
    # reset_password with email, OTP and new password
    data = json.loads(request.body)
    user = StandardUser.objects.get(email=data['email'])
    if data['password1'] != data['password2']:
        return JsonResponse({'success': False, 'error': 'passwords dont match'})
    new_password = data['password1']
    if user.is_active:
        # Check if otp is valid
        if data['otp'] == user.otp:
            if new_password != '':
                # Change Password
                user.set_password(new_password)
                user.save() # Here user otp will also be changed on save automatically
                # return new auth token derived from reset password
                new_auth_token = generate_jwt(user.username, new_password)
                return JsonResponse({'success': True, 'token' : new_auth_token})
            else:
                return JsonResponse({'success': False, 'error': 'password cant be empty'})
        else:
            return JsonResponse({'success': False, 'error': 'incorrect OTP'})
    else:
        return JsonResponse({'success': False, 'error': 'something went wrong'})

@csrf_exempt
@require_POST
@auth_required
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

@csrf_exempt
@require_POST
@auth_required
def update_username(request):
    try:
        data = json.loads(request.body)
    except Exception as e:
        # malformed request
        return JsonResponse({'success': False, 'error': str(e)})
    try:
        username=data['username']
        updated_username=data['new_username']
        # return query failure if proposed username already exists in database
        StandardUser.objects.get(username=updated_username)
        return JsonResponse({'success': False, 'error' : 'User already exists'})
    except StandardUser.DoesNotExist:
        # if proposed username does not exist, update and return success
        user = StandardUser.objects.get(username=username)
        user.username = updated_username
        user.save()
        # return new auth token derived from updated username
        auth_token = generate_jwt(user.username, user.password)
        return JsonResponse({'success': True, 'token' : auth_token})

@csrf_exempt
@require_POST
@auth_required
def update_email(request):
    try:
        data = json.loads(request.body)
    except Exception as e:
        # malformed request
        return JsonResponse({'success': False, 'error': str(e)})
    try:
        username=data['username']
        updated_email=data['new_email']
        user = StandardUser.objects.get(username=username)
        user.email = updated_email
        user.save()
        return JsonResponse({'success': True})
    except Exception as e:
        # something went wrong
        return JsonResponse({'success': False, 'error': str(e)})