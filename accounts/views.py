from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, EmailMessage
from django.contrib import auth
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from accounts.models import Account
from accounts.serializers import AccountSerializer

from .forms import RegistrationForm

from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.csrf import csrf_protect
from django.middleware import csrf
import json
from django.forms.models import model_to_dict
from django.core.serializers import serialize
import base64
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import unpad
# from cryptography.fernet import Fernet

def decrypt_password(encrypted_password):
    # key = b'mysecretkey12345'
    # iv = b'myiv123456789012'
    key = b'mysecretkey12345'
    iv = b'myiv123456789012'

    encrypted_password_bytes = base64.b64decode(encrypted_password)
    cipher = AES.new(key, AES.MODE_ECB)
    # decrypted_data = unpad(cipher.decrypt(encrypted_password_bytes), AES.block_size)
    # decrypted_password_bytes = cipher.decrypt(encrypted_password_bytes)
    decrypted_password_bytes = cipher.decrypt(encrypted_password_bytes)
    plaintext_password = decrypted_password_bytes.decode('utf-8')



    # encrypted_password_bytes = base64.b64decode(encrypted_password)
    # iv = encrypted_password[:AES.block_size]
    # cipher = AES.new(key, AES.MODE_CBC, iv)
    # plaintext_password = cipher.decrypt(encrypted_password[:AES.block_size])
    # plaintext_password = decrypted_password_bytes.decode()

    # cipher = AES.new(key, AES.MODE_EAX)
    # ciphertext, tag = cipher.encrypt_and_digest(data)
    # data = cipher.decrypt_and_verify(ciphertext, tag)
    # plaintext_password = data.decode('utf-8')
    print(plaintext_password)
    return plaintext_password
    
@csrf_exempt
def login_accounts(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            request.COOKIE['user'] = user
            request.session['user_id'] = user.id
            login(request, user)
            return JsonResponse({
                'username':user.username,
                'email':user.email,
                'id': request.session['user_id'],
                'token': csrf.get_token(request)
            })
        else:
            return JsonResponse({'success': False, 'message': 'Invalid email or password.'})
    else:
        return JsonResponse({'success': False, 'message': 'Please enter a email or password'})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data['password'] = decrypt_password(data['password'])
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success': True, 'message': "Register successfully",'details': serializer.data})
        else:
            print(serializer.data)
            return JsonResponse({'success': False, 'message': 'Invalid information.', 'details': serializer.errors})
    else:
        return JsonResponse({'success': False, 'message': 'Please enter an email or password'})

@csrf_exempt
def logout(request):
    auth.logout(request)
    request.session.flush()
    return JsonResponse({'message': 'Successfully logged out.'})

@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        old_password = data['old_password']
        new_password = data['new_password']
        confirm_password = data['confirm_new_password']
        user = Account.objects.get(username=username)
        if new_password == confirm_password:
            if user.check_password(old_password):
                if user is not None:
                    user.set_password(new_password)
                    user.save()
                    return JsonResponse({
                        'success': True,
                        'message':"Reset password successfully!"
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': "User not found",
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'message': "Incorrect password",
                    'input_password': old_password,
                })
        else:
            return JsonResponse({
                'success': False,
                'message':"Password do not match!",
                'input_password': new_password
            })
    else: 
        return JsonResponse({
            'message': 'Invalid method'
        })



