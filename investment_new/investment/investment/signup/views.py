from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserCopy, Plan, Deposit, Withdraw, QRCode
from django.contrib import messages
from investment import settings
from django.core.mail import EmailMessage, send_mail
import random
from .utils import send_otp
from datetime import datetime
import pyotp

# Create your views here.

@login_required
def HomePage(request):
    print(request.body.decode("utf-8"))
    user = UserCopy.objects.get(user=request.user)    
    context={
        'user': user,
    }
    return render(request, 'home.html',context)

def SignUp(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        code=request.POST.get('invite_code')
        request.session['phone']=request.POST.get('phone')
        pwd=request.POST.get('password')
        cpwd=request.POST.get('confpassword')

        if UserCopy.objects.filter(username=username):
            messages.error(request,"Username already taken !")
            return redirect("signup")
        
        if User.objects.filter(email=email):
            messages.error(request,"Email already registered !")
            return redirect("signup")

        if(pwd != cpwd): 
            messages.error(request,"Password and Verify Password does not match !")
            return redirect('signup')
        
        request.session['username'] = username
        request.session['pwd'] = pwd
        request.session['email'] = email
        request.session['code'] = code
        
        otp = send_otp(request)
        subject = "Welcome to FutureTune"
        message = "Welcome to FutureTune, here is your One-Time Password: " + str(otp)
        from_email = settings.EMAIL_HOST_USER
        to_list = [email]
        send_mail(subject,message,from_email,to_list,fail_silently = True)
        return redirect('otp')

        '''myuser = User.objects.create_user(username,email,pwd)
        myuser.is_active = True
        myuser.is_staff = True
        myuser.save()

        newclient = UserCopy.objects.create(user=myuser, username=username, phone_number=phone)
        newclient.save()
        login(request,myuser)
        return redirect('home')'''
        '''u=User()
        u.username=uname
        u.password=pwd[0]
        u.set_password(raw_password=pwd[0])
        if User.objects.filter(username=uname).exists():
            return HttpResponse("<h1>Username already exists</h1>")
        u.save()
        uc=UserCopy()
        print(uname[0])
        uc.phone_number=uname[0]
        uc.username=username
        uc.password=pwd
        uc.save()
        return redirect('/')'''
    return render(request, 'signup.html')

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user_phone_number = request.POST['phone_number']
        user_password = request.POST['password']
        
        try:
            myuser = UserCopy.objects.get(phone_number = user_phone_number)
        except:
            myuser = None

        if myuser is not None:
            if user_password != myuser.password:
                messages.error(request, 'Wrong Password!')
                return redirect('login')
            user = myuser.user 
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'login.html')
    
    return render(request, 'login.html')

def otp(request):
    error_msg = None
    if request.method == 'POST':
        otp = request.POST['otp']
        
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)
            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval = 180)
                if totp.verify(otp):

                    username = request.session['username']
                    email = request.session['email']
                    pwd = request.session['pwd']
                    phone = request.session['phone']
                    code = request.session['code']

                    myuser = User.objects.create_user(username,email,pwd)
                    myuser.is_active = True
                    myuser.is_staff = True
                    myuser.save()

                    newclient = UserCopy.objects.create(user=myuser, username=username, phone_number=phone, password=pwd, invitational_code=code)
                    newclient.save()

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    del request.session['username']
                    del request.session['email']
                    del request.session['pwd']
                    del request.session['phone']
                    del request.session['code']

                    login(request,myuser)
                    return redirect('home')
                else:
                    error_msg = 'Invalid one-time password'
            else:
                error_msg = 'One-time password had expired'
        else:
            error_msg = 'Oops something went wrong'

    return render(request, 'otp.html',{'msg': error_msg})

def Logout(request):
    logout(request)
    return redirect("login")

def AccountView(request):
    user = UserCopy.objects.get(user=request.user)  
    deposit = Deposit.objects.filter(user=request.user)
    context = {
            'deposit': deposit.count(),
            'user': user,   
            'username': user.username,
            'phone_number': user.phone_number,
            'balance': user.balance,
            'Deposit': user.deposit,
            'Withdraw': user.withdraw,
        }
    # print(f"Current user: {request.user.username}")
    # try:
    #     # Change this line to use request.user.username instead of request.user
    #     user_copy = UserCopy.objects.get(username=request.user.username)
    #     context = {
    #         'username': user_copy.username,
    #         'phone_number': user_copy.phone_number,
    #         'balance': user_copy.balance,
    #         'Deposit': user_copy.deposit,
    #         'Withdraw': user_copy.withdraw,
    #     }
    #     return render(request, 'account.html', context)
    # except UserCopy.DoesNotExist:
    #     print(f"UserCopy not found for {request.user.username}") 
    #     return HttpResponse("User information not found")
    return render(request, 'account.html',context)

def activity_invest_view(request):
    user = UserCopy.objects.get(user=request.user)
    plans = Plan.objects.filter(type='W')
    context = {
        'user': user,
        'plans': plans
    }
    return render(request, 'activity_invest.html', context)

def daily_invest_view(request):
    user = UserCopy.objects.get(user=request.user)
    plans = Plan.objects.filter(type='D')
    context = {
        'user': user,
        'plans': plans
    }
    return render(request, 'daily_invest.html', context)

def invest(request):
    user = UserCopy.objects.get(user=request.user)
    plans = Plan.objects.filter(type='M')
    context = {
        'user': user,
        'plans': plans
    }
    return render(request, 'invest.html', context)

def invest_plan(request, plan):
    plan = Plan.objects.get(name=plan)
    user = UserCopy.objects.get(user=request.user)
    price = plan.price
    income = plan.daily
    context={
        'plan': plan,
        'user': user
    }

    if request.method=='POST':
        quantity = int(request.POST['quantity'])
        amount = quantity * price
        daily = quantity * income
        return redirect('transaction', plan.name, amount, daily)

    return render(request, 'invest_plan.html', context)

