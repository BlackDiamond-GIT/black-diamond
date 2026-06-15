from django.db import models
from django.utils.translation import gettext_lazy as _


class FAQ(models.Model):
    question_cs = models.CharField(_('Question (CS)'), max_length=300)
    question_en = models.CharField(_('Question (EN)'), max_length=300, blank=True)
    question_ru = models.CharField(_('Question (RU)'), max_length=300, blank=True)
    answer_cs = models.TextField(_('Answer (CS)'))
    answer_en = models.TextField(_('Answer (EN)'), blank=True)
    answer_ru = models.TextField(_('Answer (RU)'), blank=True)
    order = models.IntegerField(_('Order'), default=0)
    is_active = models.BooleanField(_('Active'), default=True)
    include_in_schema = models.BooleanField(_('Include in FAQ Schema'), default=True)

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
        ordering = ['order']

    def __str__(self):
        return self.question_cs[:80]
