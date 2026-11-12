import toga
from toga.style.pack import COLUMN, ROW, Pack


class Schedule(toga.App):
    def startup(self):
        print("TOGA VERSION:", toga.__version__)

        # --- header: fixed height, sits at the top ---------------------
        self.header = toga.Label(
            "OpenLake Projects",
            style=Pack(margin=12, font_size=18, font_weight="bold"),
        )

        # --- body: the flexible middle, grows with the window ----------
        # accessors order is (title, subtitle, icon) -- icon LAST.
        self.projects = toga.DetailedList(
            accessors=("name", "tagline", "icon"),
            data=[
                {
                    "name": "Leaderboard-Pro",
                    "tagline": "Aggregates competitive programming rankings",
                    "icon": None,
                },
                {
                    "name": "Mess Portal",
                    "tagline": "Hostel mess menu and feedback",
                    "icon": None,
                },
                {
                    "name": "OpenLake Website",
                    "tagline": "The club site, on Vercel",
                    "icon": None,
                },
            ],
            style=Pack(flex=1),
        )

        # --- footer: a ROW nested inside the COLUMN --------------------
        self.count = toga.Label("3 projects", style=Pack(margin=12))

        # an empty flexible box that eats the leftover space,
        # pushing the button to the right edge
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

        # --- assemble: one root widget for the window ------------------
        main_box = toga.Box(
            children=[self.header, self.projects, footer],
            style=Pack(direction=COLUMN, flex=1),
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def on_refresh(self, widget, **kwargs):
        self.projects.data = [
            {
                "name": "Refreshed",
                "tagline": "The list was replaced",
                "icon": None,
            },
        ]
        self.count.text = "1 project"


def main():
    return Schedule()
