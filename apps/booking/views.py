"""Booking views: WhatsApp redirect with click logging."""

from __future__ import annotations

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language

from apps.services.models import Service
from apps.therapists.models import Therapist

from .click_tracking import log_booking_click
from .utils import build_whatsapp_url


def _parse_duration(raw: str) -> int | None:
    value = (raw or '').strip()
    if not value.isdigit():
        return None
    return int(value)


def _booking_out_response(
    request: HttpRequest,
    *,
    placement: str,
    therapist_slug: str = '',
    service_slug: str = '',
    duration_raw: str = '',
) -> HttpResponseRedirect:
    lang = get_language() or 'cs'

    therapist_name = ''
    if therapist_slug:
        therapist = get_object_or_404(Therapist, slug=therapist_slug, is_active=True)
        therapist_name = therapist.name

    service_name = ''
    if service_slug:
        try:
            service = Service.objects.get(slug=service_slug, is_active=True)
            service_name = service.get_title(lang)
        except Service.DoesNotExist:
            service_name = service_slug

    log_booking_click(
        request,
        channel='whatsapp',
        placement=placement,
        therapist_slug=therapist_slug,
        service_slug=service_slug,
        duration_min=_parse_duration(duration_raw),
    )

    url = build_whatsapp_url(
        therapist_name=therapist_name,
        service_name=service_name,
        duration=duration_raw,
        lang=lang,
    )
    return HttpResponseRedirect(url)


def booking_out(request: HttpRequest) -> HttpResponseRedirect:
    return _booking_out_response(
        request,
        placement=request.GET.get('placement', 'unknown'),
        therapist_slug=(request.GET.get('therapist') or '').strip(),
        service_slug=(request.GET.get('service') or '').strip(),
        duration_raw=request.GET.get('duration', ''),
    )


def whatsapp_redirect(request: HttpRequest, slug: str | None = None) -> HttpResponseRedirect:
    return _booking_out_response(
        request,
        placement=request.GET.get('placement', 'unknown'),
        therapist_slug=(slug or '').strip(),
        service_slug=(request.GET.get('service') or '').strip(),
        duration_raw=request.GET.get('duration', ''),
    )


def whatsapp_general(request: HttpRequest) -> HttpResponseRedirect:
    return _booking_out_response(
        request,
        placement=request.GET.get('placement', 'unknown'),
        therapist_slug=(request.GET.get('therapist') or '').strip(),
        service_slug=(request.GET.get('service') or '').strip(),
        duration_raw=request.GET.get('duration', ''),
    )
