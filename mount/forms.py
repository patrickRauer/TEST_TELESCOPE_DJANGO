from django import forms


class SlewForm(forms.Form):
    ra = forms.CharField(max_length=25)
    dec = forms.CharField(max_length=25)


class ParkForm(forms.Form):
    pass
