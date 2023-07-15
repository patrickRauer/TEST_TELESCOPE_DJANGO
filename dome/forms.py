from django import forms


class MoveDomeForm(forms.Form):
    azimuth = forms.FloatField(min_value=0, max_value=360, help_text='Azimuth in degree')


class AutoAlignmentForm(forms.Form):
    activate = forms.BooleanField(help_text='Automatic alignment of dome and mount', required=False)


class SwitchShutterForm(forms.Form):
    ...
