from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils import timezone

# Create your models here.
class AdoptableManager(models.Manager): # This checks to see if is adopted is true or not. If it is true, it can be filtered out later
    def get_queryset(self):
        return (
            super().get_queryset().filter(is_adopted = False)
        )

class Animal(models.Model): # this is my animal model. 
    img = models.ImageField(upload_to='img/', blank=True, null=True) # I wanted to add images becasuse thast what animal shelters have
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    species = models.CharField(max_length=30)
    breed = models.CharField(max_length=100)
    tags = TaggableManager() # tags to help filter out breeds at a later date. I'm not sure if changeing species/breed to tags would break everything, and I don't have the time tight now to test it out
    unique_for_breed = "name"
    is_adopted = models.BooleanField(default=False)
    desc = models.CharField(max_length=250)
    object = models.Manager()
    adoptable = AdoptableManager() # fiilters out if an animal is adoptable or not
    class Meta:
        ordering = ['age'] # animals are ordered by age
        indexes = [
            models.Index(fields=['age'])
        ]

    def __str__(self):
        return self.name
    
    def get_absoulute_url(self):
        return reverse('shelter:animal_view', args = [self.species,self.breed,self.name])
    
class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    joined_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    animals = models.ManyToManyField(Animal, through='VolunteerAnimalCare', related_name='volunteers')

    def __str__(self):
        return self.name
class VolunteerAnimalCare(models.Model):
    ROLE_CHOICES = [
        ('walker', 'Dog Walker'),
        ('feeder', 'Feeder'),
        ('trainer', 'Trainer'),
        ('medical', 'Medical Assistant'),
    ]
    # The two FK sides of the M2M
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    # Custom fields
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='walker')
    start_date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('volunteer', 'animal')  # prevent duplicate assignments

    def __str__(self):
        return f"{self.volunteer.name} cares for {self.animal.name} ({self.role})"
    
class Adoption(models.Model):
    animal = models.OneToOneField(Animal, on_delete=models.CASCADE)
    adopter_name = models.CharField(max_length=100)
    adoption_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.adopter_name} adopted {self.animal.name}"
    


