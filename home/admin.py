from django.contrib import admin

# Register your models here.
from .models import Institute, Course

admin.site.register(Institute)
admin.site.register(Course)