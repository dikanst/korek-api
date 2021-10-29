import getopt
import sys
import json
import os
from time import sleep

from rich.live import Live
from rich.prompt import IntPrompt
from rich.console import Console
from rich.text import Text
from pathlib import Path

from layout import make_layout, make_header, update_groups, create_group_panels


def main(argv):
    console = Console()

    config_directory = ""
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["cdir="])
    except getopt.GetoptError:
        console.print("[cyan]Usage: [green] korek.py -i <config_directory>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            console.print("[cyan]Usage: [green] korek.py -i <config_directory>")
            sys.exit()
        elif opt in "-i":
            config_directory = arg

    welcome_text = Text("Welcome to Korek! Here are the JSON files I can read: ")
    welcome_text.stylize("cyan")
    console.print(welcome_text)

    directory_contents = sorted(list(Path(config_directory).iterdir()))

    max_index = 0
    for index, file in enumerate(directory_contents):
        filename, file_extension = os.path.splitext(file)
        if file_extension in (".json", ".JSON"):
            max_index += 1
            text = Text()
            text.append(str(max_index))
            text.append(") ")
            text.append(os.path.basename(file))
            if index % 2 == 0:
                text.stylize("bold magenta")
            console.print(text)

    if max_index < 1:
        console.print(
            ":pile_of_poo: [red] Unable to find JSON configuration files. Please provide a directory with config "
            "files.\n[cyan]Usage: [green] korek -i <config_directory>")
        sys.exit(2)

    while True:
        file_index = IntPrompt.ask("[green]Please select a file [cyan](1 - " + str(max_index) + ")")
        if 1 <= file_index <= max_index:
            break
        console.print(":pile_of_poo: [prompt.invalid]Number must be between 1 and " + str(max_index))

    config_file = directory_contents[file_index - 1]
    file_name = os.path.basename(config_file)
    with open(config_file, "r") as read_file:
        config = json.load(read_file)

    refresh_rate = 3600
    if config['refresh_rate']:
        refresh_rate = config['refresh_rate']

    layout = make_layout(config)
    create_group_panels(layout, config)

    with Live(layout, refresh_per_second=4, screen=True, auto_refresh=True, transient=True):

        layout["header"].update(make_header(file_name))

        while True:
            update_groups(layout, config)
            layout["header"].update(make_header(file_name))
            sleep(refresh_rate)


if __name__ == "__main__":
    main(sys.argv[1:])
