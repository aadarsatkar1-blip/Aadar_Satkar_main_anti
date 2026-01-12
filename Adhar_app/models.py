from django.db import models
from django.utils.text import slugify

# Create your models here.

class Destination(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('student', 'Student Tour'),
        ('wedding', 'Wedding'),
        ('medical', 'Medical Tourism'),
    ]
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='destinations/')
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='sub_destinations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Package(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='packages')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='packages/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50, help_text="e.g. 5 Days / 4 Nights")
    overview = models.TextField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.destination.name})"

class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)
    travel_date = models.DateField(null=True, blank=True)
    budget = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"Enquiry from {self.name}"

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
