from django import forms
from django.forms import Textarea

from .choices import CATEGORY_CHOICES

class NewListingForm(forms.Form):
    Listing_title = forms.CharField(label = "Title", max_length=64) 
    Listing_content = forms.CharField(widget= forms.Textarea, label=" Content")
    init_price = forms.FloatField(widget=forms.NumberInput, label = "init_bid")
    picture = forms.URLField(required = False, label = "picture")
    category = forms.ChoiceField(choices = CATEGORY_CHOICES)

class NewBidForm(forms.Form):
    new_bid = forms.FloatField(widget = forms.NumberInput, label = "new_bid", required= False)

class NewCommentForm(forms.Form):
    comment_content = forms.CharField(widget= forms.Textarea, label= "new_comment", required = False)