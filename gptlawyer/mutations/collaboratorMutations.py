import graphene
import graphql_jwt
from gptlawyer import types
from gptlawyer import models
from graphql_jwt.decorators import login_required

class CreateCollaborator(graphene.Mutation):
    class Arguments:
        input = types.CollaboratorInput(required=True)

    collaborator = graphene.Field(types.CollaboratorType)

    @staticmethod
    @login_required
    def mutate(root, info, input):
        user = info.context.user

        collaborator_instance = models.Collaborator(
            user_id=input.user_id,
            study_case_id=input.study_case_id,
            # role_id=input.role_id
        )
        collaborator_instance.save()
        return CreateCollaborator(collaborator=collaborator_instance)


class UpdateCollaborator(graphene.Mutation):
    class Arguments:
        input = types.UpdateCollaboratorInput(required=True)

    collaborator = graphene.Field(types.CollaboratorType)

    @staticmethod
    @login_required
    def mutate(root, info, input):
        user = info.context.user
        
        if user.is_anonymous:
            raise Exception("Primero debe iniciar sesión")

        collaborator_instance = models.Collaborator.objects.get(pk=input.id)
        if collaborator_instance:
            if input.user_id:
                collaborator_instance.user_id = input.user_id
            if input.study_case_id:
                collaborator_instance.study_case_id = input.study_case_id

            collaborator_instance.save()
            return UpdateCollaborator(collaborator=collaborator_instance)
        return UpdateCollaborator(collaborator=None)


class DeleteCollaborator(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    collaborator = graphene.Field(types.CollaboratorType)

    @staticmethod
    @login_required
    def mutate(root, info, id):
        collaborator_instance = models.Collaborator.objects.get(pk=id)
        if collaborator_instance:
            collaborator_instance.delete()
            return DeleteCollaborator(collaborator=collaborator_instance)
        return DeleteCollaborator(collaborator=None)


class CollaboratorMutations(graphene.ObjectType):
    create_collaborator = CreateCollaborator.Field()
    update_collaborator = UpdateCollaborator.Field()
    delete_collaborator = DeleteCollaborator.Field()
