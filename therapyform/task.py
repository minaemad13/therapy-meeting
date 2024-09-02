from celery import shared_task

@shared_task
def weekly_task():
    # Your task logic here
    print("This task runs every Saturday.")
