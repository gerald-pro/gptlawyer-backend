"""
Define los modelos de Django para la aplicación.

Este módulo define los siguientes modelos:

- `Usuario`: (Se supone que lo proporciona django.contrib.auth)
- `StudyCase`: Representa un caso de estudio en el sistema.

"""
from django.db import models
from django.contrib.auth.models import User


class StudyCase(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Owner")
    collaborators = models.ManyToManyField(User, related_name="collaborator")

    class Meta:
        verbose_name = "Study Case"
        verbose_name_plural = "Study Cases"

    def __str__(self):
        return self.title

    def get_number_of_collaborators(self):
        return self.collaborators.count()
