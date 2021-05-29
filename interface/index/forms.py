from django import forms


def get_field_by_type(data_type):
    if data_type == "str" or data_type == "list":
        return forms.CharField
    elif data_type == "int":
        return forms.IntegerField
    elif data_type == "float":
        return forms.FloatField
    elif data_type == "bool":
        return forms.BooleanField


class DynamicForm(forms.Form):

    project_file = forms.FileField(
        help_text="Upload your project's zip file.",
        widget=forms.FileInput(attrs={'accept': '.zip'})
    )

    def __init__(self, *args, **kwargs):
        dynamic_fields = kwargs.pop('dynamic_fields')
        super(DynamicForm, self).__init__(*args, **kwargs)
        for obj in dynamic_fields:
            self.fields[obj['name']] = get_field_by_type(obj['type'])(help_text=obj['hint'])
