# -*- coding: utf-8 -*-
"""Account models."""

from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
