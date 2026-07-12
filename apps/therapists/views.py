from django.views.generic import RedirectView


class TherapistListView(RedirectView):
    permanent = False
    pattern_name = 'pages:home'


class TherapistDetailView(RedirectView):
    permanent = False
    pattern_name = 'pages:home'
