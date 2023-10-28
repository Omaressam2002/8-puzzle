import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, Label
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkSlider, CTkComboBox, CTkCanvas, CTkRadioButton
import customtkinter as ctk
import numpy as np
from PIL import ImageTk, Image
import time
import BFS, DFS, Astar, Tree, utils, State

class EightPuzzleGame:
    def __init__(self):
        self.initial_state = np.array(['1', '2', '5', '3', '4', '0', '6', '7', '8'])
        self.goal_state = np.array(['0', '1', '2', '3', '4', '5', '6', '7', '8'])
        self.speed = 0
        self.technique = "BFS"

        self.root = CTk()
        self.root.title("8-Puzzle Game")
        self.root.geometry('700x400')
        self.root.resizable(False, False)
        background = ImageTk.PhotoImage(Image.open("assets/purple space.jpg"))
        background_label = CTkLabel(self.root, image= background, text="")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("dark-blue")

        #### START PAGE FRAME ####
        
        self.start_frame = CTkFrame(self.root)
        self.start_frame.pack()
        # background_label = CTkLabel(self.start_frame, fg_color = "transparent")
        # background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.title_label = CTkLabel(self.start_frame, text=" 8-Puzzle Game", font=("joystix monospace", 40))
        self.title_label.pack(pady=20, padx=60)
        
        self.radio_frame = CTkFrame(self.start_frame, width=90)
        self.radio_frame.pack()
        
        self.theme_label = CTkLabel(self.radio_frame, text="Theme:", font=("joystix monospace", 20) )
        self.theme_label.pack(padx=10, pady=8)
        
        self.theme_var = tk.StringVar(value="Light")
        self.light_theme = CTkRadioButton(self.radio_frame, value="Light", text="Light", font=("joystix monospace", 16), fg_color=("#3A7EBF","#504CD1"), variable=self.theme_var, command=self.game_theme)
        self.light_theme.pack(anchor='e' ,padx=80, pady=2)
        self.dark_theme = CTkRadioButton(self.radio_frame, value="Dark", text="Dark", font=("joystix monospace", 16), fg_color=("#3A7EBF","#504CD1"), variable=self.theme_var, command=self.game_theme)
        self.dark_theme.pack(anchor='e',padx=80, pady=10)


        self.start_button = CTkButton(self.start_frame, text="Start Game", font=("joystix monospace", 20), command=self.start_game, width=70, height=40, fg_color=("#3A7EBF","#504CD1"))
        self.start_button.pack(pady=20)
        
        #### PUZZLE FRAME ####

        self.puzzle_frame = CTkFrame(self.root, width=90)
        self.puzzle_frame.pack()
        
        self.back_button = CTkButton(self.puzzle_frame, text="Back", command=self.return_to_start_page, width=50, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.back_button.pack(pady=10, padx=20, anchor='nw')
        
        self.speed_label = CTkLabel(self.puzzle_frame, text="Speed", font=("joystix monospace", 12))
        self.speed_label.pack()

        self.speed_slider = CTkSlider(self.puzzle_frame, from_=1, to=10, number_of_steps=10, orientation='horizontal', button_color=("#1B558D","#504CD1"))
        self.speed_slider.pack()

        self.technique_label = CTkLabel(self.puzzle_frame, text="Technique", font=("joystix monospace", 12))
        self.technique_label.pack()
        
        self.technique_combobox = CTkComboBox(self.puzzle_frame, values=["BFS", "DFS", "A* - Manhattan", "A* - Euclidean"], width = 200, font=("joystix monospace", 12), dropdown_font=("joystix monospace", 12),
                                              button_color=("#3A7EBF","#504CD1"), border_color=("#3A7EBF","#504CD1"), justify="center")
        self.technique_combobox.pack()
        
        button_frame = CTkFrame(self.puzzle_frame)
        button_frame.pack(pady=10)
        
        self.previous_button = CTkButton(button_frame, text="<-", width=20, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.previous_button.pack(side='left', padx=10)

        self.start_button2 = CTkButton(button_frame, text="Start", command=self.start_search, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.start_button2.pack(side='left', pady=10)
        
        self.next_button = CTkButton(button_frame, text="->", width=20, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.next_button.pack(side='left', padx=10)
        
        buttons2_frame = CTkFrame(self.puzzle_frame)
        buttons2_frame.pack(pady=(2,20), padx=10)
        
        self.show_tree_button = CTkButton(buttons2_frame, text="Show Search Tree", width=70, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.show_tree_button.pack(side='left', pady=10, padx=20)

        self.reset_button = CTkButton(buttons2_frame, text="Reset", command=self.reset_puzzle, width=50, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.reset_button.pack(side='left', pady=10, padx=20)
        
        self.show_start_page()

    def show_start_page(self):
        self.puzzle_frame.pack_forget()
        self.start_frame.pack(pady=50)
        
    def return_to_start_page(self):
        self.clear_puzzle()
        self.puzzle_frame.pack_forget()
        self.start_frame.pack(pady=50)
        self.canvas.pack_forget()

    def show_puzzle_page(self):
        self.start_frame.pack_forget()
        self.puzzle_frame.pack(side='left', pady=10, padx=(40,20))
        
        self.canvas = CTkCanvas(self.root, width=322, height=322)
        self.canvas.pack(side='left')
        
        self.draw_puzzle(self.initial_state)

    def draw_puzzle(self, state):
        
        self.canvas.delete("all")
        # Calculate the size and position of each tile
        tile_width = 105
        tile_height = 105
        padding = 5
        theme = self.theme_var.get()

        for i, tile in enumerate(state):
            if tile == '0':  # Empty tile
                row = i // 3
                col = i % 3

                x = col * tile_width + padding
                y = row * tile_height + padding

                if theme == "Light":
                    self.canvas.create_rectangle(x, y, x + tile_width, y + tile_height, fill="#EBEBEB", outline='#0F172A', width=5)
                else:
                    self.canvas.create_rectangle(x, y, x + tile_width, y + tile_height, fill="#282828", outline='#0F172A', width=6)    
                continue
            
            row = i // 3
            col = i % 3

            x = col * tile_width + padding
            y = row * tile_height + padding
            
            if theme == "Light":
                # photo = ImageTk.PhotoImage(Image.open('D:/FOE/Term 7/Artificial Intelligence/Projects/8-puzzle/assets/metal_background.jpg'))
                self.canvas.create_rectangle(x, y, x + tile_width, y + tile_height, fill="#ADEFFD", outline="#0F172A", width=5)
                # self.canvas.create_image(0,0,image=photo)
                self.canvas.create_text(x + tile_width//2, y + tile_height//2, text=tile, font=("joystix monospace", 30), fill="#0B0E16")
                
            else:
                # photo = ImageTk.PhotoImage(Image.open('D:/FOE/Term 7/Artificial Intelligence/Projects/8-puzzle/assets/metal_background.jpg'))
                self.canvas.create_rectangle(x, y, x + tile_width, y + tile_height, fill="#504CD1", outline="#0F172A", width=6)
                # self.canvas.create_image(0,0,image=photo)
                self.canvas.create_text(x + tile_width//2, y + tile_height//2, text=tile, font=("joystix monospace", 30), fill="#0C121C")

    def reset_puzzle(self):
        self.clear_puzzle
        self.canvas.pack_forget()
        self.canvas = CTkCanvas(self.root, width=322, height=322)
        # self.canvas.configure(background="blue")
        self.canvas.pack(side='left')
        self.draw_puzzle(self.initial_state)
           
    def clear_puzzle(self):
        self.canvas.delete("all")
        
    def start_game(self):
        self.show_puzzle_page()
        
    def game_theme(self):
        theme = self.theme_var.get()
        # ctk.set_smooth_theme_transition(True)
        if theme == "Dark":
            ctk.set_appearance_mode("Dark")
            
        elif theme == "Light":
            ctk.set_appearance_mode("Light")        
            
    def test_speed(self, current_state):
        # self.speed= self.speed_slider.get()
        # self.speed = 5
        print(self.speed)
        print(current_state)
        self.clear_puzzle()
        self.draw_puzzle(current_state)
        
    def start_search(self):
        self.speed = self.speed_slider.get()
        self.technique = self.technique_combobox.get()
        print(self.technique)
        # Start the search algorithm to solve the puzzle
        if (self.technique == 'BFS'):
            print("IN BFS")
            list_of_states, num_of_steps, child, start = BFS.BFS_interface(self.initial_state, self.goal_state)
            list_of_states = list_of_states[::-1]
            i = 0
            for state in list_of_states:
                self.draw_puzzle(state)
                print(state)
                self.root.after((i*100) *int(self.speed), self.draw_puzzle, state) 
                i += 1
        elif (self.technique == 'DFS'):
            print("IN DFS")
            list_of_states, num_of_steps, child, start = DFS.DFS_interface(self.initial_state, self.goal_state)
            print("States: ", list_of_states)
            list_of_states = list_of_states[::-1]
            i = 0
            for state in list_of_states:
                self.draw_puzzle(state)
                print(state)
                self.root.after((i*100) *int(self.speed), self.draw_puzzle, state) 
                i += 1
        elif (self.technique == 'A* - Manhattan'):
            print("IN A*-MANHATTAN")
            print("initial state = ", self.initial_state)
            list_of_states, num_of_steps, child, start = Astar.Astar_interface(self.initial_state, self.goal_state, criterion="manhattan")
            list_of_states = list_of_states[::-1]
            print("states: ", list_of_states)
            i = 0
            for state in list_of_states:
                self.draw_puzzle(state)
                print(state)
                self.root.after((i*100) *int(self.speed), self.draw_puzzle, state) 
                i += 1
        elif (self.technique == 'A* - Euclidean'):
            print("IN A*-ECULIDEAN")
            print("initial state = ", self.initial_state)
            list_of_states, num_of_steps, child, start = Astar.Astar_interface(self.initial_state, self.goal_state, criterion="euclidean")
            list_of_states = list_of_states[::-1]
            print("states: ", list_of_states)
            i = 0
            for state in list_of_states:
                self.draw_puzzle(state)
                print(state)
                self.root.after((i*100) *int(self.speed), self.draw_puzzle, state) 
                i += 1
        
        # current_state1 = np.array(['4', '5', '1', '0', '8', '2', '6', '3', '7'])
        # self.test_speed(current_state1)
        # self.root.after(0 *int(self.speed), self.test_speed, current_state1)
    
        # current_state2 = np.array(['4', '5', '1', '8', '0', '2', '6', '3', '7'])
        # self.test_speed(current_state2)
        # self.root.after(1000 *int(self.speed), self.test_speed, current_state2)
        
        # current_state3 = np.array(['4', '5', '1', '8', '2', '0', '6', '3', '7'])
        # self.test_speed(self.initial_state)
        # self.root.after(2000 *int(self.speed), self.test_speed, current_state3)
        
        # current_state4 = np.array(['4', '5', '1', '8', '2', '6', '0', '3', '7'])
        # self.test_speed(current_state4)
        # self.root.after(3000 *int(self.speed), self.test_speed, current_state4)
        
        # current_state5 = np.array(['4', '5', '1', '8', '2', '6', '3', '0', '7'])
        # self.test_speed(current_state5)
        # self.root.after(4000 *int(self.speed), self.test_speed, current_state5)
        # for i in number_of_steps:
            

    def run(self):
        # Show the puzzle visualization

        self.root.mainloop()

app = EightPuzzleGame()
app.run()
