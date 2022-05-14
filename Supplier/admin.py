from django.contrib import admin

from .models import Residence,Service, Ticket



admin.site.register(Residence)
class ResidenceAdmin(admin.ModelAdmin):
    fields = ( 'location','name' )
admin.site.register(Service)
admin.site.register(Ticket)
