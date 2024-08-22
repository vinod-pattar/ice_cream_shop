from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enquiry
# from django.core.mail import send_mail

# @receiver(post_save, sender=Enquiry)
# class EnquiryEmailSender(sender, instance, created, **kwargs):
#     if created:
#         # subject = 'New Enquiry'
#         # message = f'A new enquiry has been received from {instance.first_name} {instance.last_name}.\n\n{instance.message}'
#         print('New Enquiry Received')
