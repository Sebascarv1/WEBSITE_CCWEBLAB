from django.shortcuts import render
from django.views import View


class BookingHomeView(View):
    template_name = "booking/home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)