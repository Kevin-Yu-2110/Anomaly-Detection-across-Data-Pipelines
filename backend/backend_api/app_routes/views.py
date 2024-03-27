from backend_api.app_routes.forms import SignUpForm
from backend_api.models import StandardUser, Transaction
from django.core.paginator import Paginator
from django.http import JsonResponse
from email.message import EmailMessage
from datetime import datetime, timedelta
from django.db.models import Q
from django.core.serializers import serialize
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from functools import wraps
import smtplib
import json
import jwt
import csv

JWT_KEY = "3fRKDzIVo2m6sPhDkhNU9URS8nT0hTTYRbeCd3iVHyeBFuUf7mAY6n5sJ2MiinE7Jem0QzYbHVla8FtqIb4xHt1GmdWgOQDa"

def generate_jwt(username, password):
    expiration = datetime.now() + timedelta(days=1)
    payload = {'username' : username, 'password' : password, 'exp' : expiration}
    token = jwt.encode(payload, JWT_KEY, algorithm='HS256')
    return token

def validate_attached_token(request):
    try:
        token = request.META['HTTP_AUTHORIZATION'][7:] # remove "Bearer " prefix
        decoded_token = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        requesting_user = decoded_token.get('username')
        impacted_user = request.POST['username']
        return impacted_user == requesting_user
    except:
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
    username = request.POST['username']
    password = request.POST['password1']
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        # Generate JSON Web Token for User-Auth
        token = generate_jwt(username, password)
        login(request, StandardUser.objects.get(username=username))
        return JsonResponse({'success': True, 'token' : token})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})

@csrf_exempt
@require_POST
def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    # if user does not exist, return failure
    try:
        user = StandardUser.objects.get(username=username)
    except:
        return JsonResponse({'success': False, 'error' : 'Invalid Credentials'})        
    # validate password
    if user.check_password(password):
        # Generate JSON Web Token for User-Auth
        token = generate_jwt(username, password)
        login(request, user)
        return JsonResponse({'success': True, 'token' : token})
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
@require_GET
# Required to get email for user profile purposes, called once while logging in
def get_email(request):
    try:
        username = request.GET['username']
        user = StandardUser.objects.get(username=username)
        return JsonResponse({'success': True, 'email': user.email})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_POST
@auth_required
def delete_account(request):
    try:
        username = request.POST['username']
        StandardUser.objects.get(username=username).delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@csrf_exempt
@require_POST
def reset_request(request):
    email = request.POST['email']
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
    otp = request.POST['otp']
    email = request.POST['email']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    user = StandardUser.objects.get(email=email)
    if password1 != password2:
        return JsonResponse({'success': False, 'error': 'passwords dont match'})
    new_password = password1
    if user.is_active:
        # Check if otp is valid
        if otp == user.otp:
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
        Transaction.objects.create(
            username=request.POST['username'],
            payee_name=request.POST['payeeName'],
            amount=request.POST['amountPayed'],
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
        username=request.POST['username']
        updated_username=request.POST['new_username']
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
        username = request.POST['username']
        updated_email = request.POST['new_email']
        user = StandardUser.objects.get(username=username)
        user.email = updated_email
        user.save()
        return JsonResponse({'success': True})
    except Exception as e:
        # something went wrong
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_POST
@auth_required
def get_transaction_history(request):
    try:
        username=request.POST['username']
        page_no=request.POST['page_no']
        items_per_page = 50
        # get all transactions involving user as payer or payee
        transactions = Transaction.objects.filter(Q(username=username) | Q(payee_name=username)).order_by('time_of_transfer')
        paginator = Paginator(transactions, items_per_page)
        page = paginator.page(page_no)
        transactions = page.object_list
        transaction_history = serialize('json', transactions)
        transaction_history = json.loads(transaction_history)
        transaction_history = [transaction['fields'] for transaction in transaction_history]
        return JsonResponse({'success': True, 'transaction_history' : transaction_history})
    except Exception as e:
        # something went wrong
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_POST
@auth_required
def process_transaction_log(request):
    try:
        uploaded_file = request.FILES['transaction_log']
        decoded_file = uploaded_file.read().decode('utf-8').splitlines()
        csv_reader = csv.reader(decoded_file)
        rows_read = 0
        for row in csv_reader:
            if rows_read:
                Transaction.objects.create(
                    username=row[0],
                    payee_name=row[1],
                    amount=float(row[2]),
                    time_of_transfer=row[3]
                ) 
            rows_read += 1
        transactions = Transaction.objects.all()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
def get_transaction_by_field(request):
    try:
        username=request.POST['username']
        page_no=request.POST['page_no']
        field=request.POST['field']
        items_per_page = 50
        transactions = Transaction.objects.filter((Q(username=username) | Q(payee_name=username)) & Q(field=field)).order_by('time_of_transfer')
        paginator = Paginator(transactions, items_per_page)
        page = paginator.page(page_no)
        transactions = page.object_list
        transaction_history = serialize('json', transactions)
        transaction_history = json.loads(transaction_history)
        transaction_history = [transaction['fields'] for transaction in transaction_history]
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
