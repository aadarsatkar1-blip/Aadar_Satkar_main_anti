import os
import django
import re
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Adhar_django.settings')
django.setup()

from Adhar_app.models import Destination, Package
from django.core.files.base import ContentFile

# Map slug/filename to Country Name
TEMPLATE_MAP = {
    'bali': 'Bali',
    'maldives': 'Maldives',
    'india': 'India',
    'switzerland': 'Switzerland',
    'italy': 'Italy',
    'Spain': 'Spain',
    'Germany': 'Germany',
    'afferica': 'Africa',
    'thailand': 'Thailand',
    'maxico': 'Mexico',
    'jaipur': 'India', # Handle carefully, might be duplicated if processed with India
    # Note: India template might contain Jaipur/Kerala/Goa or they might be separate
}

TEMPLATE_DIR = os.path.join('Adhar_app', 'templates', 'destinations')
# Germany and others might be in root templates dir
ROOT_TEMPLATE_DIR = os.path.join('Adhar_app', 'templates')

def process_template(filename, country_name, file_path):
    print(f"Processing {country_name} from {filename}...")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. Get/Create Country
    country_slug = country_name.lower().replace(' ', '-')
    country, created = Destination.objects.get_or_create(
        slug=country_slug,
        defaults={
            'name': country_name,
            'is_active': True,
            'parent': None # Root
        }
    )
    if created:
        print(f"Created Country: {country.name}")
    else:
        print(f"Found Country: {country.name}")

    # 2. Extract Sub-Destinations
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
        style = card.find('div', class_='dest-image')['style']
        # extract url('...') inside style
        match = re.search(r"url\('?([^']+)'?\)", style)
        image_url = match.group(1) if match else ""
        # Clean static url
        if image_url.startswith("{% static '"):
            image_url = image_url.replace("{% static '", "").replace("' %}", "")
        elif image_url.startswith("/static/"):
            image_url = image_url.replace("/static/", "")

        # Create Sub-Destination (City)
        sub_slug = title.lower().replace(' ', '-')
        sub_dest, sub_created = Destination.objects.get_or_create(
            slug=sub_slug,
            parent=country,
            defaults={
                'name': title,
                'description': desc,
                'is_active': True
            }
        )
        
        if sub_created:
            print(f"  Created Sub-Dest: {title}")
            # Note: handling image upload/association is complex efficiently here without file copy
            # We will skip physical image copy for now and let user handle it or use a placeholder logic if strictly needed
            # Or mapped partially if we had the file.
        
        # 3. Create Default Package for this Sub-Dest (so modal works)
        if not sub_dest.packages.exists():
            Package.objects.create(
                destination=sub_dest,
                title=f"Best of {title}",
                duration="5 Days / 4 Nights",
                price=25000.00,
                overview=f"Enjoy a wonderful trip to {title}. {desc}",
                # image=... (Skip image to avoid errors, template will use fallback or manual fix needed)
            )
            print(f"    Created Default Package for {title}")
        
        count += 1
    print(f"Processed {count} destinations for {country_name}\n")

# List of files and their mapped Country Name
files_to_process = [
    ('bali.html', 'Bali'),
    ('maldives.html', 'Maldives'),
    ('india.html', 'India'),
    ('switzerland.html', 'Switzerland'),
    ('italy.html', 'Italy'),
    ('Spain.html', 'Spain'),
    ('thailand.html', 'Thailand'),
    ('maxico.html', 'Mexico'),
    ('afferica.html', 'Africa'),
    # Germany is in root, but process logic joins with destinations dir.
    # So we need ../Germany.html
    ('../Germany.html', 'Germany'), 
]

for relative_path, c_name in files_to_process:
    full_path = os.path.join(TEMPLATE_DIR, relative_path)
    # Adjust for ../
    if relative_path.startswith('../'):
        full_path = os.path.join(ROOT_TEMPLATE_DIR, relative_path.replace('../', ''))
        
    process_template(relative_path, c_name, full_path)
