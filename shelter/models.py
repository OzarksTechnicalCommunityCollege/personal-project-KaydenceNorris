from django.db import models

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

