from django import forms


class ObservationForm(forms.Form):
    name = forms.CharField(max_length=100)
    ra = forms.CharField(max_length=20)
    dec = forms.CharField(max_length=20)

    filter = forms.ChoiceField(choices=[(k, k) for k in ('U', 'B', 'V', 'R', 'I', 'C')])
    exposure_time = forms.IntegerField(min_value=1, max_value=600)
