import numpy as np
from go import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

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
        if go.play_at(coord):
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
        print("white: ", go.board.territory("w"))
        print("black: ", go.board.territory("b"))
    
    def print_capt():
        print("w caps: ", go.board.captured_pieces['w'])
        print("b caps: ", go.board.captured_pieces['b'])


    my_canvas.bind("<Motion>", on_mouse_move)
    my_canvas.bind("<ButtonPress>", on_click)
    text_box = Entry(root)
    text_box.place(x=825, y=100)

    terr_button = ttk.Button(root, text= "calculate territory", command = lambda: print_terr())
    captures_button = ttk.Button(root, text= "show captures", command = lambda: print_capt())
    pos_button = ttk.Button(root, text= "play", command = lambda: play())
    terr_button.place(x=825, y=200)
    pos_button.place(x=825, y=150)
    captures_button.place(x=825, y=250)

    go.board.print_tkinter_board(my_canvas)

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    while True:
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()

