from django import forms

class UploadImageForm(forms.Form):
    face_id = forms.CharField(label='Face ID', max_length=100)
    image = forms.ImageField(label='Select an Image')
