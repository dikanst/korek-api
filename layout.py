from datetime import datetime

from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

import requests


def make_header(config_file_name) -> Panel:
    grid = Table.grid(expand=True)
    grid.add_column(justify="left")
    grid.add_column(justify="center")
    grid.add_column(justify="right")

    grid.add_row(
        "Using Configuration: " + config_file_name,
        ":fire: [red][b]Korek[/b] API Monitor :fire:",
        "Last Updated: " + datetime.now().ctime()
    )
    return Panel(grid, border_style="cyan")


def make_layout(config) -> Layout:
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
    )

    layout_list = list()

    for index, _ in enumerate(config["endpoint_groups"]):
        layout_list.append(Layout(name="group" + str(index)))

    layout["main"].split(
        *layout_list,
    )

    return layout


def create_group_panels(layout, config):
    for index, group in enumerate(config["endpoint_groups"]):
        grid = Table.grid(expand=True)
        grid.add_column(justify="left")
        grid.add_column(justify="right")
        layout["group" + str(index)].update(Panel(grid, border_style="color(" + str(index+2) + ")", title=group["group_name"]))


def refresh_panel(layout, group, group_index) -> Panel:
    grid = Table.grid(expand=True)
    grid.add_column(justify="left")
    grid.add_column(justify="right")

    for endpoint in sorted(group["endpoints"], key=lambda x: x["name"]):

        url = endpoint["healthcheck"]

        resp = requests.get(url)
        if resp.ok:
            status_emoji = ":green_circle:"
        else:
            status_emoji = ":red_circle:"

        if endpoint["redirect"]:
            url = endpoint["redirect"]

        grid.add_row(
            "[u blue link=" + url + "]" + endpoint["name"],
            status_emoji
        )

        layout[group_index].update(Panel(grid, border_style="color(" + str(int(group_index[5:]) + 2) + ")", title=group["group_name"]))


def update_groups(layout, config):
    for index, group in enumerate(config["endpoint_groups"]):
        refresh_panel(layout, group, "group" + str(index))

