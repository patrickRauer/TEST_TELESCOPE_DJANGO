from django import forms
from .models import Camera, Frame
from filter_wheel.models import Filter


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = '__all__'

    id = forms.IntegerField(widget=forms.HiddenInput())


class CoolerForm(forms.Form):
    cooler_on = forms.BooleanField(required=False)
    temperature = forms.FloatField(min_value=-40, max_value=40, initial=-20)


class ImageForm(forms.Form):
    name = forms.CharField()
    frame = forms.ModelChoiceField(Frame.objects)

    filter = forms.ModelChoiceField(Filter.objects)

    exposure_time = forms.FloatField(min_value=1, max_value=600, initial=1, help_text='Exposure time in seconds')
    repeats = forms.IntegerField(min_value=1, max_value=20, initial=1, help_text='Number of images taken in a row')

    dark = forms.BooleanField(required=False)


class AbortForm(forms.Form):
    keep_image = forms.BooleanField(
        required=False,
        help_text='Check to download the current state of the image, otherwise the image will be lost. '
    )
