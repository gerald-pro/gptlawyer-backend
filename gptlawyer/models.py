"""
Define los modelos de Django para la aplicación.

Este módulo define los siguientes modelos:

- `Usuario`: (Se supone que lo proporciona django.contrib.auth)
- `StudyCase`: Representa un caso de estudio en el sistema.

"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

class User(AbstractUser):
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'user'

    def __str__(self):
        return self.username


class StudyCase(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Owner")

    class Meta:
        verbose_name = "Study Case"
        verbose_name_plural = "Study Cases"

    def __str__(self):
        return self.title


# Model for the professional_profiles table
class ProfessionalProfile(models.Model):
    profession = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    experience = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.profession} - {self.specialty}'
    

# Model for the roles table
""" class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name """

# Model for the collaborators table
class Collaborator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="study_cases_contributed")
    study_case = models.ForeignKey(StudyCase, on_delete=models.CASCADE)
    #role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'study_case')

    def __str__(self):
        return f'{self.user.name} - {self.study_case.title} - {self.role.name}'


class Document(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField(null=True)
    content_type =  models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to='gptlawyer/documents/')
    study_case = models.ForeignKey(StudyCase, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.file:
            default_storage.delete(self.file.name)
        super(Document, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name
    

# Model for the chats table
class Chat(models.Model):
    study_case = models.ForeignKey(StudyCase, on_delete=models.CASCADE)

    def __str__(self):
        return f'Chat for {self.study_case.title}'


# Model for the messages table
class Message(models.Model):
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return f'Message in {self.chat} at {self.created_at}'


# Model for the invitations table
class Invitation(models.Model):
    status = models.CharField(max_length=1)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')

    def __str__(self):
        return f'Invitation from {self.sender.name} to {self.receiver.name} - Status: {self.status}'