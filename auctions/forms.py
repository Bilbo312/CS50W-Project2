from django import forms
from django.forms import Textarea

from .choices import CATEGORY_CHOICES

class NewListingForm(forms.Form):
    Listing_title = forms.CharField(label = "Title", max_length=64) 
    init_price = forms.FloatField(widget=forms.NumberInput(attrs={'margin-bottom': 200}), label = "Init_bid")
    picture = forms.URLField(required = False, label = "Picture")
    category = forms.ChoiceField(choices = CATEGORY_CHOICES)
    Listing_content = forms.CharField(widget= forms.Textarea(attrs={'rows':3,'cols': 40}), label=" Description")

class NewBidForm(forms.Form):
    new_bid = forms.FloatField(widget = forms.NumberInput, label = "New Bid", required= False)

class NewCommentForm(forms.Form):
    comment_content = forms.CharField(widget= forms.Textarea(attrs={'rows':3,'cols': 40}), label= "New Comment", required = False)