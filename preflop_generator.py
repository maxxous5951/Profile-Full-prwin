class PreflopProfileGenerator:
    def __init__(self):
        pass
        
    def get_handrank_threshold(self, percentage):
        """Convert a percentage into a handrank threshold value"""
        # HandRank goes from 1 to 169, where 1 is the best hand (AA)
        # Convert percentage to a hand rank value
        # 0% = only AA (rank 1)
        # 100% = all hands (rank 169)
        return round(1 + (percentage / 100) * 168)
        
    def calculate_raise_size(self, base_size, num_limpers=0, aggressive_factor=1.0):
        """Calculate raise size based on base size, number of limpers and aggression"""
        # Add 1BB for each limper
        size = float(base_size)
        if num_limpers > 0:
            size += num_limpers
        
        # Adjust size based on aggression
        # More aggressive = larger sizing (±20%)
        size *= (0.8 + (aggressive_factor * 0.4))
        
        return round(size, 1)
        
    def get_position_map(self, num_players):
        """Returns a map of which positions exist based on number of players"""
        positions = {
            "EP1": False,
            "EP2": False,
            "EP3": False,
            "MP1": False,
            "MP2": False,
            "MP3": False,
            "CO": False,
            "BTN": False,
            "SB": True,   # Always exists
            "BB": True    # Always exists
        }
        
        # Activate positions based on number of players
        if num_players >= 3:
            positions["BTN"] = True
        
        if num_players >= 4:
            positions["CO"] = True
            
        if num_players >= 5:
            positions["MP3"] = True
            
        if num_players >= 6:
            positions["MP2"] = True
            
        if num_players >= 7:
            positions["MP1"] = True
            
        if num_players >= 8:
            positions["EP3"] = True
            
        if num_players >= 9:
            positions["EP2"] = True
            positions["EP1"] = True
            
        return positions
    
    def generate_preflop_profile(self, settings):
        """Generate the preflop part of the OpenHoldem profile"""
        # Extract basic settings
        num_players = settings["num_players"]
        game_type = settings["game_type"]
        aggression = settings["aggression"]
        tightness = settings["tightness"]
        limp_frequency = settings["limp_frequency"]
        threebet_frequency = settings["threebet_frequency"]
        fourbet_frequency = settings["fourbet_frequency"]
        squeeze_frequency = settings["squeeze_frequency"]
        open_raise_size = settings["open_raise_size"]
        
        # Extract specific settings from tabs
        # Open Raise tab
        ep_range = settings["ep_range"]
        mp_range = settings["mp_range"]
        lp_range = settings["lp_range"] 
        ep_sizing = settings["ep_sizing"]
        mp_sizing = settings["mp_sizing"]
        lp_sizing = settings["lp_sizing"]
        
        # Facing 3-Bet tab
        call_3bet_range = settings["call_3bet_range"]
        fourbet_vs_3bet_range = settings["fourbet_range"]
        ip_3bet_adjust = settings["ip_3bet_adjust"] / 100.0  # Convert to decimal
        vs_lp_3bet_adjust = settings["vs_lp_3bet_adjust"] / 100.0  # Convert to decimal
        
        # Facing 4-Bet tab
        call_4bet_range = settings["call_4bet_range"]
        fivebet_range = settings["fivebet_range"]
        short_stack_4bet = settings["short_stack_4bet"] / 100.0  # Convert to decimal
        
        # Squeeze tab
        squeeze_1caller = settings["squeeze_1caller"]
        squeeze_multi = settings["squeeze_multi"]
        squeeze_sizing = settings["squeeze_sizing"]
        blinds_squeeze = settings["blinds_squeeze"] / 100.0  # Convert to decimal
        btn_squeeze = settings["btn_squeeze"] / 100.0  # Convert to decimal
        
        # Convert slider values to thresholds
        tight_threshold = self.get_handrank_threshold(tightness)
        aggressive_factor = aggression / 50  # 0-2 range where 1 is neutral
        limp_factor = limp_frequency / 50  # 0-2 range where 1 is default frequency
        
        # Specific thresholds for position-based ranges
        ep_raise_threshold = self.get_handrank_threshold(ep_range)
        mp_raise_threshold = self.get_handrank_threshold(mp_range)
        lp_raise_threshold = self.get_handrank_threshold(lp_range)
        
        # Specific thresholds for 3-bet/4-bet/squeeze reactions
        call_3bet_threshold = self.get_handrank_threshold(call_3bet_range)
        fourbet_vs_3bet_threshold = self.get_handrank_threshold(fourbet_vs_3bet_range)
        call_4bet_threshold = self.get_handrank_threshold(call_4bet_range)
        fivebet_threshold = self.get_handrank_threshold(fivebet_range)
        squeeze_1caller_threshold = self.get_handrank_threshold(squeeze_1caller)
        squeeze_multi_threshold = self.get_handrank_threshold(squeeze_multi)
        
        # Adjust 3bet/4bet/squeeze frequencies based on aggression
        # Higher aggression = higher 3bet/4bet frequencies
        threebet_adjustment = 1 + (aggressive_factor - 1) * 0.5  # 0.75-1.25 range
        fourbet_adjustment = 1 + (aggressive_factor - 1) * 0.6   # 0.7-1.3 range
        squeeze_adjustment = 1 + (aggressive_factor - 1) * 0.7   # 0.65-1.35 range
        
        # Apply aggression adjustments
        threebet_threshold = self.get_handrank_threshold(threebet_frequency * threebet_adjustment)
        fourbet_threshold = self.get_handrank_threshold(fourbet_frequency * fourbet_adjustment)
        squeeze_threshold = self.get_handrank_threshold(squeeze_frequency * squeeze_adjustment)
        
        # Determine which positions exist based on number of players
        position_map = self.get_position_map(num_players)
        
        # Adjust raise sizes based on aggression and position
        adjusted_open_raise = self.calculate_raise_size(open_raise_size, 0, aggressive_factor)
        ep_open_raise = self.calculate_raise_size(ep_sizing, 0, aggressive_factor)
        mp_open_raise = self.calculate_raise_size(mp_sizing, 0, aggressive_factor)
        lp_open_raise = self.calculate_raise_size(lp_sizing, 0, aggressive_factor)
        
        # Calculate squeeze size
        squeeze_bet_size = float(squeeze_sizing)
        adjusted_squeeze_size = self.calculate_raise_size(squeeze_sizing, 0, aggressive_factor * 1.2)  # More aggressive for squeezes
        
        # Generate the profile text using string concatenation instead of a single f-string
        # to avoid issues with very long strings
        profile = "//*****************************************************************************\n"
        profile += "//\n"
        profile += f"// OpenHoldem Profile Generator - Preflop Profile\n"
        profile += f"// Generated for {num_players}-player {game_type}\n"
        profile += "// \n"
        profile += f"// Strategy Settings:\n"
        profile += f"// - Aggression: {aggression}% (Factor: {aggressive_factor:.2f}x)\n"
        profile += f"// - Tightness: {tightness}%\n"
        profile += f"// - Limp Frequency: {limp_frequency}%\n"
        profile += f"// - 3-Bet Frequency: {threebet_frequency}% (Adjusted: {threebet_frequency * threebet_adjustment:.1f}%)\n"
        profile += f"// - 4-Bet Frequency: {fourbet_frequency}% (Adjusted: {fourbet_frequency * fourbet_adjustment:.1f}%)\n"
        profile += f"// - Squeeze Frequency: {squeeze_frequency}% (Adjusted: {squeeze_frequency * squeeze_adjustment:.1f}%)\n"
        profile += f"// - Open Raise Size: {open_raise_size}x (Adjusted: {adjusted_open_raise}x)\n"
        profile += "//\n"
        profile += "// Position-Based Settings:\n"
        profile += f"// - Early Position Range: {ep_range}% (Threshold: {ep_raise_threshold})\n"
        profile += f"// - Middle Position Range: {mp_range}% (Threshold: {mp_raise_threshold})\n"
        profile += f"// - Late Position Range: {lp_range}% (Threshold: {lp_raise_threshold})\n"
        profile += f"// - Squeeze vs 1 Caller: {squeeze_1caller}% (Threshold: {squeeze_1caller_threshold})\n"
        profile += f"// - Squeeze vs 2+ Callers: {squeeze_multi}% (Threshold: {squeeze_multi_threshold})\n"
        profile += "//\n"
        profile += "// Position Map for Table Size:\n"
        
        # Add position information
        for pos, exists in position_map.items():
            profile += f"// - {pos}: {'Active' if exists else 'Inactive'}\n"
            
        profile += "//\n"
        profile += "//*****************************************************************************\n\n"

        profile += "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// PREFLOP SCENARIOS\n"
        profile += "//\n"
        profile += "//*****************************************************************************\n\n"

        # Open Raise or Open Limp
        profile += "##f$OpenRaiseOrOpenLimp##\n"
        profile += "// No action (limp or raise) before us. Hero can Open the game by Raising or Limping\n"
        profile += "WHEN InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3 RETURN f$OpenRaise_EarlyPosition FORCE\n"
        profile += "WHEN InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3 RETURN f$OpenRaise_MiddlePosition FORCE\n"
        profile += "WHEN InCutOff OR InButton RETURN f$OpenRaise_LatePosition FORCE\n"
        profile += "WHEN InSmallBlind RETURN f$OpenRaise_SB FORCE\n"
        profile += "WHEN InBigBlind RETURN Check FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        # Early Position Open Raising
        profile += "##f$OpenRaise_EarlyPosition##\n"
        profile += f"WHEN handrank169 <= {ep_raise_threshold} RETURN {ep_open_raise} FORCE\n"
        profile += f"WHEN handrank169 <= {round(tight_threshold * 0.7 * limp_factor)} RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Middle Position Open Raising
        profile += "##f$OpenRaise_MiddlePosition##\n"
        profile += f"WHEN handrank169 <= {mp_raise_threshold} RETURN {mp_open_raise} FORCE\n"
        profile += f"WHEN handrank169 <= {round(tight_threshold * 0.85 * limp_factor)} RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Late Position Open Raising
        profile += "##f$OpenRaise_LatePosition##\n"
        profile += f"WHEN handrank169 <= {lp_raise_threshold} RETURN {lp_open_raise} FORCE\n"
        profile += f"WHEN handrank169 <= {round(tight_threshold * limp_factor)} RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"
        
        # Small Blind Open Raising
        profile += "##f$OpenRaise_SB##\n"
        profile += f"WHEN handrank169 <= {round(lp_raise_threshold * 0.9)} RETURN {lp_open_raise} FORCE\n"
        profile += f"WHEN handrank169 <= {round(tight_threshold * 0.9 * limp_factor)} RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        # Limp Or Isolate Limpers
        profile += "##f$LimpOrIsolateLimpers##\n"
        profile += "// 1 or more limps before us. Hero can Limp too or Raise to isolate the limpers\n"
        profile += "WHEN f$LimpOrIsolateLimpers_Decision = 2 RETURN f$IsolateSize FORCE\n"
        profile += "WHEN f$LimpOrIsolateLimpers_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        # Isolate sizing calculation based on number of limpers
        profile += "##f$IsolateSize##\n"
        profile += f"// Base open size: {open_raise_size}BB plus 1BB per limper\n"
        profile += f"Calls * 1 + {adjusted_open_raise}\n\n"

        profile += "##f$LimpOrIsolateLimpers_Decision##\n"
        profile += "// 0 = Fold, 1 = Limp, 2 = Raise\n"
        profile += "// More aggressive with fewer limpers, tighter with more\n"
        profile += f"WHEN Calls = 1 AND handrank169 <= {round(tight_threshold * 0.7)} RETURN 2 FORCE\n"
        profile += f"WHEN Calls = 1 AND handrank169 <= {round(tight_threshold * 0.9 * limp_factor)} RETURN 1 FORCE\n\n"

        profile += f"WHEN Calls = 2 AND handrank169 <= {round(tight_threshold * 0.6)} RETURN 2 FORCE\n"
        profile += f"WHEN Calls = 2 AND handrank169 <= {round(tight_threshold * 0.85 * limp_factor)} RETURN 1 FORCE\n\n"

        profile += f"WHEN Calls >= 3 AND handrank169 <= {round(tight_threshold * 0.5)} RETURN 2 FORCE\n"
        profile += f"WHEN Calls >= 3 AND handrank169 <= {round(tight_threshold * 0.8 * limp_factor)} RETURN 1 FORCE\n\n"

        profile += "// Position based adjustments - more aggressive in position\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(tight_threshold * 0.75)} RETURN 2 FORCE\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(tight_threshold * 0.65)} RETURN 2 FORCE\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Three Bet Cold Call
        profile += "##f$ThreeBetColdCall##\n"
        profile += "// 1 Raise before Hero first action and No villains call. Hero can 3Bet, ColdCall or Fold\n"
        profile += "WHEN f$ThreeBetColdCall_Decision = 2 RETURN RaisePot FORCE\n"
        profile += "WHEN f$ThreeBetColdCall_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$ThreeBetColdCall_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = 3-Bet\n"
        profile += "// Early Position 3-bet\n"
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(threebet_threshold * 0.5)} RETURN 2 FORCE\n"
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(call_3bet_threshold * 0.6)} RETURN 1 FORCE\n\n"

        profile += "// Middle Position 3-bet\n"
        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(threebet_threshold * 0.65)} RETURN 2 FORCE\n"
        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(call_3bet_threshold * 0.7)} RETURN 1 FORCE\n\n"

        profile += "// Late Position 3-bet\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(threebet_threshold * 0.8)} RETURN 2 FORCE\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(call_3bet_threshold * 0.8)} RETURN 1 FORCE\n\n"

        profile += "// Blinds 3-bet\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(threebet_threshold * 0.7)} RETURN 2 FORCE\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(call_3bet_threshold * 0.75)} RETURN 1 FORCE\n\n"

        profile += "// Against specific positions - 3-bet looser against late position raises\n"
        profile += f"WHEN (DealPositionLastRaiser >= nplayersdealt - 2) AND handrank169 <= {round(threebet_threshold * (1 + vs_lp_3bet_adjust))} RETURN 2 FORCE\n"
        profile += f"WHEN (DealPositionLastRaiser >= nplayersdealt - 2) AND handrank169 <= {round(call_3bet_threshold * (1 + vs_lp_3bet_adjust))} RETURN 1 FORCE\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Squeeze Cold Call
        profile += "##f$SqueezeColdCall##\n"
        profile += "// 1 Raise before Hero first action and 1 or more villains calls. Hero can Squeeze, ColdCall or Fold\n"
        profile += f"WHEN f$SqueezeColdCall_Decision = 2 RETURN {adjusted_squeeze_size} * pot FORCE\n" 
        profile += "WHEN f$SqueezeColdCall_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$SqueezeColdCall_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = Squeeze\n"
        profile += "// Tighter squeeze range with more players in the pot\n"
        profile += f"WHEN CallsSinceLastRaise = 1 AND handrank169 <= {squeeze_1caller_threshold} RETURN 2 FORCE\n"
        profile += f"WHEN CallsSinceLastRaise = 1 AND handrank169 <= {round(tight_threshold * 0.7)} RETURN 1 FORCE\n\n"

        profile += f"WHEN CallsSinceLastRaise = 2 AND handrank169 <= {squeeze_multi_threshold} RETURN 2 FORCE\n"
        profile += f"WHEN CallsSinceLastRaise = 2 AND handrank169 <= {round(tight_threshold * 0.65)} RETURN 1 FORCE\n\n"

        profile += f"WHEN CallsSinceLastRaise >= 3 AND handrank169 <= {round(squeeze_multi_threshold * 0.8)} RETURN 2 FORCE\n"
        profile += f"WHEN CallsSinceLastRaise >= 3 AND handrank169 <= {round(tight_threshold * 0.6)} RETURN 1 FORCE\n\n"

        profile += "// Position-based adjustments\n"
        profile += f"WHEN (InButton) AND handrank169 <= {round(squeeze_1caller_threshold * (1 + btn_squeeze))} RETURN 2 FORCE\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(squeeze_1caller_threshold * (1 + blinds_squeeze))} RETURN 2 FORCE\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 3Bet Before First Action
        profile += "##f$Facing3BetBeforeFirstAction##\n"
        profile += "// 3bet or squeeze before Hero first action. Hero can 4Bet, ColdCall or Fold\n"
        profile += "WHEN f$Facing3BetBeforeFirstAction_Decision = 2 RETURN RaisePot FORCE\n"
        profile += "WHEN f$Facing3BetBeforeFirstAction_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$Facing3BetBeforeFirstAction_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = 4-Bet\n"
        profile += "// Very tight 4-betting range from early position\n"
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.4)} RETURN 2 FORCE\n"
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(call_3bet_threshold * 0.5)} RETURN 1 FORCE\n\n"

        profile += "// Middle position\n"
        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.5)} RETURN 2 FORCE\n"
        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(call_3bet_threshold * 0.55)} RETURN 1 FORCE\n\n"

        profile += "// Late position\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.6)} RETURN 2 FORCE\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(call_3bet_threshold * 0.6)} RETURN 1 FORCE\n\n"

        profile += "// Blinds\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.55)} RETURN 2 FORCE\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(call_3bet_threshold * 0.55)} RETURN 1 FORCE\n\n"

        profile += "// Stack depth considerations\n"
        profile += f"WHEN StackSize < 50 AND handrank169 <= {round(fourbet_vs_3bet_threshold * (1 + short_stack_4bet))} RETURN 2 FORCE\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 4Bet Before First Action
        profile += "##f$Facing4BetBeforeFirstAction##\n"
        profile += "// 4bet before Hero first action. Hero can 5Bet, ColdCall or Fold\n"
        profile += "WHEN f$Facing4BetBeforeFirstAction_Decision = 2 RETURN RaiseMax FORCE\n"
        profile += "WHEN f$Facing4BetBeforeFirstAction_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$Facing4BetBeforeFirstAction_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = 5-Bet (All-In)\n"
        profile += f"WHEN handrank169 <= {fivebet_threshold} RETURN 2 FORCE\n"
        profile += f"WHEN handrank169 <= {call_4bet_threshold} RETURN 1 FORCE\n"
        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 5Bet Before First Action
        profile += "##f$Facing5BetBeforeFirstAction##\n"
        profile += "// 5bet before Hero first action. Hero can Push, ColdCall or Fold\n"
        profile += f"WHEN handrank169 <= {round(fivebet_threshold * 0.8)} RETURN RaiseMax FORCE\n"
        profile += f"WHEN handrank169 <= {round(call_4bet_threshold * 0.8)} RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        # Facing 3Bet
        profile += "##f$Facing3Bet##\n"
        profile += "// Hero is the Original Raiser and Facing 3Bet. Hero can 4Bet, Call or Fold\n"
        profile += "WHEN f$Facing3Bet_Decision = 2 RETURN RaisePot FORCE\n"
        profile += "WHEN f$Facing3Bet_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$Facing3Bet_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = 4-Bet\n"
        profile += "// Adjust based on position\n"
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.45)} RETURN 2 FORCE\n"
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(call_3bet_threshold * 0.55)} RETURN 1 FORCE\n\n"

        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.55)} RETURN 2 FORCE\n"
        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(call_3bet_threshold * 0.6)} RETURN 1 FORCE\n\n"

        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.65)} RETURN 2 FORCE\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(call_3bet_threshold * 0.7)} RETURN 1 FORCE\n\n"

        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.6)} RETURN 2 FORCE\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(call_3bet_threshold * 0.65)} RETURN 1 FORCE\n\n"

        profile += "// Position adjustment - more aggressive in position\n"
        profile += f"WHEN f$InPosition AND handrank169 <= {round(fourbet_vs_3bet_threshold * (1 + ip_3bet_adjust))} RETURN 2 FORCE\n"
        profile += f"WHEN f$InPosition AND handrank169 <= {round(call_3bet_threshold * (1 + ip_3bet_adjust))} RETURN 1 FORCE\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # In Position helper function
        profile += "##f$InPosition##\n"
        profile += "// Helper function to determine if we're in position vs the 3bettor\n"
        profile += "WHEN LastAggressorActsAfterUs RETURN false FORCE\n"
        profile += "WHEN Others RETURN true FORCE\n\n"

        # Facing Squeeze
        profile += "##f$FacingSqueeze##\n"
        profile += "// Hero is the Original Raiser and Facing Squeeze by an opponent. Hero can 4Bet, Call or Fold\n"
        profile += "WHEN f$FacingSqueeze_Decision = 2 RETURN RaisePot FORCE\n"
        profile += "WHEN f$FacingSqueeze_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$FacingSqueeze_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = 4-Bet\n"
        profile += "// Generally tighter than regular 3-bet defense\n"
        profile += f"WHEN handrank169 <= {round(fourbet_vs_3bet_threshold * 0.5)} RETURN 2 FORCE\n"
        profile += f"WHEN handrank169 <= {round(call_3bet_threshold * 0.55)} RETURN 1 FORCE\n\n"

        profile += "// Adjust based on number of callers between raise and squeeze\n"
        profile += f"WHEN CallsSinceLastRaise = 1 AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.55)} RETURN 2 FORCE\n"
        profile += f"WHEN CallsSinceLastRaise >= 2 AND handrank169 <= {round(fourbet_vs_3bet_threshold * 0.45)} RETURN 2 FORCE\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 4Bet
        profile += "##f$Facing4Bet##\n"
        profile += "// Hero 3bet and facing 4bet. Hero can 5bet, Call or Fold\n"
        profile += "WHEN f$Facing4Bet_Decision = 2 RETURN RaiseMax FORCE\n"
        profile += "WHEN f$Facing4Bet_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$Facing4Bet_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = 5-Bet (All-In)\n"
        profile += f"WHEN handrank169 <= {fivebet_threshold} RETURN 2 FORCE\n"
        profile += f"WHEN handrank169 <= {call_4bet_threshold} RETURN 1 FORCE\n"
        profile += "// Stack depth considerations\n"
        profile += f"WHEN StackSize < 50 AND handrank169 <= {round(fivebet_threshold * (1 + short_stack_4bet))} RETURN 2 FORCE\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 5Bet
        profile += "##f$Facing5Bet##\n"
        profile += "// Hero 4bet and facing 5bet. Hero can Push, Call or Fold\n"
        profile += f"WHEN handrank169 <= {round(fivebet_threshold * 0.8)} RETURN RaiseMax FORCE\n"
        profile += f"WHEN handrank169 <= {round(call_4bet_threshold * 0.6)} RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        # Additional functions
        profile += "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// ADDITIONAL FUNCTIONS\n"
        profile += "//\n"
        profile += "//*****************************************************************************\n\n"

        # Main preflop function
        profile += "##f$preflop##\n"
        profile += "// Main preflop decision function that uses OpenPPL library functions\n"
        profile += "// to detect scenarios and then calls our decision functions\n\n"

        profile += "// Open Raise or Open Limp\n"
        profile += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 0 AND Calls = 0) RETURN f$OpenRaiseOrOpenLimp FORCE\n\n"

        profile += "// Limp or Isolate Limpers\n"
        profile += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 0 AND Calls >= 1) RETURN f$LimpOrIsolateLimpers FORCE\n\n"

        profile += "// Three Bet or Cold Call\n"
        profile += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 1 AND CallsSinceLastRaise = 0) RETURN f$ThreeBetColdCall FORCE\n\n"

        profile += "// Squeeze or Cold Call\n"
        profile += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 1 AND CallsSinceLastRaise >= 1) RETURN f$SqueezeColdCall FORCE\n\n"

        profile += "// Facing 3-Bet Before First Action\n"
        profile += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 2) RETURN f$Facing3BetBeforeFirstAction FORCE\n\n"

        profile += "// Facing 4-Bet Before First Action\n"
        profile += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 3) RETURN f$Facing4BetBeforeFirstAction FORCE\n\n"

        profile += "// Facing 5-Bet Before First Action\n"
        profile += "WHEN (BotsActionsOnThisRoundIncludingChecks = 0 AND Raises = 4) RETURN f$Facing5BetBeforeFirstAction FORCE\n\n"

        profile += "// Facing 3-Bet\n"
        profile += "WHEN (BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 1 AND NumberOfRaisesBeforeFlop = 1 AND Calls = 0 AND RaisesSinceLastPlay = 1) RETURN f$Facing3Bet FORCE\n\n"

        profile += "// Facing Squeeze\n"
        profile += "WHEN (BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 1 AND NumberOfRaisesBeforeFlop = 1 AND Calls >= 1 AND RaisesSinceLastPlay = 1) RETURN f$FacingSqueeze FORCE\n\n"

        profile += "// Facing 4-Bet\n"
        profile += "WHEN (BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 1 AND NumberOfRaisesBeforeFlop = 2 AND RaisesSinceLastPlay = 1) RETURN f$Facing4Bet FORCE\n\n"

        profile += "// Facing 5-Bet\n"
        profile += "WHEN (BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 2 AND NumberOfRaisesBeforeFlop = 2 AND RaisesSinceLastPlay = 1) RETURN f$Facing5Bet FORCE\n\n"

        profile += "// Default action if no scenario is matched\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        # Post-flop placeholders (to be expanded later)
        profile += "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// POST-FLOP PLACEHOLDERS\n"
        profile += "// These are basic placeholders that would need to be expanded\n"
        profile += "//\n"
        profile += "//*****************************************************************************\n\n"

        profile += "##f$flop##\n"
        profile += "// Basic C-bet strategy\n"
        profile += "WHEN BotRaisedBeforeFlop AND BotsActionsOnThisRoundIncludingChecks = 0 AND f$InPosition RETURN BetHalfPot FORCE\n"
        profile += "WHEN HaveTopPair OR HaveOverPair OR HaveStrongDraws RETURN BetHalfPot FORCE\n"
        profile += "WHEN Others RETURN Check FORCE\n\n"

        profile += "##f$HaveStrongDraws##\n"
        profile += "// Strong draws worth betting\n"
        profile += "WHEN HaveFlushDraw OR HaveStraightDraw RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        profile += "##f$turn##\n"
        profile += "// Basic turn strategy\n"
        profile += "WHEN BotRaisedBeforeFlop AND BotRaisedOnFlop AND f$InPosition RETURN BetHalfPot FORCE\n"
        profile += "WHEN HaveTopPair OR BetterOrStrongDraw RETURN BetHalfPot FORCE\n"
        profile += "WHEN Others RETURN Check FORCE\n\n"

        profile += "##f$HaveTopPairOrBetterOrStrongDraw##\n"
        profile += "// Hand strong enough to bet on turn\n"
        profile += "WHEN HaveTopPair OR HaveOverPair OR HaveFlushDraw OR HaveStraightDraw OR HaveTwoPair OR Better RETURN true FORCE\n"
        profile += "WHEN Others RETURN false FORCE\n\n"

        profile += "##f$river##\n"
        profile += "// Basic river strategy\n"
        profile += "WHEN HaveTwoPair OR Better RETURN BetPot FORCE\n"
        profile += "WHEN Others RETURN Check FORCE\n\n"

        profile += "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// END OF PROFILE\n"
        profile += "//\n"
        profile += "//*****************************************************************************"
        
        return profile
