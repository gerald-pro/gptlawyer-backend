import graphene
from gptlawyer import types
from gptlawyer import models
from graphql_jwt.decorators import login_required

from gptlawyer.services.process import SPinecone
from gptlawyer.services.chat import Chat


class CreateStudyCase(graphene.Mutation):
    study_case = graphene.Field(types.StudyCaseType)

    class Arguments:
        input = types.StudyCaseInput()

    @staticmethod
    @login_required
    def mutate(root, info, input):
        user = info.context.user

        study_case_instance = models.StudyCase(
            title=input.title, description=input.description, owner=user,content=""" <p class="m-0" ><Strong>Procesando...</Strong></p> """
        )
        study_case_instance.save()
        
        #Creamos el indice en picone
        index_name = "caso-"+str(study_case_instance.id)
        SPinecone.create_index(index_name)
        return CreateStudyCase(study_case=study_case_instance)


class UpdateStudyCase(graphene.Mutation):
    class Arguments:
        input = types.UpdateStudyCaseInput(required=True)

    study_case = graphene.Field(types.StudyCaseType)

    @staticmethod
    @login_required
    def mutate(root, info, input):
        study_case_instance = models.StudyCase.objects.get(pk=input.id)
        if study_case_instance:
            if input.title:
                study_case_instance.title = input.title
            if input.description:
                study_case_instance.description = input.description

            study_case_instance.save()
            

            return UpdateStudyCase(study_case=study_case_instance)
        return UpdateStudyCase(study_case=None)


class DeleteStudyCase(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    @login_required
    def mutate(root, info, id):
        study_case_instance = models.StudyCase.objects.get(pk=id)
        if study_case_instance:
            index_name = "caso-"+str(study_case_instance.id)
            study_case_instance.delete()
            #Eliminamos el caso de estudion picone
            SPinecone.delete_index(index_name )
            return DeleteStudyCase(success=True)
        return DeleteStudyCase(success=False)
    
class ProcessStudyCase(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    #@login_required
    def mutate(root, info, id):
        study_case_instance = models.StudyCase.objects.get(pk=id)
        if study_case_instance:
            index_name = "caso-"+str(study_case_instance.id)
            #Procesa el query
            chat =Chat(index_name)

            identificacion = chat.query("Numero, fecha, lugar, expediente  de auto supremo?")
            nombres = chat.query(""""parte,acusado,imputado?" respondeme en una lista.""")
            tipo =  chat.query("""Tipo de delito o de que se trata el caso ?""")
            introduccion = chat.query("""podes hacer un resumen de todo el caso el resumen que se completo?""")
            persona = chat.query("""Listar todos los Nombre de personas con el rol que tiene de este caso ?""")

            content = """
                    <p><strong>1. Introduccion :</strong></p>
                                <p>
                                    """+introduccion+"""
                                    </p> 
                    <p><strong>2. Identificación del Caso:</strong></p>
                           <p>
                            """+identificacion+"""
                            </p> 
                    <p><strong>3. Partes involucradas:</strong></p>
                           <p>
                            """+nombres+"""
                            </p> 
                    <p><strong>4. Tipo de caso:</strong></p>
                           <p>
                            """+tipo+"""
                            </p> 
                    <p><strong>5. Personas:</strong></p>
                           <p>
                            """+persona +"""
                            </p> 
                    
            """
            #print(content)
            if study_case_instance:
                if content:
                    study_case_instance.content = content
            study_case_instance.save()
            return DeleteStudyCase(success=True)
        return DeleteStudyCase(success=False)

class StudyCaseMutations(graphene.ObjectType):
    create_study_case = CreateStudyCase.Field()
    update_study_case = UpdateStudyCase.Field()
    delete_study_case = DeleteStudyCase.Field()
    process_study_case = ProcessStudyCase.Field()
