from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField


from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import Movies, Watchlists, MovieWatchlist, WatchlistTest, AWS_link, Genres

Users = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin')
    list_filter = ('is_admin', 'created_at',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('gender', 'year_of_birth', )}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()

# class UserAdmin(admin.ModelAdmin):
#     search_fields = ['email', 'name']
#     form = UserAdminChangeForm # update view
#     add_form = UserAdminCreationForm # create view



    # class Meta:
    #     model = Users

admin.site.unregister(Group)

admin.site.register(Movies)
admin.site.register(Watchlists)
admin.site.register(Users, UserAdmin)
admin.site.register(MovieWatchlist)
admin.site.register(WatchlistTest)
admin.site.register(AWS_link)
admin.site.register(Genres)


