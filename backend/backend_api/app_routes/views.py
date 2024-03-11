from django.contrib.auth import authenticate, login, logout
from backend_api.app_routes.forms import SignUpForm
from backend_api.models import StandardUser, Transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import datetime
import smtplib
from email.message import EmailMessage

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
    
@csrf_exempt
@require_POST
def reset_request(request):
    data = json.loads(request.body)
    email = data['email']
    user = StandardUser.objects.get(email=email)
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
        message = {
            'detail': 'Some Error Message'}
        return JsonResponse({'success': False, 'error': 'cant find email'})
    
@csrf_exempt
@require_POST
def reset_password(request):
    """reset_password with email, OTP and new password"""
    data = json.loads(request.body)
    user = StandardUser.objects.get(email=data['email'])
    if data['password1'] != data['password2']:
        return JsonResponse({'success': False, 'error': 'passwords dont match'})
    data['password'] = data['password1']
    if user.is_active:
        # Check if otp is valid
        if data['otp'] == user.otp:
            if data['password'] != '':
                # Change Password
                user.set_password(data['password'])
                user.save() # Here user otp will also be changed on save automatically 
                return JsonResponse({'success': True})
            else:
                message = {
                    'detail': 'Password cant be empty'}
                return JsonResponse({'success': False, 'error': 'password cant be empty'})
        else:
            message = {
                'detail': 'OTP did not match'}
            return JsonResponse({'success': False, 'error': 'incorrect OTP'})
    else:
        message = {
            'detail': 'Something went wrong'}
        return JsonResponse({'success': False, 'error': 'something went wrong'})
    
    
    


