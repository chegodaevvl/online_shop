from app_categories.models import Characteristics, CharacteristicTypes
from django.db.models import Count


def get_comparations_rows(comparation_set):
    props_list = ['header', 'goods_name', 'price']
    items_comparation_count = len(comparation_set)
    result = {'error': None}
    if items_comparation_count < 2:
        result['error'] = 'Not enough goods for comparation'
        return result
    if items_comparation_count > 4:
        result['error'] = 'Too much goods for comparation'
        return result
    items_props = Characteristics.objects.filter(goodsidx__in=comparation_set)
    common_props = set(CharacteristicTypes.objects.filter(id__in=items_props))
    for item in comparation_set:
        item_props_id = list(item.characteristictype.id for item in items_props.filter(goodsidx=item.id))
        item_props = set(CharacteristicTypes.objects.filter(id__in=item_props_id))
        common_props = common_props.intersection(item_props)
    if not common_props:
        result['error'] = 'There are no common characteristics'
        return result
    for item in common_props:
        props_list.insert(-1, item)
    result['rows'] = list()
    for prop in props_list:
        comparation_row = dict()
        if prop == 'header':
            comparation_row['name'] = prop
            comparation_row['title'] = None
            comparation_row['class'] = None
            comparation_row['values'] = list()
            for item in comparation_set:
                comparation_row['values'].append({'goods_name': item.goodsname,
                                                  'goods_image': item.image})
        elif prop == 'goods_name':
            comparation_row['name'] = prop
            comparation_row['title'] = None
            comparation_row['class'] = None
            comparation_row['values'] = list()
            for item in comparation_set:
                comparation_row['values'].append({'goods_name': item.goodsname,
                                                  'goods_id': item.id})
        elif prop == 'price':
            comparation_row['name'] = prop
            comparation_row['title'] = prop
            comparation_row['class'] = None
            comparation_row['values'] = list()
            for item in comparation_set:
                comparation_row['values'].append(item.price)
        else:
            comparation_row['name'] = prop.characteristictype
            comparation_row['title'] = prop.characteristictype
            if len(items_props.filter(characteristictype=prop.id).values('value').annotate(count=Count('value'))) > 1:
                comparation_row['class'] = None
            else:
                comparation_row['class'] = ' Compare-row_hide'
            comparation_row['values'] = list()
            for item in comparation_set:
                prop_item_value = items_props.filter(characteristictype=prop.id, goodsidx=item.id).first()
                if prop_item_value:
                    comparation_row['values'].append(prop_item_value.value)
                else:
                    comparation_row['values'].append(prop_item_value)
        result['rows'].append(comparation_row)
    return result
