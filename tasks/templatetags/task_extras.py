from django import template
from django.utils.safestring import mark_safe

register = template.Library()

_ICON_ATTRS = (
    'viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    'width="22" height="22"'
)

CATEGORY_ICONS = {
    "work": (
        f'<svg {_ICON_ATTRS}>'
        '<rect x="2" y="7" width="20" height="14" rx="2"></rect>'
        '<path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>'
        '</svg>'
    ),
    "school": (
        f'<svg {_ICON_ATTRS}>'
        '<path d="M22 10 12 5 2 10l10 5 10-5Z"></path>'
        '<path d="M6 12v5c0 1.5 2.5 3 6 3s6-1.5 6-3v-5"></path>'
        '</svg>'
    ),
    "personal": (
        f'<svg {_ICON_ATTRS}>'
        '<path d="M3 10.5 12 3l9 7.5"></path>'
        '<path d="M5 9.5V21h14V9.5"></path>'
        '<path d="M9 21v-6h6v6"></path>'
        '</svg>'
    ),
    "finance": (
        f'<svg {_ICON_ATTRS}>'
        '<line x1="12" y1="1" x2="12" y2="23"></line>'
        '<path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>'
        '</svg>'
    ),
    "projects": (
        f'<svg {_ICON_ATTRS}>'
        '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"></path>'
        '</svg>'
    ),
}

DEFAULT_ICON = (
    f'<svg {_ICON_ATTRS}>'
    '<rect x="4" y="4" width="6" height="6" rx="1"></rect>'
    '<rect x="14" y="4" width="6" height="6" rx="1"></rect>'
    '<rect x="4" y="14" width="6" height="6" rx="1"></rect>'
    '<rect x="14" y="14" width="6" height="6" rx="1"></rect>'
    '</svg>'
)


@register.filter
def category_icon(name):
    """Return an SVG line-icon matching a known category name, else a default grid icon."""
    if not name:
        return mark_safe(DEFAULT_ICON)
    return mark_safe(CATEGORY_ICONS.get(name.strip().lower(), DEFAULT_ICON))