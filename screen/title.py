import sys

from constant.fonts import *
from library.gameManager import GameManager
from library.gameState import GameState
import library.interact as interact
from library.screenManager import ScreenManager
from library.screen import Screen

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
        
        self.title_text = fonts.text(new_title_string, (umx, umy))

        # interacts

        self.buttons = interact.ButtonGroup((umx * 2, umy * 13), fontm, [
            ("N", "New Game", pygame.K_n, self.print),
            ("C", "Continue", pygame.K_c, self.print),
            ("O", "Options", pygame.K_o, self.print),
            ("H", "Help", pygame.K_h, self.print),
            ("Q", "Quit", pygame.K_q, self.quit)
        ])

        self.buttons.selected = True

    def update(self, events: List[pygame.event.Event]):
        self.buttons.update(events)

    def draw(self, screen: pygame.Surface):
        self.title_text.draw(screen)

        self.buttons.draw(screen)
    
    # Callbacks

    def print(self, event: pygame.event.Event):
        print("hello")
    
    def quit(self, event: pygame.event.Event):
        sys.exit(0)
