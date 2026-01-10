"""
Script to convert HTML templates to use Django static tags
"""
import os
import re

# Base directory
base_dir = r'd:\shubham\cursor_django_adhar\Adhar_app\templates'

# List of templates to update
templates = [
    'medical_tourism.html',
    'student_tour.html',
    'weddings.html',
    'plan_your_trip.html',
    'view_all_destinations.html',
    'small_group_expertes.html',
    'immersive_experiences.html',
    'local_based_leaders.html',
    'like_minded_travellers.html',
    'making_a_difference.html',
    'B_crop_cirtificate.html',
    'Germany.html',
]

# Destination templates
dest_templates = [
    'destinations/bali.html',
    'destinations/maldives.html', 
    'destinations/india.html',
    'destinations/switzerland.html',
    'destinations/italy.html',
    'destinations/Spain.html',
    'destinations/afferica.html',
    'destinations/thailand.html',
    'destinations/maxico.html',
]

all_templates = templates + dest_templates

def update_template(filepath):
    """Update a single template file to use Django static tags"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has {% load static %}
        if '{% load static %}' in content:
            print(f"✓ {os.path.basename(filepath)} already has {{% load static %}}")
            return
        
        # Add {% load static %} at the top after <!DOCTYPE html>
        if '<!DOCTYPE html>' in content:
            content = content.replace('<!DOCTYPE html>', '{% load static %}\n<!DOCTYPE html>', 1)
        
        # Replace hardcoded static paths
        replacements = [
            # CSS Files
            (r'href="/src/styles\.css"', 'href="{% static \'styles.css\' %}"'),
            (r'href="/static/src/styles\.css"', 'href="{% static \'styles.css\' %}"'),
            
            # JavaScript Files
            (r'src="/src/script\.js"', 'src="{% static \'src/script.js\' %}"'),
            (r'src="/static/src/script\.js"', 'src="{% static \'src/script.js\' %}"'),
            
            # Images
            (r'src="/images/logo\.jpg"', 'src="{% static \'images/logo.jpg\' %}"'),
            (r'href="/images/favicon\.png"', 'href="{% static \'images/favicon.png\' %}"'),
            
            # HTML links (convert to Django URL tags later if needed)
            (r'href="\.\./index\.html"', 'href="{% url \'home\' %}"'),
            (r'href="\.\.\/\.\.\/index\.html"', 'href="{% url \'home\' %}"'),
            (r'href="index\.html"', 'href="{% url \'home\' %}"'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Updated {os.path.basename(filepath)}")
        
    except Exception as e:
        print(f"✗ Error updating {filepath}: {e}")

# Update all templates
print("Starting template updates...")
print("=" * 50)

for template in all_templates:
    filepath = os.path.join(base_dir, template)
    if os.path.exists(filepath):
        update_template(filepath)
    else:
        print(f"✗ Not found: {template}")

print("=" * 50)
print("Template update complete!")
