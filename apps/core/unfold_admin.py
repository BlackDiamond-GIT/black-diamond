"""Shared django-unfold ModelAdmin defaults for Black Diamond Spa."""

from unfold.admin import ModelAdmin as UnfoldModelAdmin


class BDModelAdmin(UnfoldModelAdmin):
    """Unfold admin without save-and-continue / save-and-add-another (broken with TinyMCE)."""

    show_save_and_continue = False
    show_save_and_add_another = False
