from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .screenManager import ScreenManager

from .common import *
from .constant.fonts import *

from . import ui
from . import draw

class Console(ui.Form):
    class Arg():
        def __init__(self, name: str, value_type: str):
            self.name = name
            self.value_tye = value_type

    class Command():
        def __init__(self, description: str, args: list[Console.Arg] = [], optional_args: list[Console.Arg] = []):
            self.description = description
            self.args = args
            self.optional_args = optional_args

    commands: dict[str, Command] = {
        "clear": Command("Clears the console's output log."),
        "hello": Command("Prints 'Hello, world!' to the console."),
        "quit": Command("Quits the game."),
    }

    def __init__(self, sm: ScreenManager):
        super().__init__()
        
        self.sm = sm

        self.active = False

        # Keys

        self.clear_keys()
        self.add_key(pygame.K_RETURN, self.command)
        self.add_key(pygame.K_UP, self._log_commands_up)
        self.add_key(pygame.K_DOWN, self._log_commands_down)
        self.add_key(pygame.K_TAB, self._autofill)

        # Items

        self.textbox = ui.Textbox((0, 0), fontm, 100, charset="all", blacklist="`", start="", end="")
        self.add_item(self.textbox)

        # Draws

        self.rect_background = draw.Rect("gray30", (1, 1))
        self.textbox_background = draw.Rect("gray18", (1, 1))
        self.text_messages = draw.Text(fontm, "")
        self.text_hint = draw.Text(fontm, "")
        self.text_hint.color = "gray42"
        
        self.add_draw(self.rect_background)
        self.add_draw(self.textbox_background)
        self.add_draw(self.text_messages)
        self.add_draw(self.text_hint)

        # Vars

        self.log_outputs: list[str] = ["Welcome to the console.", "Type 'help' to view a list of commands."]
        self.log_outputs_index: int = 0

        self.log_commands: list[str] = []
        self.log_commands_index: int = 0
        self.log_commands_buffer: str = ""

        self.hint: str = ""
    
    def _log_commands_up(self, event: Event):
        if len(self.log_commands) == 0:
            return
        
        if self.log_commands_index == len(self.log_commands):
            self.log_commands_buffer = self.textbox.value
        
        if self.log_commands_index > 0:
            self.log_commands_index -= 1
            self.textbox.set_value(self.log_commands[self.log_commands_index])
    
    def _log_commands_down(self, event: Event):
        if len(self.log_commands) == 0:
            return
        
        self.log_commands_index += 1
        
        if self.log_commands_index >= len(self.log_commands):
            self.textbox.set_value(self.log_commands_buffer)
            self.log_commands_index = len(self.log_commands)
        else:
            self.textbox.set_value(self.log_commands[self.log_commands_index])

    def _log_commands_add(self, command: str):
        if len(self.log_commands) == 0 or command != self.log_commands[-1]:
            self.log_commands.append(command)
        self.log_commands_index = len(self.log_commands)
        self.log_commands_buffer = ""

    def _log_outputs_add(self, message: str):
        self.log_outputs.append(message)

    def _autofill(self, event: Event):
        if self.hint != "":
            self.textbox.value = self.hint


    def _on_event(self, event: Event | None):
        super()._on_event(event)

        if event != None and event.type == pygame.KEYDOWN:
            if self.textbox.value == "":
                self.hint = ""
            else:
                for command, _ in Console.commands.items():
                    if command.startswith(self.textbox.value):
                        self.hint = command
                        break

    def draw(self, surface: Surface):
        size = surface.get_size()
        height = size[1] // 2 // umy * umy
        self.rect_background.size = (size[0], height)

        self.textbox_background.size = (size[0], umy)
        self.textbox_background.dest = (0, height - umy)

        self.text_messages.value = "\n".join(self.log_outputs)

        self.text_hint.dest = (0, height - umy)
        self.text_hint.value = self.hint

        self.textbox.dest = self.textbox_background.dest
        self.textbox._max_chars = int(size[0] / fontm.width)
        
        super().draw(surface)
    
    def update(self, dt: float, events: list[Event]):
        for interact in self.interacts:
            interact.update(dt, events)

        for event in events:
            self._on_event(event)

    def command(self, event: Event):
        value = self.textbox.value.strip()

        if value == "":
            return
        elif " " not in value:
            command = value
            args = []
        else:
            command = value.split(" ", 1)[0]
            args = value.split(" ")[1:]
        
        self._log_commands_add(value)
        self.textbox.value = ""

        if command in Console.commands:
            callback = getattr(self, "command_" + command)

            if callable(callback):
                output = callback(*args)

                if output != None:
                    self._log_outputs_add(output)
                
                return
        
        self._log_outputs_add(cmd_color("indianred1") + f"Unknown command: '{command}'")
    
    # Commands

    def command_clear(self, *args) -> str | None:
        self.log_outputs.clear()

    def command_hello(self, *args) -> str | None:
        return "Hello, world!"
    
    def command_quit(self, *args) -> str | None:
        self.sm.break_flag = True
