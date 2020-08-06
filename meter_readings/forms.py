from django import forms
from .models import MeterReadings
from django.contrib.auth.models import Group
from django.contrib.auth.forms import User, UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.core.validators import ValidationError


def old_hot(request):
    old_readings = MeterReadings.objects.filter(user=request.user).order_by[0]
    hot = old_readings.hot
    return hot


class ReadingsForm(forms.ModelForm):
    class Meta:
        model = MeterReadings
        fields = ('cold', 'hot')

    def clean_hot(self):
        new_hot = self.cleaned_data['hot']
        if self.instance.hot:
            hot = self.instance.hot
            if new_hot < hot:
                raise ValidationError('Введенное значение меньше предыдущего')
        return new_hot

    def clean_cold(self):
        new_cold = self.cleaned_data['cold']
        if self.instance.cold:
            cold = self.instance.cold
            if new_cold < cold:
                raise ValidationError('Введенное значение меньше предыдущего')
        return new_cold


class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            user.groups.add(Group.objects.get(name='users'))
        return user


class UserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=(""),
        help_text=(''),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')



class AdminCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            user.groups.add(Group.objects.get(name='managers'))
        return user
