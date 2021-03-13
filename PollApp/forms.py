from django import forms
from .models import *

class QuestionForm(forms.ModelForm):
    
    class Meta:
        
        model = Poll
        fields = ['Question']

class AddpollForm(forms.ModelForm):

    class Meta:

        model = PollOptions
        fields = ['option1','option2','option3']