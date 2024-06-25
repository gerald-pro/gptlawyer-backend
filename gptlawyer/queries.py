"""
Define las consultas GraphQL disponibles en la aplicación.

Este módulo proporciona una clase `Query` que hereda de `graphene.ObjectType`
y define las siguientes consultas:
"""

import graphene
from gptlawyer import types
from gptlawyer import models
from graphql_jwt.decorators import login_required
from django.db.models import Q


class Query(graphene.ObjectType):
    current_user = graphene.Field(types.UserType, username=graphene.String())
    all_users = graphene.List(types.UserType)

    all_study_cases = graphene.List(
        types.StudyCaseType, global_search=graphene.String()
    )

    study_case = graphene.Field(
        types.StudyCaseType, id=graphene.Int(required=True)
    )

    all_collaborators = graphene.List(types.CollaboratorType, global_search=graphene.String())
    collaborator = graphene.Field(
        types.CollaboratorType, id=graphene.Int(required=True)
    )

    all_documents = graphene.List(types.DocumentType, global_search=graphene.String())
    document = graphene.Field(types.DocumentType, id=graphene.Int(required=True))
    documents_by_study_case = graphene.List(
        types.DocumentType,
        study_case_id=graphene.Int(required=True)
    )

    all_messages = graphene.List(types.MessageType, study_id=graphene.Int(required=False))

    @login_required
    def resolve_current_user(self, info, username):
        return models.User.objects.get(username__iexact=username)

    @login_required
    def resolve_all_users(root, info):
        return models.User.objects.all()

    @login_required
    def resolve_all_study_cases(root, info, global_search=None):
        if global_search:
            return models.StudyCase.objects.filter(
                Q(title__icontains=global_search)
                | Q(description__icontains=global_search)
            )
        return models.StudyCase.objects.all()

    @login_required
    def resolve_study_case(root, info, id):
        return models.StudyCase.objects.get(pk=id)

    @login_required
    def resolve_all_collaborators(root, info):
        return models.Collaborator.objects.all()

    @login_required
    def resolve_collaborator(root, info, id):
        return models.Collaborator.objects.get(pk=id)

    @login_required
    def resolve_all_documents(root, info):
        return models.Document.objects.all()
    
    @login_required
    def resolve_documents_by_study_case(self, info, study_case_id, **kwargs):
        return models.Document.objects.filter(study_case_id=study_case_id)

    @login_required
    def resolve_document(root, info, id):
        return models.Document.objects.get(id=id)
    
    def resolve_all_messages(self, info, study_id=None, **kwargs):
        if study_id is not None:
            return models.Message.objects.filter(study_id=study_id)
        return models.Message.objects.all()
    


"""     def resolve_all_roles(root, info):
        return models.Role.objects.all()

    def resolve_role(root, info, role_id):
        return models.Role.objects.get(pk=role_id)
 """
