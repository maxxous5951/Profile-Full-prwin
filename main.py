import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from preflop_generator import PreflopProfileGenerator
from flop_generator import FlopProfileGenerator
from turn_generator import TurnProfileGenerator
from river_generator import RiverProfileGenerator

class OpenHoldemProfileGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenHoldem Profile Generator")
        self.root.geometry("900x1000")
        self.root.minsize(900, 1000)
        
        # Configuration variables
        self.num_players = tk.IntVar(value=9)
        self.game_type = tk.StringVar(value="Cash Game")
        
        # Strategy variables (all with range 0-100)
        self.aggression = tk.IntVar(value=50)
        self.tightness = tk.IntVar(value=50)
        self.limp_frequency = tk.IntVar(value=30)
        self.threebet_frequency = tk.IntVar(value=40)
        self.fourbet_frequency = tk.IntVar(value=30)
        self.squeeze_frequency = tk.IntVar(value=35)
        
        # Bet sizing variables
        self.open_raise_var = tk.StringVar(value="2.5")
        
        # Flop variables
        self.ip_cbet_freq = tk.IntVar(value=70)
        self.oop_cbet_freq = tk.IntVar(value=60)
        self.ip_cbet_size = tk.StringVar(value="50")
        self.oop_cbet_size = tk.StringVar(value="66")
        self.dry_board_adjust = tk.IntVar(value=20)
        self.wet_board_adjust = tk.IntVar(value=-20)
        self.checkraise_defense = tk.IntVar(value=35)
        self.donk_response = tk.StringVar(value="Call/Raise")
        self.value_aggression = tk.IntVar(value=80)
        self.draw_aggression = tk.IntVar(value=60)
        self.semibluff_freq = tk.IntVar(value=65)
        self.multiway_cbet_freq = tk.IntVar(value=40)
        self.multiway_value_range = tk.IntVar(value=25)
        
        # Turn variables
        self.second_barrel_freq = tk.IntVar(value=60)
        self.delayed_cbet_freq = tk.IntVar(value=40)
        self.ip_turn_bet_size = tk.StringVar(value="66")
        self.oop_turn_bet_size = tk.StringVar(value="75")
        self.turn_checkraise_freq = tk.IntVar(value=25)
        self.turn_float_freq = tk.IntVar(value=30)
        self.turn_probe_freq = tk.IntVar(value=35)
        self.turn_fold_to_cbet_freq = tk.IntVar(value=60)
        self.turn_bluff_raise_freq = tk.IntVar(value=20)
        self.scare_card_adjust = tk.IntVar(value=-15)
        self.draw_complete_adjust = tk.IntVar(value=10)
        
        # River variables
        self.third_barrel_freq = tk.IntVar(value=40)
        self.delayed_second_barrel_freq = tk.IntVar(value=30)
        self.ip_river_bet_size = tk.StringVar(value="75")
        self.oop_river_bet_size = tk.StringVar(value="75")
        self.river_checkraise_freq = tk.IntVar(value=15)
        self.river_float_freq = tk.IntVar(value=20)
        self.river_probe_freq = tk.IntVar(value=25)
        self.river_fold_to_bet_freq = tk.IntVar(value=70)
        self.river_bluff_raise_freq = tk.IntVar(value=10)
        self.river_value_range = tk.IntVar(value=60)
        self.river_bluff_range = tk.IntVar(value=15)
        self.river_check_behind_range = tk.IntVar(value=80)
        
        # Push/Fold variables - initialize with default values
        self.initialize_push_fold_variables()
        
        # Create the generators
        self.preflop_generator = PreflopProfileGenerator()
        self.flop_generator = FlopProfileGenerator()
        self.turn_generator = TurnProfileGenerator()
        self.river_generator = RiverProfileGenerator()
        
        # Setup the UI
        self.create_ui()
    
    def initialize_push_fold_variables(self):
        """Initialize all Push/Fold variables with default values"""
        # 1BB stack ranges
        self.push_1bb_ep = tk.IntVar(value=75)
        self.push_1bb_mp = tk.IntVar(value=80)
        self.push_1bb_co = tk.IntVar(value=85)
        self.push_1bb_btn = tk.IntVar(value=90)
        self.push_1bb_sb = tk.IntVar(value=92)
        self.push_1bb_bb = tk.IntVar(value=95)
        self.call_1bb_vs_ep = tk.IntVar(value=60)
        self.call_1bb_vs_mp = tk.IntVar(value=65)
        self.call_1bb_vs_co = tk.IntVar(value=70)
        self.call_1bb_vs_btn = tk.IntVar(value=75)
        self.call_1bb_vs_sb = tk.IntVar(value=80)
        
        # 2BB-5BB stack ranges
        self.push_2bb_ep = tk.IntVar(value=60)
        self.push_2bb_mp = tk.IntVar(value=65)
        self.push_2bb_co = tk.IntVar(value=70)
        self.push_2bb_btn = tk.IntVar(value=75)
        self.push_2bb_sb = tk.IntVar(value=80)
        self.push_2bb_bb = tk.IntVar(value=85)
        
        self.push_3bb_ep = tk.IntVar(value=45)
        self.push_3bb_mp = tk.IntVar(value=50)
        self.push_3bb_co = tk.IntVar(value=55)
        self.push_3bb_btn = tk.IntVar(value=60)
        self.push_3bb_sb = tk.IntVar(value=65)
        self.push_3bb_bb = tk.IntVar(value=70)
        
        self.push_4bb_ep = tk.IntVar(value=35)
        self.push_4bb_mp = tk.IntVar(value=40)
        self.push_4bb_co = tk.IntVar(value=45)
        self.push_4bb_btn = tk.IntVar(value=50)
        self.push_4bb_sb = tk.IntVar(value=55)
        self.push_4bb_bb = tk.IntVar(value=60)
        
        self.push_5bb_ep = tk.IntVar(value=28)
        self.push_5bb_mp = tk.IntVar(value=32)
        self.push_5bb_co = tk.IntVar(value=36)
        self.push_5bb_btn = tk.IntVar(value=40)
        self.push_5bb_sb = tk.IntVar(value=45)
        self.push_5bb_bb = tk.IntVar(value=50)
        
        # 6BB-10BB stack ranges
        self.push_6bb_ep = tk.IntVar(value=22)
        self.push_6bb_mp = tk.IntVar(value=26)
        self.push_6bb_co = tk.IntVar(value=30)
        self.push_6bb_btn = tk.IntVar(value=35)
        self.push_6bb_sb = tk.IntVar(value=40)
        self.push_6bb_bb = tk.IntVar(value=45)
        
        self.push_7bb_ep = tk.IntVar(value=18)
        self.push_7bb_mp = tk.IntVar(value=22)
        self.push_7bb_co = tk.IntVar(value=26)
        self.push_7bb_btn = tk.IntVar(value=30)
        self.push_7bb_sb = tk.IntVar(value=35)
        self.push_7bb_bb = tk.IntVar(value=40)
        
        self.push_8bb_ep = tk.IntVar(value=15)
        self.push_8bb_mp = tk.IntVar(value=18)
        self.push_8bb_co = tk.IntVar(value=22)
        self.push_8bb_btn = tk.IntVar(value=26)
        self.push_8bb_sb = tk.IntVar(value=30)
        self.push_8bb_bb = tk.IntVar(value=35)
        
        self.push_9bb_ep = tk.IntVar(value=12)
        self.push_9bb_mp = tk.IntVar(value=15)
        self.push_9bb_co = tk.IntVar(value=18)
        self.push_9bb_btn = tk.IntVar(value=22)
        self.push_9bb_sb = tk.IntVar(value=26)
        self.push_9bb_bb = tk.IntVar(value=30)
        
        self.push_10bb_ep = tk.IntVar(value=10)
        self.push_10bb_mp = tk.IntVar(value=12)
        self.push_10bb_co = tk.IntVar(value=15)
        self.push_10bb_btn = tk.IntVar(value=18)
        self.push_10bb_sb = tk.IntVar(value=22)
        self.push_10bb_bb = tk.IntVar(value=25)
        
        # 2BB-10BB call ranges
        self.call_2bb_vs_ep = tk.IntVar(value=50)
        self.call_2bb_vs_mp = tk.IntVar(value=55)
        self.call_2bb_vs_co = tk.IntVar(value=60)
        self.call_2bb_vs_btn = tk.IntVar(value=65)
        self.call_2bb_vs_sb = tk.IntVar(value=70)
        
        self.call_3bb_vs_ep = tk.IntVar(value=40)
        self.call_3bb_vs_mp = tk.IntVar(value=45)
        self.call_3bb_vs_co = tk.IntVar(value=50)
        self.call_3bb_vs_btn = tk.IntVar(value=55)
        self.call_3bb_vs_sb = tk.IntVar(value=60)
        
        self.call_4bb_vs_ep = tk.IntVar(value=30)
        self.call_4bb_vs_mp = tk.IntVar(value=35)
        self.call_4bb_vs_co = tk.IntVar(value=40)
        self.call_4bb_vs_btn = tk.IntVar(value=45)
        self.call_4bb_vs_sb = tk.IntVar(value=50)
        
        self.call_5bb_vs_ep = tk.IntVar(value=25)
        self.call_5bb_vs_mp = tk.IntVar(value=28)
        self.call_5bb_vs_co = tk.IntVar(value=32)
        self.call_5bb_vs_btn = tk.IntVar(value=36)
        self.call_5bb_vs_sb = tk.IntVar(value=40)
        
        self.call_6_10bb_vs_ep = tk.IntVar(value=20)
        self.call_6_10bb_vs_mp = tk.IntVar(value=22)
        self.call_6_10bb_vs_co = tk.IntVar(value=25)
        self.call_6_10bb_vs_btn = tk.IntVar(value=28)
        self.call_6_10bb_vs_sb = tk.IntVar(value=32)
        
        # 10BB+ stack ranges
        self.push_10_15bb_ep = tk.IntVar(value=8)
        self.push_10_15bb_mp = tk.IntVar(value=10)
        self.push_10_15bb_co = tk.IntVar(value=12)
        self.push_10_15bb_btn = tk.IntVar(value=15)
        self.push_10_15bb_sb = tk.IntVar(value=18)
        self.push_10_15bb_bb = tk.IntVar(value=20)
        
        self.push_15_20bb_ep = tk.IntVar(value=5)
        self.push_15_20bb_mp = tk.IntVar(value=8)
        self.push_15_20bb_co = tk.IntVar(value=10)
        self.push_15_20bb_btn = tk.IntVar(value=12)
        self.push_15_20bb_sb = tk.IntVar(value=15)
        self.push_15_20bb_bb = tk.IntVar(value=18)
        
        self.push_20_25bb_ep = tk.IntVar(value=3)
        self.push_20_25bb_mp = tk.IntVar(value=5)
        self.push_20_25bb_co = tk.IntVar(value=7)
        self.push_20_25bb_btn = tk.IntVar(value=10)
        self.push_20_25bb_sb = tk.IntVar(value=12)
        self.push_20_25bb_bb = tk.IntVar(value=15)
        
        # 10BB+ call ranges
        self.call_10_15bb_vs_ep = tk.IntVar(value=15)
        self.call_10_15bb_vs_mp = tk.IntVar(value=18)
        self.call_10_15bb_vs_co = tk.IntVar(value=20)
        self.call_10_15bb_vs_btn = tk.IntVar(value=22)
        self.call_10_15bb_vs_sb = tk.IntVar(value=25)
        
        self.call_15_25bb_vs_ep = tk.IntVar(value=10)
        self.call_15_25bb_vs_mp = tk.IntVar(value=12)
        self.call_15_25bb_vs_co = tk.IntVar(value=15)
        self.call_15_25bb_vs_btn = tk.IntVar(value=18)
        self.call_15_25bb_vs_sb = tk.IntVar(value=20)
    
    def create_ui(self):
        # Create a notebook (tabbed interface)
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Create main configuration tab
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="Configuration")
        
        # Game settings
        game_frame = ttk.LabelFrame(config_frame, text="Game Settings")
        game_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(game_frame, text="Number of Players:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Combobox(game_frame, textvariable=self.num_players, 
                    values=[2, 3, 4, 5, 6, 7, 8, 9], width=5, state="readonly").grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(game_frame, text="Game Type:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Combobox(game_frame, textvariable=self.game_type,
                    values=["Cash Game", "Tournament"], width=15, state="readonly").grid(row=1, column=1, padx=5, pady=5)
        
        # Strategy settings
        strategy_frame = ttk.LabelFrame(config_frame, text="Strategy Settings")
        strategy_frame.pack(fill="x", padx=10, pady=10)
        
        # Aggression slider
        ttk.Label(strategy_frame, text="Aggression:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(strategy_frame, from_=0, to=100, variable=self.aggression, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(strategy_frame, textvariable=self.aggression).grid(row=0, column=2, padx=5, pady=5)
        
        # Tightness slider
        ttk.Label(strategy_frame, text="Tightness:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(strategy_frame, from_=0, to=100, variable=self.tightness, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(strategy_frame, textvariable=self.tightness).grid(row=1, column=2, padx=5, pady=5)
        
        # Limp frequency slider
        ttk.Label(strategy_frame, text="Limp Frequency:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(strategy_frame, from_=0, to=100, variable=self.limp_frequency, orient="horizontal").grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(strategy_frame, textvariable=self.limp_frequency).grid(row=2, column=2, padx=5, pady=5)
        
        # 3-bet frequency slider
        ttk.Label(strategy_frame, text="3-bet Frequency:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(strategy_frame, from_=0, to=100, variable=self.threebet_frequency, orient="horizontal").grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(strategy_frame, textvariable=self.threebet_frequency).grid(row=3, column=2, padx=5, pady=5)
        
        # 4-bet frequency slider
        ttk.Label(strategy_frame, text="4-bet Frequency:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(strategy_frame, from_=0, to=100, variable=self.fourbet_frequency, orient="horizontal").grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(strategy_frame, textvariable=self.fourbet_frequency).grid(row=4, column=2, padx=5, pady=5)
        
        # Squeeze frequency slider
        ttk.Label(strategy_frame, text="Squeeze Frequency:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(strategy_frame, from_=0, to=100, variable=self.squeeze_frequency, orient="horizontal").grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(strategy_frame, textvariable=self.squeeze_frequency).grid(row=5, column=2, padx=5, pady=5)
        
        # Configure the grid column to expand
        strategy_frame.columnconfigure(1, weight=1)
        
        # Bet sizing frame
        bet_frame = ttk.LabelFrame(config_frame, text="Bet Sizing")
        bet_frame.pack(fill="x", padx=10, pady=10)
        
        # Open raise size options
        ttk.Label(bet_frame, text="Open Raise Size (BB):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Combobox(bet_frame, textvariable=self.open_raise_var, values=["2", "2.2", "2.5", "3"], 
                    width=5, state="readonly").grid(row=0, column=1, padx=5, pady=5)
        
        # Generate and save buttons
        btn_frame = ttk.Frame(config_frame)
        btn_frame.pack(fill="x", padx=10, pady=20)
        
        ttk.Button(btn_frame, text="Generate Profile", command=self.generate_profile).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Save Profile", command=self.save_profile).pack(side="left", padx=5)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(config_frame, text="Preview")
        preview_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.preview_text = tk.Text(preview_frame, wrap=tk.WORD, height=15)
        self.preview_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create other tabs for specific scenarios
        self.create_preflop_tab(notebook)
        self.create_flop_tab(notebook)
        self.create_turn_tab(notebook)
        self.create_river_tab(notebook)
        self.create_push_fold_tab(notebook)
    
    def create_preflop_tab(self, notebook):
        preflop_frame = ttk.Frame(notebook)
        notebook.add(preflop_frame, text="Preflop Settings")
        
        # Create Open Raise frame
        openraise_frame = ttk.LabelFrame(preflop_frame, text="Open Raise Ranges")
        openraise_frame.pack(fill="x", padx=10, pady=10)
        
        # EP range
        ttk.Label(openraise_frame, text="Early Position Range (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ep_range = tk.IntVar(value=15)
        ttk.Scale(openraise_frame, from_=0, to=100, variable=self.ep_range, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(openraise_frame, textvariable=self.ep_range).grid(row=0, column=2, padx=5, pady=5)
        
        # MP range
        ttk.Label(openraise_frame, text="Middle Position Range (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.mp_range = tk.IntVar(value=20)
        ttk.Scale(openraise_frame, from_=0, to=100, variable=self.mp_range, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(openraise_frame, textvariable=self.mp_range).grid(row=1, column=2, padx=5, pady=5)
        
        # LP range
        ttk.Label(openraise_frame, text="Late Position Range (%):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.lp_range = tk.IntVar(value=30)
        ttk.Scale(openraise_frame, from_=0, to=100, variable=self.lp_range, orient="horizontal").grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(openraise_frame, textvariable=self.lp_range).grid(row=2, column=2, padx=5, pady=5)
        
        # Open Raise sizing
        sizing_frame = ttk.LabelFrame(preflop_frame, text="Position-Based Sizing")
        sizing_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(sizing_frame, text="EP Sizing (BB):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ep_sizing = tk.StringVar(value="3.0")
        ttk.Combobox(sizing_frame, textvariable=self.ep_sizing, values=["2.5", "3.0", "3.5", "4.0"], 
                    width=5, state="readonly").grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(sizing_frame, text="MP Sizing (BB):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.mp_sizing = tk.StringVar(value="2.8")
        ttk.Combobox(sizing_frame, textvariable=self.mp_sizing, values=["2.2", "2.5", "2.8", "3.0"], 
                    width=5, state="readonly").grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(sizing_frame, text="LP Sizing (BB):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.lp_sizing = tk.StringVar(value="2.5")
        ttk.Combobox(sizing_frame, textvariable=self.lp_sizing, values=["2.0", "2.2", "2.5", "2.8"], 
                    width=5, state="readonly").grid(row=2, column=1, padx=5, pady=5)
        
        # 3-Bet Defense
        threebet_frame = ttk.LabelFrame(preflop_frame, text="3-Bet Defense")
        threebet_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(threebet_frame, text="Call 3-Bet Range (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.call_3bet_range = tk.IntVar(value=15)
        ttk.Scale(threebet_frame, from_=0, to=100, variable=self.call_3bet_range, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(threebet_frame, textvariable=self.call_3bet_range).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(threebet_frame, text="4-Bet Range (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.fourbet_range = tk.IntVar(value=8)
        ttk.Scale(threebet_frame, from_=0, to=100, variable=self.fourbet_range, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(threebet_frame, textvariable=self.fourbet_range).grid(row=1, column=2, padx=5, pady=5)
        
        # Position adjustments
        position_adj_frame = ttk.LabelFrame(preflop_frame, text="Position Adjustments")
        position_adj_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(position_adj_frame, text="In Position 3-Bet Adjust (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ip_3bet_adjust = tk.IntVar(value=20)
        ttk.Scale(position_adj_frame, from_=0, to=100, variable=self.ip_3bet_adjust, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(position_adj_frame, textvariable=self.ip_3bet_adjust).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(position_adj_frame, text="vs Late Position 3-Bet Adjust (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.vs_lp_3bet_adjust = tk.IntVar(value=15)
        ttk.Scale(position_adj_frame, from_=0, to=100, variable=self.vs_lp_3bet_adjust, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(position_adj_frame, textvariable=self.vs_lp_3bet_adjust).grid(row=1, column=2, padx=5, pady=5)
        
        # 4-Bet defense
        fourbet_frame = ttk.LabelFrame(preflop_frame, text="4-Bet Defense")
        fourbet_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(fourbet_frame, text="Call 4-Bet Range (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.call_4bet_range = tk.IntVar(value=5)
        ttk.Scale(fourbet_frame, from_=0, to=100, variable=self.call_4bet_range, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(fourbet_frame, textvariable=self.call_4bet_range).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(fourbet_frame, text="5-Bet Range (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.fivebet_range = tk.IntVar(value=3)
        ttk.Scale(fourbet_frame, from_=0, to=100, variable=self.fivebet_range, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(fourbet_frame, textvariable=self.fivebet_range).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(fourbet_frame, text="Short Stack 4-Bet Adjust (%):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.short_stack_4bet = tk.IntVar(value=30)
        ttk.Scale(fourbet_frame, from_=0, to=100, variable=self.short_stack_4bet, orient="horizontal").grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(fourbet_frame, textvariable=self.short_stack_4bet).grid(row=2, column=2, padx=5, pady=5)
        
        # Squeeze settings
        squeeze_frame = ttk.LabelFrame(preflop_frame, text="Squeeze Settings")
        squeeze_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(squeeze_frame, text="Squeeze vs 1 Caller (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.squeeze_1caller = tk.IntVar(value=12)
        ttk.Scale(squeeze_frame, from_=0, to=100, variable=self.squeeze_1caller, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(squeeze_frame, textvariable=self.squeeze_1caller).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(squeeze_frame, text="Squeeze vs Multiple Callers (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.squeeze_multi = tk.IntVar(value=8)
        ttk.Scale(squeeze_frame, from_=0, to=100, variable=self.squeeze_multi, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(squeeze_frame, textvariable=self.squeeze_multi).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(squeeze_frame, text="Squeeze Sizing (x pot):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.squeeze_sizing = tk.StringVar(value="3.0")
        ttk.Combobox(squeeze_frame, textvariable=self.squeeze_sizing, values=["2.5", "3.0", "3.5", "4.0"], 
                    width=5, state="readonly").grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(squeeze_frame, text="Blinds Squeeze Adjust (%):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.blinds_squeeze = tk.IntVar(value=25)
        ttk.Scale(squeeze_frame, from_=0, to=100, variable=self.blinds_squeeze, orient="horizontal").grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(squeeze_frame, textvariable=self.blinds_squeeze).grid(row=3, column=2, padx=5, pady=5)
        
        ttk.Label(squeeze_frame, text="Button Squeeze Adjust (%):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.btn_squeeze = tk.IntVar(value=20)
        ttk.Scale(squeeze_frame, from_=0, to=100, variable=self.btn_squeeze, orient="horizontal").grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(squeeze_frame, textvariable=self.btn_squeeze).grid(row=4, column=2, padx=5, pady=5)
        
        # Make columns expandable
        for frame in [openraise_frame, sizing_frame, threebet_frame, position_adj_frame, fourbet_frame, squeeze_frame]:
            frame.columnconfigure(1, weight=1)

    def create_push_fold_tab(self, notebook):
        """Create a tab for Push/Fold settings"""
        push_fold_frame = ttk.Frame(notebook)
        notebook.add(push_fold_frame, text="Push/Fold")
        
        # Use a notebook for organization
        pf_notebook = ttk.Notebook(push_fold_frame)
        pf_notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create tabs for different stack sizes
        tab_1bb = ttk.Frame(pf_notebook)
        tab_2_5bb = ttk.Frame(pf_notebook)
        tab_6_10bb = ttk.Frame(pf_notebook)
        tab_10_25bb = ttk.Frame(pf_notebook)
        call_ranges = ttk.Frame(pf_notebook)
        
        pf_notebook.add(tab_1bb, text="1BB")
        pf_notebook.add(tab_2_5bb, text="2-5BB")
        pf_notebook.add(tab_6_10bb, text="6-10BB")
        pf_notebook.add(tab_10_25bb, text="10-25BB")
        pf_notebook.add(call_ranges, text="Call Ranges")
        
        # 1BB Tab
        self.create_push_fold_position_frame(tab_1bb, "1BB Stack Push Ranges", {
            "EP": self.push_1bb_ep,
            "MP": self.push_1bb_mp,
            "CO": self.push_1bb_co,
            "BTN": self.push_1bb_btn,
            "SB": self.push_1bb_sb,
            "BB": self.push_1bb_bb
        })
        
        # 2-5BB Tab
        frame_2bb = self.create_push_fold_position_frame(tab_2_5bb, "2BB Stack Push Ranges", {
            "EP": self.push_2bb_ep,
            "MP": self.push_2bb_mp,
            "CO": self.push_2bb_co,
            "BTN": self.push_2bb_btn,
            "SB": self.push_2bb_sb,
            "BB": self.push_2bb_bb
        })
        
        frame_3bb = self.create_push_fold_position_frame(tab_2_5bb, "3BB Stack Push Ranges", {
            "EP": self.push_3bb_ep,
            "MP": self.push_3bb_mp,
            "CO": self.push_3bb_co,
            "BTN": self.push_3bb_btn,
            "SB": self.push_3bb_sb,
            "BB": self.push_3bb_bb
        })
        
        frame_4bb = self.create_push_fold_position_frame(tab_2_5bb, "4BB Stack Push Ranges", {
            "EP": self.push_4bb_ep,
            "MP": self.push_4bb_mp,
            "CO": self.push_4bb_co,
            "BTN": self.push_4bb_btn,
            "SB": self.push_4bb_sb,
            "BB": self.push_4bb_bb
        })
        
        frame_5bb = self.create_push_fold_position_frame(tab_2_5bb, "5BB Stack Push Ranges", {
            "EP": self.push_5bb_ep,
            "MP": self.push_5bb_mp,
            "CO": self.push_5bb_co,
            "BTN": self.push_5bb_btn,
            "SB": self.push_5bb_sb,
            "BB": self.push_5bb_bb
        })
        
        # 6-10BB Tab
        frame_6bb = self.create_push_fold_position_frame(tab_6_10bb, "6BB Stack Push Ranges", {
            "EP": self.push_6bb_ep,
            "MP": self.push_6bb_mp,
            "CO": self.push_6bb_co,
            "BTN": self.push_6bb_btn,
            "SB": self.push_6bb_sb,
            "BB": self.push_6bb_bb
        })
        
        frame_7bb = self.create_push_fold_position_frame(tab_6_10bb, "7BB Stack Push Ranges", {
            "EP": self.push_7bb_ep,
            "MP": self.push_7bb_mp,
            "CO": self.push_7bb_co,
            "BTN": self.push_7bb_btn,
            "SB": self.push_7bb_sb,
            "BB": self.push_7bb_bb
        })
        
        frame_8bb = self.create_push_fold_position_frame(tab_6_10bb, "8BB Stack Push Ranges", {
            "EP": self.push_8bb_ep,
            "MP": self.push_8bb_mp,
            "CO": self.push_8bb_co,
            "BTN": self.push_8bb_btn,
            "SB": self.push_8bb_sb,
            "BB": self.push_8bb_bb
        })
        
        frame_9bb = self.create_push_fold_position_frame(tab_6_10bb, "9BB Stack Push Ranges", {
            "EP": self.push_9bb_ep,
            "MP": self.push_9bb_mp,
            "CO": self.push_9bb_co,
            "BTN": self.push_9bb_btn,
            "SB": self.push_9bb_sb,
            "BB": self.push_9bb_bb
        })
        
        frame_10bb = self.create_push_fold_position_frame(tab_6_10bb, "10BB Stack Push Ranges", {
            "EP": self.push_10bb_ep,
            "MP": self.push_10bb_mp,
            "CO": self.push_10bb_co,
            "BTN": self.push_10bb_btn,
            "SB": self.push_10bb_sb,
            "BB": self.push_10bb_bb
        })
        
        # 10-25BB Tab
        frame_10_15bb = self.create_push_fold_position_frame(tab_10_25bb, "10-15BB Stack Push Ranges", {
            "EP": self.push_10_15bb_ep,
            "MP": self.push_10_15bb_mp,
            "CO": self.push_10_15bb_co,
            "BTN": self.push_10_15bb_btn,
            "SB": self.push_10_15bb_sb,
            "BB": self.push_10_15bb_bb
        })
        
        frame_15_20bb = self.create_push_fold_position_frame(tab_10_25bb, "15-20BB Stack Push Ranges", {
            "EP": self.push_15_20bb_ep,
            "MP": self.push_15_20bb_mp,
            "CO": self.push_15_20bb_co,
            "BTN": self.push_15_20bb_btn,
            "SB": self.push_15_20bb_sb,
            "BB": self.push_15_20bb_bb
        })
        
        frame_20_25bb = self.create_push_fold_position_frame(tab_10_25bb, "20-25BB Stack Push Ranges", {
            "EP": self.push_20_25bb_ep,
            "MP": self.push_20_25bb_mp,
            "CO": self.push_20_25bb_co,
            "BTN": self.push_20_25bb_btn,
            "SB": self.push_20_25bb_sb,
            "BB": self.push_20_25bb_bb
        })
        
        # Call Ranges Tab
        frame_call_1bb = self.create_push_fold_call_frame(call_ranges, "1BB Stack Call Ranges", {
            "vs_EP": self.call_1bb_vs_ep,
            "vs_MP": self.call_1bb_vs_mp,
            "vs_CO": self.call_1bb_vs_co,
            "vs_BTN": self.call_1bb_vs_btn,
            "vs_SB": self.call_1bb_vs_sb
        })
        
        frame_call_2bb = self.create_push_fold_call_frame(call_ranges, "2BB Stack Call Ranges", {
            "vs_EP": self.call_2bb_vs_ep,
            "vs_MP": self.call_2bb_vs_mp,
            "vs_CO": self.call_2bb_vs_co,
            "vs_BTN": self.call_2bb_vs_btn,
            "vs_SB": self.call_2bb_vs_sb
        })
        
        frame_call_3bb = self.create_push_fold_call_frame(call_ranges, "3BB Stack Call Ranges", {
            "vs_EP": self.call_3bb_vs_ep,
            "vs_MP": self.call_3bb_vs_mp,
            "vs_CO": self.call_3bb_vs_co,
            "vs_BTN": self.call_3bb_vs_btn,
            "vs_SB": self.call_3bb_vs_sb
        })
        
        frame_call_4bb = self.create_push_fold_call_frame(call_ranges, "4BB Stack Call Ranges", {
            "vs_EP": self.call_4bb_vs_ep,
            "vs_MP": self.call_4bb_vs_mp,
            "vs_CO": self.call_4bb_vs_co,
            "vs_BTN": self.call_4bb_vs_btn,
            "vs_SB": self.call_4bb_vs_sb
        })
        
        frame_call_5bb = self.create_push_fold_call_frame(call_ranges, "5BB Stack Call Ranges", {
            "vs_EP": self.call_5bb_vs_ep,
            "vs_MP": self.call_5bb_vs_mp,
            "vs_CO": self.call_5bb_vs_co,
            "vs_BTN": self.call_5bb_vs_btn,
            "vs_SB": self.call_5bb_vs_sb
        })
        
        frame_call_6_10bb = self.create_push_fold_call_frame(call_ranges, "6-10BB Stack Call Ranges", {
            "vs_EP": self.call_6_10bb_vs_ep,
            "vs_MP": self.call_6_10bb_vs_mp,
            "vs_CO": self.call_6_10bb_vs_co,
            "vs_BTN": self.call_6_10bb_vs_btn,
            "vs_SB": self.call_6_10bb_vs_sb
        })
        
        frame_call_10_15bb = self.create_push_fold_call_frame(call_ranges, "10-15BB Stack Call Ranges", {
            "vs_EP": self.call_10_15bb_vs_ep,
            "vs_MP": self.call_10_15bb_vs_mp,
            "vs_CO": self.call_10_15bb_vs_co,
            "vs_BTN": self.call_10_15bb_vs_btn,
            "vs_SB": self.call_10_15bb_vs_sb
        })
        
        frame_call_15_25bb = self.create_push_fold_call_frame(call_ranges, "15-25BB Stack Call Ranges", {
            "vs_EP": self.call_15_25bb_vs_ep,
            "vs_MP": self.call_15_25bb_vs_mp,
            "vs_CO": self.call_15_25bb_vs_co,
            "vs_BTN": self.call_15_25bb_vs_btn,
            "vs_SB": self.call_15_25bb_vs_sb
        })
        
    def create_push_fold_position_frame(self, parent, title, position_vars):
        """Create a frame with sliders for each position"""
        frame = ttk.LabelFrame(parent, text=title)
        frame.pack(fill="x", padx=10, pady=5)
        
        row = 0
        position_names = {
            "EP": "Early Position", 
            "MP": "Middle Position", 
            "CO": "Cutoff", 
            "BTN": "Button", 
            "SB": "Small Blind", 
            "BB": "Big Blind"
        }
        
        for pos, var in position_vars.items():
            ttk.Label(frame, text=f"{position_names[pos]} (%):").grid(row=row, column=0, padx=5, pady=3, sticky="w")
            ttk.Scale(frame, from_=0, to=100, variable=var, orient="horizontal").grid(row=row, column=1, padx=5, pady=3, sticky="ew")
            ttk.Label(frame, textvariable=var).grid(row=row, column=2, padx=5, pady=3)
            row += 1
        
        frame.columnconfigure(1, weight=1)
        return frame

    def create_flop_tab(self, notebook):
        flop_frame = ttk.Frame(notebook)
        notebook.add(flop_frame, text="Flop Settings")
        
        # C-Bet settings
        cbet_frame = ttk.LabelFrame(flop_frame, text="C-Bet Settings")
        cbet_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(cbet_frame, text="IP C-Bet Frequency (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(cbet_frame, from_=0, to=100, variable=self.ip_cbet_freq, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(cbet_frame, textvariable=self.ip_cbet_freq).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(cbet_frame, text="OOP C-Bet Frequency (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(cbet_frame, from_=0, to=100, variable=self.oop_cbet_freq, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(cbet_frame, textvariable=self.oop_cbet_freq).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(cbet_frame, text="IP C-Bet Size (% of pot):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Combobox(cbet_frame, textvariable=self.ip_cbet_size, values=["33", "50", "66", "75", "100"], 
                  width=5, state="readonly").grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(cbet_frame, text="OOP C-Bet Size (% of pot):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Combobox(cbet_frame, textvariable=self.oop_cbet_size, values=["33", "50", "66", "75", "100"], 
                  width=5, state="readonly").grid(row=3, column=1, padx=5, pady=5)
        
        # Board texture adjustments
        texture_frame = ttk.LabelFrame(flop_frame, text="Board Texture Adjustments")
        texture_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(texture_frame, text="Dry Board Adjustment (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(texture_frame, from_=-50, to=50, variable=self.dry_board_adjust, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(texture_frame, textvariable=self.dry_board_adjust).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(texture_frame, text="Wet Board Adjustment (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(texture_frame, from_=-50, to=50, variable=self.wet_board_adjust, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(texture_frame, textvariable=self.wet_board_adjust).grid(row=1, column=2, padx=5, pady=5)
        
        # Facing bets
        facing_frame = ttk.LabelFrame(flop_frame, text="Facing Bets")
        facing_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(facing_frame, text="Check-Raise Defense (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(facing_frame, from_=0, to=100, variable=self.checkraise_defense, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(facing_frame, textvariable=self.checkraise_defense).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(facing_frame, text="Donk Bet Response Style:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Combobox(facing_frame, textvariable=self.donk_response, values=["Fold/Call", "Call/Raise", "Aggressive"], 
                  width=12, state="readonly").grid(row=1, column=1, padx=5, pady=5)
        
        # Hand ranges
        ranges_frame = ttk.LabelFrame(flop_frame, text="Hand Ranges")
        ranges_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(ranges_frame, text="Value Hands Aggression (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(ranges_frame, from_=0, to=100, variable=self.value_aggression, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(ranges_frame, textvariable=self.value_aggression).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(ranges_frame, text="Draw Hands Aggression (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(ranges_frame, from_=0, to=100, variable=self.draw_aggression, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(ranges_frame, textvariable=self.draw_aggression).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(ranges_frame, text="Semi-Bluff Frequency (%):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(ranges_frame, from_=0, to=100, variable=self.semibluff_freq, orient="horizontal").grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(ranges_frame, textvariable=self.semibluff_freq).grid(row=2, column=2, padx=5, pady=5)
        
        # Multiway pots (suite)
        multiway_frame = ttk.LabelFrame(flop_frame, text="Multiway Pots")
        multiway_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(multiway_frame, text="Multiway C-Bet Frequency (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(multiway_frame, from_=0, to=100, variable=self.multiway_cbet_freq, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(multiway_frame, textvariable=self.multiway_cbet_freq).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(multiway_frame, text="Multiway Value Range (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(multiway_frame, from_=0, to=100, variable=self.multiway_value_range, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(multiway_frame, textvariable=self.multiway_value_range).grid(row=1, column=2, padx=5, pady=5)
        
        # Make columns expandable
        for frame in [cbet_frame, texture_frame, facing_frame, ranges_frame, multiway_frame]:
            frame.columnconfigure(1, weight=1)

    def create_turn_tab(self, notebook):
        turn_frame = ttk.Frame(notebook)
        notebook.add(turn_frame, text="Turn Settings")
        
        # Second Barrel settings
        second_barrel_frame = ttk.LabelFrame(turn_frame, text="Second Barrel Settings")
        second_barrel_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(second_barrel_frame, text="Second Barrel Frequency (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(second_barrel_frame, from_=0, to=100, variable=self.second_barrel_freq, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(second_barrel_frame, textvariable=self.second_barrel_freq).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(second_barrel_frame, text="Delayed C-Bet Frequency (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(second_barrel_frame, from_=0, to=100, variable=self.delayed_cbet_freq, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(second_barrel_frame, textvariable=self.delayed_cbet_freq).grid(row=1, column=2, padx=5, pady=5)
        
    def create_push_fold_call_frame(self, parent, title, position_vars):
        """Create a frame with sliders for calling each position"""
        frame = ttk.LabelFrame(parent, text=title)
        frame.pack(fill="x", padx=10, pady=5)
        
        row = 0
        position_names = {
            "vs_EP": "vs Early Position", 
            "vs_MP": "vs Middle Position", 
            "vs_CO": "vs Cutoff", 
            "vs_BTN": "vs Button", 
            "vs_SB": "vs Small Blind"
        }
        
        for pos, var in position_vars.items():
            ttk.Label(frame, text=f"{position_names[pos]} (%):").grid(row=row, column=0, padx=5, pady=3, sticky="w")
            ttk.Scale(frame, from_=0, to=100, variable=var, orient="horizontal").grid(row=row, column=1, padx=5, pady=3, sticky="ew")
            ttk.Label(frame, textvariable=var).grid(row=row, column=2, padx=5, pady=3)
            row += 1
        
        frame.columnconfigure(1, weight=1)
        return frame

    def create_flop_tab(self, notebook):
        flop_frame = ttk.Frame(notebook)
        notebook.add(flop_frame, text="Flop Settings")
        
        # C-Bet settings
        cbet_frame = ttk.LabelFrame(flop_frame, text="C-Bet Settings")
        cbet_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(cbet_frame, text="IP C-Bet Frequency (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(cbet_frame, from_=0, to=100, variable=self.ip_cbet_freq, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(cbet_frame, textvariable=self.ip_cbet_freq).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(cbet_frame, text="OOP C-Bet Frequency (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(cbet_frame, from_=0, to=100, variable=self.oop_cbet_freq, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(cbet_frame, textvariable=self.oop_cbet_freq).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(cbet_frame, text="IP C-Bet Size (% of pot):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Combobox(cbet_frame, textvariable=self.ip_cbet_size, values=["33", "50", "66", "75", "100"], 
                  width=5, state="readonly").grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(cbet_frame, text="OOP C-Bet Size (% of pot):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Combobox(cbet_frame, textvariable=self.oop_cbet_size, values=["33", "50", "66", "75", "100"], 
                  width=5, state="readonly").grid(row=3, column=1, padx=5, pady=5)
        
        # Board texture adjustments
        texture_frame = ttk.LabelFrame(flop_frame, text="Board Texture Adjustments")
        texture_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(texture_frame, text="Dry Board Adjustment (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(texture_frame, from_=-50, to=50, variable=self.dry_board_adjust, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(texture_frame, textvariable=self.dry_board_adjust).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(texture_frame, text="Wet Board Adjustment (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(texture_frame, from_=-50, to=50, variable=self.wet_board_adjust, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(texture_frame, textvariable=self.wet_board_adjust).grid(row=1, column=2, padx=5, pady=5)
        
        # Facing bets
        facing_frame = ttk.LabelFrame(flop_frame, text="Facing Bets")
        facing_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(facing_frame, text="Check-Raise Defense (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(facing_frame, from_=0, to=100, variable=self.checkraise_defense, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(facing_frame, textvariable=self.checkraise_defense).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(facing_frame, text="Donk Bet Response Style:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Combobox(facing_frame, textvariable=self.donk_response, values=["Fold/Call", "Call/Raise", "Aggressive"], 
                  width=12, state="readonly").grid(row=1, column=1, padx=5, pady=5)
        
        # Hand ranges
        ranges_frame = ttk.LabelFrame(flop_frame, text="Hand Ranges")
        ranges_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(ranges_frame, text="Value Hands Aggression (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(ranges_frame, from_=0, to=100, variable=self.value_aggression, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(ranges_frame, textvariable=self.value_aggression).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(ranges_frame, text="Draw Hands Aggression (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(ranges_frame, from_=0, to=100, variable=self.draw_aggression, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(ranges_frame, textvariable=self.draw_aggression).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(ranges_frame, text="Semi-Bluff Frequency (%):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(ranges_frame, from_=0, to=100, variable=self.semibluff_freq, orient="horizontal").grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(ranges_frame, textvariable=self.semibluff_freq).grid(row=2, column=2, padx=5, pady=5)
        
        # Multiway pots (suite)
        multiway_frame = ttk.LabelFrame(flop_frame, text="Multiway Pots")
        multiway_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(multiway_frame, text="Multiway C-Bet Frequency (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(multiway_frame, from_=0, to=100, variable=self.multiway_cbet_freq, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(multiway_frame, textvariable=self.multiway_cbet_freq).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(multiway_frame, text="Multiway Value Range (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(multiway_frame, from_=0, to=100, variable=self.multiway_value_range, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(multiway_frame, textvariable=self.multiway_value_range).grid(row=1, column=2, padx=5, pady=5)
        
        # Make columns expandable
        for frame in [cbet_frame, texture_frame, facing_frame, ranges_frame, multiway_frame]:
            frame.columnconfigure(1, weight=1)

    def create_turn_tab(self, notebook):
        turn_frame = ttk.Frame(notebook)
        notebook.add(turn_frame, text="Turn Settings")
        
        # Second Barrel settings
        second_barrel_frame = ttk.LabelFrame(turn_frame, text="Second Barrel Settings")
        second_barrel_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(second_barrel_frame, text="Second Barrel Frequency (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(second_barrel_frame, from_=0, to=100, variable=self.second_barrel_freq, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(second_barrel_frame, textvariable=self.second_barrel_freq).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(second_barrel_frame, text="Delayed C-Bet Frequency (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(second_barrel_frame, from_=0, to=100, variable=self.delayed_cbet_freq, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(second_barrel_frame, textvariable=self.delayed_cbet_freq).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(second_barrel_frame, text="IP Turn Bet Size (% of pot):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Combobox(second_barrel_frame, textvariable=self.ip_turn_bet_size, values=["50", "66", "75", "100"], 
                  width=5, state="readonly").grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(second_barrel_frame, text="OOP Turn Bet Size (% of pot):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Combobox(second_barrel_frame, textvariable=self.oop_turn_bet_size, values=["50", "66", "75", "100"], 
                  width=5, state="readonly").grid(row=3, column=1, padx=5, pady=5)
        
        # Turn Card adjustments
        turn_card_frame = ttk.LabelFrame(turn_frame, text="Turn Card Adjustments")
        turn_card_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(turn_card_frame, text="Scare Card Adjustment (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(turn_card_frame, from_=-50, to=50, variable=self.scare_card_adjust, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(turn_card_frame, textvariable=self.scare_card_adjust).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(turn_card_frame, text="Draw Complete Adjustment (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(turn_card_frame, from_=-50, to=50, variable=self.draw_complete_adjust, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(turn_card_frame, textvariable=self.draw_complete_adjust).grid(row=1, column=2, padx=5, pady=5)
        
        # Facing Turn bets
        facing_turn_frame = ttk.LabelFrame(turn_frame, text="Facing Turn Bets")
        facing_turn_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(facing_turn_frame, text="Turn Check-Raise Frequency (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(facing_turn_frame, from_=0, to=100, variable=self.turn_checkraise_freq, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(facing_turn_frame, textvariable=self.turn_checkraise_freq).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(facing_turn_frame, text="Turn Float Frequency (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(facing_turn_frame, from_=0, to=100, variable=self.turn_float_freq, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(facing_turn_frame, textvariable=self.turn_float_freq).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(facing_turn_frame, text="Turn Fold to C-Bet Frequency (%):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(facing_turn_frame, from_=0, to=100, variable=self.turn_fold_to_cbet_freq, orient="horizontal").grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(facing_turn_frame, textvariable=self.turn_fold_to_cbet_freq).grid(row=2, column=2, padx=5, pady=5)
        
        # Probe betting
        probe_frame = ttk.LabelFrame(turn_frame, text="Probe Betting")
        probe_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(probe_frame, text="Turn Probe Frequency (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(probe_frame, from_=0, to=100, variable=self.turn_probe_freq, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(probe_frame, textvariable=self.turn_probe_freq).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(probe_frame, text="Turn Bluff Raise Frequency (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(probe_frame, from_=0, to=100, variable=self.turn_bluff_raise_freq, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(probe_frame, textvariable=self.turn_bluff_raise_freq).grid(row=1, column=2, padx=5, pady=5)
        
        # Make columns expandable
        for frame in [second_barrel_frame, turn_card_frame, facing_turn_frame, probe_frame]:
            frame.columnconfigure(1, weight=1)
    
    def create_river_tab(self, notebook):
        river_frame = ttk.Frame(notebook)
        notebook.add(river_frame, text="River Settings")
        
        # Third Barrel settings
        barrel_frame = ttk.LabelFrame(river_frame, text="Third Barrel Settings")
        barrel_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(barrel_frame, text="Third Barrel Frequency (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(barrel_frame, from_=0, to=100, variable=self.third_barrel_freq, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(barrel_frame, textvariable=self.third_barrel_freq).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(barrel_frame, text="Delayed Second Barrel Frequency (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(barrel_frame, from_=0, to=100, variable=self.delayed_second_barrel_freq, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(barrel_frame, textvariable=self.delayed_second_barrel_freq).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(barrel_frame, text="IP River Bet Size (% of pot):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Combobox(barrel_frame, textvariable=self.ip_river_bet_size, values=["50", "66", "75", "100"], 
                  width=5, state="readonly").grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(barrel_frame, text="OOP River Bet Size (% of pot):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Combobox(barrel_frame, textvariable=self.oop_river_bet_size, values=["50", "66", "75", "100"], 
                  width=5, state="readonly").grid(row=3, column=1, padx=5, pady=5)
        
        # Facing River bets
        facing_river_frame = ttk.LabelFrame(river_frame, text="Facing River Bets")
        facing_river_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(facing_river_frame, text="River Check-Raise Frequency (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(facing_river_frame, from_=0, to=100, variable=self.river_checkraise_freq, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(facing_river_frame, textvariable=self.river_checkraise_freq).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(facing_river_frame, text="River Float Frequency (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(facing_river_frame, from_=0, to=100, variable=self.river_float_freq, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(facing_river_frame, textvariable=self.river_float_freq).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(facing_river_frame, text="River Fold to Bet Frequency (%):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(facing_river_frame, from_=0, to=100, variable=self.river_fold_to_bet_freq, orient="horizontal").grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(facing_river_frame, textvariable=self.river_fold_to_bet_freq).grid(row=2, column=2, padx=5, pady=5)
        
        ttk.Label(facing_river_frame, text="River Bluff Raise Frequency (%):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(facing_river_frame, from_=0, to=100, variable=self.river_bluff_raise_freq, orient="horizontal").grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(facing_river_frame, textvariable=self.river_bluff_raise_freq).grid(row=3, column=2, padx=5, pady=5)
        
        # River Hand Ranges
        river_ranges_frame = ttk.LabelFrame(river_frame, text="River Hand Ranges")
        river_ranges_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(river_ranges_frame, text="River Value Range (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(river_ranges_frame, from_=0, to=100, variable=self.river_value_range, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(river_ranges_frame, textvariable=self.river_value_range).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(river_ranges_frame, text="River Bluff Range (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(river_ranges_frame, from_=0, to=100, variable=self.river_bluff_range, orient="horizontal").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(river_ranges_frame, textvariable=self.river_bluff_range).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(river_ranges_frame, text="River Check Behind Range (%):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(river_ranges_frame, from_=0, to=100, variable=self.river_check_behind_range, orient="horizontal").grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(river_ranges_frame, textvariable=self.river_check_behind_range).grid(row=2, column=2, padx=5, pady=5)
        
        # Probe betting (River)
        river_probe_frame = ttk.LabelFrame(river_frame, text="River Probe Betting")
        river_probe_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(river_probe_frame, text="River Probe Frequency (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Scale(river_probe_frame, from_=0, to=100, variable=self.river_probe_freq, orient="horizontal").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(river_probe_frame, textvariable=self.river_probe_freq).grid(row=0, column=2, padx=5, pady=5)
        
        # Make columns expandable
        for frame in [barrel_frame, facing_river_frame, river_ranges_frame, river_probe_frame]:
            frame.columnconfigure(1, weight=1)
            
    def collect_preflop_settings(self):
        """Gather all preflop settings from the UI into a dictionary"""
        return {
            "num_players": self.num_players.get(),
            "game_type": self.game_type.get(),
            "aggression": self.aggression.get(),
            "tightness": self.tightness.get(),
            "limp_frequency": self.limp_frequency.get(),
            "threebet_frequency": self.threebet_frequency.get(),
            "fourbet_frequency": self.fourbet_frequency.get(),
            "squeeze_frequency": self.squeeze_frequency.get(),
            "open_raise_size": self.open_raise_var.get(),
            "ep_range": self.ep_range.get(),
            "mp_range": self.mp_range.get(),
            "lp_range": self.lp_range.get(),
            "ep_sizing": self.ep_sizing.get(),
            "mp_sizing": self.mp_sizing.get(),
            "lp_sizing": self.lp_sizing.get(),
            "call_3bet_range": self.call_3bet_range.get(),
            "fourbet_range": self.fourbet_range.get(),
            "ip_3bet_adjust": self.ip_3bet_adjust.get(),
            "vs_lp_3bet_adjust": self.vs_lp_3bet_adjust.get(),
            "call_4bet_range": self.call_4bet_range.get(),
            "fivebet_range": self.fivebet_range.get(),
            "short_stack_4bet": self.short_stack_4bet.get(),
            "squeeze_1caller": self.squeeze_1caller.get(),
            "squeeze_multi": self.squeeze_multi.get(),
            "squeeze_sizing": self.squeeze_sizing.get(),
            "blinds_squeeze": self.blinds_squeeze.get(),
            "btn_squeeze": self.btn_squeeze.get(),
            **self.collect_push_fold_settings()
        }
    
    def collect_flop_settings(self):
        """Gather all flop settings from the UI into a dictionary"""
        return {
            "ip_cbet_freq": self.ip_cbet_freq.get(),
            "oop_cbet_freq": self.oop_cbet_freq.get(),
            "ip_cbet_size": self.ip_cbet_size.get(),
            "oop_cbet_size": self.oop_cbet_size.get(),
            "dry_board_adjust": self.dry_board_adjust.get(),
            "wet_board_adjust": self.wet_board_adjust.get(), 
            "checkraise_defense": self.checkraise_defense.get(),
            "donk_response": self.donk_response.get(),
            "value_aggression": self.value_aggression.get(),
            "draw_aggression": self.draw_aggression.get(),
            "semibluff_freq": self.semibluff_freq.get(),
            "multiway_cbet_freq": self.multiway_cbet_freq.get(),
            "multiway_value_range": self.multiway_value_range.get(),
            "aggression": self.aggression.get()  # Including global aggression for adjustments
        }
    
    def collect_turn_settings(self):
        """Gather all turn settings from the UI into a dictionary"""
        return {
            "second_barrel_freq": self.second_barrel_freq.get(),
            "delayed_cbet_freq": self.delayed_cbet_freq.get(),
            "ip_turn_bet_size": self.ip_turn_bet_size.get(),
            "oop_turn_bet_size": self.oop_turn_bet_size.get(),
            "turn_checkraise_freq": self.turn_checkraise_freq.get(),
            "turn_float_freq": self.turn_float_freq.get(),
            "turn_probe_freq": self.turn_probe_freq.get(),
            "turn_fold_to_cbet_freq": self.turn_fold_to_cbet_freq.get(),
            "turn_bluff_raise_freq": self.turn_bluff_raise_freq.get(),
            "scare_card_adjust": self.scare_card_adjust.get(),
            "draw_complete_adjust": self.draw_complete_adjust.get(),
            "aggression": self.aggression.get()  # Including global aggression for adjustments
        }
    
    def collect_river_settings(self):
        """Gather all river settings from the UI into a dictionary"""
        return {
            "third_barrel_freq": self.third_barrel_freq.get(),
            "delayed_second_barrel_freq": self.delayed_second_barrel_freq.get(),
            "ip_river_bet_size": self.ip_river_bet_size.get(),
            "oop_river_bet_size": self.oop_river_bet_size.get(),
            "river_checkraise_freq": self.river_checkraise_freq.get(),
            "river_float_freq": self.river_float_freq.get(),
            "river_probe_freq": self.river_probe_freq.get(),
            "river_fold_to_bet_freq": self.river_fold_to_bet_freq.get(),
            "river_bluff_raise_freq": self.river_bluff_raise_freq.get(),
            "river_value_range": self.river_value_range.get(),
            "river_bluff_range": self.river_bluff_range.get(),
            "river_check_behind_range": self.river_check_behind_range.get(),
            "aggression": self.aggression.get()  # Including global aggression for adjustments
        }
        
    def collect_push_fold_settings(self):
        """Collect all push/fold settings"""
        # Define all push/fold variables that should be collected
        push_fold_vars = {
            # 1BB stack ranges
            "push_1bb_ep": self.push_1bb_ep.get(),
            "push_1bb_mp": self.push_1bb_mp.get(),
            "push_1bb_co": self.push_1bb_co.get(),
            "push_1bb_btn": self.push_1bb_btn.get(),
            "push_1bb_sb": self.push_1bb_sb.get(),
            "push_1bb_bb": self.push_1bb_bb.get(),
            "call_1bb_vs_ep": self.call_1bb_vs_ep.get(),
            "call_1bb_vs_mp": self.call_1bb_vs_mp.get(),
            "call_1bb_vs_co": self.call_1bb_vs_co.get(),
            "call_1bb_vs_btn": self.call_1bb_vs_btn.get(),
            "call_1bb_vs_sb": self.call_1bb_vs_sb.get(),
            
            # 2BB-5BB stack ranges
            "push_2bb_ep": self.push_2bb_ep.get(),
            "push_2bb_mp": self.push_2bb_mp.get(),
            "push_2bb_co": self.push_2bb_co.get(),
            "push_2bb_btn": self.push_2bb_btn.get(),
            "push_2bb_sb": self.push_2bb_sb.get(),
            "push_2bb_bb": self.push_2bb_bb.get(),
            
            "push_3bb_ep": self.push_3bb_ep.get(),
            "push_3bb_mp": self.push_3bb_mp.get(),
            "push_3bb_co": self.push_3bb_co.get(),
            "push_3bb_btn": self.push_3bb_btn.get(),
            "push_3bb_sb": self.push_3bb_sb.get(),
            "push_3bb_bb": self.push_3bb_bb.get(),
            
            "push_4bb_ep": self.push_4bb_ep.get(),
            "push_4bb_mp": self.push_4bb_mp.get(),
            "push_4bb_co": self.push_4bb_co.get(),
            "push_4bb_btn": self.push_4bb_btn.get(),
            "push_4bb_sb": self.push_4bb_sb.get(),
            "push_4bb_bb": self.push_4bb_bb.get(),
            
            "push_5bb_ep": self.push_5bb_ep.get(),
            "push_5bb_mp": self.push_5bb_mp.get(),
            "push_5bb_co": self.push_5bb_co.get(),
            "push_5bb_btn": self.push_5bb_btn.get(),
            "push_5bb_sb": self.push_5bb_sb.get(),
            "push_5bb_bb": self.push_5bb_bb.get(),
            
            # 6BB-10BB stack ranges
            "push_6bb_ep": self.push_6bb_ep.get(),
            "push_6bb_mp": self.push_6bb_mp.get(),
            "push_6bb_co": self.push_6bb_co.get(),
            "push_6bb_btn": self.push_6bb_btn.get(),
            "push_6bb_sb": self.push_6bb_sb.get(),
            "push_6bb_bb": self.push_6bb_bb.get(),
            
            "push_7bb_ep": self.push_7bb_ep.get(),
            "push_7bb_mp": self.push_7bb_mp.get(),
            "push_7bb_co": self.push_7bb_co.get(),
            "push_7bb_btn": self.push_7bb_btn.get(),
            "push_7bb_sb": self.push_7bb_sb.get(),
            "push_7bb_bb": self.push_7bb_bb.get(),
            
            "push_8bb_ep": self.push_8bb_ep.get(),
            "push_8bb_mp": self.push_8bb_mp.get(),
            "push_8bb_co": self.push_8bb_co.get(),
            "push_8bb_btn": self.push_8bb_btn.get(),
            "push_8bb_sb": self.push_8bb_sb.get(),
            "push_8bb_bb": self.push_8bb_bb.get(),
            
            "push_9bb_ep": self.push_9bb_ep.get(),
            "push_9bb_mp": self.push_9bb_mp.get(),
            "push_9bb_co": self.push_9bb_co.get(),
            "push_9bb_btn": self.push_9bb_btn.get(),
            "push_9bb_sb": self.push_9bb_sb.get(),
            "push_9bb_bb": self.push_9bb_bb.get(),
            
            "push_10bb_ep": self.push_10bb_ep.get(),
            "push_10bb_mp": self.push_10bb_mp.get(),
            "push_10bb_co": self.push_10bb_co.get(),
            "push_10bb_btn": self.push_10bb_btn.get(),
            "push_10bb_sb": self.push_10bb_sb.get(),
            "push_10bb_bb": self.push_10bb_bb.get(),
            
            # 2BB-10BB call ranges
            "call_2bb_vs_ep": self.call_2bb_vs_ep.get(),
            "call_2bb_vs_mp": self.call_2bb_vs_mp.get(),
            "call_2bb_vs_co": self.call_2bb_vs_co.get(),
            "call_2bb_vs_btn": self.call_2bb_vs_btn.get(),
            "call_2bb_vs_sb": self.call_2bb_vs_sb.get(),
            
            "call_3bb_vs_ep": self.call_3bb_vs_ep.get(),
            "call_3bb_vs_mp": self.call_3bb_vs_mp.get(),
            "call_3bb_vs_co": self.call_3bb_vs_co.get(),
            "call_3bb_vs_btn": self.call_3bb_vs_btn.get(),
            "call_3bb_vs_sb": self.call_3bb_vs_sb.get(),
            
            "call_4bb_vs_ep": self.call_4bb_vs_ep.get(),
            "call_4bb_vs_mp": self.call_4bb_vs_mp.get(),
            "call_4bb_vs_co": self.call_4bb_vs_co.get(),
            "call_4bb_vs_btn": self.call_4bb_vs_btn.get(),
            "call_4bb_vs_sb": self.call_4bb_vs_sb.get(),
            
            "call_5bb_vs_ep": self.call_5bb_vs_ep.get(),
            "call_5bb_vs_mp": self.call_5bb_vs_mp.get(),
            "call_5bb_vs_co": self.call_5bb_vs_co.get(),
            "call_5bb_vs_btn": self.call_5bb_vs_btn.get(),
            "call_5bb_vs_sb": self.call_5bb_vs_sb.get(),
            
            "call_6_10bb_vs_ep": self.call_6_10bb_vs_ep.get(),
            "call_6_10bb_vs_mp": self.call_6_10bb_vs_mp.get(),
            "call_6_10bb_vs_co": self.call_6_10bb_vs_co.get(),
            "call_6_10bb_vs_btn": self.call_6_10bb_vs_btn.get(),
            "call_6_10bb_vs_sb": self.call_6_10bb_vs_sb.get(),
            
            # 10BB+ stack ranges
            "push_10_15bb_ep": self.push_10_15bb_ep.get(),
            "push_10_15bb_mp": self.push_10_15bb_mp.get(),
            "push_10_15bb_co": self.push_10_15bb_co.get(),
            "push_10_15bb_btn": self.push_10_15bb_btn.get(),
            "push_10_15bb_sb": self.push_10_15bb_sb.get(),
            "push_10_15bb_bb": self.push_10_15bb_bb.get(),
            
            "push_15_20bb_ep": self.push_15_20bb_ep.get(),
            "push_15_20bb_mp": self.push_15_20bb_mp.get(),
            "push_15_20bb_co": self.push_15_20bb_co.get(),
            "push_15_20bb_btn": self.push_15_20bb_btn.get(),
            "push_15_20bb_sb": self.push_15_20bb_sb.get(),
            "push_15_20bb_bb": self.push_15_20bb_bb.get(),
            
            "push_20_25bb_ep": self.push_20_25bb_ep.get(),
            "push_20_25bb_mp": self.push_20_25bb_mp.get(),
            "push_20_25bb_co": self.push_20_25bb_co.get(),
            "push_20_25bb_btn": self.push_20_25bb_btn.get(),
            "push_20_25bb_sb": self.push_20_25bb_sb.get(),
            "push_20_25bb_bb": self.push_20_25bb_bb.get(),
            
            # 10BB+ call ranges
            "call_10_15bb_vs_ep": self.call_10_15bb_vs_ep.get(),
            "call_10_15bb_vs_mp": self.call_10_15bb_vs_mp.get(),
            "call_10_15bb_vs_co": self.call_10_15bb_vs_co.get(),
            "call_10_15bb_vs_btn": self.call_10_15bb_vs_btn.get(),
            "call_10_15bb_vs_sb": self.call_10_15bb_vs_sb.get(),
            
            "call_15_25bb_vs_ep": self.call_15_25bb_vs_ep.get(),
            "call_15_25bb_vs_mp": self.call_15_25bb_vs_mp.get(),
            "call_15_25bb_vs_co": self.call_15_25bb_vs_co.get(),
            "call_15_25bb_vs_btn": self.call_15_25bb_vs_btn.get(),
            "call_15_25bb_vs_sb": self.call_15_25bb_vs_sb.get()
        }
        
        return push_fold_vars
    
    def generate_profile(self):
        # Get all settings from UI
        preflop_settings = self.collect_preflop_settings()
        flop_settings = self.collect_flop_settings()
        turn_settings = self.collect_turn_settings()
        river_settings = self.collect_river_settings()
        
        # Generate profile using the generators
        preflop_profile = self.preflop_generator.generate_preflop_profile(preflop_settings)
        flop_profile = self.flop_generator.generate_flop_profile(flop_settings)
        turn_profile = self.turn_generator.generate_turn_profile(turn_settings)
        river_profile = self.river_generator.generate_river_profile(river_settings)
        
        # Combine the profiles
        full_profile = preflop_profile + "\n\n" + flop_profile + "\n\n" + turn_profile + "\n\n" + river_profile
        
        # Display in preview
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, full_profile)
        
        messagebox.showinfo("Profile Generated", "OpenHoldem profile has been generated and is ready to save.")
        
    def save_profile(self):
        if not self.preview_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Empty Profile", "Please generate a profile first.")
            return
            
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".ohf",
            filetypes=[("OpenHoldem Files", "*.ohf"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.preview_text.get(1.0, tk.END))
            messagebox.showinfo("Save Successful", f"Profile saved to {file_path}")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = OpenHoldemProfileGenerator(root)
        root.mainloop()
    except Exception as e:
        import traceback
        print(f"Une erreur s'est produite: {e}")
        print(traceback.format_exc())
        input("Appuyez sur Entrée pour quitter...")
        
        
