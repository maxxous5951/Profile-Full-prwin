import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QSlider, QComboBox, QPushButton, QTextEdit, 
                           QFrame, QFileDialog, QMessageBox, QScrollArea, QGridLayout, QGroupBox)
from PyQt6.QtCore import Qt
import os
from preflop_generator import PreflopProfileGenerator
from flop_generator import FlopProfileGenerator
from turn_generator import TurnProfileGenerator
from river_generator import RiverProfileGenerator

class OpenHoldemProfileGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenHoldem Profile Generator")
        self.setMinimumSize(1000, 800)
        
        # Configuration variables
        self.num_players = 9
        self.game_type = "Cash Game"
        
        # Flop variables
        self.ip_cbet_freq = 70
        self.oop_cbet_freq = 60
        self.ip_cbet_size = "50"
        self.oop_cbet_size = "66"
        self.dry_board_adjust = 20
        self.wet_board_adjust = -20
        self.checkraise_defense = 35
        self.donk_response = "Call/Raise"
        self.value_aggression = 80
        self.draw_aggression = 60
        self.semibluff_freq = 65
        self.multiway_cbet_freq = 40
        self.multiway_value_range = 25
        
        # Turn variables
        self.second_barrel_freq = 60
        self.delayed_cbet_freq = 40
        self.ip_turn_bet_size = "66"
        self.oop_turn_bet_size = "75"
        self.turn_checkraise_freq = 25
        self.turn_float_freq = 30
        self.turn_probe_freq = 35
        self.turn_fold_to_cbet_freq = 60
        self.turn_bluff_raise_freq = 20
        self.scare_card_adjust = -15
        self.draw_complete_adjust = 10
        
        # River variables
        self.third_barrel_freq = 40
        self.delayed_second_barrel_freq = 30
        self.ip_river_bet_size = "75"
        self.oop_river_bet_size = "75"
        self.river_checkraise_freq = 15
        self.river_float_freq = 20
        self.river_probe_freq = 25
        self.river_fold_to_bet_freq = 70
        self.river_bluff_raise_freq = 10
        self.river_value_range = 60
        self.river_bluff_range = 15
        self.river_check_behind_range = 80
        
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
        self.push_1bb_ep = 75
        self.push_1bb_mp = 80
        self.push_1bb_co = 85
        self.push_1bb_btn = 90
        self.push_1bb_sb = 92
        self.push_1bb_bb = 95
        self.call_1bb_vs_ep = 60
        self.call_1bb_vs_mp = 65
        self.call_1bb_vs_co = 70
        self.call_1bb_vs_btn = 75
        self.call_1bb_vs_sb = 80
        
        # 2BB-5BB stack ranges
        self.push_2bb_ep = 60
        self.push_2bb_mp = 65
        self.push_2bb_co = 70
        self.push_2bb_btn = 75
        self.push_2bb_sb = 80
        self.push_2bb_bb = 85
        
        self.push_3bb_ep = 45
        self.push_3bb_mp = 50
        self.push_3bb_co = 55
        self.push_3bb_btn = 60
        self.push_3bb_sb = 65
        self.push_3bb_bb = 70
        
        self.push_4bb_ep = 35
        self.push_4bb_mp = 40
        self.push_4bb_co = 45
        self.push_4bb_btn = 50
        self.push_4bb_sb = 55
        self.push_4bb_bb = 60
        
        self.push_5bb_ep = 28
        self.push_5bb_mp = 32
        self.push_5bb_co = 36
        self.push_5bb_btn = 40
        self.push_5bb_sb = 45
        self.push_5bb_bb = 50
        
        # 6BB-10BB stack ranges
        self.push_6bb_ep = 22
        self.push_6bb_mp = 26
        self.push_6bb_co = 30
        self.push_6bb_btn = 35
        self.push_6bb_sb = 40
        self.push_6bb_bb = 45
        
        self.push_7bb_ep = 18
        self.push_7bb_mp = 22
        self.push_7bb_co = 26
        self.push_7bb_btn = 30
        self.push_7bb_sb = 35
        self.push_7bb_bb = 40
        
        self.push_8bb_ep = 15
        self.push_8bb_mp = 18
        self.push_8bb_co = 22
        self.push_8bb_btn = 26
        self.push_8bb_sb = 30
        self.push_8bb_bb = 35
        
        self.push_9bb_ep = 12
        self.push_9bb_mp = 15
        self.push_9bb_co = 18
        self.push_9bb_btn = 22
        self.push_9bb_sb = 26
        self.push_9bb_bb = 30
        
        self.push_10bb_ep = 10
        self.push_10bb_mp = 12
        self.push_10bb_co = 15
        self.push_10bb_btn = 18
        self.push_10bb_sb = 22
        self.push_10bb_bb = 25
        
        # 2BB-10BB call ranges
        self.call_2bb_vs_ep = 50
        self.call_2bb_vs_mp = 55
        self.call_2bb_vs_co = 60
        self.call_2bb_vs_btn = 65
        self.call_2bb_vs_sb = 70
        
        self.call_3bb_vs_ep = 40
        self.call_3bb_vs_mp = 45
        self.call_3bb_vs_co = 50
        self.call_3bb_vs_btn = 55
        self.call_3bb_vs_sb = 60
        
        self.call_4bb_vs_ep = 30
        self.call_4bb_vs_mp = 35
        self.call_4bb_vs_co = 40
        self.call_4bb_vs_btn = 45
        self.call_4bb_vs_sb = 50
        
        self.call_5bb_vs_ep = 25
        self.call_5bb_vs_mp = 28
        self.call_5bb_vs_co = 32
        self.call_5bb_vs_btn = 36
        self.call_5bb_vs_sb = 40
        
        self.call_6_10bb_vs_ep = 20
        self.call_6_10bb_vs_mp = 22
        self.call_6_10bb_vs_co = 25
        self.call_6_10bb_vs_btn = 28
        self.call_6_10bb_vs_sb = 32
        
        # 10BB+ stack ranges
        self.push_10_15bb_ep = 8
        self.push_10_15bb_mp = 10
        self.push_10_15bb_co = 12
        self.push_10_15bb_btn = 15
        self.push_10_15bb_sb = 18
        self.push_10_15bb_bb = 20
        
        self.push_15_20bb_ep = 5
        self.push_15_20bb_mp = 8
        self.push_15_20bb_co = 10
        self.push_15_20bb_btn = 12
        self.push_15_20bb_sb = 15
        self.push_15_20bb_bb = 18
        
        self.push_20_25bb_ep = 3
        self.push_20_25bb_mp = 5
        self.push_20_25bb_co = 7
        self.push_20_25bb_btn = 10
        self.push_20_25bb_sb = 12
        self.push_20_25bb_bb = 15
        
        # 10BB+ call ranges
        self.call_10_15bb_vs_ep = 15
        self.call_10_15bb_vs_mp = 18
        self.call_10_15bb_vs_co = 20
        self.call_10_15bb_vs_btn = 22
        self.call_10_15bb_vs_sb = 25
        
        self.call_15_25bb_vs_ep = 10
        self.call_15_25bb_vs_mp = 12
        self.call_15_25bb_vs_co = 15
        self.call_15_25bb_vs_btn = 18
        self.call_15_25bb_vs_sb = 20

    def create_ui(self):
        # Create central widget with its layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        
        # Create a notebook (tabbed interface)
        notebook = QTabWidget()
        main_layout.addWidget(notebook)
        
        # Create main configuration tab
        config_frame = QScrollArea()
        config_frame.setWidgetResizable(True)
        config_widget = QWidget()
        config_layout = QVBoxLayout(config_widget)
        config_frame.setWidget(config_widget)
        notebook.addTab(config_frame, "Configuration")
        
        # Game and strategy settings are removed as requested
        
        # Generate and save buttons
        btn_frame = QWidget()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        
        generate_btn = QPushButton("Generate Profile")
        generate_btn.clicked.connect(self.generate_profile)
        save_btn = QPushButton("Save Profile")
        save_btn.clicked.connect(self.save_profile)
        
        btn_layout.addWidget(generate_btn)
        btn_layout.addWidget(save_btn)
        btn_layout.addStretch(1)
        
        config_layout.addWidget(btn_frame)
        
        # Preview frame
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_text = QTextEdit()
        preview_layout.addWidget(self.preview_text)
        
        config_layout.addWidget(preview_group)
        
        # Hidden config values for internal use (they won't be shown in the UI)
        self.num_players_combo = QComboBox()
        self.num_players_combo.addItems([str(i) for i in range(2, 10)])
        self.num_players_combo.setCurrentIndex(7)  # Default to 9 players
        
        self.game_type_combo = QComboBox()
        self.game_type_combo.addItems(["Cash Game", "Tournament"])
        
        self.aggression_slider = QSlider(Qt.Orientation.Horizontal)
        self.aggression_slider.setRange(0, 100)
        self.aggression_slider.setValue(50)
        
        self.tightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.tightness_slider.setRange(0, 100)
        self.tightness_slider.setValue(50)
        
        self.open_raise_combo = QComboBox()
        self.open_raise_combo.addItems(["2", "2.2", "2.5", "3"])
        self.open_raise_combo.setCurrentIndex(2)  # Default to 2.5
        
        # Create other tabs for specific scenarios
        self.create_preflop_tab(notebook)
        self.create_flop_tab(notebook)
        self.create_turn_tab(notebook)
        self.create_river_tab(notebook)
        self.create_push_fold_tab(notebook)

    def create_preflop_tab(self, notebook):
        preflop_scroll = QScrollArea()
        preflop_scroll.setWidgetResizable(True)
        preflop_widget = QWidget()
        preflop_layout = QVBoxLayout(preflop_widget)
        preflop_scroll.setWidget(preflop_widget)
        notebook.addTab(preflop_scroll, "Preflop Settings")
        
        # Create Open Raise frame
        openraise_group = QGroupBox("Open Raise Ranges")
        openraise_layout = QGridLayout(openraise_group)
        
        # EP range
        openraise_layout.addWidget(QLabel("Early Position Range (%):"), 0, 0)
        self.ep_range_slider = QSlider(Qt.Orientation.Horizontal)
        self.ep_range_slider.setRange(0, 100)
        self.ep_range_slider.setValue(15)
        self.ep_range_label = QLabel("15")
        self.ep_range_slider.valueChanged.connect(lambda v: self.ep_range_label.setText(str(v)))
        openraise_layout.addWidget(self.ep_range_slider, 0, 1)
        openraise_layout.addWidget(self.ep_range_label, 0, 2)
        
        # MP range
        openraise_layout.addWidget(QLabel("Middle Position Range (%):"), 1, 0)
        self.mp_range_slider = QSlider(Qt.Orientation.Horizontal)
        self.mp_range_slider.setRange(0, 100)
        self.mp_range_slider.setValue(20)
        self.mp_range_label = QLabel("20")
        self.mp_range_slider.valueChanged.connect(lambda v: self.mp_range_label.setText(str(v)))
        openraise_layout.addWidget(self.mp_range_slider, 1, 1)
        openraise_layout.addWidget(self.mp_range_label, 1, 2)
        
        # LP range
        openraise_layout.addWidget(QLabel("Late Position Range (%):"), 2, 0)
        self.lp_range_slider = QSlider(Qt.Orientation.Horizontal)
        self.lp_range_slider.setRange(0, 100)
        self.lp_range_slider.setValue(30)
        self.lp_range_label = QLabel("30")
        self.lp_range_slider.valueChanged.connect(lambda v: self.lp_range_label.setText(str(v)))
        openraise_layout.addWidget(self.lp_range_slider, 2, 1)
        openraise_layout.addWidget(self.lp_range_label, 2, 2)
        
        preflop_layout.addWidget(openraise_group)
        
        # Open Raise sizing
        sizing_group = QGroupBox("Position-Based Sizing")
        sizing_layout = QGridLayout(sizing_group)
        
        sizing_layout.addWidget(QLabel("EP Sizing (BB):"), 0, 0)
        self.ep_sizing_combo = QComboBox()
        self.ep_sizing_combo.addItems(["2.5", "3.0", "3.5", "4.0"])
        self.ep_sizing_combo.setCurrentIndex(1)  # Default to 3.0
        sizing_layout.addWidget(self.ep_sizing_combo, 0, 1)
        
        sizing_layout.addWidget(QLabel("MP Sizing (BB):"), 1, 0)
        self.mp_sizing_combo = QComboBox()
        self.mp_sizing_combo.addItems(["2.2", "2.5", "2.8", "3.0"])
        self.mp_sizing_combo.setCurrentIndex(2)  # Default to 2.8
        sizing_layout.addWidget(self.mp_sizing_combo, 1, 1)
        
        sizing_layout.addWidget(QLabel("LP Sizing (BB):"), 2, 0)
        self.lp_sizing_combo = QComboBox()
        self.lp_sizing_combo.addItems(["2.0", "2.2", "2.5", "2.8"])
        self.lp_sizing_combo.setCurrentIndex(2)  # Default to 2.5
        sizing_layout.addWidget(self.lp_sizing_combo, 2, 1)
        
        preflop_layout.addWidget(sizing_group)
        
        # 3-Bet Defense
        threebet_group = QGroupBox("3-Bet Defense")
        threebet_layout = QGridLayout(threebet_group)
        
        threebet_layout.addWidget(QLabel("Call 3-Bet Range (%):"), 0, 0)
        self.call_3bet_range_slider = QSlider(Qt.Orientation.Horizontal)
        self.call_3bet_range_slider.setRange(0, 100)
        self.call_3bet_range_slider.setValue(15)
        self.call_3bet_range_label = QLabel("15")
        self.call_3bet_range_slider.valueChanged.connect(lambda v: self.call_3bet_range_label.setText(str(v)))
        threebet_layout.addWidget(self.call_3bet_range_slider, 0, 1)
        threebet_layout.addWidget(self.call_3bet_range_label, 0, 2)
        
        threebet_layout.addWidget(QLabel("4-Bet Range (%):"), 1, 0)
        self.fourbet_range_slider = QSlider(Qt.Orientation.Horizontal)
        self.fourbet_range_slider.setRange(0, 100)
        self.fourbet_range_slider.setValue(8)
        self.fourbet_range_label = QLabel("8")
        self.fourbet_range_slider.valueChanged.connect(lambda v: self.fourbet_range_label.setText(str(v)))
        threebet_layout.addWidget(self.fourbet_range_slider, 1, 1)
        threebet_layout.addWidget(self.fourbet_range_label, 1, 2)
        
        preflop_layout.addWidget(threebet_group)
        
        # Position adjustments
        position_adj_group = QGroupBox("Position Adjustments")
        position_adj_layout = QGridLayout(position_adj_group)
        
        position_adj_layout.addWidget(QLabel("In Position 3-Bet Adjust (%):"), 0, 0)
        self.ip_3bet_adjust_slider = QSlider(Qt.Orientation.Horizontal)
        self.ip_3bet_adjust_slider.setRange(0, 100)
        self.ip_3bet_adjust_slider.setValue(20)
        self.ip_3bet_adjust_label = QLabel("20")
        self.ip_3bet_adjust_slider.valueChanged.connect(lambda v: self.ip_3bet_adjust_label.setText(str(v)))
        position_adj_layout.addWidget(self.ip_3bet_adjust_slider, 0, 1)
        position_adj_layout.addWidget(self.ip_3bet_adjust_label, 0, 2)
        
        position_adj_layout.addWidget(QLabel("vs Late Position 3-Bet Adjust (%):"), 1, 0)
        self.vs_lp_3bet_adjust_slider = QSlider(Qt.Orientation.Horizontal)
        self.vs_lp_3bet_adjust_slider.setRange(0, 100)
        self.vs_lp_3bet_adjust_slider.setValue(15)
        self.vs_lp_3bet_adjust_label = QLabel("15")
        self.vs_lp_3bet_adjust_slider.valueChanged.connect(lambda v: self.vs_lp_3bet_adjust_label.setText(str(v)))
        position_adj_layout.addWidget(self.vs_lp_3bet_adjust_slider, 1, 1)
        position_adj_layout.addWidget(self.vs_lp_3bet_adjust_label, 1, 2)
        
        preflop_layout.addWidget(position_adj_group)
        
        # 4-Bet defense
        fourbet_group = QGroupBox("4-Bet Defense")
        fourbet_layout = QGridLayout(fourbet_group)
        
        fourbet_layout.addWidget(QLabel("Call 4-Bet Range (%):"), 0, 0)
        self.call_4bet_range_slider = QSlider(Qt.Orientation.Horizontal)
        self.call_4bet_range_slider.setRange(0, 100)
        self.call_4bet_range_slider.setValue(5)
        self.call_4bet_range_label = QLabel("5")
        self.call_4bet_range_slider.valueChanged.connect(lambda v: self.call_4bet_range_label.setText(str(v)))
        fourbet_layout.addWidget(self.call_4bet_range_slider, 0, 1)
        fourbet_layout.addWidget(self.call_4bet_range_label, 0, 2)
        
        fourbet_layout.addWidget(QLabel("5-Bet Range (%):"), 1, 0)
        self.fivebet_range_slider = QSlider(Qt.Orientation.Horizontal)
        self.fivebet_range_slider.setRange(0, 100)
        self.fivebet_range_slider.setValue(3)
        self.fivebet_range_label = QLabel("3")
        self.fivebet_range_slider.valueChanged.connect(lambda v: self.fivebet_range_label.setText(str(v)))
        fourbet_layout.addWidget(self.fivebet_range_slider, 1, 1)
        fourbet_layout.addWidget(self.fivebet_range_label, 1, 2)
        
        fourbet_layout.addWidget(QLabel("Short Stack 4-Bet Adjust (%):"), 2, 0)
        self.short_stack_4bet_slider = QSlider(Qt.Orientation.Horizontal)
        self.short_stack_4bet_slider.setRange(0, 100)
        self.short_stack_4bet_slider.setValue(30)
        self.short_stack_4bet_label = QLabel("30")
        self.short_stack_4bet_slider.valueChanged.connect(lambda v: self.short_stack_4bet_label.setText(str(v)))
        fourbet_layout.addWidget(self.short_stack_4bet_slider, 2, 1)
        fourbet_layout.addWidget(self.short_stack_4bet_label, 2, 2)
        
        preflop_layout.addWidget(fourbet_group)
        
        # Squeeze settings
        squeeze_group = QGroupBox("Squeeze Settings")
        squeeze_layout = QGridLayout(squeeze_group)
        
        squeeze_layout.addWidget(QLabel("Squeeze vs 1 Caller (%):"), 0, 0)
        self.squeeze_1caller_slider = QSlider(Qt.Orientation.Horizontal)
        self.squeeze_1caller_slider.setRange(0, 100)
        self.squeeze_1caller_slider.setValue(12)
        self.squeeze_1caller_label = QLabel("12")
        self.squeeze_1caller_slider.valueChanged.connect(lambda v: self.squeeze_1caller_label.setText(str(v)))
        squeeze_layout.addWidget(self.squeeze_1caller_slider, 0, 1)
        squeeze_layout.addWidget(self.squeeze_1caller_label, 0, 2)
        
        squeeze_layout.addWidget(QLabel("Squeeze vs Multiple Callers (%):"), 1, 0)
        self.squeeze_multi_slider = QSlider(Qt.Orientation.Horizontal)
        self.squeeze_multi_slider.setRange(0, 100)
        self.squeeze_multi_slider.setValue(8)
        self.squeeze_multi_label = QLabel("8")
        self.squeeze_multi_slider.valueChanged.connect(lambda v: self.squeeze_multi_label.setText(str(v)))
        squeeze_layout.addWidget(self.squeeze_multi_slider, 1, 1)
        squeeze_layout.addWidget(self.squeeze_multi_label, 1, 2)
        
        squeeze_layout.addWidget(QLabel("Squeeze Sizing (x pot):"), 2, 0)
        self.squeeze_sizing_combo = QComboBox()
        self.squeeze_sizing_combo.addItems(["2.5", "3.0", "3.5", "4.0"])
        self.squeeze_sizing_combo.setCurrentIndex(1)  # Default to 3.0
        squeeze_layout.addWidget(self.squeeze_sizing_combo, 2, 1)
        
        squeeze_layout.addWidget(QLabel("Blinds Squeeze Adjust (%):"), 3, 0)
        self.blinds_squeeze_slider = QSlider(Qt.Orientation.Horizontal)
        self.blinds_squeeze_slider.setRange(0, 100)
        self.blinds_squeeze_slider.setValue(25)
        self.blinds_squeeze_label = QLabel("25")
        self.blinds_squeeze_slider.valueChanged.connect(lambda v: self.blinds_squeeze_label.setText(str(v)))
        squeeze_layout.addWidget(self.blinds_squeeze_slider, 3, 1)
        squeeze_layout.addWidget(self.blinds_squeeze_label, 3, 2)
        
        squeeze_layout.addWidget(QLabel("Button Squeeze Adjust (%):"), 4, 0)
        self.btn_squeeze_slider = QSlider(Qt.Orientation.Horizontal)
        self.btn_squeeze_slider.setRange(0, 100)
        self.btn_squeeze_slider.setValue(20)
        self.btn_squeeze_label = QLabel("20")
        self.btn_squeeze_slider.valueChanged.connect(lambda v: self.btn_squeeze_label.setText(str(v)))
        squeeze_layout.addWidget(self.btn_squeeze_slider, 4, 1)
        squeeze_layout.addWidget(self.btn_squeeze_label, 4, 2)
        
        preflop_layout.addWidget(squeeze_group)

    def create_flop_tab(self, notebook):
        flop_scroll = QScrollArea()
        flop_scroll.setWidgetResizable(True)
        flop_widget = QWidget()
        flop_layout = QVBoxLayout(flop_widget)
        flop_scroll.setWidget(flop_widget)
        notebook.addTab(flop_scroll, "Flop Settings")
        
        # C-Bet settings
        cbet_group = QGroupBox("C-Bet Settings")
        cbet_layout = QGridLayout(cbet_group)
        
        cbet_layout.addWidget(QLabel("IP C-Bet Frequency (%):"), 0, 0)
        self.ip_cbet_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.ip_cbet_freq_slider.setRange(0, 100)
        self.ip_cbet_freq_slider.setValue(70)
        self.ip_cbet_freq_label = QLabel("70")
        self.ip_cbet_freq_slider.valueChanged.connect(lambda v: self.ip_cbet_freq_label.setText(str(v)))
        cbet_layout.addWidget(self.ip_cbet_freq_slider, 0, 1)
        cbet_layout.addWidget(self.ip_cbet_freq_label, 0, 2)
        
        cbet_layout.addWidget(QLabel("OOP C-Bet Frequency (%):"), 1, 0)
        self.oop_cbet_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.oop_cbet_freq_slider.setRange(0, 100)
        self.oop_cbet_freq_slider.setValue(60)
        self.oop_cbet_freq_label = QLabel("60")
        self.oop_cbet_freq_slider.valueChanged.connect(lambda v: self.oop_cbet_freq_label.setText(str(v)))
        cbet_layout.addWidget(self.oop_cbet_freq_slider, 1, 1)
        cbet_layout.addWidget(self.oop_cbet_freq_label, 1, 2)
        
        cbet_layout.addWidget(QLabel("IP C-Bet Size (% of pot):"), 2, 0)
        self.ip_cbet_size_combo = QComboBox()
        self.ip_cbet_size_combo.addItems(["33", "50", "66", "75", "100"])
        self.ip_cbet_size_combo.setCurrentIndex(1)  # Default to 50
        cbet_layout.addWidget(self.ip_cbet_size_combo, 2, 1)
        
        cbet_layout.addWidget(QLabel("OOP C-Bet Size (% of pot):"), 3, 0)
        self.oop_cbet_size_combo = QComboBox()
        self.oop_cbet_size_combo.addItems(["33", "50", "66", "75", "100"])
        self.oop_cbet_size_combo.setCurrentIndex(2)  # Default to 66
        cbet_layout.addWidget(self.oop_cbet_size_combo, 3, 1)
        
        flop_layout.addWidget(cbet_group)
        
        # Board texture adjustments
        texture_group = QGroupBox("Board Texture Adjustments")
        texture_layout = QGridLayout(texture_group)
        
        texture_layout.addWidget(QLabel("Dry Board Adjustment (%):"), 0, 0)
        self.dry_board_adjust_slider = QSlider(Qt.Orientation.Horizontal)
        self.dry_board_adjust_slider.setRange(-50, 50)
        self.dry_board_adjust_slider.setValue(20)
        self.dry_board_adjust_label = QLabel("20")
        self.dry_board_adjust_slider.valueChanged.connect(lambda v: self.dry_board_adjust_label.setText(str(v)))
        texture_layout.addWidget(self.dry_board_adjust_slider, 0, 1)
        texture_layout.addWidget(self.dry_board_adjust_label, 0, 2)
        
        texture_layout.addWidget(QLabel("Wet Board Adjustment (%):"), 1, 0)
        self.wet_board_adjust_slider = QSlider(Qt.Orientation.Horizontal)
        self.wet_board_adjust_slider.setRange(-50, 50)
        self.wet_board_adjust_slider.setValue(-20)
        self.wet_board_adjust_label = QLabel("-20")
        self.wet_board_adjust_slider.valueChanged.connect(lambda v: self.wet_board_adjust_label.setText(str(v)))
        texture_layout.addWidget(self.wet_board_adjust_slider, 1, 1)
        texture_layout.addWidget(self.wet_board_adjust_label, 1, 2)
        
        flop_layout.addWidget(texture_group)
        
        # Facing bets
        facing_group = QGroupBox("Facing Bets")
        facing_layout = QGridLayout(facing_group)
        
        facing_layout.addWidget(QLabel("Check-Raise Defense (%):"), 0, 0)
        self.checkraise_defense_slider = QSlider(Qt.Orientation.Horizontal)
        self.checkraise_defense_slider.setRange(0, 100)
        self.checkraise_defense_slider.setValue(35)
        self.checkraise_defense_label = QLabel("35")
        self.checkraise_defense_slider.valueChanged.connect(lambda v: self.checkraise_defense_label.setText(str(v)))
        facing_layout.addWidget(self.checkraise_defense_slider, 0, 1)
        facing_layout.addWidget(self.checkraise_defense_label, 0, 2)
        
        facing_layout.addWidget(QLabel("Donk Bet Response Style:"), 1, 0)
        self.donk_response_combo = QComboBox()
        self.donk_response_combo.addItems(["Fold/Call", "Call/Raise", "Aggressive"])
        self.donk_response_combo.setCurrentIndex(1)  # Default to Call/Raise
        facing_layout.addWidget(self.donk_response_combo, 1, 1)
        
        flop_layout.addWidget(facing_group)
        
        # Hand ranges
        ranges_group = QGroupBox("Hand Ranges")
        ranges_layout = QGridLayout(ranges_group)
        
        ranges_layout.addWidget(QLabel("Value Hands Aggression (%):"), 0, 0)
        self.value_aggression_slider = QSlider(Qt.Orientation.Horizontal)
        self.value_aggression_slider.setRange(0, 100)
        self.value_aggression_slider.setValue(80)
        self.value_aggression_label = QLabel("80")
        self.value_aggression_slider.valueChanged.connect(lambda v: self.value_aggression_label.setText(str(v)))
        ranges_layout.addWidget(self.value_aggression_slider, 0, 1)
        ranges_layout.addWidget(self.value_aggression_label, 0, 2)
        
        ranges_layout.addWidget(QLabel("Draw Hands Aggression (%):"), 1, 0)
        self.draw_aggression_slider = QSlider(Qt.Orientation.Horizontal)
        self.draw_aggression_slider.setRange(0, 100)
        self.draw_aggression_slider.setValue(60)
        self.draw_aggression_label = QLabel("60")
        self.draw_aggression_slider.valueChanged.connect(lambda v: self.draw_aggression_label.setText(str(v)))
        ranges_layout.addWidget(self.draw_aggression_slider, 1, 1)
        ranges_layout.addWidget(self.draw_aggression_label, 1, 2)
        
        ranges_layout.addWidget(QLabel("Semi-Bluff Frequency (%):"), 2, 0)
        self.semibluff_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.semibluff_freq_slider.setRange(0, 100)
        self.semibluff_freq_slider.setValue(65)
        self.semibluff_freq_label = QLabel("65")
        self.semibluff_freq_slider.valueChanged.connect(lambda v: self.semibluff_freq_label.setText(str(v)))
        ranges_layout.addWidget(self.semibluff_freq_slider, 2, 1)
        ranges_layout.addWidget(self.semibluff_freq_label, 2, 2)
        
        flop_layout.addWidget(ranges_group)
        
        # Multiway pots
        multiway_group = QGroupBox("Multiway Pots")
        multiway_layout = QGridLayout(multiway_group)
        
        multiway_layout.addWidget(QLabel("Multiway C-Bet Frequency (%):"), 0, 0)
        self.multiway_cbet_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.multiway_cbet_freq_slider.setRange(0, 100)
        self.multiway_cbet_freq_slider.setValue(40)
        self.multiway_cbet_freq_label = QLabel("40")
        self.multiway_cbet_freq_slider.valueChanged.connect(lambda v: self.multiway_cbet_freq_label.setText(str(v)))
        multiway_layout.addWidget(self.multiway_cbet_freq_slider, 0, 1)
        multiway_layout.addWidget(self.multiway_cbet_freq_label, 0, 2)
        
        multiway_layout.addWidget(QLabel("Multiway Value Range (%):"), 1, 0)
        self.multiway_value_range_slider = QSlider(Qt.Orientation.Horizontal)
        self.multiway_value_range_slider.setRange(0, 100)
        self.multiway_value_range_slider.setValue(25)
        self.multiway_value_range_label = QLabel("25")
        self.multiway_value_range_slider.valueChanged.connect(lambda v: self.multiway_value_range_label.setText(str(v)))
        multiway_layout.addWidget(self.multiway_value_range_slider, 1, 1)
        multiway_layout.addWidget(self.multiway_value_range_label, 1, 2)
        
        flop_layout.addWidget(multiway_group)

    def create_turn_tab(self, notebook):
        turn_scroll = QScrollArea()
        turn_scroll.setWidgetResizable(True)
        turn_widget = QWidget()
        turn_layout = QVBoxLayout(turn_widget)
        turn_scroll.setWidget(turn_widget)
        notebook.addTab(turn_scroll, "Turn Settings")
        
        # Second Barrel settings
        second_barrel_group = QGroupBox("Second Barrel Settings")
        second_barrel_layout = QGridLayout(second_barrel_group)
        
        second_barrel_layout.addWidget(QLabel("Second Barrel Frequency (%):"), 0, 0)
        self.second_barrel_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.second_barrel_freq_slider.setRange(0, 100)
        self.second_barrel_freq_slider.setValue(60)
        self.second_barrel_freq_label = QLabel("60")
        self.second_barrel_freq_slider.valueChanged.connect(lambda v: self.second_barrel_freq_label.setText(str(v)))
        second_barrel_layout.addWidget(self.second_barrel_freq_slider, 0, 1)
        second_barrel_layout.addWidget(self.second_barrel_freq_label, 0, 2)
        
        second_barrel_layout.addWidget(QLabel("Delayed C-Bet Frequency (%):"), 1, 0)
        self.delayed_cbet_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.delayed_cbet_freq_slider.setRange(0, 100)
        self.delayed_cbet_freq_slider.setValue(40)
        self.delayed_cbet_freq_label = QLabel("40")
        self.delayed_cbet_freq_slider.valueChanged.connect(lambda v: self.delayed_cbet_freq_label.setText(str(v)))
        second_barrel_layout.addWidget(self.delayed_cbet_freq_slider, 1, 1)
        second_barrel_layout.addWidget(self.delayed_cbet_freq_label, 1, 2)
        
        second_barrel_layout.addWidget(QLabel("IP Turn Bet Size (% of pot):"), 2, 0)
        self.ip_turn_bet_size_combo = QComboBox()
        self.ip_turn_bet_size_combo.addItems(["50", "66", "75", "100"])
        self.ip_turn_bet_size_combo.setCurrentIndex(1)  # Default to 66
        second_barrel_layout.addWidget(self.ip_turn_bet_size_combo, 2, 1)
        
        second_barrel_layout.addWidget(QLabel("OOP Turn Bet Size (% of pot):"), 3, 0)
        self.oop_turn_bet_size_combo = QComboBox()
        self.oop_turn_bet_size_combo.addItems(["50", "66", "75", "100"])
        self.oop_turn_bet_size_combo.setCurrentIndex(2)  # Default to 75
        second_barrel_layout.addWidget(self.oop_turn_bet_size_combo, 3, 1)
        
        turn_layout.addWidget(second_barrel_group)
        
        # Turn Card adjustments
        turn_card_group = QGroupBox("Turn Card Adjustments")
        turn_card_layout = QGridLayout(turn_card_group)
        
        turn_card_layout.addWidget(QLabel("Scare Card Adjustment (%):"), 0, 0)
        self.scare_card_adjust_slider = QSlider(Qt.Orientation.Horizontal)
        self.scare_card_adjust_slider.setRange(-50, 50)
        self.scare_card_adjust_slider.setValue(-15)
        self.scare_card_adjust_label = QLabel("-15")
        self.scare_card_adjust_slider.valueChanged.connect(lambda v: self.scare_card_adjust_label.setText(str(v)))
        turn_card_layout.addWidget(self.scare_card_adjust_slider, 0, 1)
        turn_card_layout.addWidget(self.scare_card_adjust_label, 0, 2)
        
        turn_card_layout.addWidget(QLabel("Draw Complete Adjustment (%):"), 1, 0)
        self.draw_complete_adjust_slider = QSlider(Qt.Orientation.Horizontal)
        self.draw_complete_adjust_slider.setRange(-50, 50)
        self.draw_complete_adjust_slider.setValue(10)
        self.draw_complete_adjust_label = QLabel("10")
        self.draw_complete_adjust_slider.valueChanged.connect(lambda v: self.draw_complete_adjust_label.setText(str(v)))
        turn_card_layout.addWidget(self.draw_complete_adjust_slider, 1, 1)
        turn_card_layout.addWidget(self.draw_complete_adjust_label, 1, 2)
        
        turn_layout.addWidget(turn_card_group)
        
        # Facing Turn bets
        facing_turn_group = QGroupBox("Facing Turn Bets")
        facing_turn_layout = QGridLayout(facing_turn_group)
        
        facing_turn_layout.addWidget(QLabel("Turn Check-Raise Frequency (%):"), 0, 0)
        self.turn_checkraise_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.turn_checkraise_freq_slider.setRange(0, 100)
        self.turn_checkraise_freq_slider.setValue(25)
        self.turn_checkraise_freq_label = QLabel("25")
        self.turn_checkraise_freq_slider.valueChanged.connect(lambda v: self.turn_checkraise_freq_label.setText(str(v)))
        facing_turn_layout.addWidget(self.turn_checkraise_freq_slider, 0, 1)
        facing_turn_layout.addWidget(self.turn_checkraise_freq_label, 0, 2)
        
        facing_turn_layout.addWidget(QLabel("Turn Float Frequency (%):"), 1, 0)
        self.turn_float_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.turn_float_freq_slider.setRange(0, 100)
        self.turn_float_freq_slider.setValue(30)
        self.turn_float_freq_label = QLabel("30")
        self.turn_float_freq_slider.valueChanged.connect(lambda v: self.turn_float_freq_label.setText(str(v)))
        facing_turn_layout.addWidget(self.turn_float_freq_slider, 1, 1)
        facing_turn_layout.addWidget(self.turn_float_freq_label, 1, 2)
        
        facing_turn_layout.addWidget(QLabel("Turn Fold to C-Bet Frequency (%):"), 2, 0)
        self.turn_fold_to_cbet_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.turn_fold_to_cbet_freq_slider.setRange(0, 100)
        self.turn_fold_to_cbet_freq_slider.setValue(60)
        self.turn_fold_to_cbet_freq_label = QLabel("60")
        self.turn_fold_to_cbet_freq_slider.valueChanged.connect(lambda v: self.turn_fold_to_cbet_freq_label.setText(str(v)))
        facing_turn_layout.addWidget(self.turn_fold_to_cbet_freq_slider, 2, 1)
        facing_turn_layout.addWidget(self.turn_fold_to_cbet_freq_label, 2, 2)
        
        turn_layout.addWidget(facing_turn_group)
        
        # Probe betting
        probe_group = QGroupBox("Probe Betting")
        probe_layout = QGridLayout(probe_group)
        
        probe_layout.addWidget(QLabel("Turn Probe Frequency (%):"), 0, 0)
        self.turn_probe_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.turn_probe_freq_slider.setRange(0, 100)
        self.turn_probe_freq_slider.setValue(35)
        self.turn_probe_freq_label = QLabel("35")
        self.turn_probe_freq_slider.valueChanged.connect(lambda v: self.turn_probe_freq_label.setText(str(v)))
        probe_layout.addWidget(self.turn_probe_freq_slider, 0, 1)
        probe_layout.addWidget(self.turn_probe_freq_label, 0, 2)
        
        probe_layout.addWidget(QLabel("Turn Bluff Raise Frequency (%):"), 1, 0)
        self.turn_bluff_raise_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.turn_bluff_raise_freq_slider.setRange(0, 100)
        self.turn_bluff_raise_freq_slider.setValue(20)
        self.turn_bluff_raise_freq_label = QLabel("20")
        self.turn_bluff_raise_freq_slider.valueChanged.connect(lambda v: self.turn_bluff_raise_freq_label.setText(str(v)))
        probe_layout.addWidget(self.turn_bluff_raise_freq_slider, 1, 1)
        probe_layout.addWidget(self.turn_bluff_raise_freq_label, 1, 2)
        
        turn_layout.addWidget(probe_group)

    def create_river_tab(self, notebook):
        river_scroll = QScrollArea()
        river_scroll.setWidgetResizable(True)
        river_widget = QWidget()
        river_layout = QVBoxLayout(river_widget)
        river_scroll.setWidget(river_widget)
        notebook.addTab(river_scroll, "River Settings")
        
        # Third Barrel settings
        barrel_group = QGroupBox("Third Barrel Settings")
        barrel_layout = QGridLayout(barrel_group)
        
        barrel_layout.addWidget(QLabel("Third Barrel Frequency (%):"), 0, 0)
        self.third_barrel_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.third_barrel_freq_slider.setRange(0, 100)
        self.third_barrel_freq_slider.setValue(40)
        self.third_barrel_freq_label = QLabel("40")
        self.third_barrel_freq_slider.valueChanged.connect(lambda v: self.third_barrel_freq_label.setText(str(v)))
        barrel_layout.addWidget(self.third_barrel_freq_slider, 0, 1)
        barrel_layout.addWidget(self.third_barrel_freq_label, 0, 2)
        
        barrel_layout.addWidget(QLabel("Delayed Second Barrel Frequency (%):"), 1, 0)
        self.delayed_second_barrel_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.delayed_second_barrel_freq_slider.setRange(0, 100)
        self.delayed_second_barrel_freq_slider.setValue(30)
        self.delayed_second_barrel_freq_label = QLabel("30")
        self.delayed_second_barrel_freq_slider.valueChanged.connect(lambda v: self.delayed_second_barrel_freq_label.setText(str(v)))
        barrel_layout.addWidget(self.delayed_second_barrel_freq_slider, 1, 1)
        barrel_layout.addWidget(self.delayed_second_barrel_freq_label, 1, 2)
        
        barrel_layout.addWidget(QLabel("IP River Bet Size (% of pot):"), 2, 0)
        self.ip_river_bet_size_combo = QComboBox()
        self.ip_river_bet_size_combo.addItems(["50", "66", "75", "100"])
        self.ip_river_bet_size_combo.setCurrentIndex(2)  # Default to 75
        barrel_layout.addWidget(self.ip_river_bet_size_combo, 2, 1)
        
        barrel_layout.addWidget(QLabel("OOP River Bet Size (% of pot):"), 3, 0)
        self.oop_river_bet_size_combo = QComboBox()
        self.oop_river_bet_size_combo.addItems(["50", "66", "75", "100"])
        self.oop_river_bet_size_combo.setCurrentIndex(2)  # Default to 75
        barrel_layout.addWidget(self.oop_river_bet_size_combo, 3, 1)
        
        river_layout.addWidget(barrel_group)
        
        # Facing River bets
        facing_river_group = QGroupBox("Facing River Bets")
        facing_river_layout = QGridLayout(facing_river_group)
        
        facing_river_layout.addWidget(QLabel("River Check-Raise Frequency (%):"), 0, 0)
        self.river_checkraise_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.river_checkraise_freq_slider.setRange(0, 100)
        self.river_checkraise_freq_slider.setValue(15)
        self.river_checkraise_freq_label = QLabel("15")
        self.river_checkraise_freq_slider.valueChanged.connect(lambda v: self.river_checkraise_freq_label.setText(str(v)))
        facing_river_layout.addWidget(self.river_checkraise_freq_slider, 0, 1)
        facing_river_layout.addWidget(self.river_checkraise_freq_label, 0, 2)
        
        facing_river_layout.addWidget(QLabel("River Float Frequency (%):"), 1, 0)
        self.river_float_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.river_float_freq_slider.setRange(0, 100)
        self.river_float_freq_slider.setValue(20)
        self.river_float_freq_label = QLabel("20")
        self.river_float_freq_slider.valueChanged.connect(lambda v: self.river_float_freq_label.setText(str(v)))
        facing_river_layout.addWidget(self.river_float_freq_slider, 1, 1)
        facing_river_layout.addWidget(self.river_float_freq_label, 1, 2)
        
        facing_river_layout.addWidget(QLabel("River Fold to Bet Frequency (%):"), 2, 0)
        self.river_fold_to_bet_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.river_fold_to_bet_freq_slider.setRange(0, 100)
        self.river_fold_to_bet_freq_slider.setValue(70)
        self.river_fold_to_bet_freq_label = QLabel("70")
        self.river_fold_to_bet_freq_slider.valueChanged.connect(lambda v: self.river_fold_to_bet_freq_label.setText(str(v)))
        facing_river_layout.addWidget(self.river_fold_to_bet_freq_slider, 2, 1)
        facing_river_layout.addWidget(self.river_fold_to_bet_freq_label, 2, 2)
        
        facing_river_layout.addWidget(QLabel("River Bluff Raise Frequency (%):"), 3, 0)
        self.river_bluff_raise_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.river_bluff_raise_freq_slider.setRange(0, 100)
        self.river_bluff_raise_freq_slider.setValue(10)
        self.river_bluff_raise_freq_label = QLabel("10")
        self.river_bluff_raise_freq_slider.valueChanged.connect(lambda v: self.river_bluff_raise_freq_label.setText(str(v)))
        facing_river_layout.addWidget(self.river_bluff_raise_freq_slider, 3, 1)
        facing_river_layout.addWidget(self.river_bluff_raise_freq_label, 3, 2)
        
        river_layout.addWidget(facing_river_group)
        
        # River Hand Ranges
        river_ranges_group = QGroupBox("River Hand Ranges")
        river_ranges_layout = QGridLayout(river_ranges_group)
        
        river_ranges_layout.addWidget(QLabel("River Value Range (%):"), 0, 0)
        self.river_value_range_slider = QSlider(Qt.Orientation.Horizontal)
        self.river_value_range_slider.setRange(0, 100)
        self.river_value_range_slider.setValue(60)
        self.river_value_range_label = QLabel("60")
        self.river_value_range_slider.valueChanged.connect(lambda v: self.river_value_range_label.setText(str(v)))
        river_ranges_layout.addWidget(self.river_value_range_slider, 0, 1)
        river_ranges_layout.addWidget(self.river_value_range_label, 0, 2)
        
        river_ranges_layout.addWidget(QLabel("River Bluff Range (%):"), 1, 0)
        self.river_bluff_range_slider = QSlider(Qt.Orientation.Horizontal)
        self.river_bluff_range_slider.setRange(0, 100)
        self.river_bluff_range_slider.setValue(15)
        self.river_bluff_range_label = QLabel("15")
        self.river_bluff_range_slider.valueChanged.connect(lambda v: self.river_bluff_range_label.setText(str(v)))
        river_ranges_layout.addWidget(self.river_bluff_range_slider, 1, 1)
        river_ranges_layout.addWidget(self.river_bluff_range_label, 1, 2)
        
        river_ranges_layout.addWidget(QLabel("River Check Behind Range (%):"), 2, 0)
        self.river_check_behind_range_slider = QSlider(Qt.Orientation.Horizontal)
        self.river_check_behind_range_slider.setRange(0, 100)
        self.river_check_behind_range_slider.setValue(80)
        self.river_check_behind_range_label = QLabel("80")
        self.river_check_behind_range_slider.valueChanged.connect(lambda v: self.river_check_behind_range_label.setText(str(v)))
        river_ranges_layout.addWidget(self.river_check_behind_range_slider, 2, 1)
        river_ranges_layout.addWidget(self.river_check_behind_range_label, 2, 2)
        
        river_layout.addWidget(river_ranges_group)
        
        # Probe betting (River)
        river_probe_group = QGroupBox("River Probe Betting")
        river_probe_layout = QGridLayout(river_probe_group)
        
        river_probe_layout.addWidget(QLabel("River Probe Frequency (%):"), 0, 0)
        self.river_probe_freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.river_probe_freq_slider.setRange(0, 100)
        self.river_probe_freq_slider.setValue(25)
        self.river_probe_freq_label = QLabel("25")
        self.river_probe_freq_slider.valueChanged.connect(lambda v: self.river_probe_freq_label.setText(str(v)))
        river_probe_layout.addWidget(self.river_probe_freq_slider, 0, 1)
        river_probe_layout.addWidget(self.river_probe_freq_label, 0, 2)
        
        river_layout.addWidget(river_probe_group)
        
    def create_push_fold_tab(self, notebook):
        """Create a tab for Push/Fold settings"""
        push_fold_scroll = QScrollArea()
        push_fold_scroll.setWidgetResizable(True)
        push_fold_widget = QWidget()
        push_fold_layout = QVBoxLayout(push_fold_widget)
        push_fold_scroll.setWidget(push_fold_widget)
        notebook.addTab(push_fold_scroll, "Push/Fold")
        
        # Use a notebook for organization
        pf_notebook = QTabWidget()
        push_fold_layout.addWidget(pf_notebook)
        
        # Create tabs for different stack sizes
        tab_1bb = QScrollArea()
        tab_1bb.setWidgetResizable(True)
        widget_1bb = QWidget()
        layout_1bb = QVBoxLayout(widget_1bb)
        tab_1bb.setWidget(widget_1bb)
        
        tab_2_5bb = QScrollArea()
        tab_2_5bb.setWidgetResizable(True)
        widget_2_5bb = QWidget()
        layout_2_5bb = QVBoxLayout(widget_2_5bb)
        tab_2_5bb.setWidget(widget_2_5bb)
        
        tab_6_10bb = QScrollArea()
        tab_6_10bb.setWidgetResizable(True)
        widget_6_10bb = QWidget()
        layout_6_10bb = QVBoxLayout(widget_6_10bb)
        tab_6_10bb.setWidget(widget_6_10bb)
        
        tab_10_25bb = QScrollArea()
        tab_10_25bb.setWidgetResizable(True)
        widget_10_25bb = QWidget()
        layout_10_25bb = QVBoxLayout(widget_10_25bb)
        tab_10_25bb.setWidget(widget_10_25bb)
        
        call_ranges = QScrollArea()
        call_ranges.setWidgetResizable(True)
        widget_call = QWidget()
        layout_call = QVBoxLayout(widget_call)
        call_ranges.setWidget(widget_call)
        
        pf_notebook.addTab(tab_1bb, "1BB")
        pf_notebook.addTab(tab_2_5bb, "2-5BB")
        pf_notebook.addTab(tab_6_10bb, "6-10BB")
        pf_notebook.addTab(tab_10_25bb, "10-25BB")
        pf_notebook.addTab(call_ranges, "Call Ranges")
        
        # 1BB Tab
        frame_1bb = self.create_push_fold_position_frame("1BB Stack Push Ranges", {
            "EP": (self.push_1bb_ep, lambda v: setattr(self, 'push_1bb_ep', v)),
            "MP": (self.push_1bb_mp, lambda v: setattr(self, 'push_1bb_mp', v)),
            "CO": (self.push_1bb_co, lambda v: setattr(self, 'push_1bb_co', v)),
            "BTN": (self.push_1bb_btn, lambda v: setattr(self, 'push_1bb_btn', v)),
            "SB": (self.push_1bb_sb, lambda v: setattr(self, 'push_1bb_sb', v)),
            "BB": (self.push_1bb_bb, lambda v: setattr(self, 'push_1bb_bb', v))
        })
        layout_1bb.addWidget(frame_1bb)
        
        # 2-5BB Tab
        frame_2bb = self.create_push_fold_position_frame("2BB Stack Push Ranges", {
            "EP": (self.push_2bb_ep, lambda v: setattr(self, 'push_2bb_ep', v)),
            "MP": (self.push_2bb_mp, lambda v: setattr(self, 'push_2bb_mp', v)),
            "CO": (self.push_2bb_co, lambda v: setattr(self, 'push_2bb_co', v)),
            "BTN": (self.push_2bb_btn, lambda v: setattr(self, 'push_2bb_btn', v)),
            "SB": (self.push_2bb_sb, lambda v: setattr(self, 'push_2bb_sb', v)),
            "BB": (self.push_2bb_bb, lambda v: setattr(self, 'push_2bb_bb', v))
        })
        layout_2_5bb.addWidget(frame_2bb)
        
        frame_3bb = self.create_push_fold_position_frame("3BB Stack Push Ranges", {
            "EP": (self.push_3bb_ep, lambda v: setattr(self, 'push_3bb_ep', v)),
            "MP": (self.push_3bb_mp, lambda v: setattr(self, 'push_3bb_mp', v)),
            "CO": (self.push_3bb_co, lambda v: setattr(self, 'push_3bb_co', v)),
            "BTN": (self.push_3bb_btn, lambda v: setattr(self, 'push_3bb_btn', v)),
            "SB": (self.push_3bb_sb, lambda v: setattr(self, 'push_3bb_sb', v)),
            "BB": (self.push_3bb_bb, lambda v: setattr(self, 'push_3bb_bb', v))
        })
        layout_2_5bb.addWidget(frame_3bb)
        
        frame_4bb = self.create_push_fold_position_frame("4BB Stack Push Ranges", {
            "EP": (self.push_4bb_ep, lambda v: setattr(self, 'push_4bb_ep', v)),
            "MP": (self.push_4bb_mp, lambda v: setattr(self, 'push_4bb_mp', v)),
            "CO": (self.push_4bb_co, lambda v: setattr(self, 'push_4bb_co', v)),
            "BTN": (self.push_4bb_btn, lambda v: setattr(self, 'push_4bb_btn', v)),
            "SB": (self.push_4bb_sb, lambda v: setattr(self, 'push_4bb_sb', v)),
            "BB": (self.push_4bb_bb, lambda v: setattr(self, 'push_4bb_bb', v))
        })
        layout_2_5bb.addWidget(frame_4bb)
        
        frame_5bb = self.create_push_fold_position_frame("5BB Stack Push Ranges", {
            "EP": (self.push_5bb_ep, lambda v: setattr(self, 'push_5bb_ep', v)),
            "MP": (self.push_5bb_mp, lambda v: setattr(self, 'push_5bb_mp', v)),
            "CO": (self.push_5bb_co, lambda v: setattr(self, 'push_5bb_co', v)),
            "BTN": (self.push_5bb_btn, lambda v: setattr(self, 'push_5bb_btn', v)),
            "SB": (self.push_5bb_sb, lambda v: setattr(self, 'push_5bb_sb', v)),
            "BB": (self.push_5bb_bb, lambda v: setattr(self, 'push_5bb_bb', v))
        })
        layout_2_5bb.addWidget(frame_5bb)
        
        # 6-10BB Tab
        frame_6bb = self.create_push_fold_position_frame("6BB Stack Push Ranges", {
            "EP": (self.push_6bb_ep, lambda v: setattr(self, 'push_6bb_ep', v)),
            "MP": (self.push_6bb_mp, lambda v: setattr(self, 'push_6bb_mp', v)),
            "CO": (self.push_6bb_co, lambda v: setattr(self, 'push_6bb_co', v)),
            "BTN": (self.push_6bb_btn, lambda v: setattr(self, 'push_6bb_btn', v)),
            "SB": (self.push_6bb_sb, lambda v: setattr(self, 'push_6bb_sb', v)),
            "BB": (self.push_6bb_bb, lambda v: setattr(self, 'push_6bb_bb', v))
        })
        layout_6_10bb.addWidget(frame_6bb)
        
        frame_7bb = self.create_push_fold_position_frame("7BB Stack Push Ranges", {
            "EP": (self.push_7bb_ep, lambda v: setattr(self, 'push_7bb_ep', v)),
            "MP": (self.push_7bb_mp, lambda v: setattr(self, 'push_7bb_mp', v)),
            "CO": (self.push_7bb_co, lambda v: setattr(self, 'push_7bb_co', v)),
            "BTN": (self.push_7bb_btn, lambda v: setattr(self, 'push_7bb_btn', v)),
            "SB": (self.push_7bb_sb, lambda v: setattr(self, 'push_7bb_sb', v)),
            "BB": (self.push_7bb_bb, lambda v: setattr(self, 'push_7bb_bb', v))
        })
        layout_6_10bb.addWidget(frame_7bb)
        
        frame_8bb = self.create_push_fold_position_frame("8BB Stack Push Ranges", {
            "EP": (self.push_8bb_ep, lambda v: setattr(self, 'push_8bb_ep', v)),
            "MP": (self.push_8bb_mp, lambda v: setattr(self, 'push_8bb_mp', v)),
            "CO": (self.push_8bb_co, lambda v: setattr(self, 'push_8bb_co', v)),
            "BTN": (self.push_8bb_btn, lambda v: setattr(self, 'push_8bb_btn', v)),
            "SB": (self.push_8bb_sb, lambda v: setattr(self, 'push_8bb_sb', v)),
            "BB": (self.push_8bb_bb, lambda v: setattr(self, 'push_8bb_bb', v))
        })
        layout_6_10bb.addWidget(frame_8bb)
        
        frame_9bb = self.create_push_fold_position_frame("9BB Stack Push Ranges", {
            "EP": (self.push_9bb_ep, lambda v: setattr(self, 'push_9bb_ep', v)),
            "MP": (self.push_9bb_mp, lambda v: setattr(self, 'push_9bb_mp', v)),
            "CO": (self.push_9bb_co, lambda v: setattr(self, 'push_9bb_co', v)),
            "BTN": (self.push_9bb_btn, lambda v: setattr(self, 'push_9bb_btn', v)),
            "SB": (self.push_9bb_sb, lambda v: setattr(self, 'push_9bb_sb', v)),
            "BB": (self.push_9bb_bb, lambda v: setattr(self, 'push_9bb_bb', v))
        })
        layout_6_10bb.addWidget(frame_9bb)
        
        frame_10bb = self.create_push_fold_position_frame("10BB Stack Push Ranges", {
            "EP": (self.push_10bb_ep, lambda v: setattr(self, 'push_10bb_ep', v)),
            "MP": (self.push_10bb_mp, lambda v: setattr(self, 'push_10bb_mp', v)),
            "CO": (self.push_10bb_co, lambda v: setattr(self, 'push_10bb_co', v)),
            "BTN": (self.push_10bb_btn, lambda v: setattr(self, 'push_10bb_btn', v)),
            "SB": (self.push_10bb_sb, lambda v: setattr(self, 'push_10bb_sb', v)),
            "BB": (self.push_10bb_bb, lambda v: setattr(self, 'push_10bb_bb', v))
        })
        layout_6_10bb.addWidget(frame_10bb)
        
        # 10-25BB Tab
        frame_10_15bb = self.create_push_fold_position_frame("10-15BB Stack Push Ranges", {
            "EP": (self.push_10_15bb_ep, lambda v: setattr(self, 'push_10_15bb_ep', v)),
            "MP": (self.push_10_15bb_mp, lambda v: setattr(self, 'push_10_15bb_mp', v)),
            "CO": (self.push_10_15bb_co, lambda v: setattr(self, 'push_10_15bb_co', v)),
            "BTN": (self.push_10_15bb_btn, lambda v: setattr(self, 'push_10_15bb_btn', v)),
            "SB": (self.push_10_15bb_sb, lambda v: setattr(self, 'push_10_15bb_sb', v)),
            "BB": (self.push_10_15bb_bb, lambda v: setattr(self, 'push_10_15bb_bb', v))
        })
        layout_10_25bb.addWidget(frame_10_15bb)
        
        frame_15_20bb = self.create_push_fold_position_frame("15-20BB Stack Push Ranges", {
            "EP": (self.push_15_20bb_ep, lambda v: setattr(self, 'push_15_20bb_ep', v)),
            "MP": (self.push_15_20bb_mp, lambda v: setattr(self, 'push_15_20bb_mp', v)),
            "CO": (self.push_15_20bb_co, lambda v: setattr(self, 'push_15_20bb_co', v)),
            "BTN": (self.push_15_20bb_btn, lambda v: setattr(self, 'push_15_20bb_btn', v)),
            "SB": (self.push_15_20bb_sb, lambda v: setattr(self, 'push_15_20bb_sb', v)),
            "BB": (self.push_15_20bb_bb, lambda v: setattr(self, 'push_15_20bb_bb', v))
        })
        layout_10_25bb.addWidget(frame_15_20bb)
        
        frame_20_25bb = self.create_push_fold_position_frame("20-25BB Stack Push Ranges", {
            "EP": (self.push_20_25bb_ep, lambda v: setattr(self, 'push_20_25bb_ep', v)),
            "MP": (self.push_20_25bb_mp, lambda v: setattr(self, 'push_20_25bb_mp', v)),
            "CO": (self.push_20_25bb_co, lambda v: setattr(self, 'push_20_25bb_co', v)),
            "BTN": (self.push_20_25bb_btn, lambda v: setattr(self, 'push_20_25bb_btn', v)),
            "SB": (self.push_20_25bb_sb, lambda v: setattr(self, 'push_20_25bb_sb', v)),
            "BB": (self.push_20_25bb_bb, lambda v: setattr(self, 'push_20_25bb_bb', v))
        })
        layout_10_25bb.addWidget(frame_20_25bb)
        
        # Call Ranges Tab
        frame_call_1bb = self.create_push_fold_call_frame("1BB Stack Call Ranges", {
            "vs_EP": (self.call_1bb_vs_ep, lambda v: setattr(self, 'call_1bb_vs_ep', v)),
            "vs_MP": (self.call_1bb_vs_mp, lambda v: setattr(self, 'call_1bb_vs_mp', v)),
            "vs_CO": (self.call_1bb_vs_co, lambda v: setattr(self, 'call_1bb_vs_co', v)),
            "vs_BTN": (self.call_1bb_vs_btn, lambda v: setattr(self, 'call_1bb_vs_btn', v)),
            "vs_SB": (self.call_1bb_vs_sb, lambda v: setattr(self, 'call_1bb_vs_sb', v))
        })
        layout_call.addWidget(frame_call_1bb)
        
        frame_call_2bb = self.create_push_fold_call_frame("2BB Stack Call Ranges", {
            "vs_EP": (self.call_2bb_vs_ep, lambda v: setattr(self, 'call_2bb_vs_ep', v)),
            "vs_MP": (self.call_2bb_vs_mp, lambda v: setattr(self, 'call_2bb_vs_mp', v)),
            "vs_CO": (self.call_2bb_vs_co, lambda v: setattr(self, 'call_2bb_vs_co', v)),
            "vs_BTN": (self.call_2bb_vs_btn, lambda v: setattr(self, 'call_2bb_vs_btn', v)),
            "vs_SB": (self.call_2bb_vs_sb, lambda v: setattr(self, 'call_2bb_vs_sb', v))
        })
        layout_call.addWidget(frame_call_2bb)
        
        frame_call_3bb = self.create_push_fold_call_frame("3BB Stack Call Ranges", {
            "vs_EP": (self.call_3bb_vs_ep, lambda v: setattr(self, 'call_3bb_vs_ep', v)),
            "vs_MP": (self.call_3bb_vs_mp, lambda v: setattr(self, 'call_3bb_vs_mp', v)),
            "vs_CO": (self.call_3bb_vs_co, lambda v: setattr(self, 'call_3bb_vs_co', v)),
            "vs_BTN": (self.call_3bb_vs_btn, lambda v: setattr(self, 'call_3bb_vs_btn', v)),
            "vs_SB": (self.call_3bb_vs_sb, lambda v: setattr(self, 'call_3bb_vs_sb', v))
        })
        layout_call.addWidget(frame_call_3bb)
        
        frame_call_4bb = self.create_push_fold_call_frame("4BB Stack Call Ranges", {
            "vs_EP": (self.call_4bb_vs_ep, lambda v: setattr(self, 'call_4bb_vs_ep', v)),
            "vs_MP": (self.call_4bb_vs_mp, lambda v: setattr(self, 'call_4bb_vs_mp', v)),
            "vs_CO": (self.call_4bb_vs_co, lambda v: setattr(self, 'call_4bb_vs_co', v)),
            "vs_BTN": (self.call_4bb_vs_btn, lambda v: setattr(self, 'call_4bb_vs_btn', v)),
            "vs_SB": (self.call_4bb_vs_sb, lambda v: setattr(self, 'call_4bb_vs_sb', v))
        })
        layout_call.addWidget(frame_call_4bb)
        
        frame_call_5bb = self.create_push_fold_call_frame("5BB Stack Call Ranges", {
            "vs_EP": (self.call_5bb_vs_ep, lambda v: setattr(self, 'call_5bb_vs_ep', v)),
            "vs_MP": (self.call_5bb_vs_mp, lambda v: setattr(self, 'call_5bb_vs_mp', v)),
            "vs_CO": (self.call_5bb_vs_co, lambda v: setattr(self, 'call_5bb_vs_co', v)),
            "vs_BTN": (self.call_5bb_vs_btn, lambda v: setattr(self, 'call_5bb_vs_btn', v)),
            "vs_SB": (self.call_5bb_vs_sb, lambda v: setattr(self, 'call_5bb_vs_sb', v))
        })
        layout_call.addWidget(frame_call_5bb)
        
        frame_call_6_10bb = self.create_push_fold_call_frame("6-10BB Stack Call Ranges", {
            "vs_EP": (self.call_6_10bb_vs_ep, lambda v: setattr(self, 'call_6_10bb_vs_ep', v)),
            "vs_MP": (self.call_6_10bb_vs_mp, lambda v: setattr(self, 'call_6_10bb_vs_mp', v)),
            "vs_CO": (self.call_6_10bb_vs_co, lambda v: setattr(self, 'call_6_10bb_vs_co', v)),
            "vs_BTN": (self.call_6_10bb_vs_btn, lambda v: setattr(self, 'call_6_10bb_vs_btn', v)),
            "vs_SB": (self.call_6_10bb_vs_sb, lambda v: setattr(self, 'call_6_10bb_vs_sb', v))
        })
        layout_call.addWidget(frame_call_6_10bb)
        
        frame_call_10_15bb = self.create_push_fold_call_frame("10-15BB Stack Call Ranges", {
            "vs_EP": (self.call_10_15bb_vs_ep, lambda v: setattr(self, 'call_10_15bb_vs_ep', v)),
            "vs_MP": (self.call_10_15bb_vs_mp, lambda v: setattr(self, 'call_10_15bb_vs_mp', v)),
            "vs_CO": (self.call_10_15bb_vs_co, lambda v: setattr(self, 'call_10_15bb_vs_co', v)),
            "vs_BTN": (self.call_10_15bb_vs_btn, lambda v: setattr(self, 'call_10_15bb_vs_btn', v)),
            "vs_SB": (self.call_10_15bb_vs_sb, lambda v: setattr(self, 'call_10_15bb_vs_sb', v))
        })
        layout_call.addWidget(frame_call_10_15bb)
        
        frame_call_15_25bb = self.create_push_fold_call_frame("15-25BB Stack Call Ranges", {
            "vs_EP": (self.call_15_25bb_vs_ep, lambda v: setattr(self, 'call_15_25bb_vs_ep', v)),
            "vs_MP": (self.call_15_25bb_vs_mp, lambda v: setattr(self, 'call_15_25bb_vs_mp', v)),
            "vs_CO": (self.call_15_25bb_vs_co, lambda v: setattr(self, 'call_15_25bb_vs_co', v)),
            "vs_BTN": (self.call_15_25bb_vs_btn, lambda v: setattr(self, 'call_15_25bb_vs_btn', v)),
            "vs_SB": (self.call_15_25bb_vs_sb, lambda v: setattr(self, 'call_15_25bb_vs_sb', v))
        })
        layout_call.addWidget(frame_call_15_25bb)
        
    def create_push_fold_position_frame(self, title, position_vars):
        """Create a frame with sliders for each position"""
        frame = QGroupBox(title)
        layout = QGridLayout(frame)
        
        row = 0
        position_names = {
            "EP": "Early Position", 
            "MP": "Middle Position", 
            "CO": "Cutoff", 
            "BTN": "Button", 
            "SB": "Small Blind", 
            "BB": "Big Blind"
        }
        
        for pos, (value, setter) in position_vars.items():
            layout.addWidget(QLabel(f"{position_names[pos]} (%):"), row, 0)
            
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(value)
            label = QLabel(str(value))
            
            # Connect the value change to update both the label and the attribute
            slider.valueChanged.connect(lambda v, lbl=label, set_fn=setter: (lbl.setText(str(v)), set_fn(v)))
            
            layout.addWidget(slider, row, 1)
            layout.addWidget(label, row, 2)
            row += 1
        
        return frame

    def create_push_fold_call_frame(self, title, position_vars):
        """Create a frame with sliders for calling each position"""
        frame = QGroupBox(title)
        layout = QGridLayout(frame)
        
        row = 0
        position_names = {
            "vs_EP": "vs Early Position", 
            "vs_MP": "vs Middle Position", 
            "vs_CO": "vs Cutoff", 
            "vs_BTN": "vs Button", 
            "vs_SB": "vs Small Blind"
        }
        
        for pos, (value, setter) in position_vars.items():
            layout.addWidget(QLabel(f"{position_names[pos]} (%):"), row, 0)
            
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(value)
            label = QLabel(str(value))
            
            # Connect the value change to update both the label and the attribute
            slider.valueChanged.connect(lambda v, lbl=label, set_fn=setter: (lbl.setText(str(v)), set_fn(v)))
            
            layout.addWidget(slider, row, 1)
            layout.addWidget(label, row, 2)
            row += 1
        
        return frame
        
    def collect_preflop_settings(self):
        """Gather all preflop settings from the UI into a dictionary"""
        return {
            "num_players": int(self.num_players_combo.currentText()),
            "game_type": self.game_type_combo.currentText(),
            "aggression": self.aggression_slider.value(),
            "tightness": self.tightness_slider.value(),
            "limp_frequency": 30,  # Fixed value now
            "threebet_frequency": 40,  # Fixed value now
            "fourbet_frequency": 30,  # Fixed value now
            "squeeze_frequency": 35,  # Fixed value now
            "open_raise_size": self.open_raise_combo.currentText(),
            "ep_range": self.ep_range_slider.value(),
            "mp_range": self.mp_range_slider.value(),
            "lp_range": self.lp_range_slider.value(),
            "ep_sizing": self.ep_sizing_combo.currentText(),
            "mp_sizing": self.mp_sizing_combo.currentText(),
            "lp_sizing": self.lp_sizing_combo.currentText(),
            "call_3bet_range": self.call_3bet_range_slider.value(),
            "fourbet_range": self.fourbet_range_slider.value(),
            "ip_3bet_adjust": self.ip_3bet_adjust_slider.value(),
            "vs_lp_3bet_adjust": self.vs_lp_3bet_adjust_slider.value(),
            "call_4bet_range": self.call_4bet_range_slider.value(),
            "fivebet_range": self.fivebet_range_slider.value(),
            "short_stack_4bet": self.short_stack_4bet_slider.value(),
            "squeeze_1caller": self.squeeze_1caller_slider.value(),
            "squeeze_multi": self.squeeze_multi_slider.value(),
            "squeeze_sizing": self.squeeze_sizing_combo.currentText(),
            "blinds_squeeze": self.blinds_squeeze_slider.value(),
            "btn_squeeze": self.btn_squeeze_slider.value(),
            "push_1bb_ep": self.push_1bb_ep,
            "push_1bb_mp": self.push_1bb_mp,
            "push_1bb_co": self.push_1bb_co,
            "push_1bb_btn": self.push_1bb_btn,
            "push_1bb_sb": self.push_1bb_sb,
            "push_1bb_bb": self.push_1bb_bb,
            "call_1bb_vs_ep": self.call_1bb_vs_ep,
            "call_1bb_vs_mp": self.call_1bb_vs_mp,
            "call_1bb_vs_co": self.call_1bb_vs_co,
            "call_1bb_vs_btn": self.call_1bb_vs_btn,
            "call_1bb_vs_sb": self.call_1bb_vs_sb,
            
            # 2BB-5BB stack ranges
            "push_2bb_ep": self.push_2bb_ep,
            "push_2bb_mp": self.push_2bb_mp,
            "push_2bb_co": self.push_2bb_co,
            "push_2bb_btn": self.push_2bb_btn,
            "push_2bb_sb": self.push_2bb_sb,
            "push_2bb_bb": self.push_2bb_bb,
            
            "push_3bb_ep": self.push_3bb_ep,
            "push_3bb_mp": self.push_3bb_mp,
            "push_3bb_co": self.push_3bb_co,
            "push_3bb_btn": self.push_3bb_btn,
            "push_3bb_sb": self.push_3bb_sb,
            "push_3bb_bb": self.push_3bb_bb,
            
            "push_4bb_ep": self.push_4bb_ep,
            "push_4bb_mp": self.push_4bb_mp,
            "push_4bb_co": self.push_4bb_co,
            "push_4bb_btn": self.push_4bb_btn,
            "push_4bb_sb": self.push_4bb_sb,
            "push_4bb_bb": self.push_4bb_bb,
            
            "push_5bb_ep": self.push_5bb_ep,
            "push_5bb_mp": self.push_5bb_mp,
            "push_5bb_co": self.push_5bb_co,
            "push_5bb_btn": self.push_5bb_btn,
            "push_5bb_sb": self.push_5bb_sb,
            "push_5bb_bb": self.push_5bb_bb,
            
            # 6BB-10BB stack ranges
            "push_6bb_ep": self.push_6bb_ep,
            "push_6bb_mp": self.push_6bb_mp,
            "push_6bb_co": self.push_6bb_co,
            "push_6bb_btn": self.push_6bb_btn,
            "push_6bb_sb": self.push_6bb_sb,
            "push_6bb_bb": self.push_6bb_bb,
            
            "push_7bb_ep": self.push_7bb_ep,
            "push_7bb_mp": self.push_7bb_mp,
            "push_7bb_co": self.push_7bb_co,
            "push_7bb_btn": self.push_7bb_btn,
            "push_7bb_sb": self.push_7bb_sb,
            "push_7bb_bb": self.push_7bb_bb,
            
            "push_8bb_ep": self.push_8bb_ep,
            "push_8bb_mp": self.push_8bb_mp,
            "push_8bb_co": self.push_8bb_co,
            "push_8bb_btn": self.push_8bb_btn,
            "push_8bb_sb": self.push_8bb_sb,
            "push_8bb_bb": self.push_8bb_bb,
            
            "push_9bb_ep": self.push_9bb_ep,
            "push_9bb_mp": self.push_9bb_mp,
            "push_9bb_co": self.push_9bb_co,
            "push_9bb_btn": self.push_9bb_btn,
            "push_9bb_sb": self.push_9bb_sb,
            "push_9bb_bb": self.push_9bb_bb,
            
            "push_10bb_ep": self.push_10bb_ep,
            "push_10bb_mp": self.push_10bb_mp,
            "push_10bb_co": self.push_10bb_co,
            "push_10bb_btn": self.push_10bb_btn,
            "push_10bb_sb": self.push_10bb_sb,
            "push_10bb_bb": self.push_10bb_bb,
            
            # Call ranges
            "call_2bb_vs_ep": self.call_2bb_vs_ep,
            "call_2bb_vs_mp": self.call_2bb_vs_mp,
            "call_2bb_vs_co": self.call_2bb_vs_co,
            "call_2bb_vs_btn": self.call_2bb_vs_btn,
            "call_2bb_vs_sb": self.call_2bb_vs_sb,
            
            "call_3bb_vs_ep": self.call_3bb_vs_ep,
            "call_3bb_vs_mp": self.call_3bb_vs_mp,
            "call_3bb_vs_co": self.call_3bb_vs_co,
            "call_3bb_vs_btn": self.call_3bb_vs_btn,
            "call_3bb_vs_sb": self.call_3bb_vs_sb,
            
            "call_4bb_vs_ep": self.call_4bb_vs_ep,
            "call_4bb_vs_mp": self.call_4bb_vs_mp,
            "call_4bb_vs_co": self.call_4bb_vs_co,
            "call_4bb_vs_btn": self.call_4bb_vs_btn,
            "call_4bb_vs_sb": self.call_4bb_vs_sb,
            
            "call_5bb_vs_ep": self.call_5bb_vs_ep,
            "call_5bb_vs_mp": self.call_5bb_vs_mp,
            "call_5bb_vs_co": self.call_5bb_vs_co,
            "call_5bb_vs_btn": self.call_5bb_vs_btn,
            "call_5bb_vs_sb": self.call_5bb_vs_sb,
            
            "call_6_10bb_vs_ep": self.call_6_10bb_vs_ep,
            "call_6_10bb_vs_mp": self.call_6_10bb_vs_mp,
            "call_6_10bb_vs_co": self.call_6_10bb_vs_co,
            "call_6_10bb_vs_btn": self.call_6_10bb_vs_btn,
            "call_6_10bb_vs_sb": self.call_6_10bb_vs_sb,
            
            # 10BB+ stack ranges
            "push_10_15bb_ep": self.push_10_15bb_ep,
            "push_10_15bb_mp": self.push_10_15bb_mp,
            "push_10_15bb_co": self.push_10_15bb_co,
            "push_10_15bb_btn": self.push_10_15bb_btn,
            "push_10_15bb_sb": self.push_10_15bb_sb,
            "push_10_15bb_bb": self.push_10_15bb_bb,
            
            "push_15_20bb_ep": self.push_15_20bb_ep,
            "push_15_20bb_mp": self.push_15_20bb_mp,
            "push_15_20bb_co": self.push_15_20bb_co,
            "push_15_20bb_btn": self.push_15_20bb_btn,
            "push_15_20bb_sb": self.push_15_20bb_sb,
            "push_15_20bb_bb": self.push_15_20bb_bb,
            
            "push_20_25bb_ep": self.push_20_25bb_ep,
            "push_20_25bb_mp": self.push_20_25bb_mp,
            "push_20_25bb_co": self.push_20_25bb_co,
            "push_20_25bb_btn": self.push_20_25bb_btn,
            "push_20_25bb_sb": self.push_20_25bb_sb,
            "push_20_25bb_bb": self.push_20_25bb_bb,
            
            "call_10_15bb_vs_ep": self.call_10_15bb_vs_ep,
            "call_10_15bb_vs_mp": self.call_10_15bb_vs_mp,
            "call_10_15bb_vs_co": self.call_10_15bb_vs_co,
            "call_10_15bb_vs_btn": self.call_10_15bb_vs_btn,
            "call_10_15bb_vs_sb": self.call_10_15bb_vs_sb,
            
            "call_15_25bb_vs_ep": self.call_15_25bb_vs_ep,
            "call_15_25bb_vs_mp": self.call_15_25bb_vs_mp,
            "call_15_25bb_vs_co": self.call_15_25bb_vs_co,
            "call_15_25bb_vs_btn": self.call_15_25bb_vs_btn,
            "call_15_25bb_vs_sb": self.call_15_25bb_vs_sb
        }
    
    def collect_flop_settings(self):
        """Gather all flop settings from the UI into a dictionary"""
        return {
            "ip_cbet_freq": self.ip_cbet_freq_slider.value(),
            "oop_cbet_freq": self.oop_cbet_freq_slider.value(),
            "ip_cbet_size": self.ip_cbet_size_combo.currentText(),
            "oop_cbet_size": self.oop_cbet_size_combo.currentText(),
            "dry_board_adjust": self.dry_board_adjust_slider.value(),
            "wet_board_adjust": self.wet_board_adjust_slider.value(), 
            "checkraise_defense": self.checkraise_defense_slider.value(),
            "donk_response": self.donk_response_combo.currentText(),
            "value_aggression": self.value_aggression_slider.value(),
            "draw_aggression": self.draw_aggression_slider.value(),
            "semibluff_freq": self.semibluff_freq_slider.value(),
            "multiway_cbet_freq": self.multiway_cbet_freq_slider.value(),
            "multiway_value_range": self.multiway_value_range_slider.value(),
            "aggression": self.aggression_slider.value()  # Including global aggression for adjustments
        }
    
    def collect_turn_settings(self):
        """Gather all turn settings from the UI into a dictionary"""
        return {
            "second_barrel_freq": self.second_barrel_freq_slider.value(),
            "delayed_cbet_freq": self.delayed_cbet_freq_slider.value(),
            "ip_turn_bet_size": self.ip_turn_bet_size_combo.currentText(),
            "oop_turn_bet_size": self.oop_turn_bet_size_combo.currentText(),
            "turn_checkraise_freq": self.turn_checkraise_freq_slider.value(),
            "turn_float_freq": self.turn_float_freq_slider.value(),
            "turn_probe_freq": self.turn_probe_freq_slider.value(),
            "turn_fold_to_cbet_freq": self.turn_fold_to_cbet_freq_slider.value(),
            "turn_bluff_raise_freq": self.turn_bluff_raise_freq_slider.value(),
            "scare_card_adjust": self.scare_card_adjust_slider.value(),
            "draw_complete_adjust": self.draw_complete_adjust_slider.value(),
            "aggression": self.aggression_slider.value()  # Including global aggression for adjustments
        }
    
    def collect_river_settings(self):
        """Gather all river settings from the UI into a dictionary"""
        return {
            "third_barrel_freq": self.third_barrel_freq_slider.value(),
            "delayed_second_barrel_freq": self.delayed_second_barrel_freq_slider.value(),
            "ip_river_bet_size": self.ip_river_bet_size_combo.currentText(),
            "oop_river_bet_size": self.oop_river_bet_size_combo.currentText(),
            "river_checkraise_freq": self.river_checkraise_freq_slider.value(),
            "river_float_freq": self.river_float_freq_slider.value(),
            "river_probe_freq": self.river_probe_freq_slider.value(),
            "river_fold_to_bet_freq": self.river_fold_to_bet_freq_slider.value(),
            "river_bluff_raise_freq": self.river_bluff_raise_freq_slider.value(),
            "river_value_range": self.river_value_range_slider.value(),
            "river_bluff_range": self.river_bluff_range_slider.value(),
            "river_check_behind_range": self.river_check_behind_range_slider.value(),
            "aggression": self.aggression_slider.value()  # Including global aggression for adjustments
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
        self.preview_text.setText(full_profile)
        
        QMessageBox.information(self, "Profile Generated", "OpenHoldem profile has been generated and is ready to save.")
        
    def save_profile(self):
        if not self.preview_text.toPlainText().strip():
            QMessageBox.warning(self, "Empty Profile", "Please generate a profile first.")
            return
            
        # Ask for save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Profile",
            "",
            "OpenHoldem Files (*.ohf);;Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.preview_text.toPlainText())
            QMessageBox.information(self, "Save Successful", f"Profile saved to {file_path}")
            
if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        
        # Définir le style Fusion comme base
        from PyQt6.QtWidgets import QStyleFactory
        app.setStyle("Fusion")
        
        # Appliquer une feuille de style personnalisée avec un thème sombre/violet
        qss = """
        QWidget {
            background-color: #14131B;
            color: #FFFFFF;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        QMainWindow, QDialog {
            background-color: #14131B;
        }
        
        QPushButton {
            background-color: #0a522c;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #9632E3;
        }
        
        QPushButton:pressed {
            background-color: #6215A3;
        }
        
        QLineEdit, QTextEdit, QComboBox {
            border: 1px solid #3F3D56;
            border-radius: 4px;
            padding: 6px;
            background-color: #1E1D2A;
            color: white;
        }
        
        QTextEdit {
            background-color: #1E1D2A;
        }
        
        QTabWidget::pane {
            border: 1px solid #3F3D56;
            background-color: #14131B;
        }
        
        QTabBar::tab {
            background-color: #1E1D2A;
            color: white;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: #0a522c;
        }
        
        QGroupBox {
            border: 1px solid #3F3D56;
            border-radius: 4px;
            margin-top: 16px;
            padding-top: 16px;
            color: white;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 10px;
            background-color: #14131B;
            color: white;
        }
        
        QSlider::groove:horizontal {
            border: none;
            height: 8px;
            background: #1E1D2A;
            margin: 2px 0;
            border-radius: 4px;
        }
        
        QSlider::handle:horizontal {
            background: #0a522c;
            border: none;
            width: 16px;
            height: 16px;
            margin: -4px 0;
            border-radius: 8px;
        }
        
        QScrollArea, QScrollBar {
            background-color: #14131B;
            border: none;
        }
        
        QScrollBar:vertical {
            background-color: #1E1D2A;
            width: 12px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #3F3D56;
            min-height: 20px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #0a522c;
        }
        
        QScrollBar:horizontal {
            background-color: #1E1D2A;
            height: 12px;
            margin: 0px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #3F3D56;
            min-width: 20px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #0a522c;
        }
        
        QScrollBar::add-line, QScrollBar::sub-line {
            width: 0px;
            height: 0px;
        }
        
        QLabel {
            color: white;
        }
        """
        
        app.setStyleSheet(qss)
        
        window = OpenHoldemProfileGenerator()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        import traceback
        print(f"An error occurred: {e}")
        print(traceback.format_exc())
        input("Press Enter to exit...")
