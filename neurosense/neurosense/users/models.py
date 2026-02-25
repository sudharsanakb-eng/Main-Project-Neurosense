from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models

class User(AbstractUser):
    """
    Default custom user model for neurosense.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    username=models.CharField(_("Enter user name") ,unique=True)
    password=models.CharField(_("Enter Password") ,unique=True)
    email=models.EmailField(_("Enter Email"), unique=True)
    rolechoices=[('User','User'),('councillor','councillor')]
    role=models.CharField(_("Enter role"),choices=rolechoices,null=False,blank=False,default='admin')



    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
