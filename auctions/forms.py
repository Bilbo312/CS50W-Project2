from django import forms
from django.forms import Textarea

from .models import Category

class NewListingForm(forms.Form):
    Listing_title = forms.CharField(label = "Title", max_length=64) 
    Listing_content = forms.CharField(widget= forms.Textarea, label=" Content")
    init_price = forms.FloatField(widget=forms.NumberInput, label = "init_bid")
    picture = forms.URLField(required = False, label = "picture")
    category = forms.ChoiceField(widget=forms.Select, choices = Category.CATEGORY_CHOICES)

class NewBidForm(forms.Form):
    new_bid = forms.FloatField(widget = forms.NumberInput, label = "new_bid", required= False)