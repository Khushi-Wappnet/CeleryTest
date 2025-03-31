# CeleryTest Project

This is a Django project integrated with Celery for handling asynchronous tasks. The primary purpose of this project is to demonstrate how to set up Celery and create a periodic task that runs every hour to send notifications.

## Project Structure

```
CeleryTest
├── CeleryTest
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── myapp
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tasks.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd CeleryTest
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Set up a message broker (e.g., Redis or RabbitMQ). For example, if using Redis, install it and run the server.

2. Update the `settings.py` file to include the Celery configuration:
   ```python
   CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Example for Redis
   CELERY_ACCEPT_CONTENT = ['json']
   CELERY_TASK_SERIALIZER = 'json'
   ```

## Creating a Periodic Task

1. In `myapp/tasks.py`, define a task that sends notifications:
   ```python
   from celery import shared_task

   @shared_task
   def send_notification():
       print("Notification sent!")
   ```

2. In `CeleryTest/celery.py`, configure Celery:
   ```python
   from celery import Celery
   import os

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CeleryTest.settings')

   app = Celery('CeleryTest')
   app.config_from_object('django.conf:settings', namespace='CELERY')
   app.autodiscover_tasks()
   ```

3. Set up periodic tasks in `CeleryTest/celery.py`:
   ```python
   from celery.schedules import crontab

   app.conf.beat_schedule = {
       'send-notification-every-hour': {
           'task': 'myapp.tasks.send_notification',
           'schedule': crontab(minute=0, hour='*'),  # Every hour
       },
   }
   ```

## Running the Project

1. Start the Django development server:
   ```
   python manage.py runserver
   ```

2. Start the Celery worker:
   ```
   celery -A CeleryTest worker --loglevel=info
   ```

3. Start the Celery beat scheduler:
   ```
   celery -A CeleryTest beat --loglevel=info
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.