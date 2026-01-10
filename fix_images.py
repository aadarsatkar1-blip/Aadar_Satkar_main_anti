"""
Script to fix ALL image references in templates
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

def update_images(filepath):
    """Update all image references to use Django static tags"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Background images: url('/images/...') -> url('{% static 'images/...' %}')
        # Capture the path inside /images/...
        # Regex explanation:
        # url\(        Match url(
        # ['"]?        Match optional quote
        # (/images/    Match start of path (Group 1 start)
        # [^'"]+)      Match anything not a quote (Group 1 end)
        # ['"]?        Match optional closing quote
        # \)           Match closing )
        
        def replace_bg_url(match):
            path = match.group(1) # e.g. /images/Bali.jpg
            static_path = path.lstrip('/')
            return f"url('{{% static '{static_path}' %}}')"

        content = re.sub(r"url\(['\"]?(/images/[^'\")]+)['\"]?\)", replace_bg_url, content)
        
        
        # 2. Img src: src="/images/..." -> src="{% static 'images/...' %}"
        def replace_img_src(match):
            path = match.group(1)
            static_path = path.lstrip('/')
            return f'src="{{% static \'{static_path}\' %}}"'

        content = re.sub(r'src="(/images/[^"]+)"', replace_img_src, content)
        
        
        # 3. Poster images: poster="/images/..."
        def replace_poster_src(match):
            path = match.group(1)
            static_path = path.lstrip('/')
            return f'poster="{{% static \'{static_path}\' %}}"'

        content = re.sub(r'poster="(/images/[^"]+)"', replace_poster_src, content)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated images in {os.path.basename(filepath)}")
        else:
            print(f"- No image changes needed for {os.path.basename(filepath)}")
            
    except Exception as e:
        print(f"✗ Error updating {filepath}: {e}")

print("Fixing all image references...")
print("=" * 60)

for template in all_templates:
    filepath = os.path.join(base_dir, template)
    if os.path.exists(filepath):
        update_images(filepath)
    else:
        print(f"✗ Not found: {template}")

print("=" * 60)
print("Image update complete!")
