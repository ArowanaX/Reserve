from django.contrib import admin

from .models import Residence, Service, Tag, RestaurantMenu, ResidenceIndoorAlbum, ResidenceOutdoorAlbum, Ticket



admin.site.register(Residence)
class ResidenceAdmin(admin.ModelAdmin):
    fields = ( 'location','name' )
admin.site.register(Service)
admin.site.register(Tag)
admin.site.register(RestaurantMenu)
admin.site.register(ResidenceIndoorAlbum)
admin.site.register(ResidenceOutdoorAlbum)
admin.site.register(Ticket)
