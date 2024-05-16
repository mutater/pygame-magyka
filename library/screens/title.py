from ..screen import *
from . import *

class TitleScreen(Screen):
    name = "title"
    
    def start(self):
        super().start()

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
  ..................................... *68889*` ..... -` ..... By Vincent G, aka mutater ..""".split("\n")
        
        new_title_string = ""

        for i in range(len(title_string)):
            new_title_string += f"/c[{to_hex((25, 50 + i * 5, 250 - i * 5))}]{title_string[i]}\n"
        
        self.form.add_draw(draw.Label(fontm, new_title_string, (umx, umy)))

        self.form.add_item(ui.ButtonGroup((umx * 2, umy * 17), fontm, [
            ("N", "New Game", pygame.K_n, self.new_game),
            ("O", "Options", pygame.K_o, self.options),
            ("H", "Help", pygame.K_h, self.print),
            ("Q", "Quit", pygame.K_q, self.quit)
        ]))
    
    # Callbacks

    def print(self, event: Event):
        print("hello")
    
    def new_game(self, event: Event):
        self.sm.clear()
        self.sm.push(NewGameScreen)
    
    def options(self, event: Event):
        self.sm.push(OptionsScreen)

    def quit(self, event: Event):
        self.sm.break_flag = True
