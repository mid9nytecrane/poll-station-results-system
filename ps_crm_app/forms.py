from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 

from .models import pollStations, presResult,parlResult


class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ["username", "email", "password1", "password2"]

    
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'User Name',
        'class': 'form-control'
    }), label="", help_text='<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>')

    email = forms.CharField(max_length=255, widget=forms.EmailInput(attrs={
        'placeholder':'Email Address',
        'class':'form-control'
    }), label="", )

    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
        'placeholder':'Password',
        'class':'form-control',
    }),  label="", help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>')

    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
        'placeholder':'Repeat Password',
        'class':'form-control',     
    }), label="", help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>')



class pollStationForm(forms.ModelForm):
    ps_name = forms.CharField(required=True,max_length=50, widget=forms.TextInput(attrs={'placeholder':'Poll Station', 'class':'form-control'}), label="")

    ps_code = forms.CharField(required=True,max_length=50, widget=forms.TextInput(attrs={'placeholder':'Poll Station Code', 'class':'form-control'}), label="")

    serial_num = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Serial Number', 'class':'form-control'}), label="")
    
    reg_voters = forms.IntegerField(required=True, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Registered Voters', 'class': 'form-control'}), label="")
    
    class Meta:
        model = pollStations
        fields = ('ps_name', 'ps_code', 'serial_num', 'reg_voters')



class presResultForm(forms.ModelForm):

    CANDIDATES = {
        'John Dramani Mahama': 'John Dramani Mahama',
        'Mahamudu Bawumia': 'Mahamudu Bawumia',
        'Nana Kwame Badiako': 'Nana Kwame Badiako',
        'Alan John Kyerematen': 'Alan John Kyerematen',
    }

    PARTY = {
        'NDC':'NDC',
        'NPP':'NPP',
        'NEW FORCE': 'NEW FORCE',
        'MOVEMENT FOR CHANGE': 'MOVEMENT FOR CHANGE',
    }

    name = forms.ChoiceField(choices=CANDIDATES,widget=forms.Select(attrs={
        'class': 'form-control',
    }), label="Candidate")

    party = forms.ChoiceField(choices=PARTY,widget=forms.Select(attrs={
        'class': 'form-control',
    }), label="Party")

    votes = forms.IntegerField(required=True,min_value=0,widget=forms.NumberInput(attrs={
        'class':'form-control'
    }), label="Votes")

    class Meta:
        model = presResult
        fields = ('name', 'party', 'votes')



#parliamentary results form 
class parlResultForm(forms.ModelForm):

    PARTY = {
        'NDC':'NDC',
        'NPP':'NPP',
        'NEW FORCE': 'NEW FORCE',
        'MOVEMENT FOR CHANGE': 'MOVEMENT FOR CHANGE',
    }


    name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={
        'class': 'form-control',
    }), label="Candidate")

    party = forms.ChoiceField(choices=PARTY,widget=forms.Select(attrs={
        'class': 'form-control',
    }), label="Party")

    votes = forms.IntegerField(required=True,min_value=0,widget=forms.NumberInput(attrs={
        'class':'form-control'
    }), label="Votes")


    class Meta:
        model = parlResult
        fields =  ('name', 'party', 'votes')