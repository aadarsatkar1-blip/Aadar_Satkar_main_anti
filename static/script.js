// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');

        // Animate hamburger
        hamburger.classList.toggle('active');
    });
}

// Close mobile menu when clicking on a link
if (navMenu && hamburger) {
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', (e) => {
            // Check if this link is a dropdown toggle (has a sibling dropdown-content)
            const dropdownContent = link.nextElementSibling;

            // Only toggle if we are on mobile (check window width or if navMenu has fixed position)
            // A simple check is if the hamburger is visible (display != none)
            const isMobile = window.getComputedStyle(hamburger).display !== 'none';

            if (isMobile && dropdownContent && dropdownContent.classList.contains('dropdown-content')) {
                e.preventDefault(); // Prevent navigation for parent links
                const parent = link.parentElement;
                parent.classList.toggle('active');
            } else {
                // Normal link, close menu
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');

                // Close all open dropdowns
                document.querySelectorAll('.dropdown.active').forEach(d => d.classList.remove('active'));
            }
        });
    });
}

// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Scroll Animation for Elements
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards for animation
document.querySelectorAll('.diff-card, .dest-card, .testimonial-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Newsletter Form Handling with EmailJS
const newsletterForm = document.querySelector('.newsletter-form');

if (newsletterForm) {
    newsletterForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const email = newsletterForm.querySelector('input[type="email"]').value;

        if (!email) return;

        // 💡 Send email to EmailJS
        emailjs.send("service_69zwhft", "template_qdckahs", {
            email: email
        })
            .then(() => {
                alert(`Thank you for subscribing! We'll send updates to ${email}`);
                newsletterForm.reset();
            })
            .catch((error) => {
                console.error("EmailJS Error:", error);
                alert("❌ Subscription failed. Please try again.");
            });
    });
}


//plan your trip form handling with EmailJS
const tripForm = document.getElementById('tripForm');
const formStatus = document.getElementById('formStatus');

if (tripForm && formStatus) {
    tripForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const submitBtn = tripForm.querySelector('button');
        if (submitBtn) {
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;
        }

        const formData = new FormData(tripForm);

        try {
            const response = await fetch('https://formspree.io/f/mrbjnnob', {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (response.ok) {
                formStatus.innerHTML = `<p style="color: green;">✅ Request sent successfully!</p>`;
                tripForm.reset();
            } else {
                throw new Error('Failed');
            }
        } catch (error) {
            formStatus.innerHTML = `<p style="color: red;">❌ Error sending request</p>`;
        } finally {
            if (formStatus) formStatus.style.display = 'block';
            if (submitBtn) {
                submitBtn.textContent = 'Send Request';
                submitBtn.disabled = false;
            }
        }
    });
}





// CTA Button Click Handler
const ctaButton = document.querySelector('.cta-button');
if (ctaButton) {
    ctaButton.addEventListener('click', () => {
        const destSection = document.querySelector('.destinations');
        if (destSection) {
            destSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
}

// Add parallax effect to hero
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});

// Destination Cards Hover Effect
document.querySelectorAll('.dest-card').forEach(card => {
    card.addEventListener('mouseenter', function () {
        this.style.transform = 'translateY(-10px) scale(1.02)';
    });

    card.addEventListener('mouseleave', function () {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// Add active state to navigation on scroll
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-menu a');

    let current = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= (sectionTop - 200)) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').includes(current)) {
            link.classList.add('active');
        }
    });
});

// Counter Animation for Statistics (if needed)
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);

    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start);
        }
    }, 16);
}

// Initialize tooltips or additional features
document.addEventListener('DOMContentLoaded', () => {

    // Add loading animation
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.2s ease';
        document.body.style.opacity = '1';
    }, 100);
});


// Home Button Scroll to Top

document.getElementById('homeBtn')?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});




// ========================================
// UNIVERSAL DYNAMIC MODAL SYSTEM
// Works for ALL destination cards on ANY page
// ========================================

