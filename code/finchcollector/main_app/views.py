from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Finch, Toy
from .forms import FeedingForm

class FinchCreate(CreateView, LoginRequiredMixin):
  model = Finch
  fields = ['name', 'breed', 'description', 'age']
  
  def form_valid(self, form):
      form.instance.user = self.request.user
      # Createview
      return super().form_valid(form)

class FinchUpdate(UpdateView):
  model = Finch
  fields = ['breed', 'description', 'age']

class FinchDelete(DeleteView):
  model = Finch
  success_url = '/finches/'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def finches_index(request):
  finches = Finch.objects.filter(user=request.user)
  
  return render(request, 'finches/index.html', { 'finches': finches })
@login_required
def finches_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)
  # instantiate FeedingForm to be rendered in the template
  toys_finch_doesnt_have = Toy.objects.exclude(id__in = finch.toys.all().values_list('id'))

  feeding_form = FeedingForm()
  return render(request, 'finches/detail.html', {
    'finch': finch, 'feeding_form': feeding_form, 'toys': toys_finch_doesnt_have
  })
@login_required
def assoc_toy(request, finch_id, toy_id):

  finch = Finch.objects.get(id=finch_id)
  finch.toys.add(toy_id)
  return redirect('detail', finch_id=finch_id)

@login_required
def add_feeding(request, finch_id):
	# create the ModelForm using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('detail', finch_id=finch_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # this is how to log in
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up try again'
    form = UserCreationForm()
    context = {
        'form': form,
        'error_message': error_message,
    }
    return render(request, 'registration/signup.html', context)

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'