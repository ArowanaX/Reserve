from django.contrib import admin

from .models import Residence, Service, Tag, RestaurantMenu, ResidenceIndoorAlbum, ResidenceOutdoorAlbum



admin.site.register(Residence)
admin.site.register(Service)
admin.site.register(Tag)
admin.site.register(RestaurantMenu)
admin.site.register(ResidenceIndoorAlbum)
admin.site.register(ResidenceOutdoorAlbum)
