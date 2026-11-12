from django.http import JsonResponse

from .models import Project


def project_list(request):
    """Return every project as JSON.

    The keys here are chosen to match the Toga DetailedList accessors
    on the client, so the app needs no translation layer.
    """
    return JsonResponse(
        {
            "projects": [
                {
                    "name": project.name,
                    "tagline": project.tagline,
                    "maintainer": project.maintainer,
                    "repo_url": project.repo_url,
                }
                for project in Project.objects.all()
            ]
        }
    )
