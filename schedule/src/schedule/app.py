import httpx2
import toga
from toga.style.pack import COLUMN, ROW, Pack

API_URL = "http://127.0.0.1:8000/api/projects/"


class Schedule(toga.App):
    def startup(self):
        self.header = toga.Label(
            "OpenLake Projects",
            style=Pack(margin=12, font_size=18, font_weight="bold"),
        )

        # accessors order is (title, subtitle, icon) -- icon LAST.
        self.projects = toga.DetailedList(
            accessors=("name", "tagline", "icon"),
            data=[],
            style=Pack(flex=1),
        )

        self.count = toga.Label("Starting up...", style=Pack(margin=12))
        spacer = toga.Box(style=Pack(flex=1))
        self.refresh_button = toga.Button(
            "Refresh",
            on_press=self.on_refresh,
            style=Pack(margin=8),
        )
        footer = toga.Box(
            children=[self.count, spacer, self.refresh_button],
            style=Pack(direction=ROW),
        )

        main_box = toga.Box(
            children=[self.header, self.projects, footer],
            style=Pack(direction=COLUMN, flex=1),
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    async def on_running(self, **kwargs):
        """Runs once, after the app's event loop starts. Load the first batch."""
        await self.load_projects()

    async def on_refresh(self, widget, **kwargs):
        """Toga accepts a coroutine as a handler -- no threads to manage."""
        await self.load_projects()

    async def load_projects(self):
        self.count.text = "Loading..."
        self.refresh_button.enabled = False

        try:
            async with httpx2.AsyncClient(timeout=10) as client:
                response = await client.get(API_URL)
            response.raise_for_status()
        except httpx2.HTTPError as exc:
            self.count.text = "Could not reach the API"
            self.projects.data = [
                {
                    "name": "Connection failed",
                    "tagline": str(exc),
                    "icon": None,
                }
            ]
            return
        finally:
            self.refresh_button.enabled = True

        projects = response.json()["projects"]
        self.projects.data = [
            {
                "name": project["name"],
                "tagline": f"{project['tagline']} - {project['maintainer']}",
                "icon": None,
            }
            for project in projects
        ]
        self.count.text = f"{len(projects)} projects"


def main():
    return Schedule()
