from .models import Banners
from random import sample


def get_random_banners(banners_count: int) -> dict:
    active_banners = Banners.objects.filter(isactive=True)
    active_banners_count = len(active_banners)
    result = list()
    if active_banners_count > 5:
        result_idx = sample(range(active_banners_count), banners_count)
        for idx in result_idx:
            result.append(active_banners[idx])
    else:
        result = active_banners
    return result
