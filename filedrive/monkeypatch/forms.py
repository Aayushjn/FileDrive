import sys
from django import forms

BS4_FORM_CLASS = sys.intern("form-control")
BS4_FORM_SELECT_CLASS = sys.intern("form-select")
BS4_FORM_CHECK_CLASS = sys.intern("form-check")

BS4_VALID_CLASS = sys.intern("is-valid")
BS4_INVALID_CLASS = sys.intern("is-invalid")


class Form(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                css_class = BS4_FORM_SELECT_CLASS
            elif isinstance(field.widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                css_class = BS4_FORM_CHECK_CLASS
            else:
                css_class = BS4_FORM_CLASS

            css_classes = field.widget.attrs.get("class")
            if css_classes is None:
                css_classes = css_class
            elif BS4_FORM_CLASS not in css_classes:
                css_classes += f" {css_class}"
            field.widget.attrs["class"] = css_classes
            
            self.fields[field_name] = field

    def is_valid(self) -> bool:
        res = super().is_valid()

        if "__all__" in self.errors:
            for field_name in self.fields:
                self.fields[field_name].widget.attrs["class"] += f" {BS4_INVALID_CLASS}"
        else:
            for field_name in self.fields:
                if field_name in self.errors:
                    self.fields[field_name].widget.attrs["class"] += f" {BS4_INVALID_CLASS}"
                else:
                    self.fields[field_name].widget.attrs["class"] += f" {BS4_VALID_CLASS}"

        return res


class ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            css_classes = field.widget.attrs.get("class")
            if css_classes is None:
                css_classes = BS4_FORM_CLASS
            elif BS4_FORM_CLASS not in css_classes:
                css_classes += f" {BS4_FORM_CLASS}"
            field.widget.attrs["class"] = css_classes
            
            self.fields[field_name] = field
    
    def is_valid(self) -> bool:
        res = super().is_valid()

        if "__all__" in self.errors:
            for field_name in self.fields:
                self.fields[field_name].widget.attrs["class"] += f" {BS4_INVALID_CLASS}"
        else:
            for field_name in self.fields:
                if field_name in self.errors:
                    self.fields[field_name].widget.attrs["class"] += f" {BS4_INVALID_CLASS}"
                else:
                    self.fields[field_name].widget.attrs["class"] += f" {BS4_VALID_CLASS}"

        return res


forms.Form = Form
forms.ModelForm = ModelForm
