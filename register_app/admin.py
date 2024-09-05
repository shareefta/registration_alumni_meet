from django.contrib import admin
from .models import *
# Register your models here.

class AlumniAdmin(admin.ModelAdmin):
    list_display = ('name', 'place', 'mobile_number', 'whatsapp_number', 'name_of_wife', 'no_of_child_below_5', 'no_of_child_above_5', 'is_registered')
    list_filter = ('is_registered',)

admin.site.register(Alumni, AlumniAdmin)
