import os
import django
import re
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Adhar_django.settings')
django.setup()

from Adhar_app.models import Destination, Package
from django.utils.text import slugify

TEMPLATE_DIR = os.path.join('Adhar_app', 'templates')

def process_special_template(filename, category):
    print(f"Processing {filename} for category {category}...")
    file_path = os.path.join(TEMPLATE_DIR, filename)
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract destination cards
    cards = soup.find_all('div', class_='dest-card')
    count = 0
    for card in cards:
        # Extract Title
        title_tag = card.find('h3')
        if not title_tag: continue
        title = title_tag.get_text(strip=True)
        
        # Extract Desc
        desc_tag = card.find('p')
        desc = desc_tag.get_text(strip=True) if desc_tag else ""
        
        # Extract Image URL
        image_div = card.find('div', class_='dest-image')
        image_url = ""
        if image_div:
            if image_div.has_attr('style'):
                style = image_div['style']
                match = re.search(r"url\('?([^']+)'?\)", style)
                image_url = match.group(1) if match else ""
            elif image_div.has_attr('data-bg'):
                image_url = image_div['data-bg']
        
        # Clean static url
        if image_url.startswith("{% static '"):
            image_url = image_url.replace("{% static '", "").replace("' %}", "")
        elif image_url.startswith("/static/"):
            image_url = image_url.replace("/static/", "")

        # Create Destination
        # We prefix the slug with category to avoid conflicts (e.g., 'goa' in Wedding vs India)
        sub_slug = f"{category}-{slugify(title)}"
        
        dest, created = Destination.objects.get_or_create(
            slug=sub_slug,
            defaults={
                'name': title,
                'description': desc,
                'image': image_url, # Note: using static path temporarily, will need media fix if purely dynamic
                'category': category,
                'is_active': True
            }
        )
        
        if created:
            print(f"  Created {category.capitalize()} Destination: {title}")
        else:
            print(f"  Found {category.capitalize()} Destination: {title}")
            dest.category = category
            dest.save()
        
        # Create Default Package for this Dest (so modal works)
        if not dest.packages.exists():
            Package.objects.create(
                destination=dest,
                title=f"Best of {title}",
                duration="5 Days / 4 Nights",
                price=25000.00,
                overview=f"Enjoy a wonderful trip to {title}. {desc}",
            )
            print(f"    Created Default Package for {title}")
        
        count += 1
    print(f"Processed {count} items for {category}\n")

# List of template files and their categories
special_templates = [
    ('student_tour.html', 'student'),
    ('weddings.html', 'wedding'),
    ('medical_tourism.html', 'medical'),
]

if __name__ == "__main__":
    for filename, category in special_templates:
        process_special_template(filename, category)