document.addEventListener('DOMContentLoaded', function () {

    // Check if modal exists on this page
    const modal = document.getElementById('itinerary-modal');
    if (!modal) {
        console.log('ℹ️ No modal found on this page');
        return;
    }

    // Get all modal elements
    const modalTitle = document.getElementById('modal-title');
    const modalImage = document.getElementById('modal-image');
    const modalPrice = document.getElementById('modal-price');
    const modalTimeline = document.getElementById('modal-timeline');
    const formDestinationName = document.getElementById('form-destination-name');
    const destinationInput = document.getElementById('destination-input');
    const itineraryView = document.getElementById('itinerary-view');
    const planningView = document.getElementById('planning-form-view');
    const closeBtn = document.querySelector('.modal-close-btn');
    const customizeBtn = document.getElementById('customize-trip-btn');
    const backBtn = document.getElementById('back-to-itinerary-btn');
    const form = document.getElementById('trip-planning-form');
    const modalFormStatus = document.getElementById('form-status');

    // ========================================
    // AUTO-GENERATE ITINERARY FOR ANY DESTINATION
    // ========================================
    function generateItinerary(destinationName) {
        // Smart itinerary based on destination type
        const isIsland = ['Maldives', 'Bali', 'Hawaii', 'Seychelles', 'Fiji'].some(island =>
            destinationName.includes(island)
        );

        const isCity = ['Dubai', 'Singapore', 'New York', 'Tokyo', 'London'].some(city =>
            destinationName.includes(city)
        );

        if (isIsland) {
            return [
                { day: 'Day 1', title: `Arrival in ${destinationName}`, desc: 'Airport transfer, resort check-in, and welcome drinks.' },
                { day: 'Day 2-3', title: 'Beach & Water Activities', desc: 'Snorkeling, diving, kayaking, and sunset cruises.' },
                { day: 'Day 4-5', title: 'Spa & Relaxation', desc: 'Spa treatments, yoga sessions, and private beach dining.' },
                { day: 'Day 6', title: 'Island Exploration', desc: 'Visit local villages, markets, and hidden beaches.' },
                { day: 'Day 7', title: 'Departure', desc: `Farewell ${destinationName} with unforgettable memories.` }
            ];
        } else if (isCity) {
            return [
                { day: 'Day 1', title: `${destinationName} Arrival`, desc: 'City orientation tour and hotel check-in.' },
                { day: 'Day 2', title: 'Top Landmarks', desc: `Visit the most iconic attractions of ${destinationName}.` },
                { day: 'Day 3', title: 'Cultural Immersion', desc: 'Museums, art galleries, and local cuisine experiences.' },
                { day: 'Day 4', title: 'Shopping & Entertainment', desc: 'Explore shopping districts and nightlife.' },
                { day: 'Day 5', title: 'Departure', desc: 'Transfer to airport with city memories.' }
            ];
        } else {
            // Default multi-destination itinerary
            return [
                { day: 'Day 1', title: `Welcome to ${destinationName}`, desc: 'Airport pickup, hotel check-in, and welcome orientation.' },
                { day: 'Day 2-3', title: 'Major Attractions', desc: `Guided tours of ${destinationName}'s most famous landmarks and cultural sites.` },
                { day: 'Day 4-5', title: 'Cultural Experiences', desc: 'Authentic local experiences, traditional cuisine, and cultural activities.' },
                { day: 'Day 6', title: 'Free Day', desc: 'Leisure time to explore at your own pace or join optional activities.' },
                { day: 'Day 7', title: 'Departure', desc: `Farewell ${destinationName}. Safe travels home!` }
            ];
        }
    }

    // ========================================
    // OPEN MODAL FUNCTION
    // ========================================
    // OPEN MODAL FUNCTION
    // ========================================
    function openModal(destinationLabel, destinationTitle, destinationImage, destinationPrice) {
        // Set modal title
        if (modalTitle) {
            modalTitle.textContent = destinationTitle || destinationLabel;
        }

        // Set hero image
        if (modalImage && destinationImage) {
            modalImage.style.backgroundImage = `url('${destinationImage}')`;
        }

        // Show/Hide price section
        if (modalPrice && modalPrice.parentElement) {
            if (destinationPrice) {
                modalPrice.parentElement.style.display = 'block';
                modalPrice.textContent = '₹' + destinationPrice;
            } else {
                modalPrice.parentElement.style.display = 'none';
            }
        }

        // Generate and populate itinerary
        if (modalTimeline) {
            const itinerary = generateItinerary(destinationLabel);
            modalTimeline.innerHTML = itinerary.map(item => `
                <div class="timeline-item">
                    <h4>${item.day}: ${item.title}</h4>
                    <p>${item.desc}</p>
                </div>
            `).join('');
        }

        // Set form destination
        if (formDestinationName) {
            formDestinationName.textContent = destinationLabel;
        }
        if (destinationInput) {
            destinationInput.value = destinationLabel;
        }

        // Reset views (show itinerary, hide form)
        if (itineraryView) itineraryView.classList.remove('hidden');
        if (planningView) planningView.classList.add('hidden');

        // Clear any previous form status
        if (modalFormStatus) {
            modalFormStatus.style.display = 'none';
            modalFormStatus.className = '';
        }

        // Show modal
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    // ========================================
    // AUTO-DETECT ALL DESTINATION CARDS
    // ========================================
    const allCards = document.querySelectorAll('.dest-card');



    allCards.forEach((card, index) => {
        // Make cards clearly clickable
        card.style.cursor = 'pointer';

        card.addEventListener('click', function (e) {
            e.preventDefault();

            // Extract destination label (e.g., "France", "Maldives")
            // Priority: data-destination attribute > dest-label text > default
            const labelElement = card.querySelector('.dest-label');
            const dataDest = card.dataset.destination;
            const destinationLabel = dataDest ? dataDest : (labelElement ? labelElement.textContent.trim() : `Destination ${index + 1}`);

            // Extract destination title (e.g., "French Excellence")
            const titleElement = card.querySelector('.dest-info h3');
            const destinationTitle = titleElement ? titleElement.textContent.trim() : destinationLabel;

            // Extract background image URL
            const imageElement = card.querySelector('.dest-image');
            let destinationImage = '';

            if (imageElement) {
                const bgStyle = window.getComputedStyle(imageElement).backgroundImage;
                destinationImage = bgStyle
                    .replace(/^url\(['"]?/, '')
                    .replace(/['"]?\)$/, '')
                    .trim();
            }

            // Extract Price
            const destinationPrice = card.dataset.price;

            // Open modal with extracted data
            openModal(destinationLabel, destinationTitle, destinationImage, destinationPrice);


        });
    });

    // ========================================
    // CLOSE MODAL
    // ========================================
    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Close button
    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }

    // Click outside modal
    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    // ESC key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });

    // ========================================
    // SWITCH BETWEEN VIEWS
    // ========================================
    if (customizeBtn) {
        customizeBtn.addEventListener('click', function () {
            if (itineraryView) itineraryView.classList.add('hidden');
            if (planningView) planningView.classList.remove('hidden');
        });
    }

    if (backBtn) {
        backBtn.addEventListener('click', function () {
            if (planningView) planningView.classList.add('hidden');
            if (itineraryView) itineraryView.classList.remove('hidden');
        });
    }

    // ========================================
    // FORM SUBMISSION (Formspree)
    // ========================================
    if (form && modalFormStatus) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn ? submitBtn.textContent : 'Submit Request';

            if (submitBtn) {
                submitBtn.textContent = 'Sending...';
                submitBtn.disabled = true;
            }

            // Prepare form data
            const formData = new FormData(form);

            // Ensure destination is included
            if (destinationInput && destinationInput.value) {
                formData.set('destination', destinationInput.value);
            }

            try {
                // Send to Formspree
                const response = await fetch('https://formspree.io/f/mrbjnnob', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Accept': 'application/json'
                    }
                });

                if (response.ok) {
                    // Success
                    modalFormStatus.className = 'success';
                    modalFormStatus.innerHTML = '✅ Request sent successfully! We\'ll contact you within 24 hours.';
                    modalFormStatus.style.display = 'block';
                    form.reset();

                    // Auto-close modal after 3 seconds
                    setTimeout(closeModal, 3000);
                } else {
                    throw new Error('Submission failed');
                }
            } catch (error) {
                // Error handling
                console.error('Form Error:', error);
                modalFormStatus.className = 'error';
                modalFormStatus.innerHTML = '❌ Error sending request. Please call us at <a href="tel:+917023030002" style="color: inherit; text-decoration: underline;">+91 7023030002</a>';
                modalFormStatus.style.display = 'block';
            } finally {
                // Reset button
                if (submitBtn) {
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                }
            }
        });
    }


});


