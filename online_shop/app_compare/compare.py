from django.conf import settings
from app_goods.models import Goods


class Comparation(object):

    def __init__(self, request):
        self.session = request.session
        comparation = self.session.get(settings.COMPARE_SESSION_ID)
        if not comparation:
            comparation = self.session[settings.COMPARE_SESSION_ID] = list()
        self.comparation = comparation

    def add(self, goods_id):
        if goods_id not in self.comparation:
            self.comparation.append(goods_id)
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, goods_id):
        if goods_id in self.comparation:
            self.comparation.remove(goods_id)
        self.save()

    def clear(self):
        del self.session[settings.COMPARE_SESSION_ID]
        self.save()

    def __iter__(self):
        goods = Goods.objects.filter(id__in=self.comparation)
        for item in goods:
            yield item

    def __len__(self):
        return len(self.comparation)
