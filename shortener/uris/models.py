import string
import random

from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.conf import settings


SHORT_CODE_LEN = 12


class Link(models.Model):
    
    ALPHABET = string.ascii_lowercase+string.ascii_uppercase+string.digits

    target_url = models.URLField()
    short_code = models.CharField(max_length=SHORT_CODE_LEN, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=None, null=True)
    
    @staticmethod
    def generate_short_code():
        short_code = ""
        for i in range(SHORT_CODE_LEN):
            short_code += random.choice(Link.ALPHABET)
        return short_code
    
    @property
    def short_path(self):
        return reverse("short", kwargs={"short_code": self.short_code}) 

