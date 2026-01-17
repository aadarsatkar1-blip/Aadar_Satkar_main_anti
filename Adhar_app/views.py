from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Destination, Subscriber, Enquiry
from django.conf import settings
from supabase import create_client
import threading

# Create your views here.

# Initialize Supabase client
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# Home Page
def home(request):
    # Fetch specific popular destinations by slug for the homepage cards
    # Using select_related to optimize parent relationship if needed
    popular_slugs = ['germany', 'italy', 'africa', 'spain', 'maldives', 'bali']
    destinations = Destination.objects.filter(slug__in=popular_slugs).select_related('parent')
    
    # Sort them to match the desired order
    dest_map = {d.slug: d for d in destinations}
    sorted_destinations = [dest_map[slug] for slug in popular_slugs if slug in dest_map]
    
    # Fetch special category destinations for the "Specialized Travel" section
    # Optimized: Single query instead of 3 separate queries
    category_dests = list(Destination.objects.filter(
        is_active=True, 
        category__in=['student', 'wedding', 'medical']
    ).order_by('category', 'created_at'))
    
    # Map to individual variables - get first of each category
    student_dest = next((d for d in category_dests if d.category == 'student'), None)
    wedding_dest = next((d for d in category_dests if d.category == 'wedding'), None)
    medical_dest = next((d for d in category_dests if d.category == 'medical'), None)
    
    context = {
        'page_title': 'Aadar Satkar | Best Travel & Tour Planning',
        'destinations': sorted_destinations,
        'student_dest': student_dest,
        'wedding_dest': wedding_dest,
        'medical_dest': medical_dest,
    }
    return render(request, 'index.html', context)

# Destination Views
# ... (Keep existing hardcoded views if you want strict backward compat, 
# but ideally we replace them. For now, let's ADD the generic view at the end)

# def bali(request):
#     context = {
#         'destination': 'Bali',
#         'description': 'Experience the magic of Bali with stunning beaches, ancient temples, and vibrant culture.'
#     }
#     return render(request, 'destinations/bali.html', context)

# def maldives(request):
#     context = {
#         'destination': 'Maldives',
#         'description': 'Discover paradise in the Maldives with crystal-clear waters and luxury resorts.'
#     }
#     return render(request, 'destinations/maldives.html', context)

# def india(request):
#     context = {
#         'destination': 'India',
#         'description': 'Explore incredible India with its rich heritage, diverse cultures, and breathtaking landscapes.'
#     }
#     return render(request, 'destinations/india.html', context)

# def switzerland(request):
#     context = {
#         'destination': 'Switzerland',
#         'description': 'Experience the Swiss Alps, pristine lakes, and charming cities.'
#     }
#     return render(request, 'destinations/switzerland.html', context)

# def italy(request):
#     context = {
#         'destination': 'Italy',
#         'description': 'Immerse yourself in Italian art, culture, cuisine, and history.'
#     }
#     return render(request, 'destinations/italy.html', context)

# def spain(request):
#     context = {
#         'destination': 'Spain',
#         'description': 'Discover Spanish passion through flamenco, tapas, and stunning architecture.'
#     }
#     return render(request, 'destinations/Spain.html', context)

# def germany(request):
#     context = {
#         'destination': 'Germany',
#         'description': 'Explore German castles, beer gardens, and rich history.'
#     }
#     return render(request, 'Germany.html', context)

# def affrica(request):
#     context = {
#         'destination': 'Africa',
#         'description': 'Embark on an African safari adventure and witness incredible wildlife.'
#     }
#     return render(request, 'destinations/afferica.html', context)

# def thailand(request):
#     context = {
#         'destination': 'Thailand',
#         'description': 'Experience Thai hospitality, beaches, temples, and delicious cuisine.'
#     }
#     return render(request, 'destinations/thailand.html', context)

# def maxico(request):
#     context = {
#         'destination': 'Mexico',
#         'description': 'Discover ancient Mayan ruins, beautiful beaches, and vibrant culture.'
#     }
#     return render(request, 'destinations/maxico.html', context)

# # India Destinations
# def jaipur(request):
#     context = {
#         'destination': 'Jaipur',
#         'description': 'The Pink City with magnificent palaces and forts.'
#     }
#     return render(request, 'destinations/india.html', context)

# def kerala(request):
#     context = {
#         'destination': 'Kerala',
#         'description': 'God\'s Own Country with backwaters and lush greenery.'
#     }
#     return render(request, 'destinations/india.html', context)

# def goa(request):
#     context = {
#         'destination': 'Goa',
#         'description': 'Beach paradise with Portuguese heritage.'
#     }
#     return render(request, 'destinations/india.html', context)

