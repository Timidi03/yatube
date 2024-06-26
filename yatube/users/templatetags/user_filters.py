from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})

@register.filter
def uglify(value):
    return ''.join(
        [value[i].lower() if i % 2 == 0 else value[i].upper() for i in range(len(value))]
    )