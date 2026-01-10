import os
import django
from django.core.files import File
from django.conf import settings
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Adhar_django.settings')
django.setup()

from Adhar_app.models import Destination

def populate_images():
    # Source directory for static images
    STATIC_IMAGES_DIR = Path(settings.BASE_DIR) / 'Adhar_app' / 'static' / 'images'
    
    if not STATIC_IMAGES_DIR.exists():
        print(f"Error: Static images directory not found at {STATIC_IMAGES_DIR}")
        return

    destinations = Destination.objects.all()
    print(f"Checking {destinations.count()} destinations for missing images...")

    updated_count = 0
    
    for dest in destinations:
        # if dest.image:
        #     print(f"Skipping {dest.name} (already has image)")
        #     continue
            
        # Try to find a matching image
        # Priority 1: Exact name match (e.g. "Jaipur.jpg")
        # Priority 2: Slug match (e.g. "jaipur.jpg")
        # Priority 3: Name with spaces (e.g. "Costa Rica.jpg")
        
        possible_names = [
            f"{dest.name}.jpg",
            f"{dest.name}.jpeg",
            f"{dest.name}.png",
            f"{dest.name}.webp",
            f"{dest.slug}.jpg",
            f"{dest.slug}.jpeg",
            f"{dest.slug}.png",
            f"{dest.slug}.webp",
            # Special cases for names with spaces
            f"{dest.name.replace(' ', '%20')}.jpg", 
        ]
        
        found_file = None
        
        # Check standard paths
        for filename in possible_names:
            file_path = STATIC_IMAGES_DIR / filename
            if file_path.exists():
                found_file = file_path
                break
        
        # Fuzzy matching if not found (e.g. "Delhi, India.jpg" for "Delhi")
        if not found_file:
            for file_path in STATIC_IMAGES_DIR.glob('*'):
                if file_path.is_file():
                    # Check if destination name is part of filename (case insensitive)
                    if dest.name.lower() in file_path.name.lower():
                        found_file = file_path
                        break

        if found_file:
            print(f"Found image for {dest.name}: {found_file.name}")
            try:
                # Open the file and save it to the model
                # We interpret the file content and save it to the image field
                # This will copy it to MEDIA_ROOT
                with open(found_file, 'rb') as f:
                    # Save with the original filename
                    dest.image.save(found_file.name, File(f), save=True)
                    updated_count += 1
            except Exception as e:
                print(f"Failed to save image for {dest.name}: {e}")
        else:
            print(f"No image found for {dest.name}")

    print(f"\nSuccessfully updated {updated_count} destinations with images.")

if __name__ == '__main__':
    populate_images()
