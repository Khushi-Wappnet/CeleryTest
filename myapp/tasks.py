from celery import shared_task

@shared_task
def send_notification():
    print("Notification sent!")
    return "Notification sent!"