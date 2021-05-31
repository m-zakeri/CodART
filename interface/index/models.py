from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from tinymce import models as tinymce_models


class Parameter(models.Model):
    class ParameterDataTypes(models.TextChoices):
        INTEGER = 'int', _("Integer")
        FLOAT = 'float', _("Float")
        STRING = 'str', _("String")
        BOOLEAN = 'bool', _("Boolean")
        LIST = 'list', _("List")

    name = models.CharField(max_length=128)
    description = tinymce_models.HTMLField(blank=True, null=True)
    data_type = models.CharField(max_length=128, choices=ParameterDataTypes.choices)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )


class Plugin(models.Model):
    name = models.CharField(max_length=128)
    map_string = models.CharField(max_length=256)
    description = tinymce_models.HTMLField(blank=True, null=True)
    input_example = tinymce_models.HTMLField(blank=True, null=True)
    output_example = tinymce_models.HTMLField(blank=True, null=True)
    parameters = models.ManyToManyField(Parameter)

    def has_example(self):
        if self.input_example is None or self.output_example is None:
            return False
        return True

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ('name', )


class Refactoring(Plugin):
    pre_conditions = tinymce_models.HTMLField(blank=True, null=True)
    post_conditions = tinymce_models.HTMLField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse_lazy('refactoring_detail', kwargs={'refactoring_id': self.id})
