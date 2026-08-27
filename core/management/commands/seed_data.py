from django.core.management.base import BaseCommand
from core.models import Category, Product, Service

class Command(BaseCommand):
    help = 'Seeds initial sample data for Doche Concessionaries with accurate pricing and product photos'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Doche Concessionaries database with exact updated prices...')

        # Clear old items to refresh cleanly
        Product.objects.all().delete()
        Category.objects.all().delete()
        Service.objects.all().delete()

        # Categories
        cakes_cat = Category.objects.create(name='Signature Cakes', slug='cakes')
        savory_cat = Category.objects.create(name='Savory Snacks', slug='savory-snacks')
        sweet_cat = Category.objects.create(name='Sweet Pastries & Treats', slug='sweet-treats')

        # Services
        services_data = [
            {
                'name': 'Custom Cake Order',
                'description': 'Bespoke multi-tier or single-tier decorated & plain naked cakes tailored for birthdays, weddings, and anniversaries.',
                'minimum_notice_days': 3,
                'base_price': 25000.00
            },
            {
                'name': 'Event Catering & Snack Bar',
                'description': 'Full concessionary snack setups including live Puff Puff stations, party packs, and curated snack platters.',
                'minimum_notice_days': 5,
                'base_price': 50000.00
            },
            {
                'name': 'Bulk Retail & Souvenir Jars',
                'description': 'Branded sealed jars of crunchy peanuts, chin chin, and plantain chips ideal for party souvenirs and retail packs.',
                'minimum_notice_days': 2,
                'base_price': 15000.00
            },
            {
                'name': 'Express Snack Box Delivery',
                'description': 'Freshly prepared daily snack assortments containing cupcakes, foil cakes, ring doughnuts, and egg rolls.',
                'minimum_notice_days': 1,
                'base_price': 8000.00
            },
        ]

        for s in services_data:
            Service.objects.create(**s)

        # Products with exact updated prices requested by user
        products_data = [
            {
                'name': 'Glazed Ring Doughnuts',
                'category': sweet_cat,
                'description': 'Fluffy, pillowy fried glazed ring doughnuts dusted with sweet sugar crystals.',
                'starting_price': 500.00,
                'image_url': 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=800&q=80',
                'badge_tag': 'N500 each',
                'is_featured': True
            },
            {
                'name': 'Golden Stuffed Egg Rolls',
                'category': savory_cat,
                'description': 'Golden crispy fried dough wrapped around a seasoned hard-boiled whole egg.',
                'starting_price': 1000.00,
                'image_url': 'https://images.unsplash.com/photo-1541529086526-db283c563270?auto=format&fit=crop&w=800&q=80',
                'badge_tag': 'N1,000 each',
                'is_featured': True
            },
            {
                'name': 'Golden Sweet Puff Puff',
                'category': sweet_cat,
                'description': 'Traditional West African sweet yeast dough spheres fried to golden perfection.',
                'starting_price': 100.00,
                'image_url': 'https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?auto=format&fit=crop&w=800&q=80',
                'badge_tag': 'N100 per piece',
                'is_featured': True
            },
            {
                'name': 'Quick-Serve Red Velvet Foil Cake',
                'category': cakes_cat,
                'description': 'Moist rich red velvet cake baked directly in a quick-serve foil container with protective wrap.',
                'starting_price': 2000.00,
                'image_url': 'https://images.unsplash.com/photo-1606890737304-57a1ca8a5b62?auto=format&fit=crop&w=800&q=80',
                'badge_tag': 'N2,000 Foil Pack',
                'is_featured': True
            },
            {
                'name': 'Crispy Plantain Chips (Snack Tub)',
                'category': savory_cat,
                'description': 'Thinly sliced organic plantains kettle-fried with light sea salt in clear snack tubs.',
                'starting_price': 1000.00,
                'image_url': 'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?auto=format&fit=crop&w=800&q=80',
                'badge_tag': 'N1,000 Tub',
                'is_featured': True
            },
            {
                'name': 'Artisanal Red Velvet & Marble Cupcakes',
                'category': cakes_cat,
                'description': 'Rich velvet, marble swirl, and chocolate cupcakes baked fresh with light buttery texture and vibrant sponge.',
                'starting_price': 8500.00,
                'image_url': '/media/products/IMG-20260629-WA0042.jpeg',
                'badge_tag': 'Box of 6 (N8,500)',
                'is_featured': True
            },
            {
                'name': 'Crunchy Coated Peanuts (Green Lid Jar)',
                'category': savory_cat,
                'description': 'Our flagship golden flour-coated crunchy roasted peanuts packed in airtight luxury branded Doche green-lid display jars.',
                'starting_price': 3500.00,
                'image_url': '/media/products/IMG-20260827-WA0018.jpg',
                'badge_tag': 'Signature Jar (N3,500)',
                'is_featured': True
            },
            {
                'name': 'Crispy Gourmet Chin Chin (Green Lid Jar)',
                'category': sweet_cat,
                'description': 'Our legendary golden crispy fried pastry bites infused with nutmeg and vanilla in airtight green-lid gift jars.',
                'starting_price': 3500.00,
                'image_url': '/media/products/IMG-20260827-WA0006.jpg',
                'badge_tag': 'Gift Jar (N3,500)',
                'is_featured': True
            },
            {
                'name': 'Crispy Gourmet Chin Chin (Medium Tub)',
                'category': sweet_cat,
                'description': 'Delicious crunchy fried pastry bites packaged in convenient quick-serve clear snack tubs.',
                'starting_price': 1000.00,
                'image_url': '/media/products/IMG-20260827-WA0004.jpg',
                'badge_tag': 'Medium Tub (N1,000)',
                'is_featured': False
            },
            {
                'name': 'Coated Peanuts (Portion Tub)',
                'category': savory_cat,
                'description': 'Doche signature crunchy coated peanuts packaged in microwave-safe portion tubs.',
                'starting_price': 1200.00,
                'image_url': '/media/products/IMG-20260827-WA0016.jpg',
                'badge_tag': 'Portion Tub (N1,200)',
                'is_featured': False
            },
            {
                'name': 'Plain Naked Cake (Non-Decorated Sponge)',
                'category': cakes_cat,
                'description': 'Elegant multi-layered un-frosted plain sponge cake baked to perfection, ideal for custom topping or personal decorating.',
                'starting_price': 25000.00,
                'image_url': 'https://images.unsplash.com/photo-1535141192574-5d4897c13136?auto=format&fit=crop&w=800&q=80',
                'badge_tag': 'Plain Non-Decorated (N25,000)',
                'is_featured': True
            },
        ]

        for p in products_data:
            Product.objects.create(**p)

        self.stdout.write(self.style.SUCCESS('Successfully re-seeded database with Ring Doughnuts N500, Egg Rolls N1000, Puff Puff N100, Foil Cakes N2000, Plantain Chips N1000!'))
