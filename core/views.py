from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from .forms import *
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
  paginate_by = 5

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

class VoteFormView(FormView):
  form_class = VoteForm

  def form_valid(self, form):
      user = self.request.user
      pick = Pick.objects.get(pk=form.data["pick"])
      try:
        reply = Reply.objects.get(pk=form.data["reply"])
        prev_votes = Vote.objects.filter(user=user, reply=reply)
        has_voted = (prev_votes.count()>0)
        if not has_voted:
          Vote.objects.create(user=user, reply=reply)
        else:
          prev_votes[0].delete()
        return redirect(reverse('pick_detail', args=[form.data["pick"]]))
      except:
        prev_votes = Vote.objects.filter(user=user, pick=pick)
        has_voted = (prev_votes.count()>0)
      if not has_voted:
        Vote.objects.create(user=user, pick=pick)
      else:
        prev_votes[0].delete()
      return redirect('pick_list')

class UserDetailView(DetailView):
  model = User
  slug_field = 'username'
  template_name = 'user/user_detail.html'
  context_object_name = 'user_in_view'

  def get_context_data(self, **kwargs):
      context = super(UserDetailView, self).get_context_data(**kwargs)
      user_in_view = User.objects.get(username=self.kwargs['slug'])
      picks = Pick.objects.filter(user=user_in_view)
      context['picks'] = picks
      replies = Reply.objects.filter(user=user_in_view)
      context['replies'] = replies
      return context

class UserUpdateView(UpdateView):
    model = User
    slug_field = "username"
    template_name = "user/user_form.html"
    fields = ['email', 'first_name', 'last_name']
    def get_success_url(self):
        return reverse('user_detail', args=[self.request.user.username])

    def get_object(self, *args, **kwargs):
        object = super(UserUpdateView, self).get_object(*args, **kwargs)
        if object != self.request.user:
            raise PermissionDenied()
        return object

class UserDeleteView(DeleteView):
    model = User
    slug_field = "username"
    template_name = 'user/user_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('logout')

    def get_object(self, *args, **kwargs):
        object = super(UserDeleteView, self).get_object(*args, **kwargs)
        if object != self.request.user:
            raise PermissionDenied()
        return object

    def delete(self, request, *args, **kwargs):
        user = super(UserDeleteView, self).get_object(*args)
        user.is_active = False
        user.save()
        return redirect(self.get_success_url())

class SearchPickListView(PickListView):
    def get_queryset(self):
        incoming_query_string = self.request.GET.get('query','')
        return Pick.objects.filter(sport__icontains=incoming_query_string)