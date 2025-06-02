from django.contrib import admin

# Register your models here.
from wayapp.models import Note, SpecialPilgrim, PilgrimVideo

admin.site.register(Note)

admin.site.register(SpecialPilgrim)

admin.site.register(PilgrimVideo)