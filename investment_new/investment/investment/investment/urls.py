"""
URL configuration for investment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from signup import views
from django.conf.urls.static import static 
from django.conf import settings


urlpatterns = [
    path('futurem3@admin', admin.site.urls),
    path('signup/', views.SignUp, name='signup'),
    path('',views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('home', views.HomePage, name= 'home'),
    path('account/', views.AccountView, name='account'),
    path('activity-invest/', views.activity_invest_view, name='activity_invest'),
    path('daily-invest/', views.daily_invest_view, name='daily_invest'),
    path('invest/', views.invest, name='invest'),
    path('invest_plan/<str:plan>', views.invest_plan, name='invest_plan'),
    path('help/', views.Help, name='help'),
    path('review/', views.review, name='review'),
    path('orders/', views.orders, name='orders'),
    path('withdrawal_orders/', views.withdrawal_orders, name='withdrawal_orders'),
    path('otp/', views.otp, name='otp'),
    path('transaction/<str:plan>/<int:amount>/<int:daily>/', views.transaction, name='transaction'),
    path('completed/', views.completed, name='completed'),
    path('deposit/<str:plan>/<int:amount>/<int:daily>/', views.deposit, name='deposit'),
    path('bank/', views.bank, name='bank'),
    path('withdrawal/', views.withdrawal, name='withdrawal'),
    path('orders/', views.orders, name='orders'),
    path('forgotpass/', views.ForgotPass, name='forgotpass'),
    path('passotp/<str:username>', views.PassOTP, name='passotp'),
    path('resetpass/<str:username>', views.resetpass, name='resetpass'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)