import numpy as np
from go import *
from tkinter import *
from tkinter import ttk

if __name__ == "__main__":
    go = Go()
    root = Tk()
    root.geometry("1100x800")
    # frm = ttk.Frame(root, padding=0)
    my_canvas = Canvas(root, width=707, height= 707)

    def play():
        hand = text_box.get()
        coord = go.hand_to_coord(hand)
        play_at(coord)

    def play_at(coord):
        if go.is_legal(coord):
            go.move(coord)
            go.capture(coord)
            go.next_turn(coord)
            go.board.print_tkinter_board(my_canvas)
        else:
            print("illegal move")
        
    def canvas_coord_to_coord(x,y):
        return(int(np.trunc((x-42)/35)), int(np.trunc((y-42)/35)))

    def on_mouse_move(evt):
        # TODO Diplay placeholder for next move
        pass

    def on_click(evt):
        coord = canvas_coord_to_coord(evt.x, evt.y)
        play_at(coord)

    def print_terr():
        print("white: ", go.territory("w"))
        print("black: ", go.territory("b"))


    my_canvas.bind("<Motion>", on_mouse_move)
    my_canvas.bind("<ButtonPress>", on_click)
    text_box = Entry(root)
    text_box.place(x=810, y=120)

    terr_button = ttk.Button(root, text= "calculate territory", command = lambda: print_terr())
    pos_button = ttk.Button(root, text= "play", command = lambda: play())
    terr_button.place(x=825, y=200)
    pos_button.place(x=850, y=165)

    go.board.print_tkinter_board(my_canvas)

    while True:
        root.mainloop()

