from django import  forms
from .models import Comment

class emailPostForm(forms.Form):
    name= forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields = ('name','email','body')
        widgets = {
            'name':forms.TextInput(attrs={'placeholder':'name'}),
            'email':forms.EmailInput(attrs={'placeholder':'email'}),
            'body':forms.Textarea(attrs={"placeholder":"join the conversation"})
            }

class SearchForm(forms.Form):
    query = forms.CharField()