def transaction(request, plan, amount, daily):
    myplan = Plan.objects.get(name=plan)
    user = UserCopy.objects.get(user=request.user)
    qr = QRCode.objects.get(name="QR-1")

    if request.method == 'POST':
        upi = request.POST['upi']
        user.upi_id = upi
        user.save()
        
        Deposit.objects.create(user=request.user, upi_id=upi, amount=amount, daily=daily, plan=myplan)
        return redirect('completed')

    context={
        'qr': qr,
        'user': user,
        'plan': myplan,
        'amount': amount,
        'daily': daily
    }
    return render(request, 'transaction.html', context)

def Help(request):
    return render(request,'help.html')

def review(request):
    return render(request, 'review.html')

def orders(request):
    user = UserCopy.objects.get(user=request.user)
    deposits = Deposit.objects.filter(user=request.user)
    context={
        'user':user,
        'deposits': deposits
    }
    return render(request, 'orders.html',context)

def deposit(request, plan, amount, daily):
    plan = Plan.objects.get(name=plan)
    user = UserCopy.objects.get(user=request.user)    
    Deposit.objects.create(user=request.user, upi_id=user.upi_id, amount=amount, daily=daily, plan=plan)
    return redirect('completed')

def completed(request):
    return render(request, 'completed.html')

def bank(request):
    user = UserCopy.objects.get(user=request.user)
    if request.method=='POST':
        ifsc = request.POST['ifsc']
        holder = request.POST['holder']
        acc_num = request.POST['acc_num']

        if UserCopy.objects.filter(ifsc=ifsc):
            messages.error(request, 'IFSC code already registered!')
            return redirect('bank')

        if UserCopy.objects.filter(account_number=acc_num):
            messages.error(request, 'Account number already registered!')
            return redirect('bank')
        
        user.ifsc = ifsc
        user.account_holder = holder
        user.account_number = acc_num
        user.save()
        return redirect('withdrawal')

    return render(request, 'bank.html')

def withdrawal(request):
    user = UserCopy.objects.get(user=request.user)
    deposit = Deposit.objects.filter(user=request.user)

    context={
        'user': user,
        'deposit': deposit
    }

    if user.account_number is None:
        return redirect('bank')
    
    if request.method=='POST':
        check = request.POST.get('check', 'off')
        if check=='on':
            coin = request.POST['coin']
            upi = request.POST['upi']
            pwd = request.POST['pwd']

            if len(upi) == 0:
                messages.error(request,"Enter UPI ID !")
                return render(request, 'withdrawal.html',context)

            if UserCopy.objects.get(upi_id=upi):
                messages.error(request, 'UPI ID already registered!')
                return redirect('withdrawal')

            if user.password != pwd:
                messages.error(request,"Incorrect Password !")
                return render(request, 'withdrawal.html',context)
                
            user.coin -= int(coin)
            user.save()
            Withdraw.objects.create(user=request.user,upi_id = upi, coin = coin)
            return redirect('completed')
        
        balance = request.POST['balance']
        upi = request.POST['upi']
        pwd = request.POST['pwd']

        if UserCopy.objects.get(upi_id=upi):
            messages.error(request, 'UPI ID already registered!')
            return redirect('withdrawal')

        if int(balance)>user.balance:
            messages.error(request,"You don't have enough balance !")
            return render(request, 'withdrawal.html',context)

        if int(balance)<300:
            messages.error(request,"Can't make any withdrawals under ₹300 !")
            return render(request, 'withdrawal.html',context)

        if (user.password != pwd):
            messages.error(request,"Incorrect Password !")
            return render(request, 'withdrawal.html',context)
        
        user.balance -= int(balance)
        user.save()
        Withdraw.objects.create(user=request.user,upi_id = user.upi_id, amount = balance)
        return redirect('completed')

    return render(request, 'withdrawal.html',context)

def withdrawal_orders(request):
    user = UserCopy.objects.get(user=request.user)
    withdrawals = Withdraw.objects.filter(user=request.user)
    context={
        'user':user,
        'withdrawals': withdrawals
    }
    return render(request, 'withdrawal_orders.html',context)

def ForgotPass(request):
    if request.method=='POST':
        username = request.POST['username']
        try:
            user = UserCopy.objects.get(username=username)
        except:
            user = None
        if user is None:
            messages.error(request, 'Invalid Username !')
            return redirect('forgotpass')
        otp = send_otp(request)
        subject = "FutureTune | Forgot Password"
        message = "Here is your One-Time Password: " + str(otp)
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.user.email]
        send_mail(subject,message,from_email,to_list,fail_silently = True)
        return redirect('passotp', username)
    
    return render(request, 'forgotpass.html')

def PassOTP(request, username):
    if request.method == 'POST':
        otp = request.POST['passotp']
        
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)
            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval = 180)
                if totp.verify(otp):

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']

                    return redirect('resetpass', username)
                else:
                    messages.error(request,'Invalid one-time password')
            else:
                messages.error(request,'One-time password had expired')
        else:
            messages.error(request,'Oops something went wrong')
    
    context={
        'username': username,
    }
    return render(request, 'passotp.html', context)

def resetpass(request, username):
    if request.method=='POST':
        newpass = request.POST['newpassword']
        confirm = request.POST['newconfirm']
        if newpass != confirm:
            messages.error(request, 'Password and confirm password are not same!')
            return redirect(resetpass)
        user = UserCopy.objects.get(username=username)
        user.password = newpass
        user.save()
        login(request, user.user)
        return redirect('home')

    context={
        'username': username,
    }
    return render(request, 'resetpass.html',context)