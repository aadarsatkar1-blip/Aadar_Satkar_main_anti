from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Destination

# Create your views here.

# Home Page
def home(request):
    # Fetch specific popular destinations by slug for the homepage cards
    popular_slugs = ['germany', 'italy', 'africa', 'spain', 'maldives', 'bali']
    destinations = Destination.objects.filter(slug__in=popular_slugs)
    
    # Sort them to match the desired order
    dest_map = {d.slug: d for d in destinations}
    sorted_destinations = [dest_map[slug] for slug in popular_slugs if slug in dest_map]
    
    context = {
        'page_title': 'Aadar Satkar | Best Travel & Tour Planning',
        'destinations': sorted_destinations,
    }
    return render(request, 'index.html', context)

# Destination Views
# ... (Keep existing hardcoded views if you want strict backward compat, 
# but ideally we replace them. For now, let's ADD the generic view at the end)

def bali(request):
    context = {
        'destination': 'Bali',
        'description': 'Experience the magic of Bali with stunning beaches, ancient temples, and vibrant culture.'
    }
    return render(request, 'destinations/bali.html', context)

def maldives(request):
    context = {
        'destination': 'Maldives',
        'description': 'Discover paradise in the Maldives with crystal-clear waters and luxury resorts.'
    }
    return render(request, 'destinations/maldives.html', context)

def india(request):
    context = {
        'destination': 'India',
        'description': 'Explore incredible India with its rich heritage, diverse cultures, and breathtaking landscapes.'
    }
    return render(request, 'destinations/india.html', context)

def switzerland(request):
    context = {
        'destination': 'Switzerland',
        'description': 'Experience the Swiss Alps, pristine lakes, and charming cities.'
    }
    return render(request, 'destinations/switzerland.html', context)

def italy(request):
    context = {
        'destination': 'Italy',
        'description': 'Immerse yourself in Italian art, culture, cuisine, and history.'
    }
    return render(request, 'destinations/italy.html', context)

def spain(request):
    context = {
        'destination': 'Spain',
        'description': 'Discover Spanish passion through flamenco, tapas, and stunning architecture.'
    }
    return render(request, 'destinations/Spain.html', context)

def germany(request):
    context = {
        'destination': 'Germany',
        'description': 'Explore German castles, beer gardens, and rich history.'
    }
    return render(request, 'Germany.html', context)

def affrica(request):
    context = {
        'destination': 'Africa',
        'description': 'Embark on an African safari adventure and witness incredible wildlife.'
    }
    return render(request, 'destinations/afferica.html', context)

def thailand(request):
    context = {
        'destination': 'Thailand',
        'description': 'Experience Thai hospitality, beaches, temples, and delicious cuisine.'
    }
    return render(request, 'destinations/thailand.html', context)

def maxico(request):
    context = {
        'destination': 'Mexico',
        'description': 'Discover ancient Mayan ruins, beautiful beaches, and vibrant culture.'
    }
    return render(request, 'destinations/maxico.html', context)

# India Destinations
def jaipur(request):
    context = {
        'destination': 'Jaipur',
        'description': 'The Pink City with magnificent palaces and forts.'
    }
    return render(request, 'destinations/india.html', context)

def kerala(request):
    context = {
        'destination': 'Kerala',
        'description': 'God\'s Own Country with backwaters and lush greenery.'
    }
    return render(request, 'destinations/india.html', context)

def goa(request):
    context = {
        'destination': 'Goa',
        'description': 'Beach paradise with Portuguese heritage.'
    }
    return render(request, 'destinations/india.html', context)

# Special Services
def weddings(request):
    return render(request, 'weddings.html')

def student_tour(request):
    return render(request, 'student_tour.html')

def medical_tourism(request):
    return render(request, 'medical_tourism.html')

def extra(request):
    return render(request, 'index.html')

# Information Pages
def view_all_destinations(request):
    # Fetch all active destinations that are Countries (no parent)
    destinations = Destination.objects.filter(is_active=True, parent__isnull=True).order_by('-created_at')
    return render(request, 'view_all_destinations.html', {'destinations': destinations})

def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    
    # Check if this destination has children (sub-destinations)
    sub_destinations = destination.sub_destinations.filter(is_active=True)
    
    if sub_destinations.exists():
        # It's a Country -> Show list of Cities (Sub-Destinations)
        return render(request, 'country_detail.html', {
            'destination': destination,
            'sub_destinations': sub_destinations
        })
    else:
        # It's a City/End-Node -> Show Packages (Existing Logic)
        return render(request, 'destination_detail.html', {'destination': destination})

def small_group_expertes(request):
    return render(request, 'small_group_expertes.html')

def immersive_experiences(request):
    return render(request, 'immersive_experiences.html')

def local_based_leaders(request):
    return render(request, 'local_based_leaders.html')

def like_minded_travellers(request):
    return render(request, 'like_minded_travellers.html')

def making_a_difference(request):
    return render(request, 'making_a_difference.html')

def B_crop_cirtificate(request):
    return render(request, 'B_crop_cirtificate.html')

def plan_your_trip(request):
    return render(request, 'plan_your_trip.html')

# Footer Links - Placeholder views
def meet_the_foundation(request):
    return render(request, 'index.html')

def our_story(request):
    return render(request, 'index.html')

def our_purpose(request):
    return render(request, 'index.html')

def careers(request):
    return render(request, 'index.html')

def trip_styles(request):
    return render(request, 'index.html')

def destinations(request):
    return render(request, 'view_all_destinations.html')

def travel_tips(request):
    return render(request, 'index.html')

def faqs(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'index.html')

# Social Media - External redirects (you can add proper redirects later)
def facebook(request):
    from django.shortcuts import redirect
    return redirect('https://facebook.com')

def instagram(request):
    from django.shortcuts import redirect
    return redirect('https://instagram.com')

def twitter(request):
    from django.shortcuts import redirect
    return redirect('https://twitter.com')
