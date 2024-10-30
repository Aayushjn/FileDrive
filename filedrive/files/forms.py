from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField(allow_empty_file=False, required=True, widget=forms.ClearableFileInput(attrs={"hidden": "", "onchange": "form.submit()"}))
