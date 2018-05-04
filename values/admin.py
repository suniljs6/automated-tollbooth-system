
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(vehicle_fare)
admin.site.register(types)
admin.site.register(vehicle)
admin.site.register(admin_user)
admin.site.register(end_user)
admin.site.register(authority_user)
admin.site.register(tollbooth)
admin.site.register(user_info)
admin.site.register(user_log)
admin.site.register(tollbooth_info)

