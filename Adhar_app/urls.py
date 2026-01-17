from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Main Destinations
    # Main Destinations - Commented out to use generic slug view
    # path('bali/', views.bali, name='bali'),
    # path('maldives/', views.maldives, name='maldives'),
    # path('india/', views.india, name='india'),
    # path('switzerland/', views.switzerland, name='switzerland'),
    # path('italy/', views.italy, name='italy'),
    # path('spain/', views.spain, name='spain'),
    # path('germany/', views.germany, name='germany'),
    # path('africa/', views.affrica, name='affrica'),
    # path('thailand/', views.thailand, name='thailand'),
    # path('mexico/', views.maxico, name='maxico'),
    
    # # India Destinations
    # path('jaipur/', views.jaipur, name='jaipur'),
    # path('kerala/', views.kerala, name='kerala'),
    # path('goa/', views.goa, name='goa'),
    
    # Special Services
    path('weddings/', views.weddings, name='weddings'),
    path('student-tour/', views.student_tour, name='student_tour'),
    path('medical-tourism/', views.medical_tourism, name='medical_tourism'),
    path('extra/', views.extra, name='extra'),
    
    # Information Pages
    path('destinations/', views.view_all_destinations, name='view_all_destinations'),
    path('small-group-experts/', views.small_group_expertes, name='small_group_expertes'),
    path('immersive-experiences/', views.immersive_experiences, name='immersive_experiences'),
    path('local-based-leaders/', views.local_based_leaders, name='local_based_leaders'),
    path('like-minded-travellers/', views.like_minded_travellers, name='like_minded_travellers'),
    path('making-a-difference/', views.making_a_difference, name='making_a_difference'),
    path('b-corp-certificate/', views.B_crop_cirtificate, name='B_crop_cirtificate'),
    path('plan-your-trip/', views.plan_your_trip, name='plan_your_trip'),
    
    # Footer Links
    path('meet-the-foundation/', views.meet_the_foundation, name='meet_the_foundation'),
    path('our-story/', views.our_story, name='our_story'),
    path('our-purpose/', views.our_purpose, name='our_purpose'),
    path('careers/', views.careers, name='careers'),
    path('trip-styles/', views.trip_styles, name='trip_styles'),
    path('all-destinations/', views.destinations, name='destinations'),
    path('travel-tips/', views.travel_tips, name='travel_tips'),
    path('faqs/', views.faqs, name='faqs'),
    path('contact/', views.contact, name='contact'),
    
    # Social Media
    path('facebook/', views.facebook, name='facebook'),
    path('instagram/', views.instagram, name='instagram'),
    path('twitter/', views.twitter, name='twitter'),
    
    # Generic Destination Detail (Must be last to avoid conflicts)
    path('<slug:slug>/', views.destination_detail, name='destination_detail'),

    # Form Handlers
    path('subscribe/', views.subscribe, name='subscribe'),
    path('submit-enquiry/', views.submit_enquiry, name='submit_enquiry'),

    
]
