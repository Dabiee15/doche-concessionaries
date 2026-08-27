from django import forms
from .models import Booking, Service, Product
from django.utils import timezone

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_email', 'customer_phone', 'service', 'product', 'booking_date', 'booking_time', 'quantity_notes']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name (e.g., Jane Doe)'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@example.com'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number (e.g., 09077925555)'}),
            'service': forms.Select(attrs={'class': 'form-select', 'id': 'id_service'}),
            'product': forms.Select(attrs={'class': 'form-select', 'id': 'id_product'}),
            'booking_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date', 'id': 'id_booking_date'}),
            'booking_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time', 'id': 'id_booking_time'}),
            'quantity_notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Specify quantities, flavors, event theme, or special instructions...'}),
        }

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        if self.instance.pk is None and booking_date and booking_date < timezone.now().date():
            raise forms.ValidationError("Booking date cannot be in the past. Please select a future date.")
        return booking_date
