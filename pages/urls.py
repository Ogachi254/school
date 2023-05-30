# urls.py
from django.urls import path
from .views import HomePageView, AboutPageView, ContactView, SchoolsView, AdmissionsView, FacilitiesView, CoCurriculumView, CalendarView, DownloadsView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('schools/', SchoolsView.as_view(), name='schools'),
    path('admissions/', AdmissionsView.as_view(), name='admissions'),
    path('facilities/', FacilitiesView.as_view(), name='facilities'),
    path('co-curriculum/', CoCurriculumView.as_view(), name='co_curriculum'),
    path('calendar/', CalendarView.as_view(), name='calendar'),  # Add the calendar URL
    path('downloads/', DownloadsView.as_view(), name='downloads'),  # Add the downloads URL
]
