from django.contrib import admin
from .models import *


admin.site.register(UserCopy)
admin.site.register(Deposit)
admin.site.register(Plan)
admin.site.register(QRCode)
admin.site.register(Withdraw)

# Register your models here.
