"""
Define las consultas GraphQL disponibles en la aplicación.

Este módulo proporciona una clase `Query` que hereda de `graphene.ObjectType`
y define las siguientes consultas:
"""

import graphene
from gptlawyer import types, models
from django.contrib.auth.models import User

class Query(graphene.ObjectType):
    current_user = graphene.Field(types.UserType, username=graphene.String())
    users = graphene.List(types.UserType)
    study_cases = graphene.List(types.StudyCaseType) 

    def resolve_current_user(self, info, username):
        """
        Obtiene el usuario actual por nombre de usuario.
        """
        return (
            User.objects.get(username__iexact=username)
        )
    
    def resolve_users(root, info):
        """
        Obtiene todos los usuarios.
        """
        return (
            User.objects.all()
        )
    
    def resolve_study_cases(root, info):
        """
        Obtiene todos los casos de estudio.
        """
        return (
            models.StudyCase.objects.all()
        )
