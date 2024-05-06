from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from library.gameManager import GameManager
    from library.gameState import GameState
    from library.screenManager import ScreenManager

from library.screen import Screen
from library.input.interactable import Interactable
from library.input.button import Button

from constant.fonts import *

class TitleScreen(Screen):
    name = "title"

    def __init__(self, gm: GameManager, gs: GameState, sm: ScreenManager, name: str):
        super().__init__(gm, gs, sm, name)
    
    def start(self):
        title_string = """\
  x*8888x.:d8888:.:d888b                                        x688889x                  
 X   98888X:`88888:`8888!                           8L           !8888!                  
X8x.  8888X   888X  8888!                          8888!   .dL   '8888   ..              
X8888 X8888   8888  8888'    .uu689u.   .uu6889u.  `Y888k:*888.   8888 d888L    .uu689u. 
'*888 !8888  !888* !888*   .888`"8888" d888`"8888    8888  888!   8888`"88*"  .888`"8888"
  `98  X888  X888  X888    8888  8888  8888  8888    8888  888!   8888 .d*.   8888  8888 
   '   X888  X888  8888    8888  8888  8888  8888    8888  888!   8888=8888   8888  8888 
   dx .8888  X888  8888.   8888  8888  8888  8888    8888  888!   8888 '888&  8888  8888 
 .88888888*  X888  X888X.  8888.:8888  888&.:8888   x888&.:888'   8888  8888. 8888.:8888 
  "88888*    *888  `8888"  "888*""888" "888*"8888.   "88"" 888  '"888*" 8888" "888*""888"
                                             "8888         88F                           
...................................... .d8! . `888 ...... 98" ............................
 ..................................... 4888o.o88" ..... ./" ...............................
  ..................................... *68889*` ..... -` ..... By Vincent G, aka Mutater .."""
        
        title_string_split = title_string.split("\n")
        new_title_string = ""

        for i in range(len(title_string_split)):
            new_title_string += f"/c[{to_hex((25, 50 + i * 5, 250 - i * 5))}]{title_string_split[i]}\n"
        
        self.title_text = fonts.text(new_title_string)

        # Interactables

        self.test = Interactable()
        self.test.set_keys([pygame.K_a, pygame.K_b])
        self.test.set_callbacks([
            ("main", self.print)
        ])
        self.interactables.append(self.test)

        self.test2 = Button((umx, umy * 15), fontm.text("Button")).with_inputs(pygame.K_b, self.print)
        self.interactables.append(self.test2)

    def update(self, events: List[pygame.event.Event]):
        self.update_interactables(events)

    def draw(self, screen: pygame.Surface):
        self.title_text.draw(screen, (umx, umy))

        self.draw_interactables(screen)
    
    # Callbacks

    def print(self, event: pygame.event.Event):
        print("hello")
