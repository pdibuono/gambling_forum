from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
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
    
    def get_context_data(self, **kwargs):
        context = super(PickDetailView, self).get_context_data(**kwargs)
        pick = Pick.objects.get(id=self.kwargs['pk'])
        replies = Reply.objects.filter(pick=pick)
        context['replies'] = replies
        return context

class PickUpdateView(UpdateView):
    model = Pick
    template_name = 'pick/pick_form.html'
    fields = ['sport', 'description']

class PickDeleteView(DeleteView):
    model = Pick
    template_name = 'pick/pick_confirm_delete.html'
    success_url = reverse_lazy('pick_list')

class ReplyCreateView(CreateView):
    model = Reply
    template_name = "reply/reply_form.html"
    fields = ['text']

    def get_success_url(self):
       return self.object.pick.get_absolute_url()

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.pick = Pick.objects.get(id=self.kwargs['pk'])
        return super(ReplyCreateView, self).form_valid(form)