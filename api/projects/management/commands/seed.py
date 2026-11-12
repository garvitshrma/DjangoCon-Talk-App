from django.core.management.base import BaseCommand

from projects.models import Project

SEED = [
    {
        "name": "Leaderboard-Pro",
        "tagline": "Aggregates competitive programming rankings",
        "maintainer": "Lakshya Soni",
        "repo_url": "https://github.com/OpenLake/Leaderboard-Pro",
    },
    {
        "name": "Mess Portal",
        "tagline": "Hostel mess menu, feedback and billing",
        "maintainer": "OpenLake",
        "repo_url": "",
    },
    {
        "name": "OpenLake Website",
        "tagline": "The club site, deployed on Vercel",
        "maintainer": "OpenLake",
        "repo_url": "",
    },
    {
        "name": "Bitefy",
        "tagline": "QR-code restaurant management, built with Django REST",
        "maintainer": "Garvit Sharma",
        "repo_url": "",
    },
]


class Command(BaseCommand):
    help = "Load demo project rows."

    def handle(self, *args, **options):
        created = 0
        for row in SEED:
            _, made = Project.objects.get_or_create(name=row["name"], defaults=row)
            created += int(made)
        self.stdout.write(self.style.SUCCESS(f"{created} projects created."))
