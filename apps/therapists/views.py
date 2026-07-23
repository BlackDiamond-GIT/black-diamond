from django.views.generic import RedirectView
from django.urls import reverse


class TherapistListView(RedirectView):
    permanent = False
    pattern_name = 'pages:home'


class TherapistDetailView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """Ignore the matched therapist slug when reversing the homepage."""
        return reverse('pages:home')
