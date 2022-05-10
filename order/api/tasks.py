from celery import shared_task


@shared_task
def send_order_email(email):
    email.send(fail_silently=False)
    return None
