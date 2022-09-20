from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import manager, managerProfile, managerFeedback, Payment, served


class managerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'username')
    search_fields = ('first_name', 'last_name', 'email', 'username',)
    list_filter = ('is_active', 'is_archived', 'updated', 'created')

    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True, is_archived=False, is_verified=True)
        self.message_user(request, ngettext(
            '%d manager has successfully been marked as active.',
            '%d managers have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Approve manager"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_archived=True, is_active=False)
        self.message_user(request, ngettext(
            '%d Finance manager has been archived successfully.',
            '%d Finance managers have been archived successfully.',
            updated,
        ) % updated, messages.INFO)

    make_inactive.short_description = "Archive manager"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class managerProfileAdmin(admin.ModelAdmin):
    list_display = ('User', 'phone_number', 'image', 'gender', 'is_active', 'created', 'updated')
    list_filter = ('gender', 'is_active', 'updated', 'created')
    search_fields = ('phone_number',)
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, ngettext(
            '%d Profile has been successfully marked as active.',
            '%d Profiles have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Mark selected Profiles as active"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, ngettext(
            '%d Profile has been successfully marked as inactive.',
            '%d Profiles has been successfully marked as inactive.',
            updated,
        ) % updated)

    make_inactive.short_description = "Mark selected Profiles as inactive"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class managerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message', 'created')
    list_filter = ('created',)
    search_fields = ('subject', 'message',)

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class servedAdmin(admin.ModelAdmin):
    list_display = ('Appointment', 'client', 'manager', 'is_confirmed', 'updated', 'created')
    list_filter = ('manager', 'is_confirmed',  'updated', 'created')
    search_fields = ('payment',)
    actions = ['make_served']

    def make_confirmed(self, request, queryset):
        updated = queryset.update(is_confirmed=True)
        self.message_user(request, ngettext(
            '%d Payment has been confirmed successfully.',
            '%d Payment have been confirmed successfully.',
            updated,
        ) % updated, messages.SUCCESS)

    make_confirmed.short_description = "Confirm selected as served"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


admin.site.register(manager, managerAdmin)
admin.site.register(managerProfile, managerProfileAdmin)
admin.site.register(managerFeedback, managerFeedbackAdmin)
admin.site.register(served, servedAdmin)


