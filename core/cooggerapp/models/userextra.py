# django 
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save
from django.db.utils import IntegrityError

# models
from .topic import UTopic

# 3.part 
from django_md_editor.models import EditorMdField
from django_follow_system.models import Follow

# choices
from core.cooggerapp.choices import FOLLOW, make_choices

# python
import requests

class OtherAddressesOfUsers(models.Model):
    "maybe ManyToManyField in UserProfile"
    choices = models.CharField(
        blank=True,
        null=True,
        max_length=15,
        choices=make_choices(FOLLOW),
        verbose_name="website",
    )
    address = models.CharField(
        blank=True, null=True, max_length=50, verbose_name="write address / username"
    )

    def __str__(self):
        return f"{self.choices} - {self.address}"

    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = EditorMdField(blank=True, null=True)
    address = models.ManyToManyField(
        OtherAddressesOfUsers,
        blank=True,
    )
    email_permission = models.BooleanField(default=True)


def save_github_follow(instance):
    github_following_url = instance.githubauthuser.get_extra_data_as_dict.get("url") + "/following"
    for f in requests.get(github_following_url).json():
        user = User.objects.filter(username=f.get("login"))
        if user.exists():
            instance.follow.following.add(user[0])

def save_github_repos(instance):
    github_repos_url = instance.githubauthuser.get_extra_data_as_dict.get("repos_url")
    for repo in requests.get(github_repos_url).json():
        if repo.get("fork") == False:
            UTopic(
                user=instance, 
                name=repo.get("name"), 
                definition=repo.get("description"), 
                address=repo.get("html_url"), 
            ).save()

@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile(user=instance).save()
    save_github_follow(instance)
    save_github_repos(instance)