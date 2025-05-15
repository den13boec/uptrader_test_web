from django import template
from menu.models import MenuItem
from django.urls import resolve

register = template.Library()

@register.inclusion_tag('menu_item.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url_name = resolve(request.path_info).url_name

    items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')
    item_map = {item.id: item for item in items}
    children_map = {}

    for item in items:
        children_map.setdefault(item.parent_id, []).append(item)

    def build_tree(parent_id=None):
        result = []
        for item in children_map.get(parent_id, []):
            node = {
                'item': item,
                'children': build_tree(item.id),
                'is_active': item.named_url == current_url_name or item.explicit_url == request.path,
            }
            result.append(node)
        return result

    return {'menu_tree': build_tree(), 'request': request}
