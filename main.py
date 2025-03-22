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
        self.root.geometry("900x700")
        self.root.minsize(900, 700)
        
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
        
        # Create the generators
        self.preflop_generator = PreflopProfileGenerator()
        self.flop_generator = FlopProfileGenerator()
        self.turn_generator = TurnProfileGenerator()
        self.river_generator = RiverProfileGenerator()
        
        # Setup the UI
        self.create_ui()
    
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
        
        # Additional tabs for future expansion
        facing3bet_frame = ttk.Frame(notebook)
        notebook.add(facing3bet_frame, text="Facing 3-Bet")
        
        facing4bet_frame = ttk.Frame(notebook)
        notebook.add(facing4bet_frame, text="Facing 4-Bet")
        
        squeeze_frame = ttk.Frame(notebook)
        notebook.add(squeeze_frame, text="Squeeze")
    
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
            "btn_squeeze": self.btn_squeeze.get()
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
    root = tk.Tk()
    app = OpenHoldemProfileGenerator(root)
    root.mainloop()
