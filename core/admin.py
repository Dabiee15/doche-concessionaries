from django.contrib import admin
from .models import Category, Product, Service, Booking

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

from django.utils.html import format_html

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'category', 'starting_price', 'badge_tag', 'is_available', 'is_featured']
    list_filter = ['category', 'is_available', 'is_featured']
    search_fields = ['name', 'badge_tag']
    fields = ['category', 'name', 'description', 'starting_price', 'image', 'image_url', 'badge_tag', 'is_available', 'is_featured']

    def image_preview(self, obj):
        url = obj.get_image_url
        return format_html('<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 6px;" />', url)
    image_preview.short_description = 'Thumbnail'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_price', 'minimum_notice_days']
    search_fields = ['name']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_phone', 'service', 'product', 'booking_date', 'booking_time', 'status', 'estimated_price']
    list_filter = ['status', 'booking_date']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']