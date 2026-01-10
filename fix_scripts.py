"""
Script to fix script.js path in all templates
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
    'view_all_destinations.html', # Already fixed manually, but good to check
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

def update_scripts(filepath):
    """Update script.js references to use correct static path"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern 1: HTML src="/src/script.js" -> src="{% static 'script.js' %}"
        content = re.sub(r'src="/src/script\.js"', 'src="{% static \'script.js\' %}"', content)
        
        # Pattern 2: Django {% static 'src/script.js' %} -> {% static 'script.js' %}
        # (This catches the ones I might have 'fixed' incorrectly before)
        content = re.sub(r"{% static 'src/script\.js' %}", "{% static 'script.js' %}", content)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated script path in {os.path.basename(filepath)}")
        else:
            print(f"- No script path changes needed for {os.path.basename(filepath)}")
            
    except Exception as e:
        print(f"✗ Error updating {filepath}: {e}")

print("Fixing script paths...")
print("=" * 60)

for template in all_templates:
    filepath = os.path.join(base_dir, template)
    if os.path.exists(filepath):
        update_scripts(filepath)
    else:
        print(f"✗ Not found: {template}")

print("=" * 60)
print("Script update complete!")
