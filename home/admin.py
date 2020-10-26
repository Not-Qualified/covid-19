from django.contrib import admin
from .models import (VaccineUpdate, 
					HospitalRegister, 
					VaccineUpdatePost, 
					HitCounter, )

class HospitalRegisterAdmin(admin.ModelAdmin):
	list_filter = ("verified", )

# Register your models here.
admin.site.register(VaccineUpdate, )
admin.site.register(VaccineUpdatePost, )
admin.site.register(HospitalRegister, HospitalRegisterAdmin, )
admin.site.register(HitCounter, )