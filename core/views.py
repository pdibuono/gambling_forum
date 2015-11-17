from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import *
from django.core.exceptions import PermissionDenied

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
        user_replies = Reply.objects.filter(pick=pick, user=self.request.user)
        context['user_replies'] = user_replies
        return context

class PickUpdateView(UpdateView):
    model = Pick
    template_name = 'pick/pick_form.html'
    fields = ['sport', 'description']

    def get_object(self, *args, **kwargs):
        object = super(PickUpdateView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object

class PickDeleteView(DeleteView):
    model = Pick
    template_name = 'pick/pick_confirm_delete.html'
    success_url = reverse_lazy('pick_list')

    def get_object(self, *args, **kwargs):
        object = super(PickDeleteView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object

class ReplyCreateView(CreateView):
    model = Reply
    template_name = "reply/reply_form.html"
    fields = ['text']

    def get_success_url(self):
       return self.object.pick.get_absolute_url()

    def form_valid(self, form):
        pick = Pick.objects.get(id=self.kwargs['pk'])
        if Reply.objects.filter(pick=pick, user=self.request.user).exists():
          raise PermissionDenied
        form.instance.user = self.request.user
        form.instance.pick = Pick.objects.get(id=self.kwargs['pk'])
        return super(ReplyCreateView, self).form_valid(form)

class ReplyUpdateView(UpdateView):
    model = Reply
    pk_url_kwarg = 'reply_pk'
    template_name = 'reply/reply_form.html'
    fields = ['text']

    def get_success_url(self):
        return self.object.pick.get_absolute_url()

    def get_object(self, *args, **kwargs):
        object = super(ReplyUpdateView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object

class ReplyDeleteView(DeleteView):
    model = Reply
    pk_url_kwarg = 'reply_pk'
    template_name = 'reply/reply_confirm_delete.html'

    def get_success_url(self):
        return self.object.pick.get_absolute_url()

    def get_object(self, *args, **kwargs):
        object = super(ReplyDeleteView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object