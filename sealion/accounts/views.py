# -*- coding: utf-8 -*-
"""Account views."""

import datetime

from django.views.generic import TemplateView

from . import services

class ProfileView(TemplateView):
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        """Show git history"""
        token = request.user.social_auth.first().access_token
        services.get_user_organisations(request.user, token)
        for org in request.user.organization_set.filter(membership__enabled=True).all():
            for repo in services.get_organisation_repos(org.login, token):
                services.get_user_events(repo, request.user, token)
        return super().get(request, *args, **kwargs)
