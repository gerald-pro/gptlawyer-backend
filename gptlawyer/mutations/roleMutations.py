import graphene
from gptlawyer import types
from gptlawyer import models


class CreateRole(graphene.Mutation):
    class Arguments:
        input = types.RoleInput(required=True)

    role = graphene.Field(types.RoleType)

    @staticmethod
    def mutate(root, info, input):
        role_instance = models.Role(name=input.name)
        role_instance.save()
        return CreateRole(role=role_instance)


class UpdateRole(graphene.Mutation):
    class Arguments:
        input = types.UpdateRoleInput(required=True)

    role = graphene.Field(types.RoleType)

    @staticmethod
    def mutate(root, info, input):
        role_instance = models.Role.objects.get(pk=input.id)
        if role_instance:
            if input.name:
                role_instance.name = input.name
            role_instance.save()
            return UpdateRole(role=role_instance)
        return UpdateRole(role=None)


class DeleteRole(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    role = graphene.Field(types.RoleType)

    @staticmethod
    def mutate(root, info, id):
        role_instance = models.Role.objects.get(pk=id)
        if role_instance:
            role_instance.delete()
            return DeleteRole(role=role_instance)
        return DeleteRole(role=None)
    

class RoleMutations(graphene.ObjectType):
    create_role = CreateRole.Field()
    update_role = UpdateRole.Field()
    delete_role = DeleteRole.Field()