import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from preflop_generator import PreflopProfileGenerator

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
        
        # Create the PreflopProfileGenerator
        self.preflop_generator = PreflopProfileGenerator()
        
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
        # These will be filled with more detailed options in the complete version
        openraise_frame = ttk.Frame(notebook)
        notebook.add(openraise_frame, text="Open Raise")
        
        facing3bet_frame = ttk.Frame(notebook)
        notebook.add(facing3bet_frame, text="Facing 3-Bet")
        
        facing4bet_frame = ttk.Frame(notebook)
        notebook.add(facing4bet_frame, text="Facing 4-Bet")
        
        squeeze_frame = ttk.Frame(notebook)
        notebook.add(squeeze_frame, text="Squeeze")
    
    def collect_settings(self):
        """Gather all settings from the UI into a dictionary"""
        return {
            "num_players": self.num_players.get(),
            "game_type": self.game_type.get(),
            "aggression": self.aggression.get(),
            "tightness": self.tightness.get(),
            "limp_frequency": self.limp_frequency.get(),
            "threebet_frequency": self.threebet_frequency.get(),
            "fourbet_frequency": self.fourbet_frequency.get(),
            "squeeze_frequency": self.squeeze_frequency.get(),
            "open_raise_size": self.open_raise_var.get()
        }
    
    def generate_profile(self):
        # Get all settings from UI
        settings = self.collect_settings()
        
        # Generate profile using the preflop generator
        profile = self.preflop_generator.generate_preflop_profile(settings)
        
        # Display in preview
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, profile)
        
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