# Special Services
def weddings(request):
    # Optimized: Use select_related to avoid N+1 queries for parent relationships
    destinations = Destination.objects.filter(
        is_active=True, 
        category='wedding'
    ).select_related('parent').order_by('-created_at')
    return render(request, 'weddings.html', {'destinations': destinations})

def student_tour(request):
    # Optimized: Use select_related to avoid N+1 queries for parent relationships
    destinations = Destination.objects.filter(
        is_active=True, 
        category='student'
    ).select_related('parent').order_by('-created_at')
    return render(request, 'student_tour.html', {'destinations': destinations})

def medical_tourism(request):
    # Optimized: Use select_related to avoid N+1 queries for parent relationships
    destinations = Destination.objects.filter(
        is_active=True, 
        category='medical'
    ).select_related('parent').order_by('-created_at')
    return render(request, 'medical_tourism.html', {'destinations': destinations})

def extra(request):
    return render(request, 'index.html')

# Information Pages
def view_all_destinations(request):
    # Fetch all active destinations that are Countries (no parent)
    # Optimized: Prefetch related sub_destinations to avoid N+1 queries
    destinations = Destination.objects.filter(
        is_active=True, 
        parent__isnull=True
    ).prefetch_related('sub_destinations').order_by('-created_at')
    return render(request, 'view_all_destinations.html', {'destinations': destinations})

def destination_detail(request, slug):
    # Optimized: Use select_related and prefetch_related to avoid N+1 queries
    destination = get_object_or_404(
        Destination.objects.select_related('parent').prefetch_related('packages'),
        slug=slug
    )
    
    # Check if this destination has children (sub-destinations)
    sub_destinations = destination.sub_destinations.filter(is_active=True).select_related('parent')
    
    if sub_destinations.exists():
        # It's a Country -> Show list of Cities (Sub-Destinations)
        return render(request, 'country_detail.html', {
            'destination': destination,
            'sub_destinations': sub_destinations
        })
    else:
        # It's a City/End-Node -> Show Packages (Existing Logic)
        # Packages are already prefetched above
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

# Form Handlers
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                # 1. Store in Django DB (Regular flow)
                Subscriber.objects.update_or_create(email=email)
                
                # 2. Store in Supabase directly via API (For redundancy and dashboard visibility)
                # Using a background thread to prevent hanging the main request
                def store_in_supabase(email_addr):
                    try:
                        # Try 'subscribers' table
                        try:
                            supabase.table("subscribers").upsert({"email": email_addr}).execute()
                        except Exception as e:
                            # Fallback to Django table name
                            supabase.table("Adhar_app_subscriber").upsert({"email": email_addr}).execute()
                    except Exception as e:
                        print(f"Supabase Background Storage Warning: {e}")

                threading.Thread(target=store_in_supabase, args=(email,)).start()
                
                return JsonResponse({'status': 'success', 'message': f'Thank you for subscribing with {email}!'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def submit_enquiry(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        destination_name = request.POST.get('destination')
        message = request.POST.get('message')
        
        # Optional fields from other potential forms
        travel_date = request.POST.get('travel_date') 
        budget = request.POST.get('budget')

        if name and email and phone:
            try:
                # Try to find destination object if destination_name is provided
                destination_obj = None
                if destination_name:
                    # Try exact match or slug match
                    destination_obj = Destination.objects.filter(name__iexact=destination_name).first()
                    if not destination_obj:
                        destination_obj = Destination.objects.filter(slug__iexact=destination_name).first()

                Enquiry.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    destination=destination_obj,
                    message=f"Destination: {destination_name}\n\n{message}" if not destination_obj else message,
                    travel_date=travel_date if travel_date else None,
                    budget=budget if budget else ''
                )
                
                # Store in Supabase directly via API (For redundancy and dashboard visibility)
                # Using a background thread to prevent hanging the main request
                def store_enquiry_in_supabase():
                    try:
                        enquiry_data = {
                            "name": name,
                            "email": email,
                            "phone": phone,
                            "message": f"Destination: {destination_name}\n\n{message}" if not destination_obj else (message or ""),
                            "travel_date": travel_date,
                            "budget": budget or ""
                        }
                        # Try 'enquiries' table first
                        try:
                            supabase.table("enquiries").insert(enquiry_data).execute()
                        except Exception:
                            # Fallback to Django table name
                            supabase.table("Adhar_app_enquiry").insert(enquiry_data).execute()
                    except Exception as e:
                        print(f"Supabase Enquiry Background Storage Warning: {e}")

                threading.Thread(target=store_enquiry_in_supabase).start()
                return JsonResponse({'status': 'success', 'message': 'Your enquiry has been submitted successfully!'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
