from online_shop.celery import app
from common.utils.import_utils import import_goods


@app.task
def import_task(files, email):
    import_goods(files=files, email=email)
