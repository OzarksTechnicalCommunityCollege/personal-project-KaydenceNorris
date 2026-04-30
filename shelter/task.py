from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_favorite_confirmation(animal_name, animal_species, user_email):
    """
    Queued task: sends a confirmation email when a user favorites an animal.
    Runs asynchronously via RabbitMQ — does not block the HTTP response.
    """
    subject = f"You favorited {animal_name}!"
    message = (
        f"Thanks for showing interest in {animal_name} the {animal_species}. "
        f"Our shelter staff will be in touch soon. "
        f"In the meantime, you can view all your favorites on our site."
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=None,          # uses DEFAULT_FROM_EMAIL in settings
        recipient_list=[user_email],
        fail_silently=False,
    )
    return f"Confirmation email sent to {user_email} for {animal_name}"