from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UkrainianUserCreationForm 
from .models import Quote
from .models import Author
from .forms import AuthorForm
from .forms import QuoteForm
from django.shortcuts import render


def index(request):
    # Получаем все цитаты из базы данных
    quotes = Quote.objects.all()
    for quote in quotes:
        print(quote)
    # Передаем цитаты в шаблон для отображения
    return render(request, 'index.html', {'quotes': quotes})


def home(request):
    quotes = Quote.objects.all()
    print(quotes)
    return render(request, 'index.html', {'quotes': quotes})

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author_detail.html', {'author': author})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AuthorForm(user=request.user)
    return render(request, 'add_author.html', {'form': form})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = QuoteForm(user=request.user)
    return render(request, 'add_quote.html', {'form': form})



def register(request):
    if request.method == 'POST':
        form = UkrainianUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = UkrainianUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})