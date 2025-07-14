# from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
# from django.contrib import messages
# from . models import Customer
# # Create your views here.
# def show_account(request):

#     if request.POST and 'register' in request.POST:
#         try:   
#             username=request.POST.get('username')
#             password=request.POST.get('password')
#             email=request.POST.get('email')
#             address=request.POST.get('address')
#             phone=request.POST.get('phone')
#             #  create user accounts
          
#             user=User.objects.create(
#                 username=username,
#                 password=password,
#                 email=email
#             )
#             # create customer account
#             customer=Customer.objects.create(
#                 user=user,
#                 phone=phone,
#                 address=address
#             )
#             return redirect('home')
#         except Exception as e:    
#             error_message="duplicate username or invalid credentials"
#             messages.error(request,error_message)
#     return render(request,'account.html')



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Customer

def sign_out(request):
     logout(request)
     return redirect('home')
def show_account(request):
    if request.method == "POST" and 'register' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        try:
            # Always use create_user to hash the password!
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            Customer.objects.create(
                 name=username,
                user=user,
                phone=phone,
                address=address
            )

            messages.success(request, "Account created successfully.")
            return redirect('account')

        except Exception as e:
            error_message = "Username already exists or invalid input."
            messages.error(request, error_message)

    elif "login" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")


    return render(request, 'account.html')
