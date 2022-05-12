import json
from app_goods.models import Goods


def get_browsing_history(cookies, amount):
    if 'browsing_history' not in cookies:
        return None
    else:
        cookies = json.loads(cookies['browsing_history'])[:amount]
        goods = []
        for goods_id in cookies:
            goods.append(Goods.objects.get(id=goods_id))
        return goods
