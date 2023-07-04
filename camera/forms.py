from django import forms


class ImageForm(forms.Form):
    start_x = forms.IntegerField(min_value=0, max_value=4096, initial=0)
    start_y = forms.IntegerField(min_value=0, max_value=4096, initial=0)

    width = forms.IntegerField(min_value=256, max_value=4096, initial=4096)
    height = forms.IntegerField(min_value=256, max_value=4096, initial=4096)

    bin_x = forms.IntegerField(min_value=1, max_value=4, initial=1)
    bin_y = forms.IntegerField(min_value=1, max_value=4, initial=1)

    exposure_time = forms.FloatField(min_value=1, max_value=600, initial=1, help_text='Exposure time in seconds')

    dark = forms.BooleanField(required=False)


class AbortForm(forms.Form):
    keep_image = forms.BooleanField(
        required=False,
        help_text='Check to download the current state of the image, otherwise the image will be lost. '
    )
