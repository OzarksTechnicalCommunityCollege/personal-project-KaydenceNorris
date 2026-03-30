from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Animal, Adoption

# Signal 1: Log when a new animal is added to the shelter
@receiver(post_save, sender=Animal)
def animal_created(sender, instance, created, **kwargs):
    if created:
        print(f"[SIGNAL] New animal added to shelter: {instance.name} ({instance.species})")

# Signal 2: Automatically mark animal as adopted when an Adoption record is saved
@receiver(post_save, sender=Adoption)
def mark_animal_adopted(sender, instance, created, **kwargs):
    if created:
        animal = instance.animal
        animal.is_adopted = True
        animal.save()
        print(f"[SIGNAL] {animal.name} has been marked as adopted by {instance.adopter_name}.")