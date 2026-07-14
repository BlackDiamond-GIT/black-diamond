from django.views.generic import RedirectView


class SchedulePageView(RedirectView):
    permanent = False
    pattern_name = 'pages:home'
