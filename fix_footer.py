"""
Script to ensure all templates have id="contact" in the footer.
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

def add_contact_id(filepath):
    """Add id="contact" to footer tag if missing"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check if id="contact" already exists in footer
        if '<footer class="footer" id="contact">' in content:
            print(f"- Already properly set in {os.path.basename(filepath)}")
            return

        # Replace standard footer class with id appended
        # Pattern matches <footer class="footer"> with optional whitespace
        content = re.sub(
            r'<footer class="footer">', 
            '<footer class="footer" id="contact">', 
            content
        )
        
        # Fallback for other variations if simple sub fails (e.g. no class)
        if content == original_content and '<footer' in content and 'id="contact"' not in content:
            # Try replacing just <footer
            content = re.sub(r'<footer(?![^>]*id="contact")', '<footer id="contact"', content, count=1)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Added id='contact' to {os.path.basename(filepath)}")
        else:
            print(f"- No changes needed for {os.path.basename(filepath)}")
            
    except Exception as e:
        print(f"✗ Error updating {filepath}: {e}")

print("Fixing footer IDs...")
print("=" * 60)

for template in all_templates:
    filepath = os.path.join(base_dir, template)
    if os.path.exists(filepath):
        add_contact_id(filepath)
    else:
        print(f"✗ Not found: {template}")

print("=" * 60)
print("Footer update complete!")
