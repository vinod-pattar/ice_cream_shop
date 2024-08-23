from django.db.models.signals import post_save
from django.dispatch import receiver
from website.models import Enquiry
from django.core.mail import send_mail

@receiver(post_save, sender=Enquiry)
def EnquiryEmailSender(sender, instance, created, **kwargs):
    if created:
        subject = 'Thank you for you enquiry'
        message = f'Hi {instance.first_name} {instance.last_name},\n\n We have received your enquiry with regards to {instance.product.name}. We will soon reach out to you. Thank you!!!'
        from_email = 'vinod@example.com'
        recipient_list = [instance.email]
        
        send_mail(subject, message, from_email, recipient_list)


