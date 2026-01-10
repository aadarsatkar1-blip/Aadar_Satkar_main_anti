"""
Script to fix the Contact link in Navbar to allow scrolling.
Replaces href="{% url 'contact' %}" with href="#contact".
"""
import os
import re

base_dir = r'd:\shubham\cursor_django_adhar\Adhar_app\templates'

# All templates to check
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
    'index.html'
]

def fix_contact_link(filepath):
    """Replace {% url 'contact' %} with #contact"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace the Django URL tag for contact with ID anchor
        # Matches single or double quotes
        content = re.sub(
            r'href=["\']\{\%\s*url\s*[\'"]contact[\'"]\s*\%\}\s*["\']', 
            'href="#contact"', 
            content
        )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed contact link in {os.path.basename(filepath)}")
        else:
            print(f"- No changes needed for {os.path.basename(filepath)}")
            
    except Exception as e:
        print(f"✗ Error updating {filepath}: {e}")

print("Fixing Contact links...")
print("=" * 60)

for template in all_templates:
    filepath = os.path.join(base_dir, template)
    if os.path.exists(filepath):
        fix_contact_link(filepath)
    else:
        print(f"✗ Not found: {template}")

print("=" * 60)
print("Contact link update complete!")
