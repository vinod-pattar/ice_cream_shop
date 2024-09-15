from django.db.models.signals import post_save
from django.dispatch import receiver
from website.models import Enquiry
from .views import confirm_enquiry_email, admin_confirm_email

@receiver(post_save, sender=Enquiry)
def EnquiryEmailSender(sender, instance, created, **kwargs):
    if created:
        confirm_enquiry_email(instance)
        admin_confirm_email(instance)
        # Send enquiry email to the admin 


