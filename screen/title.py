from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from library.gameManager import GameManager
    from library.gameState import GameState
    from library.screenManager import ScreenManager

from library.screen import Screen

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
        
        title_string = "\n".join(["/c[blue]" + string for string in title_string.split("\n")])
        self.title_text = fontm.text(title_string)

    def update(self):
        print("update")

    def draw(self, screen: pygame.Surface):
        screen.fill("darkslategray")

        self.title_text.draw(screen, (0, 0))

        pygame.display.flip()
