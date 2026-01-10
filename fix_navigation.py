"""
Script to convert HTML navigation links to Django URL tags
"""
import os
import re

base_dir = r'd:\shubham\cursor_django_adhar\Adhar_app\templates'

# All templates to update
all_templates = [
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

def update_navigation(filepath):
    """Update navigation links to use Django URL tags"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace HTML links with Django URL tags
        replacements = [
            # Destination links
            (r'href="bali\.html"', 'href="{% url \'bali\' %}"'),
            (r'href="maldives\.html"', 'href="{% url \'maldives\' %}"'),
            (r'href="india\.html"', 'href="{% url \'india\' %}"'),
            (r'href="switzerland\.html"', 'href="{% url \'switzerland\' %}"'),
            (r'href="italy\.html"', 'href="{% url \'italy\' %}"'),
            (r'href="Spain\.html"', 'href="{% url \'spain\' %}"'),
            (r'href="spain\.html"', 'href="{% url \'spain\' %}"'),
            (r'href="germany\.html"', 'href="{% url \'germany\' %}"'),
            (r'href="afferica\.html"', 'href="{% url \'affrica\' %}"'),
            (r'href="thailand\.html"', 'href="{% url \'thailand\' %}"'),
            (r'href="maxico\.html"', 'href="{% url \'maxico\' %}"'),
            
            # Destination links with path
            (r'href="destinations/bali\.html"', 'href="{% url \'bali\' %}"'),
            (r'href="destinations/maldives\.html"', 'href="{% url \'maldives\' %}"'),
            (r'href="destinations/india\.html"', 'href="{% url \'india\' %}"'),
            (r'href="destinations/switzerland\.html"', 'href="{% url \'switzerland\' %}"'),
            (r'href="destinations/italy\.html"', 'href="{% url \'italy\' %}"'),
            (r'href="destinations/Spain\.html"', 'href="{% url \'spain\' %}"'),
            
            # Service links
            (r'href="weddings\.html"', 'href="{% url \'weddings\' %}"'),
            (r'href="student_tour\.html"', 'href="{% url \'student_tour\' %}"'),
            (r'href="student_tours\.html"', 'href="{% url \'student_tour\' %}"'),
            (r'href="medical_tourism\.html"', 'href="{% url \'medical_tourism\' %}"'),
            (r'href="plan_your_trip\.html"', 'href="{% url \'plan_your_trip\' %}"'),
            
            # Service links with path
            (r'href="\.\./weddings\.html"', 'href="{% url \'weddings\' %}"'),
            (r'href="\.\./student_tour\.html"', 'href="{% url \'student_tour\' %}"'),
            (r'href="\.\./medical_tourism\.html"', 'href="{% url \'medical_tourism\' %}"'),
            (r'href="\.\./plan_your_trip\.html"', 'href="{% url \'plan_your_trip\' %}"'),
            
            # Info pages
            (r'href="view_all_destinations\.html"', 'href="{% url \'view_all_destinations\' %}"'),
            (r'href="\.\./view_all_destinations\.html"', 'href="{% url \'view_all_destinations\' %}"'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Only write if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated navigation in {os.path.basename(filepath)}")
        else:
            print(f"- No changes needed for {os.path.basename(filepath)}")
        
    except Exception as e:
        print(f"✗ Error updating {filepath}: {e}")

print("Updating navigation links to Django URL tags...")
print("=" * 60)

for template in all_templates:
    filepath = os.path.join(base_dir, template)
    if os.path.exists(filepath):
        update_navigation(filepath)
    else:
        print(f"✗ Not found: {template}")

print("=" * 60)
print("Navigation update complete!")
print("\nNow all links should use Django URL routing!")
