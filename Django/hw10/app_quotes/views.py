import json

from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import AuthorForm, QuoteForm
from .models import Quote, Tag, Author
from ..seeds.soup import parse_and_store_data
from ..seeds.get_data_from_json import get_authors, get_quotes, get_tags


# Create your views here.
def get_top10tags():
    tags = Tag.objects.all()
    topTenTags: list = sorted(tags, key=lambda tag: (tag.quotes.all().count(), tag.name), reverse=True)[:10]
    return topTenTags


def insert_into_db():
    parse_and_store_data()
    tags: list[str] = get_tags()
    authors: list[dict] = get_authors()
    quotes: list[dict] = get_quotes()

    for tag_name in tags:
        new_tag = Tag(name=tag_name)
        new_tag.save()

    for author in authors:
        new_author = Author(fullname=author['fullname'],
                            born_date=author['born_date'],
                            born_location=author['born_location'],
                            bio=author['bio'])
        new_author.save()


def main(request):
    if request.method == 'POST':
        insert_into_db()

    quotes = Quote.objects.all().order_by('-id')
    tags = Tag.objects.all()
    topTenTags = get_top10tags()

    tag_name = request.GET.get('tag_name')
    if tag_name:
        try:
            tag_id = Tag.objects.get(name=tag_name.capitalize()).id
            quotes = quotes.filter(tags__in=[tag_id])
        except Tag.DoesNotExist as e:
            quotes = []

    paginator = Paginator(quotes, 4)
    page = request.GET.get('page')
    quotes = paginator.get_page(page)

    return render(request, 'app_quotes/index.html', {'quotes': quotes, 'topTenTags': topTenTags})


def about_author(request, id):
    author = Author.objects.get(pk=id)

    return render(request, 'app_quotes/about_author.html', {'author': author})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app_quotes:index')

        return render(request, 'app_quotes/add_author.html', {'form': form})

    return render(request, 'app_quotes/add_author.html', {'form': AuthorForm()})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app_quotes:index')

        return render(request, 'app_quotes/add_quote.html', {'form': form})

    return render(request, 'app_quotes/add_quote.html', {'form': QuoteForm()})
