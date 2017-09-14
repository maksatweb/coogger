from django.forms import ModelForm
from blogapp.models import *

# Create the form class.

class CommentForm(ModelForm):
     class Meta:
         model = Comment
         fields = ["comment"]

