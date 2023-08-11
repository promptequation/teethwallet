from api.models.user_model import User, UserLang
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class UserAdminExtended(UserAdmin):
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)

    group.short_description = 'Groups'

    list_display = ('id', 'username', 'email', 'city', 'country', 'group')
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, UserAdminExtended)
admin.site.register(UserLang)
