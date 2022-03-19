from django.contrib import admin
from .models import Member, Location, Properties


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    model = Member


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    model = Location


@admin.register(Properties)
class PropertiesAdmin(admin.ModelAdmin):
    model = Properties
