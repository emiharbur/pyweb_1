from django.contrib import admin
from .models import StaffBasicInfo
from .models import Daycheckon
from .models import Salaryset
from .models import subjecttable
from .models import useradd
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
class useraddinline (admin.TabularInline):
    model =  useradd
    can_delete = False
    verbose_name_plural = '用户附加信息'

class UserAdmin(BaseUserAdmin):
     inlines = (useraddinline,)


admin.site.unregister(User)
admin.site.register(User,UserAdmin)
