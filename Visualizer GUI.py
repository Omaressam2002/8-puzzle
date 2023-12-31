import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, Label
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkSlider, CTkComboBox, CTkCanvas, CTkRadioButton, CTkScrollableFrame, CTkCheckBox, CTkEntry
import customtkinter as ctk
import numpy as np
from PIL import ImageTk, Image
import time
import BFS, DFS, Astar, Tree, utils, State
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import timeit

import warnings
warnings.filterwarnings("ignore")

  

class EightPuzzleGame:
    def __init__(self):
        self.initial_state = np.array(['8', '2', '1', '5', '4', '6', '0', '3', '7'])
        self.goal_state = np.array(['0', '1', '2', '3', '4', '5', '6', '7', '8'])
        self.speed = 0
        self.technique = "BFS"

        self.root = CTk()
        self.root.title("8-Puzzle Game")
        self.root.geometry('1200x500')
        self.root.resizable(False, False)
        background = ImageTk.PhotoImage(Image.open("assets/purple space.jpg"))
        background_label = CTkLabel(self.root, image= background, text="")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("dark-blue")

        #### START PAGE FRAME ####
        
        self.start_frame = CTkFrame(self.root)
        self.start_frame.pack()
        
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
        
        buttons1_frame = CTkFrame(self.puzzle_frame)
        buttons1_frame.pack(pady=(10,5), padx=5)
        
        self.back_button = CTkButton(buttons1_frame, text="Back", command=self.return_to_start_page, width=50, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.back_button.pack(pady=10, padx=20, side = 'left')
        
        self.nodes_expanded_button = CTkCheckBox(buttons1_frame, text="Nodes Expanded", width=90, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.nodes_expanded_button.pack(pady=10, padx=20, side = 'left')
        
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
        

        self.start_button2 = CTkButton(button_frame, text="Start", command=self.start_search, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.start_button2.pack(side='left', pady=10, padx=10)
        
        
        self.change_puzzle_button = CTkButton(button_frame, text="Change Puzzle", font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"), command= self.change_puzzle)
        self.change_puzzle_button.pack(side='left', padx=10)
        
        buttons2_frame = CTkFrame(self.puzzle_frame)
        buttons2_frame.pack(pady=(2,20), padx=10)
        
        self.show_tree_button = CTkCheckBox(buttons2_frame, text="Show Search Tree", width=70, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.show_tree_button.pack(side='left', pady=10, padx=20)

        self.reset_button = CTkButton(buttons2_frame, text="Reset", command=self.reset_puzzle, width=50, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.reset_button.pack(side='left', pady=10, padx=20)
        
        self.analysis_frame = CTkScrollableFrame(self.root, width = 350, height=250)
        self.analysis_frame.pack()
        
        #### GRID FRAME ####

        self.grid_frame = CTkFrame(self.root, width=300, height=200)
        self.grid_frame.pack(padx=100)
        
        buttons0_grid_frame = CTkFrame(self.grid_frame)
        buttons0_grid_frame.pack(pady=(10,20), padx=10)
        
        self.back2_button = CTkButton(buttons0_grid_frame, text="Back", command=self.return_to_puzzle_page, width=50, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.back2_button.pack(side = 'left', pady=20, padx=20)
        
        self.clear_grid_button = CTkButton(buttons0_grid_frame, text="Clear", command=self.reset_change_puzzle, width=50, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.clear_grid_button.pack(side = 'left', pady=20, padx=10)
        
        self.buttons_grid_frame = CTkFrame(self.grid_frame, width=300, height=300)
        self.buttons_grid_frame.pack(padx=20)

        self.temp = []
        for i in range(9):
            button = CTkButton(self.buttons_grid_frame, text=i, width=60, height=60,
                            font=("joystix monospace", 30), fg_color=("#3A7EBF", "#504CD1"),
                            command=lambda i=i: self.button_click(i))
            button.grid(row=i // 3, column=i % 3, padx=2, pady=2)
        
        buttons2_grid_frame = CTkFrame(self.grid_frame)
        buttons2_grid_frame.pack(side='left', pady=(10,20), padx=20)
        
        
        self.save1_button = CTkButton(buttons2_grid_frame, text="Save as initial state", command=self.save_initial_puzzle, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.save1_button.pack(pady=(10,4), padx=4)
        
        self.save2_button = CTkButton(buttons2_grid_frame, text="Save as goal state", command=self.save_goal_puzzle, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.save2_button.pack(pady=(4,10), padx=4)
        
        self.show_start_page()   
        
    def is_solvable(self, initial_state, goal_state):
        def count_inversions(state):
            inversions = 0
            size = state.size

            for i in range(size - 1):
                for j in range(i + 1, size):
                    if state[i] != '0' and state[j] != '0' and state[i] > state[j]:
                        inversions += 1
                        
            print("No of inversions: ", inversions)
            return inversions

        initial_inversions = count_inversions(initial_state)
        goal_inversions = count_inversions(goal_state)

        return initial_inversions % 2 == goal_inversions % 2 
        
    def reset_change_puzzle(self):
        self.temp = []
        self.clear_puzzle
        self.draw_puzzle(self.temp)
        
    def save_initial_puzzle(self):
        if (len(self.temp) == 9):
            self.initial_state = np.array(self.temp)
            print(self.initial_state)
            self.clear_puzzle
            self.draw_puzzle(self.initial_state)
            self.reset_change_puzzle
            print("INITIAL STATE SAVED SUCCESSFULLY")         

    def save_goal_puzzle(self):
        if (len(self.temp) == 9):
                self.goal_state = np.array(self.temp)
                print(self.goal_state)
                self.reset_change_puzzle
                print("GOAL STATE SAVED SUCCESSFULLY")    

    def show_start_page(self):
        self.grid_frame.pack_forget()
        self.puzzle_frame.pack_forget()
        self.analysis_frame.pack_forget()
        self.start_frame.pack(pady=50)
        
    def return_to_start_page(self):
        self.clear_puzzle()
        self.puzzle_frame.pack_forget()
        self.grid_frame.pack_forget()
        widgets = self.analysis_frame.winfo_children()
        # Destroy each widget in the frame
        for widget in widgets:
            widget.destroy()
        self.analysis_frame.pack_forget()
        self.start_frame.pack(pady=50)
        self.canvas.pack_forget()
        
    def return_to_puzzle_page(self):
        self.clear_puzzle
        self.canvas.pack_forget()
        self.grid_frame.pack_forget()
        widgets = self.analysis_frame.winfo_children()
        # Destroy each widget in the frame
        for widget in widgets:
            widget.destroy()
        self.analysis_frame.pack_forget()
        self.puzzle_frame.pack(side='left', pady=10, padx=(80,40))
        self.canvas = CTkCanvas(self.root, width=322, height=322)
        self.canvas.pack(side='left')
        
        self.draw_puzzle(self.initial_state)
        
        self.analysis_frame.pack(side = 'left', padx=(40,40))
        self.analysis_frame2 = CTkFrame(self.analysis_frame)
        self.analysis_frame2.pack()
        self.analysis_frame_title = CTkLabel(self.analysis_frame2, text ="Analysis History", font=("joystix monospace", 16))
        self.analysis_frame_title.pack(side = 'left', padx=(40,0))
        
        self.analysis_frame_clear_button = CTkButton(self.analysis_frame2, text ="Clear", width=50, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"), command=self.clear_analysis_frame)
        self.analysis_frame_clear_button.pack(side = 'left', padx=(30,0))

    def show_puzzle_page(self):
        self.start_frame.pack_forget()
        self.puzzle_frame.pack(side='left', pady=10, padx=(80,40))
        self.grid_frame.pack_forget()
        self.canvas = CTkCanvas(self.root, width=322, height=322)
        self.canvas.pack(side='left')
        
        self.draw_puzzle(self.initial_state)
        
        self.analysis_frame2 = CTkFrame(self.analysis_frame)
        self.analysis_frame2.pack()
        self.analysis_frame.pack(side = 'left', padx=(40,40))
        self.analysis_frame_title = CTkLabel(self.analysis_frame2, text ="Analysis History", font=("joystix monospace", 16))
        self.analysis_frame_title.pack(side = 'left', padx=(40,0))
        
        self.analysis_frame_clear_button = CTkButton(self.analysis_frame2, text ="Clear", width=50, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"), command=self.clear_analysis_frame)
        self.analysis_frame_clear_button.pack(side = 'left', padx=(30,0))
        
    def change_puzzle(self):
        self.start_frame.pack_forget()
        self.analysis_frame.pack_forget()
        widgets = self.analysis_frame.winfo_children()
        # Destroy each widget in the frame
        for widget in widgets:
            widget.destroy()
        self.clear_puzzle()
        self.canvas.pack_forget()
        self.puzzle_frame.pack_forget()
        self.grid_frame.pack(side='left', padx=(300,20))
        self.canvas = CTkCanvas(self.root, width=322, height=322)
        self.canvas.pack(side='left', padx=(20,100))
        
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

    def clear_analysis_frame(self):
        widgets = self.analysis_frame.winfo_children()
        # Destroy each widget in the frame
        for widget in widgets:
            widget.destroy()
        self.analysis_frame.pack_forget()
        self.analysis_frame.pack(side = 'left', padx=(40,40))
        self.analysis_frame2 = CTkFrame(self.analysis_frame)
        self.analysis_frame2.pack()
        self.analysis_frame_title = CTkLabel(self.analysis_frame2, text ="Analysis History", font=("joystix monospace", 16))
        self.analysis_frame_title.pack(side = 'left', padx=(40,0))
        
        self.analysis_frame_clear_button = CTkButton(self.analysis_frame2, text ="Clear", width=50, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"), command=self.clear_analysis_frame)
        self.analysis_frame_clear_button.pack(side = 'left', padx=(30,0))
        
    def reset_puzzle(self):
        self.clear_puzzle
        self.canvas.pack_forget()
        self.grid_frame.pack_forget()
        
        widgets = self.analysis_frame.winfo_children()
        # Destroy each widget in the frame
        for widget in widgets:
            widget.destroy()
        self.analysis_frame.pack_forget()
        
        self.canvas = CTkCanvas(self.root, width=322, height=322)
        self.canvas.pack(side = 'left')
        self.draw_puzzle(self.initial_state)
        self.analysis_frame.pack(side='left', padx=(40,40))
        
        self.analysis_frame2 = CTkFrame(self.analysis_frame)
        self.analysis_frame2.pack()
        self.analysis_frame_title = CTkLabel(self.analysis_frame2, text ="Analysis History", font=("joystix monospace", 16))
        self.analysis_frame_title.pack(side = 'left', padx=(40,0))
        
        self.analysis_frame_clear_button = CTkButton(self.analysis_frame2, text ="Clear", width=50, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"), command=self.clear_analysis_frame)
        self.analysis_frame_clear_button.pack(side = 'left', padx=(30,0))
           
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

    def button_click(self, i):
        if len(self.temp) > 9:
            return
        for j in range (len(self.temp)):
            if i == int(self.temp[j]):
                return
        self.temp.append(str(i))
        print(self.temp)
        self.clear_puzzle
        self.draw_puzzle(self.temp)
        
    def start_search(self):
        if self.is_solvable(self.initial_state, self.goal_state):
            print("PUZZLE SOLVABLE")

            self.speed = self.speed_slider.get()
            self.technique = self.technique_combobox.get()
            print(self.technique)
            self.reset_puzzle
            # Start the search algorithm to solve the puzzle
            
            ####    BFS    ####
            if (self.technique == 'BFS'):
                print("IN BFS")
                # check running time from here
                begin = timeit.default_timer()
                list_of_states, num_of_steps, child, start, list_of_explored ,search_depth = BFS.BFS_interface(self.initial_state, self.goal_state)
                stop = timeit.default_timer()

                BFS_time = stop - begin
                list_of_states = list_of_states[::-1]
                i = 0
                if self.nodes_expanded_button.get():
                    for explored_state in list(list_of_explored):
                        self.draw_puzzle(explored_state)
                        self.root.after((i*100) *int(self.speed), self.draw_puzzle, explored_state) 
                        i += 1
                    self.analyze_algorithm(self.technique, iteration= "explored", number_of_steps = len(list_of_explored), time_taken = BFS_time, search_depth = search_depth)
                    if self.show_tree_button.get():
                        self.construct(start, list_of_states, list_of_explored)
                else:
                    for state in list_of_states:
                        self.draw_puzzle(state)
                        #print(state)
                        self.root.after((i*100) *int(self.speed), self.draw_puzzle, state) 
                        i += 1
                    self.analyze_algorithm(self.technique, iteration= "Path", number_of_steps = num_of_steps, time_taken = BFS_time, search_depth = search_depth)
                    if self.show_tree_button.get():
                        self.construct(start, list_of_states, list_of_explored)
                    
            elif (self.technique == 'DFS'):
                print("IN DFS")
                begin = timeit.default_timer()
                list_of_states, num_of_steps, child, start, list_of_explored ,search_depth = DFS.DFS_interface(self.initial_state, self.goal_state)
                stop = timeit.default_timer()

                DFS_time = stop - begin

                list_of_states = list_of_states[::-1]
                # explored doesnt need to be reversed
                i = 0
                if self.nodes_expanded_button.get():
                    for explored_state in list(list_of_explored):
                        self.draw_puzzle(explored_state)
                        #print(explored_state)
                        self.root.after((i*100) *int(self.speed), self.draw_puzzle, explored_state) 
                        i += 1
                    self.analyze_algorithm(self.technique, iteration= "explored", number_of_steps = len(list_of_explored), time_taken = DFS_time, search_depth = search_depth)
                    if self.show_tree_button.get():
                        self.construct(start, list_of_states, list_of_explored)
                else:
                    for state in list_of_states:
                        self.draw_puzzle(state)
                        #print(state)
                        self.root.after((i*100) *int(self.speed), self.draw_puzzle, state) 
                        i += 1
                    self.analyze_algorithm(self.technique, iteration= "Path", number_of_steps = num_of_steps, time_taken = DFS_time, search_depth = search_depth)
                    if self.show_tree_button.get():
                        self.construct(start, list_of_states, list_of_explored)
                    
            elif (self.technique == 'A* - Manhattan'):
                print("IN A*-MANHATTAN")
                begin = timeit.default_timer()
                list_of_states, num_of_steps, child, start, list_of_explored ,search_depth = Astar.Astar_interface(self.initial_state, self.goal_state, criterion="manhattan")
                stop = timeit.default_timer()

                astar_manhattan_time = stop - begin

                list_of_states = list_of_states[::-1]
                i = 0
                if self.nodes_expanded_button.get():
                    for explored_state in list(list_of_explored):
                        self.draw_puzzle(explored_state)
                        #print(explored_state)
                        self.root.after((i*100) *int(self.speed), self.draw_puzzle, explored_state) 
                        i += 1
                    self.analyze_algorithm(self.technique, iteration= "explored", number_of_steps = len(list_of_explored), time_taken = astar_manhattan_time, search_depth = search_depth)
                    if self.show_tree_button.get():
                        self.construct(start, list_of_states, list_of_explored)
                else:
                    for state in list_of_states:
                        self.draw_puzzle(state)
                        #print(state)
                        self.root.after((i*100) *int(self.speed), self.draw_puzzle, state) 
                        i += 1
                    self.analyze_algorithm(self.technique, iteration= "Path", number_of_steps = num_of_steps, time_taken = astar_manhattan_time, search_depth = search_depth)
                    if self.show_tree_button.get():
                        self.construct(start, list_of_states, list_of_explored)
                
            elif (self.technique == 'A* - Euclidean'):
                print("IN A*-ECULIDEAN")
                print("initial state = ", self.initial_state)
                
                begin = timeit.default_timer()

                list_of_states, num_of_steps, child, start, list_of_explored ,search_depth = Astar.Astar_interface(self.initial_state, self.goal_state, criterion="euclidean")
                stop = timeit.default_timer()

                astar_euclidean_time = stop - begin
                list_of_states = list_of_states[::-1]
                i = 0
                if self.nodes_expanded_button.get():
                    for explored_state in list(list_of_explored):
                        self.draw_puzzle(explored_state)
                        #print(explored_state)
                        self.root.after((i*100) *int(self.speed), self.draw_puzzle, explored_state) 
                        i += 1
                    self.analyze_algorithm(self.technique, iteration= "explored", number_of_steps = len(list_of_explored), time_taken = astar_euclidean_time, search_depth = search_depth)
                    if self.show_tree_button.get():
                        self.construct(start, list_of_states, list_of_explored)
                        # self.construct(child)
                else:
                    for state in list_of_states:
                        self.draw_puzzle(state)
                        #print(state)
                        self.root.after((i*100) *int(self.speed), self.draw_puzzle, state) 
                        i += 1
                    self.analyze_algorithm(self.technique, iteration= "Path", number_of_steps = num_of_steps, time_taken = astar_euclidean_time, search_depth = search_depth)
                    if self.show_tree_button.get():
                        self.construct(start, list_of_states, list_of_explored)
                        # self.construct(child)
        else:
            print("PUZZLE UNSOLVABLE")
            solvable_text = "Oops.. It seems like the puzzle is \nunsolvable! Try changing either the\ninitial or goal state."
            solvable_label = CTkLabel(self.analysis_frame, text = solvable_text, text_color = "red", font=("joystix monospace", 12), width = 200)   
            solvable_label.pack(anchor="w", pady=4, padx=7)
            return        
        
    def analyze_algorithm (self, algorithm, iteration, number_of_steps, time_taken, search_depth):
        steps_text = f"--> {algorithm} {iteration} Steps: {number_of_steps - 1}\n Time taken: {time_taken*1000:.4f} ms\n Search depth: {search_depth}"
        analysis_label = CTkLabel(self.analysis_frame, text = steps_text, font=("joystix monospace", 12), width = 280)   
        analysis_label.pack(anchor="w", pady=3)
        
    def construct(self, start, states, explored):
        #t = Tree.tree(start)
        #t.traverseTree(start)
        tree_frame = CTkFrame(self.root)
        tree_frame.pack()
        nodes_colors = []

        #Directed graph for visualization
        graph = nx.DiGraph()

        # Function to recursively traverse and visualize the search tree
        def visualize_search_tree(state, parent=None, level=0):
            state.level = level  # Assign the level attribute to the node
            graph.add_node(state)
            
            #Adding colors to the color array
            if any(np.array_equal(np.array(list(state.toString())), arr) for arr in explored) and any(np.array_equal(np.array(list(state.toString())), arr) for arr in states):
                nodes_colors.append("#FFC500")
            elif any(np.array_equal(np.array(list(state.toString())), arr) for arr in explored):
                nodes_colors.append("#B0F1FF") 
            else:
                nodes_colors.append("#353CAE")

            # Add an edge to connect the node with its parent
            if parent is not None:
                graph.add_edge(parent, state)

            # Recursively visualize the child nodes
            for child_state in state.children:
                visualize_search_tree(child_state, state, level + 1)

        # Call the visualization function with the root state
        visualize_search_tree(start)

        # Create a networkx graph layout using the Spring layout algorithm
        pos = nx.spring_layout(graph, k=0.05)

        # Get the node labels from the 'toString()' function
        node_labels = {n: n.toString() for n in graph.nodes}

        # Get the levels of the nodes for positioning
        levels = {n: n.level for n in graph.nodes}

        # Set node size and spacing
        node_size = 700
        vertical_spacing = 500 
        horizontal_spacing = 0
        padx = 48

        # Calculate the number of nodes in each level
        level_counts = {level: sum(1 for node in graph.nodes if levels[node] == level) for level in set(levels.values())}

        # Calculate the additional spacing needed for each level
        additional_spacing = {level: (count - 1) * horizontal_spacing for level, count in level_counts.items() if level != 0}

        # Adjust node positions based on levels and additional spacing
        y_values = set(levels.values())
        y_positions = {
        level: -level * vertical_spacing - additional_spacing.get(level, 0)
        for level in sorted(y_values)
        }
        adjusted_pos = {node: (pos[node][0], y_positions[levels[node]]) for node in graph.nodes}

        # Draw the tree
        nx.draw_networkx(
            graph,
            adjusted_pos,
            with_labels=False,
            node_shape='s',
            node_size=node_size,
            node_color=nodes_colors,
            edgecolors='black',
        )
        nx.draw_networkx_labels(
            graph,
            adjusted_pos,
            labels=node_labels,
            font_size=10,
            font_family= "joystix monospace",
            font_color='black',
            verticalalignment='center',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'),
        )
        
        legend_patches = [
            mpatches.Patch(color='#FFC500', label='Path'),
            mpatches.Patch(color='#B0F1FF', label='Explored'),
            mpatches.Patch(color='#353CAE', label='Not Explored')
        ]

        # Add legend
        legend = plt.legend(handles=legend_patches, title='Node Status')
        legend.get_title().set_fontsize(12)
        for text in legend.get_texts():
            text.set_fontsize(10)
            text.set_fontfamily("Joystix Monospace")
        # Show the tree
        plt.axis('off')
        plt.show()
        
    def run(self):
        # Show the puzzle visualization
        self.root.mainloop()

app = EightPuzzleGame()
app.run()
