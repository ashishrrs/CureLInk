from .models import *
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import send_mail
from CureLink import settings
from django.utils.html import strip_tags


@shared_task(bind=True)
def send_mail_func(self, args1, args2):
    article_objects = Article.objects.filter(
        hours=args1, minutes=args2, published=0).all()
    print(article_objects)
    for obj in article_objects:
        mail_subject = "NewLetter"
        html_message = render_to_string('temp.html', {'val1': obj.name,
                                                      'val2': obj.description})
        message = strip_tags(html_message)

        subscriber_objects = Subscriber.objects.filter(topic=obj.topic).all()
        print(subscriber_objects)
        for subs in subscriber_objects:
            to_email = subs.email_id
            send_mail(
                subject=mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=True,
            )
        obj.published = 1
        obj.save()
    return "Done"
