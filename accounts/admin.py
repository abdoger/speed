from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Code)
admin.site.register(OtpToken)
admin.site.register(Video)
admin.site.register(UserProfile)






# from import_export.admin import ImportExportModelAdmin

# @admin.register(UserProfile)
# class UserProfileImportExport(ImportExportModelAdmin):
#     pass




