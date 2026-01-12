from django.contrib import admin
from .models import Destination, Package, Enquiry, Subscriber

# Register your models here.

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'parent', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'category', 'parent')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'price', 'duration', 'is_featured')
    search_fields = ('title', 'destination__name')
    list_filter = ('destination', 'is_featured')

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'destination', 'travel_date', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('created_at', 'destination')
    readonly_fields = ('created_at',)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)
