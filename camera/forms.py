from django import forms
from .models import Camera
from filter_wheel.models import Filter


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = '__all__'

    id = forms.IntegerField(widget=forms.HiddenInput())


class ImageForm(forms.Form):
    start_x = forms.IntegerField(min_value=0, max_value=4096, initial=0)
    start_y = forms.IntegerField(min_value=0, max_value=4096, initial=0)

    width = forms.IntegerField(min_value=256, max_value=4096, initial=4096)
    height = forms.IntegerField(min_value=256, max_value=4096, initial=4096)

    bin_x = forms.IntegerField(min_value=1, max_value=4, initial=1)
    bin_y = forms.IntegerField(min_value=1, max_value=4, initial=1)

    filter = forms.ModelChoiceField(Filter.objects)

    exposure_time = forms.FloatField(min_value=1, max_value=600, initial=1, help_text='Exposure time in seconds')
    repeats = forms.IntegerField(min_value=1, max_value=20, initial=1, help_text='Number of images taken in a row')

    dark = forms.BooleanField(required=False)


class AbortForm(forms.Form):
    keep_image = forms.BooleanField(
        required=False,
        help_text='Check to download the current state of the image, otherwise the image will be lost. '
    )
