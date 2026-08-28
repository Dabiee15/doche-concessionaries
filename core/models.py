from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from django.templatetags.static import static as static_url
import os

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Upload image file directly from device")
    image_url = models.CharField(max_length=500, blank=True, help_text="External Image URL (fallback)")
    badge_tag = models.CharField(max_length=50, blank=True, default='Fresh Baked')
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_image_url(self):
        if self.image:
            base_name = os.path.basename(self.image.name)
            # Check staticfiles/ (collectstatic output used in production by WhiteNoise)
            for candidate_dir in ['staticfiles', 'static']:
                candidate = os.path.join(settings.BASE_DIR, candidate_dir, 'images', base_name)
                if os.path.exists(candidate):
                    return static_url(f'images/{base_name}')
            return self.image.url
        if self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=800&q=80'

    def __str__(self):
        return f"{self.name} - ₦{self.starting_price}"


class Service(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    minimum_notice_days = models.IntegerField(default=2)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Confirmation'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    booking_date = models.DateField()
    booking_time = models.TimeField()
    quantity_notes = models.TextField(help_text='Specify quantity, flavor, or event details', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.pk is None and self.booking_date and self.booking_date < timezone.now().date():
            raise ValidationError({'booking_date': 'Booking date cannot be in the past.'})
        existing = Booking.objects.filter(
            booking_date=self.booking_date,
            booking_time=self.booking_time,
            status='CONFIRMED'
        ).exclude(pk=self.pk)
        if existing.exists():
            raise ValidationError('This slot is already confirmed. Please choose another date or time.')

    def __str__(self):
        return f'{self.customer_name} - {self.booking_date} ({self.status})'