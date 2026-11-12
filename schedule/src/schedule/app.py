import ssl

import certifi
import httpx2
import toga
from toga.style.pack import COLUMN, ROW, Pack

API_URL = "https://djangocon-talk-app.onrender.com/api/projects/"

# httpx2 relies on `truststore`, which reads the OS trust store. Android keeps
# its CA certificates somewhere Python's OpenSSL does not look, so every HTTPS
# call fails with CERTIFICATE_VERIFY_FAILED. Bundling certifi and building the
# SSL context from it works on every platform.
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())


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
            async with httpx2.AsyncClient(timeout=60, verify=SSL_CONTEXT) as client:
                response = await client.get(API_URL)
            response.raise_for_status()
        except httpx2.HTTPError as exc:
            # Several httpx exceptions stringify to "", so always show the class.
            detail = f"{type(exc).__name__}: {exc}" if str(exc) else type(exc).__name__
            self.count.text = "Could not reach the API"
            self.projects.data = [
                {
                    "name": "Connection failed",
                    "tagline": detail,
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
