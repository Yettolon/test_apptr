from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import UserData
# Register your models here.
@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display=('email','imageee')
    def imageee(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' width='60'/>".format(obj.image.url))
        return "None"
    imageee.short_description = "Image"