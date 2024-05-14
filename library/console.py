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
        def __init__(self, name: str, description: str):
            self.name = name
            self.description = description

    class Command():
        def __init__(self, description: str, args: list[Console.Arg] = [], optional_args: list[Console.Arg] = []):
            self.description = description
            self.args = args
            self.optional_args = optional_args

    commands: dict[str, Command] = {
        "clear": Command("Clears the console's output log."),
        "hello": Command("Prints 'Hello, world!' to the console."),
        "hi": Command("Prints 'Hi, World!' to the console."),
        "say": Command("Prints the passed arg to the console.", args=[Arg("arg", "the passed arg")]),
        "quit": Command("Quits the game."),
    }

    def __init__(self, sm: ScreenManager):
        super().__init__()
        
        self.sm = sm

        self.active = False

        # Keys

        self.clear_keys()
        self.add_key(pygame.K_RETURN, self._command)
        self.add_key(pygame.K_UP, self._on_key_up_arrow)
        self.add_key(pygame.K_DOWN, self._on_key_down_arrow)
        self.add_key(pygame.K_TAB, self._on_key_tab)

        # Items

        self.textbox = ui.Textbox((0, 0), fontm, 100, charset="all", blacklist="`", start="", end="")
        self.add_item(self.textbox)

        # Draws

        self.rect_bg = draw.Rect("gray30", (1, 1))

        self.rect_textbox_bg = draw.Rect("gray18", (1, 1))

        self.text_messages = draw.Text(fontm, "")

        self.text_hint = draw.Text(fontm, "")
        self.text_hint.color = "darkgray"
        self.text_hint.align = "bottomleft"

        self.rect_hint_bg = draw.Rect("gray18", (1, 1))
        self.rect_hint_bg.align = "bottomleft"
        
        self.add_draw(self.rect_bg)
        self.add_draw(self.rect_textbox_bg)
        self.add_draw(self.text_messages)
        self.add_draw(self.rect_hint_bg)
        self.add_draw(self.text_hint)

        # Vars

        self.log_outputs: list[str] = ["Welcome to the console.", "Type 'help' to view a list of commands."]
        self.log_outputs_index: int = 0

        self.log_commands: list[str] = []
        self.log_commands_index: int = 0
        self.log_commands_buffer: str = ""

        self.hints: list[str] = []
        self.hints_index: int = 0
        self.hints_string: str = ""
        self.hints_width: int = 0
        self.hints_command: str = ""
    
    # Events

    def _on_key_up_arrow(self, event: Event):
        if self.hints == []:
            if len(self.log_commands) == 0:
                return
            
            if self.log_commands_index == len(self.log_commands):
                self.log_commands_buffer = self.textbox.value
            
            if self.log_commands_index > 0:
                self.log_commands_index -= 1
                self.textbox.set_value(self.log_commands[self.log_commands_index])
        else:
            self.hints_index -= 1
            if self.hints_index < 0:
                self.hints_index = len(self.hints) - 1
            
            self._update_hints_string_commands()
    
    def _on_key_down_arrow(self, event: Event):
        if self.hints == []:
            if len(self.log_commands) == 0:
                return
            
            self.log_commands_index += 1
            
            if self.log_commands_index >= len(self.log_commands):
                self.textbox.set_value(self.log_commands_buffer)
                self.log_commands_index = len(self.log_commands)
            else:
                self.textbox.set_value(self.log_commands[self.log_commands_index])
        else:
            self.hints_index += 1
            if self.hints_index >= len(self.hints):
                self.hints_index = 0
            
            self._update_hints_string_commands()

    def _on_key_tab(self, event: Event):
        if self.hints != []:
            self.textbox.set_value(self.hints[self.hints_index])
            self.hints = []
            self.hints_string = ""

    def _on_event(self, event: Event | None):
        super()._on_event(event)

        if event != None and event.type == pygame.KEYDOWN and event.unicode != "":
            if event.unicode in charset_all or event.key == pygame.K_BACKSPACE:
                self._update_hints()

    # Methods

    def _update_hints(self):
        self.hints_command = self.textbox.value.split(" ")[0]
        self.hints = []
        self.hints_width = 0

        for command, _ in Console.commands.items():
            if command == self.hints_command:
                self.hints = []
                self._update_hints_string_args()
                return
            elif command.startswith(self.textbox.value):
                self.hints_width = max(self.hints_width, len(command))
                self.hints.append(command)
        
        self.hints_index = len(self.hints) - 1
        self._update_hints_string_commands()

    def _update_hints_string_commands(self):
        self.hints_string = ""

        for i in range(len(self.hints)):
            self.hints_string += cmd_color("lightblue" if i == self.hints_index else "lightgray") + self.hints[i]

            if i != len(self.hints) - 1:
                self.hints_string += "\n"
    
    def _update_hints_string_args(self):
        self.hints_string = self.hints_command + " "

        for arg in Console.commands[self.hints_command].args:
            self.hints_string += arg.name
        
        self.hints_width = len(self.hints_string)

    def _log_commands_add(self, command: str):
        if len(self.log_commands) == 0 or command != self.log_commands[-1]:
            self.log_commands.append(command)
        self.log_commands_index = len(self.log_commands)
        self.log_commands_buffer = ""

    def _log_outputs_add(self, message: str):
        self.log_outputs.append(message)

    def _has_command(self, command: str) -> bool:
        return command in Console.commands and hasattr(self, "command_")

    def _command(self, event: Event):
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

        try:
            callback = getattr(self, "command_" + command)

            if callable(callback):
                output = callback(*args)

                if output != None:
                    self._log_outputs_add(output)
            else:
                raise AttributeError()
        except AttributeError:
            self._log_outputs_add(cmd_color("indianred1") + f"Unknown command: '{command}'")

    def update(self, dt: float, events: list[Event]):
        for interact in self.interacts:
            interact.update(dt, events)

        for event in events:
            self._on_event(event)

    def draw(self, surface: Surface):
        size = surface.get_size()
        height = size[1] // 2 // umy * umy
        self.rect_bg.size = (size[0], height)

        self.rect_textbox_bg.size = (size[0], umy)
        self.rect_textbox_bg.dest = (0, height - umy)

        self.text_messages.value = "\n".join(self.log_outputs)

        self.rect_hint_bg.dest = (0, height - umy)
        self.rect_hint_bg.size = (umx * self.hints_width, umy * len(self.hints_string.split("\n")))

        self.text_hint.dest = (0, height - umy)
        self.text_hint.value = self.hints_string

        self.textbox.dest = self.rect_textbox_bg.dest
        self.textbox._max_chars = int(size[0] / fontm.width)
        
        super().draw(surface)
    
    # Commands

    def command_clear(self, *args) -> str | None:
        self.log_outputs.clear()

    def command_hello(self, *args) -> str | None:
        return "Hello, world!"
    
    def command_hi(self, *args) -> str | None:
        return "Hi, world!"
    
    def command_quit(self, *args) -> str | None:
        self.sm.break_flag = True
