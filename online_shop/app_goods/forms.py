from django import forms


class ImportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices')
        super(ImportForm, self).__init__(*args, **kwargs)
        self.fields['files'].choices = self.choices
        self.fields['files'].initial = [choice[0] for choice in self.fields['files'].choices]
    email = forms.EmailField(required=False)
    files = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
