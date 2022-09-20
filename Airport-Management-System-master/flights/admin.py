from admin_interface.models import Theme
from django.contrib import admin
from django.contrib.auth.models import Group

from flights.models import ClientService, Appointment, service


class ClientServiceAdmin(admin.ModelAdmin):
    list_display = ('code', 'price', 'updated', 'created')
    search_fields = ('code',)
    list_filter = ('updated', 'created')

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'ClientService', 'client', 'updated', 'created')
    search_fields = ('code',)
    list_filter = ('updated', 'created')

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

class serviceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'date', 'updated', 'created')
    search_fields = ('code',)
    list_filter = ('updated', 'created')

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True



admin.site.register(ClientService, ClientServiceAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(service, serviceAdmin)