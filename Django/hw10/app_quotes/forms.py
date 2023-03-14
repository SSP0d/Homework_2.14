from django import forms

from .models import Author, Quote, Tag

class AuthorForm(forms.ModelForm):
    fullname = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    born_date = forms.DateField(widget=forms.DateInput(attrs={"class": "form-control", "placeholder": "DD/MM/YYYY"}))
    born_location = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'bio']


class QuoteForm(forms.ModelForm):
    text = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    author = forms.ModelChoiceField(queryset=Author.objects.all().order_by('fullname'), widget=forms.Select(attrs={"class": "form-select"}))
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all().order_by('name'), widget=forms.SelectMultiple(attrs={"class": "form-select", "size": "7"}))

    class Meta:
        model = Quote
        fields = ['text', 'author', 'tags']
