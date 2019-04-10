from django import forms
from .models import Response
from .models import Response, Feedback
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class StockQuestionForm(forms.ModelForm):
    STOCK_TREND = [
    ('Bullish', 'Bullish'),
    ('Bearish', 'Bearish')
]
    bullish_bearish = forms.ChoiceField(label='Bullish or Bearish:',choices=STOCK_TREND)
    target_price = forms.DecimalField(label='Target Price:',min_value=0)

    class Meta:
        model = Response
        fields = ['bullish_bearish','target_price']


class FeedbackForm(forms.ModelForm):
    rate_choices=[('1','1'),
         ('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10')
         
         ]
    
    rate_function = forms.ChoiceField(label='1) Rate the overall functionlity of the app', choices=rate_choices, widget=forms.RadioSelect)
    most_function = forms.CharField(label='2) What functionalities are the most useful? ', widget=forms.TextInput)
    improve_function= forms.CharField(label='3) What functionalities would you improve/add for the future?', widget=forms.TextInput)

    rate_design = forms.ChoiceField(label='4) Rate the overall design of the app. Take into account ease of use and appeal', choices=rate_choices, widget=forms.RadioSelect)
    most_design = forms.CharField(label='5) What design aspects did you like? ', widget=forms.TextInput)
    improve_design= forms.CharField(label='6) What aspect of the design would you like to change/improve?', widget=forms.TextInput)

    class Meta:
        model = Feedback
        fields = ['rate_function','most_function','improve_function','rate_design','most_design','improve_design']
