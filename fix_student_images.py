import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Adhar_django.settings')
django.setup()

from Adhar_app.models import Destination

data = {
    'student-historical-india': 'images/History.jpg',
    'student-science-innovation': 'images/Science.jpg',
    'student-himalayan-camps': 'images/Adventure.jpg',
    'student-industrial-visits': 'images/Industry.jpg',
    'student-wildlife-safari': 'images/Nature.jpg',
    'student-nasa-space-camp': 'images/International.jpg',
}

for slug, img in data.items():
    try:
        dest = Destination.objects.get(slug=slug)
        dest.image = img
        dest.save()
        print(f"Updated {slug} with {img}")
    except Destination.DoesNotExist:
        print(f"Destination {slug} not found")
