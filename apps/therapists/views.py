from django.views.generic import ListView, DetailView
from apps.core.mixins import ExtraCssMixin
from .models import Therapist


class TherapistListView(ExtraCssMixin, ListView):
    model = Therapist
    template_name = 'therapists/list.html'
    context_object_name = 'therapists'
    queryset = Therapist.objects.filter(is_active=True).prefetch_related('specialties')
    extra_css = [
        'css/components/cards.css',
        'css/components/glass.css',
        'css/components/buttons.css',
    ]


class TherapistDetailView(ExtraCssMixin, DetailView):
    model = Therapist
    template_name = 'therapists/detail.html'
    context_object_name = 'therapist'
    extra_css = [
        'css/pages/therapist-detail.css',
        'css/components/glass.css',
        'css/components/cards.css',
        'css/components/buttons.css',
    ]

    def get_queryset(self):
        return (
            Therapist.objects.filter(is_active=True)
            .prefetch_related(
                'specialties',
                'offers',
                'loves',
                'extras',
                'hashtags',
                'languages',
                'gallery_cloudinary',
            )
        )
