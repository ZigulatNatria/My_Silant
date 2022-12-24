from django.contrib import admin
from .models import Machine, TO, Complaint
# Register your models here.
admin.site.register(Machine)
admin.site.register(TO)
admin.site.register(Complaint)