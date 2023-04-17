from django.contrib import admin
from . import models
# Register your models here.



@admin.register(models.Chat)
class MessageAdmin(admin.ModelAdmin):
    pass


