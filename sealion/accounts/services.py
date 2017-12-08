# -*- coding: utf-8 -*-
"""Account services."""
import datetime

from github import Github

from .models import Organization, Membership, Repository, Event

def get_user_organisations(user, token):
    """Get organisations of a user."""
    gh = Github(token)
    gh_user = gh.get_user()
    for org in gh_user.get_orgs():
        organization, created = Organization.objects.get_or_create(login=org.login)
        if created:
            organization.name = org.name
            organization.save()
        if not organization.users.filter(pk=user.pk).exists():
            Membership.objects.get_or_create(user=user, org=organization)

def get_organisation_repos(org_login, token):
    """Get Repositories of an organization."""
    gh = Github(token)
    org = gh.get_organization('primarysite')
    organization, created = Organization.objects.get_or_create(login=org.login)
    if created:
        organization.name = org.name
        organization.save()
    repos = org.get_repos()
    for repo in repos:
        repository, created = Repository.objects.get_or_create(github_id=repo.id)
        if created:
            repository.full_name = repo.full_name
            repository.name = repo.name
            repository.save()
            print(repo.name)
        yield repository

def get_user_events(repository, user, token):
    """Get all events for a user in a repository."""
    gh = Github(token)
    gh_user = gh.get_user()
    repo = gh.get_repo(repository.github_id)
    last_week = datetime.datetime.now() - datetime.timedelta(days=7)
    events = repo.get_events()
    for gh_event in events:
        if gh_event.created_at < last_week:
            break
        if gh_event.actor.login == gh_user.login:
            event, created = Event.objects.get_or_create(github_id=gh_event.id, user=user, repository=repository)
            if not created:
                break
            event.event_type = gh_event.type
            event.created_at = gh_event.created_at
            event.save()
            print (repo.name, event.event_type)




