import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from gptlawyer import models


class UserType(DjangoObjectType):
    class Meta:
        model = User


class StudyCaseType(DjangoObjectType):
    class Meta:
        model = models.StudyCase

    number_of_collaborators = graphene.String()

    def resolve_number_of_collaborators(self, info):
        """
        Obtiene el número de colaboradores para un caso de estudio.
        """
        return self.get_number_of_collaborators()