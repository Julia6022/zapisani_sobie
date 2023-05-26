from django import forms
from .models import UserProfile, Message, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_countries.fields import CountryField


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Login',
                               max_length=150,
                               required=True,
                               widget=forms.TextInput())

    password = forms.CharField(label='Hasło',
                               max_length=150,
                               required=True,
                               widget=forms.PasswordInput(attrs={'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150,
                               required=True,
                               label='Login',
                               widget=forms.TextInput())

    email = forms.EmailField(required=True,
                             max_length=255,
                             widget=forms.TextInput(),
                             label='E-mail')

    password1 = forms.CharField(max_length=50,
                                required=True,
                                label='Hasło',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    password2 = forms.CharField(max_length=50,
                                required=True,
                                label='Potwierdzenie hasła',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(),
                                 label='Imię')

    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(),
                                label='Nazwisko')

    sex = forms.ChoiceField(required=True,
                            label='Płeć',
                            choices=[
                                ('W', 'Kobieta'),
                                ('M', 'Mężczyzna'),
                                ('O', 'Inne')])

    date_of_birth = forms.DateField(required=True,
                                    label='Data urodzenia',
                                    widget=forms.SelectDateWidget(years=range(1923, 2023)))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'sex', 'date_of_birth']


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(max_length=500,
                          required=False,
                          widget=forms.TextInput,
                          label='Opis')

    country = CountryField(blank_label='Kraj zamieszkania')

    interests = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        label='Zainteresowania',
        required=False,
        choices=[
            ('movies_series', 'Filmy/seriale'),
            ('music', 'Muzyka'),
            ('singing', 'Śpiewanie'),
            ('dancing', 'Taniec'),
            ('books', 'Książki'),
            ('poetics', 'Poezja'),
            ('photography', 'Fotografia'),
            ('painting_drawing', 'Malowanie/rysowanie'),
            ('art', 'Sztuka'),
            ('theater', 'Teatr'),
            ('learning_languages', 'Nauka języków'),
            ('cooking_baking', 'Gotowanie/pieczenie'),
            ('traveling', 'Podróżowanie'),
            ('swimming', 'Pływanie'),
            ('cycling', 'Jazda na rowerze'),
            ('skiing_snowboarding', 'Narty/snowboard'),
            ('football', 'Piłka nożna'),
            ('basketball', 'Koszykówka'),
            ('volleyball', 'Siatkówka'),
            ('tennis', 'Tenis'),
            ('other_sport', 'Inny sport')])

    languages = forms.CharField(
        max_length=200,
        widget=forms.TextInput(),
        label='Znane języki: ',
        required=False)

    education = forms.CharField(
        max_length=200,
        widget=forms.TextInput(),
        label='Wykształcenie: ',
        required=False)

    job = forms.CharField(
        max_length=200,
        widget=forms.TextInput(),
        label='Praca: ',
        required=False)

    sex_preference = forms.ChoiceField(
        label='Interesują mnie: ',
        required=False,
        choices=[
            ('W', 'Kobiety'),
            ('M', 'Mężczyźni'),
            ('O', 'Inni'),
            ('A', 'Wszyscy')])

    min_age_preference = forms.IntegerField(label='Minimum age', required=False)
    max_age_preference = forms.IntegerField(label='Maximum age', required=False)

    profile_pic = forms.ImageField(widget=forms.FileInput())

    class Meta:
            model = UserProfile
            fields = ['bio', 'country', 'interests', 'languages', 'education', 'job', 'sex_preference', 'min_age_preference', 'max_age_preference', 'profile_pic']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']