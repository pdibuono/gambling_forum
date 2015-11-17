from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from django.core.urlresolvers import reverse_lazy
from .models import *

# Create your views here.

class Home(TemplateView):
    template_name = "home.html"

class PickCreateView(CreateView):
    model = Pick
    template_name = "pick/pick_form.html"
    fields = ['sport', 'description']
    success_url = reverse_lazy('pick_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PickCreateView, self).form_valid(form)

class PickListView(ListView):
    model = Pick
    template_name = "pick/pick_list.html"
    
class PickDetailView(DetailView):
    model = Pick
    template_name = 'pick/pick_detail.html'
    
class PickUpdateView(UpdateView):
    model = Pick
    template_name = 'pick/pick_form.html'
    fields = ['sport', 'description']