from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Service, Booking
from .forms import BookingForm

def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    featured = products.filter(is_featured=True)
    services = Service.objects.all()
    return render(request, 'home.html', {
        'categories': categories,
        'products': products,
        'featured': featured,
        'services': services,
    })

def product_list(request):
    query = request.GET.get('q', '')
    cat_slug = request.GET.get('category', '')
    
    products = Product.objects.filter(is_available=True)
    if cat_slug:
        products = products.filter(category__slug=cat_slug)
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(badge_tag__icontains=query))
        
    categories = Category.objects.all()
    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': cat_slug,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:3]
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products,
    })

def booking_view(request):
    selected_product_id = request.GET.get('product')
    initial_data = {}
    selected_product = None
    if selected_product_id:
        selected_product = Product.objects.filter(id=selected_product_id, is_available=True).first()
        if selected_product:
            initial_data['product'] = selected_product.id

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            
            # Calculate estimated price
            est = 0
            if booking.service:
                est += float(booking.service.base_price)
            if booking.product:
                est += float(booking.product.starting_price)
            booking.estimated_price = est if est > 0 else 5000.00
            
            # Check slot availability validation
            existing = Booking.objects.filter(
                booking_date=booking.booking_date,
                booking_time=booking.booking_time,
                status='CONFIRMED'
            )
            if existing.exists():
                form.add_error('booking_time', 'This slot is already booked and confirmed! Please select another date or time slot.')
            else:
                booking.save()
                messages.success(request, 'Your booking request has been submitted successfully!')
                return redirect('booking_success', pk=booking.pk)
        else:
            messages.error(request, 'Please correct the errors in the form below.')
    else:
        form = BookingForm(initial=initial_data)

    services = Service.objects.all()
    products = Product.objects.filter(is_available=True)
    return render(request, 'booking.html', {
        'form': form,
        'services': services,
        'products': products,
        'selected_product': selected_product,
    })

def booking_success(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'booking_success.html', {'booking': booking})

def manage_bookings(request):
    status_filter = request.GET.get('status', '')
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        new_status = request.POST.get('status')
        if booking_id and new_status:
            booking = get_object_or_404(Booking, pk=booking_id)
            booking.status = new_status
            booking.save()
            messages.success(request, f'Updated status for booking #{booking.id} to {new_status}.')
            return redirect('manage_bookings')

    bookings = Booking.objects.all().order_by('-created_at')
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    return render(request, 'manage_bookings.html', {
        'bookings': bookings,
        'current_filter': status_filter,
    })

def edit_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            b = form.save(commit=False)
            if 'estimated_price' in request.POST and request.POST['estimated_price']:
                try:
                    b.estimated_price = float(request.POST['estimated_price'])
                except ValueError:
                    pass
            if 'status' in request.POST and request.POST['status']:
                b.status = request.POST['status']
            b.save()
            messages.success(request, f'Updated booking details for #{booking.id} successfully.')
            return redirect('manage_bookings')
        else:
            messages.error(request, 'Please check form inputs.')
    else:
        form = BookingForm(instance=booking)

    return render(request, 'edit_booking.html', {
        'form': form,
        'booking': booking,
    })