from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Topic)
admin.site.register(Article)
admin.site.register(Subscriber)
