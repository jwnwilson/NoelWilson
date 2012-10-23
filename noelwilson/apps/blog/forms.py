from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django import forms
from noelwilson.apps.accounts.models import UserProfile
from noelwilson.apps.blog.models import Entry
from noelwilson.apps.blog.models import Category

class BlogForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField( widget = forms.Textarea )
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    tags = forms.CharField()
    
    def clean_title(self):
        cd = self.cleaned_data
        title = cd.get('title')
        
        if len(title) < 3:
            raise forms.ValidationError("Please title more than 2 chars")
            
        return title
        
    def clean_text(self):
        cd = self.cleaned_data
        text = cd.get('text')
        
        if len(text) < 10:
            raise forms.ValidationError("Please more text.")
            
        return text
        
class CommentForm(forms.Form):
    author = forms.CharField()
    text = forms.CharField( widget = forms.Textarea )
    
    def clean_author(self):
        cd = self.cleaned_data
        if cd.get('author') == None:
        	return 'Anonymous'
		return cd.get('author')
		
class CategoryForm(forms.Form):
    category_name = forms.CharField()
    
    """def clean_category(self):
        cd = self.cleaned_data
        print cd
        if cd.get('category_name') == None:
        	raise forms.ValidationError("Category cannot be empty")
		return cd.get('category_name')"""
		
class BlogManagerForm(forms.Form):
    # Get titles of users blog posts
    user = None
    entryTitles=None
    # check box
    entry_List = None
    
    def __init__(self, user, *args, **kwargs):
        super(BlogManagerForm, self).__init__(*args, **kwargs)
        self.user = user
        self.entryTitles = self.getEntryTitles()
        self.fields['entry_List'] = forms.MultipleChoiceField(required= False,widget= CheckboxSelectMultiple, choices= self.entryTitles)
        
    def clean_entryList(self, submitType):
        cd = self.cleaned_data
        if submitType == 'edit_selected':
            ret = cd.get('entry_List')
            if len(ret) > 1:
                raise forms.ValidationError("Please select only one blog to edit.")
            else:
                return ret
        else:
            return cd.get('entry_List')
        
    def getEntryTitles(self):
        entries = Entry.objects.getUser_entries(self.user)
        self.entryTitles = []
        for entry in entries:
            self.entryTitles.append((entry.title,entry.title))
        return self.entryTitles
        