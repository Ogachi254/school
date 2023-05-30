# views.py
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'

class SchoolsView(TemplateView):
    template_name = 'schools.html'

class AdmissionsView(TemplateView):
    template_name = 'admissions.html'

class FacilitiesView(TemplateView):
    template_name = 'facilities.html'

class CoCurriculumView(TemplateView):
    template_name = 'co_curriculum.html'

class ContactView(View):
    template_name = 'contact.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # Process the form data here
        # You can access the submitted data using request.POST dictionary

        # Redirect after processing the form
        return redirect('home')

class CalendarView(TemplateView):
    template_name = 'calendar.html'

class DownloadsView(TemplateView):
    template_name = 'downloads.html'
