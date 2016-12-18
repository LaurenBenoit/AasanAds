from django.contrib import admin

from core.models import *
admin.site.register(Ad)
admin.site.register(Locations)
admin.site.register(Topup)
admin.site.register(TopupLocationCounter)
admin.site.register(SMSIncoming)
admin.site.register(SMSOutgoing)
admin.site.register(Transaction)
# Register your models here.
