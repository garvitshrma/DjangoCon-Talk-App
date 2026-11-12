from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300)
    maintainer = models.CharField(max_length=100)
    repo_url = models.URLField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
