# -*- coding: utf-8 -*-
"""Account models."""
# Standard Library
import uuid

# Django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Custom user model to provide a uuid field."""

    uid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)


class Organization(models.Model):
    """Github organisations."""

    login = models.CharField(max_length=200, unique=True, null=False, blank=False)
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(User, through='Membership')

    def __str__(self):
        return self.login

class Membership(models.Model):
    """Membership of a user in an organization."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.org)

class Repository(models.Model):
    """Github repository."""

    github_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name

class Event(models.Model):
    """Github Events."""

    class Meta:
        ordering = ['-created_at']

    event_type = models.CharField(max_length=32)
    github_id = models.CharField(max_length=32)
    created_at = models.DateTimeField(null=True, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
