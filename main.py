import numpy as np
from board import *
from go import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from MCT import *

if __name__ == "__main__":
    go = Go()
    go_board = go.board
    root = Tk()
    root.geometry("1100x800")
    my_canvas = Canvas(root, width=707, height= 707)
    mct = MCT(go_board, go)
    global current_node
    current_node = mct
    # print(mct)
    # mct.new_move(10)
    

    def play_from_text_box(state=go_board):
        hand = text_box.get()
        coord = go.hand_to_coord(hand)
        play_at(state, coord)

    def play_at(coord, state=go_board):
        clock = time.time()
        if go.is_legal(state, coord):
            go.play_at(state, coord)
            go.board.print_tkinter_board(my_canvas)
            print("play_at", time.time() - clock)
            #mct.set_played_move(coord)
            #go.legal_moves(new_state)
        else:
            print("illegal move")
        
    def canvas_coord_to_coord(x,y):
        return(int(np.trunc((x-42)/35)), int(np.trunc((y-42)/35)))

    def on_click(evt):
        coord = canvas_coord_to_coord(evt.x, evt.y)
        play_at(coord, go.board)

    def print_terr():
        print("white: ", go.board.territory("w"))
        print("black: ", go.board.territory("b"))
    
    def print_capt():
        print("w caps: ", go.board.captured_pieces['w'])
        print("b caps: ", go.board.captured_pieces['b'])
    
    def tree_search(start_node, search_depth):
        (new_current_node, new_move) = mct.tree_search(start_node, None, True, search_depth)
        mct.current_node = new_current_node
        play_at(new_move)
        print(new_current_node)
        mct.pretty_print()
    

    my_canvas.bind("<ButtonPress>", on_click)
    text_box = Entry(root)
    text_box.place(x=825, y=100)

    terr_button = ttk.Button(root, text= "calculer le territoire", command = lambda: print_terr())
    captures_button = ttk.Button(root, text= "captures", command = lambda: print_capt())
    pos_button = ttk.Button(root, text= "jouer", command = lambda: play_from_text_box())
    tree_search_button = ttk.Button(root, text= "tree search", command = lambda: tree_search(mct.current_node, 60))
    print_tree_button = ttk.Button(root, text= "print tree", command = lambda: mct.pretty_print())
    pass_button = ttk.Button(root, text = "passer", command = lambda: go.play_pass())
    pass_button.place(x=825, y=400)
    print_tree_button.place(x=825, y=350)
    tree_search_button.place(x=825, y=300)
    terr_button.place(x=825, y=200)
    pos_button.place(x=825, y=150)
    captures_button.place(x=825, y=250)

    mct.state.print_tkinter_board(my_canvas)

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    while True:
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()

