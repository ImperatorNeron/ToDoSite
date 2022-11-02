from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# ToDo: Don't use * at all because of it you can get circle import errors
# ToDo: use task.models, task.forms and so on
from .models import *
from .forms import SignUpForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = SignUpForm
    # Fields for some category
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'More information about user',
            {
                'fields': (
                    'phone', 'bio', 'photo', 'score', 'slug'
                )
            }
        )
    )

# ToDo: use one style of naming, like CustomUserAdmin and TaskAdmin
class TaskAdminSettings(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_complete', 'to_do_date')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_editable = ('is_complete',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Task, TaskAdminSettings)
admin.site.register(SiteImages)
