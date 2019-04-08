from django import template

register = template.Library()
#register.filter('get_model_by_pk'=get_model_by_pk)



@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_percent(dig1, dig2):
    #возвращает float процентов сколько от dig1 составляет dig2
    return round(dig2 / dig1 * 100, 1)
