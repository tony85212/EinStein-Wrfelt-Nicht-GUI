from tkinter import *
from tkinter import messagebox
import random

root = Tk()
root.minsize(700,700)
root.maxsize(700,700)
root.title("Eubstein Chess")
background_image =  PhotoImage(file='image/board.png')

#GLOBAL VARIABLE OF ASSIGN CLICK
select = True
pre_click_position = 0
pre_piece = 0
piece_move = []
#MOVE_GEN
red_pos = [[1, 5, 6], [2, 6, 7], [3, 7, 8], [4, 8, 9], [9], [6, 10, 11], [7, 11, 12], [8, 12, 13],
           [9, 13, 14], [14], [11, 15, 16], [12, 16, 17], [13, 17, 18], [14, 18, 19], [19], [16, 20, 21], 
          [17, 21, 22], [18, 22, 23], [19, 23, 24], [24], [21], [22], [23], [24], []]
black_pos = [[], [0], [1], [2], [3], [0], [0, 1, 5], [1, 2, 6], [2, 3, 7], [3, 4, 8], [5], [5 , 6, 10]
               , [6, 7, 11], [7, 8, 12], [8, 9, 13], [10], [10, 11, 15], [11, 12, 16], [12, 13, 17], [13, 14, 18]
               , [15], [15, 16, 20], [16, 17, 21], [17, 18, 22], [18, 19, 23]]
#GLOBAL IMAGE
piece_image = []
dice_image = []
turn_image = []
img_piece = []

for i in range(13):
     piece_image.append(PhotoImage(file='image/' + str(i) + '.png'))
for i in range(7):
     dice_image.append(PhotoImage(file='image/dice' + str(i) + '.png'))
turn_image.append(PhotoImage(file='image/red.png'))
turn_image.append(PhotoImage(file='image/blue.png'))

class Board():
     boardinfo = [1, 2, 3, 0, 0,
                          4, 5, 0, 0, 0,
                          6, 0, 0, 0, 7,
                          0, 0, 0, 8, 9,
                          0, 0, 10, 11, 12]
     #pieceinfo = [25, 0, 1, 2, 5, 6, 10, 14, 18, 19, 22, 23, 24]
     dice = 0
     isdice = False
     turn = 0
     nearest_piece = []
     def initialize(self):
          r = random.sample(range(1, 7), 6)
          b = random.sample(range(7, 13), 6)
          self.boardinfo = [r[0], r[1], r[2], 0, 0,
                          r[3], r[4], 0, 0, 0,
                          r[5], 0, 0, 0, b[0],
                          0, 0, 0, b[1], b[2],
                          0, 0, b[3], b[4], b[5]]
          self.dice = 0
          self.isdice = False
          self.turn = 0
          self.nearest_piece = []
          
     def locate_min(self):
          tf_board = [0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0,
                          0, 0, 10, 0, 0]
          for i in range(25):
               if(self.turn == 0):
                    if(self.boardinfo[i] > 6 or self.boardinfo[i] == 0):
                         tf_board[i] = 25
                    else:
                         tf_board[i] = abs(self.dice - self.boardinfo[i])
               else:
                    if(self.boardinfo[i] > 6):
                         tf_board[i] = abs(self.dice - self.boardinfo[i])
                    else:
                         tf_board[i] = 25
          smallest = min(tf_board)
          return [index for index, element in enumerate(tf_board) if smallest == element]
     def dicing(self):
          real_dice = random.randint(1, 6)
          self.dice = real_dice + self.turn * 6
          isdice = True
          buttonDicing.config(state = "disabled")
          buttonDicing.config(image = dice_image[real_dice])
          self.nearest_piece = self.locate_min()
          #print(self.nearest_piece)
def asign_click(b, click_position):
     global select
     global pre_click_position
     global pre_piece
     global piece_move
     if(select and b.dice and click_position in b.nearest_piece):
          pre_click_position = click_position
          pre_piece = b.boardinfo[click_position]
          piece_move = move_gen(b, click_position)

          select = False
     elif(select == False and b.dice):
          if(click_position in piece_move):
               gui_board.itemconfig(img_piece[pre_click_position], image = piece_image[0])
               gui_board.itemconfig(img_piece[click_position], image = piece_image[pre_piece])
               b.boardinfo[click_position] = b.boardinfo[pre_click_position]
               b.boardinfo[pre_click_position] = 0
               b.turn = (b.turn + 1 )%2
               select = True
               isdice = False
               buttonDicing.config(state = "normal")
               buttonDicing.config(image = dice_image[0])
               labelTurn.config(image = turn_image[b.turn])
               #WIN CONDITION
               red_live = False
               black_live = False
               for i in range(25):
                    if(b.boardinfo[i] > 0 and b.boardinfo[i] < 7):
                         red_live = True
                    elif(b.boardinfo[i] > 6):                         
                         black_live = True                    
               if((b.boardinfo[24] > 0 and b.boardinfo[24] < 7) or not black_live):
                    messagebox.showinfo("Info", "red win!")
                    buttonDicing.config(state = "disabled")
               elif(b.boardinfo[0] > 6 or not red_live):
                    messagebox.showinfo("Info", "black win!")
                    buttonDicing.config(state = "disabled")
          else:
              select = True          
def move_gen(b, click_position):
     move = []
     if(b.turn == 0):
          for i in range(len(red_pos[click_position])):
               move.append(red_pos[click_position][i])
     else:
          for i in range(len(black_pos[click_position])):
               move.append(black_pos[click_position][i])
     return move
def gui_ini(b):
     b.initialize()
     gui_board.delete('all')
     img_piece[:] = []
     gui_board.image = background_image
     gui_board.create_image(250, 250, image = background_image)
     for i in range(25):
         symbol  = b.boardinfo[i]
         img_piece.append(gui_board.create_image(int(i%5)* 100 + 50, int(i/5) * 100 + 50, image = piece_image[symbol]))
         gui_board.tag_bind(img_piece[i], '<1>', lambda event ,x = i:asign_click(b, x))
     buttonDicing.config(state = "normal")
     buttonDicing.config(image = dice_image[0])
     labelTurn.config(image = turn_image[0])
     
b = Board()
#BUTTON
buttonRestart = Button(root, text = "restart", command = lambda: gui_ini(b))
buttonRestart.grid(row = 0 ,column = 0, padx = 520, pady = 0, sticky = N + W )
restart_image =  PhotoImage(file='image/restart.png')
buttonRestart.config(image = restart_image)
buttonDicing = Button(root, text = "dicing", command = b.dicing)
buttonDicing.grid(row = 0 ,column = 0, padx = 540, pady = 150, sticky = N + W )
buttonDicing.config(image = dice_image[0])
labelTurn = Label(root, text = "turn")
labelTurn.grid(row = 0 ,column = 0, padx = 530, pady = 300, sticky = N + W )
labelTurn.config(image = turn_image[0])
labelLabel = Label(root, text = "turn")
labelLabel.grid(row = 0 ,column = 0, padx = 175, pady = 550, sticky = N + W )
label_image = PhotoImage(file='image/label.png')
labelLabel.config(image = label_image)
#GUI
gui_board = Canvas(root, width = 500, height = 500, bg = 'black') 
gui_board.grid(row = 0 ,column = 0, sticky = N +W)
gui_ini(b)

root.mainloop()    
