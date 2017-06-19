from django import template
from django.forms import CheckboxInput, RadioSelect, CheckboxSelectMultiple, \
    FileInput, DateInput


WIDGETS_NO_FORM_CONTROL = (
    CheckboxInput,
    RadioSelect,
    CheckboxSelectMultiple,
    FileInput,
)

register = template.Library()

@register.inclusion_tag('ms_utils/form/form.html')
def bsform(form):
    return dict(form=form)

@register.inclusion_tag('ms_utils/form/field.html')
def bsfield(field):
    return render_field(field)

@register.inclusion_tag('ms_utils/form/field.html')
def bsfieldname(name, form):
    field = form[name]
    return render_field(field)

@register.simple_tag
def bslayout(form):
    rows = getattr(form, 'bs_layout', None)
    if not rows:
        return False

    num = 0
    row_groups = []
    row_group = []
    for row in rows:
        row_group.append(row)
        num += row[1]
        if num == 12:
            row_groups.append(row_group)
            num = 0
            row_group = []
    return row_groups

def render_field(field):
    form = field.form
    widget = field.field.widget
    widget_class = type(widget)

    field.is_checkbox = isinstance(widget, CheckboxInput)
    field.is_radio = isinstance(widget, RadioSelect)

    field.is_date = isinstance(widget, DateInput)

    field.has_addon = field.is_date

    if field.errors:
        field.bs_class = 'has-error'
    else:
        field.bs_class = ''

    if not widget_class in WIDGETS_NO_FORM_CONTROL:
        widget.attrs['class'] = 'form-control'

    return dict(field=field)
