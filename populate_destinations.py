
import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Adhar_django.settings')
django.setup()

from Adhar_app.models import Destination
from django.conf import settings

# Source images path (static)
STATIC_IMAGES_DIR = os.path.join(settings.BASE_DIR, 'Adhar_app', 'static', 'images')

# Target media path
MEDIA_DEST_DIR = os.path.join(settings.MEDIA_ROOT, 'destinations')
os.makedirs(MEDIA_DEST_DIR, exist_ok=True)

destinations_data = [
    {
        'name': 'Bali',
        'image_src': 'Bali.jpg',
        'description': 'Experience the magic of Bali with stunning beaches, ancient temples, and vibrant culture.',
        'slug': 'bali'
    },
    {
        'name': 'Maldives',
        'image_src': 'Maldives.jpg',
        'description': 'Discover paradise in the Maldives with crystal-clear waters and luxury resorts.',
        'slug': 'maldives'
    },
    {
        'name': 'Italy',
        'image_src': 'Italy.jpg',
        'description': 'Immerse yourself in Italian art, culture, cuisine, and history.',
        'slug': 'italy'
    },
    {
        'name': 'Switzerland',
        'image_src': 'Switzerland.jpg',
        'description': 'Experience the Swiss Alps, pristine lakes, and charming cities.',
        'slug': 'switzerland'
    },
    {
        'name': 'Germany',
        'image_src': 'germany.jpg',
        'description': 'Explore German castles, beer gardens, and rich history.',
        'slug': 'germany'
    },
    {
        'name': 'Spain',
        'image_src': 'Spain.jpg',
        'description': 'Discover Spanish passion through flamenco, tapas, and stunning architecture.',
        'slug': 'spain'
    },
    {
        'name': 'Africa',
        'image_src': 'Affirca.jpg',
        'description': 'Embark on an African safari adventure and witness incredible wildlife.',
        'slug': 'africa'
    },
    {
        'name': 'Thailand',
        'image_src': 'Thailand.jpg',
        'description': 'Experience Thai hospitality, beaches, temples, and delicious cuisine.',
        'slug': 'thailand'
    },
    {
        'name': 'Mexico',
        'image_src': 'Mexico.jpg',
        'description': 'Discover ancient Mayan ruins, beautiful beaches, and vibrant culture.',
        'slug': 'mexico'
    },
    {
        'name': 'India',
        'image_src': 'India.jpg',
        'description': 'Explore incredible India with its rich heritage, diverse cultures, and breathtaking landscapes.',
        'slug': 'india'
    },
]

print("Starting population...")

for data in destinations_data:
    # 1. Check if image exists in static
    src_path = os.path.join(STATIC_IMAGES_DIR, data['image_src'])
    if os.path.exists(src_path):
        # 2. Copy to media/destinations/
        dest_filename = data['image_src'] # Keep same name
        dest_path = os.path.join(MEDIA_DEST_DIR, dest_filename)
        shutil.copy2(src_path, dest_path)
        print(f"Copied {data['image_src']} to media folder.")
        
        # 3. Create/Update DB Object
        # db path is relative to MEDIA_ROOT
        db_image_path = f"destinations/{dest_filename}"
        
        obj, created = Destination.objects.get_or_create(
            slug=data['slug'],
            defaults={
                'name': data['name'],
                'description': data['description'],
                'image': db_image_path,
                'is_active': True
            }
        )
        if not created:
            obj.image = db_image_path
            obj.save()
            print(f"Updated {data['name']}")
        else:
            print(f"Created {data['name']}")
            
    else:
        print(f"WARNING: Image not found for {data['name']}: {src_path}")

print("Population complete!")
