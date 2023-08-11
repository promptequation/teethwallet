from celery import shared_task


@shared_task(bind=True)
def print_task(self, *args, **kwargs):
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print(key, value)
