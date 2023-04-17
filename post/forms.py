from django import forms
from .models import Post,Comment

class PostUpdate(forms.ModelForm):
    class Meta:
       model=Post
       fields = ('body',)
       labels={
            'body':'Update your post'
        }
       widget = {
           'body':forms.Textarea(attrs={"class":"form-control","row":'3'})
       }




class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
       
        widgets = {
            'body':forms.Textarea(attrs={'class':'form-control'})
        }


class CommentReplyForm(forms.ModelForm):
    class  Meta:
        model = Comment
        fields = ('body',)



class PostSearchForm(forms.Form):
    search = forms.CharField()