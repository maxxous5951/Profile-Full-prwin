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
        # Extract settings
        num_players = settings["num_players"]
        game_type = settings["game_type"]
        aggression = settings["aggression"]
        tightness = settings["tightness"]
        limp_frequency = settings["limp_frequency"]
        threebet_frequency = settings["threebet_frequency"]
        fourbet_frequency = settings["fourbet_frequency"]
        squeeze_frequency = settings["squeeze_frequency"]
        open_raise_size = settings["open_raise_size"]
        
        # Convert slider values to thresholds
        tight_threshold = self.get_handrank_threshold(tightness)
        aggressive_factor = aggression / 50  # 0-2 range where 1 is neutral
        limp_factor = limp_frequency / 50  # 0-2 range where 1 is default frequency
        
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
        
        # Adjust raise sizes based on aggression
        adjusted_open_raise = self.calculate_raise_size(open_raise_size, 0, aggressive_factor)
        
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
        profile += f"WHEN f$OpenRaiseOrOpenLimp_Decision = 2 RETURN {adjusted_open_raise} FORCE\n"
        profile += "WHEN f$OpenRaiseOrOpenLimp_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$OpenRaiseOrOpenLimp_Decision##\n"
        profile += "// 0 = Fold, 1 = Limp, 2 = Raise\n"
        
        # Only include positions that exist in this game format
        if position_map["EP1"] or position_map["EP2"] or position_map["EP3"]:
            profile += "// Early Position (Under the Gun, UTG+1, UTG+2)\n"
            ep_condition = []
            if position_map["EP1"]:
                ep_condition.append("InEarlyPosition1")
            if position_map["EP2"]:
                ep_condition.append("InEarlyPosition2") 
            if position_map["EP3"]:
                ep_condition.append("InEarlyPosition3")
            
            ep_condition_str = " OR ".join(ep_condition)
            profile += f"WHEN ({ep_condition_str}) AND (handrank169 <= {round(tight_threshold * 0.5)}) RETURN 2 FORCE\n"
            profile += f"WHEN ({ep_condition_str}) AND (handrank169 <= {round(tight_threshold * 0.7 * limp_factor)}) RETURN 1 FORCE\n\n"

        if position_map["MP1"] or position_map["MP2"] or position_map["MP3"]:
            profile += "// Middle Position (MP1, MP2, MP3)\n"
            mp_condition = []
            if position_map["MP1"]:
                mp_condition.append("InMiddlePosition1")
            if position_map["MP2"]:
                mp_condition.append("InMiddlePosition2") 
            if position_map["MP3"]:
                mp_condition.append("InMiddlePosition3")
            
            mp_condition_str = " OR ".join(mp_condition)
            profile += f"WHEN ({mp_condition_str}) AND (handrank169 <= {round(tight_threshold * 0.65)}) RETURN 2 FORCE\n"
            profile += f"WHEN ({mp_condition_str}) AND (handrank169 <= {round(tight_threshold * 0.85 * limp_factor)}) RETURN 1 FORCE\n\n"

        if position_map["CO"] or position_map["BTN"]:
            profile += "// Late Position (CO, BTN)\n"
            lp_condition = []
            if position_map["CO"]:
                lp_condition.append("InCutOff")
            if position_map["BTN"]:
                lp_condition.append("InButton") 
            
            lp_condition_str = " OR ".join(lp_condition)
            profile += f"WHEN ({lp_condition_str}) AND (handrank169 <= {round(tight_threshold * 0.8)}) RETURN 2 FORCE\n"
            profile += f"WHEN ({lp_condition_str}) AND (handrank169 <= {round(tight_threshold * limp_factor)}) RETURN 1 FORCE\n\n"

        profile += "// Small Blind\n"
        profile += f"WHEN InSmallBlind AND (handrank169 <= {round(tight_threshold * 0.75)}) RETURN 2 FORCE\n"
        profile += f"WHEN InSmallBlind AND (handrank169 <= {round(tight_threshold * 0.9 * limp_factor)}) RETURN 1 FORCE\n\n"

        profile += "// Big Blind (we only check here, handled in f$CheckOrBetOrRaise)\n"
        profile += "WHEN InBigBlind RETURN 0 FORCE\n\n"
        
        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Limp Or Isolate Limpers
        profile += "##f$LimpOrIsolateLimpers##\n"
        profile += "// 1 or more limps before us. Hero can Limp too or Raise to isolate the limpers\n"
        # Calculate isolation size based on aggression
        iso_size = self.calculate_raise_size(open_raise_size, 1, aggressive_factor)
        profile += f"WHEN f$LimpOrIsolateLimpers_Decision = 2 RETURN {iso_size} FORCE\n"
        profile += "WHEN f$LimpOrIsolateLimpers_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

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
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(tight_threshold * 0.6)} RETURN 1 FORCE\n\n"

        profile += "// Middle Position 3-bet\n"
        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(threebet_threshold * 0.65)} RETURN 2 FORCE\n"
        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(tight_threshold * 0.7)} RETURN 1 FORCE\n\n"

        profile += "// Late Position 3-bet\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(threebet_threshold * 0.8)} RETURN 2 FORCE\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(tight_threshold * 0.8)} RETURN 1 FORCE\n\n"

        profile += "// Blinds 3-bet\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(threebet_threshold * 0.7)} RETURN 2 FORCE\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(tight_threshold * 0.75)} RETURN 1 FORCE\n\n"

        profile += "// Against specific positions - 3-bet looser against late position raises\n"
        profile += f"WHEN (DealPositionLastRaiser >= nplayersdealt - 2) AND handrank169 <= {round(threebet_threshold * 0.9)} RETURN 2 FORCE\n"
        profile += f"WHEN (DealPositionLastRaiser >= nplayersdealt - 2) AND handrank169 <= {round(tight_threshold * 0.85)} RETURN 1 FORCE\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Squeeze Cold Call
        profile += "##f$SqueezeColdCall##\n"
        profile += "// 1 Raise before Hero first action and 1 or more villains calls. Hero can Squeeze, ColdCall or Fold\n"
        profile += "WHEN f$SqueezeColdCall_Decision = 2 RETURN RaisePot FORCE\n"
        profile += "WHEN f$SqueezeColdCall_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$SqueezeColdCall_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = Squeeze\n"
        profile += "// Tighter squeeze range with more players in the pot\n"
        profile += f"WHEN CallsSinceLastRaise = 1 AND handrank169 <= {round(squeeze_threshold * 0.7)} RETURN 2 FORCE\n"
        profile += f"WHEN CallsSinceLastRaise = 1 AND handrank169 <= {round(tight_threshold * 0.7)} RETURN 1 FORCE\n\n"

        profile += f"WHEN CallsSinceLastRaise = 2 AND handrank169 <= {round(squeeze_threshold * 0.6)} RETURN 2 FORCE\n"
        profile += f"WHEN CallsSinceLastRaise = 2 AND handrank169 <= {round(tight_threshold * 0.65)} RETURN 1 FORCE\n\n"

        profile += f"WHEN CallsSinceLastRaise >= 3 AND handrank169 <= {round(squeeze_threshold * 0.5)} RETURN 2 FORCE\n"
        profile += f"WHEN CallsSinceLastRaise >= 3 AND handrank169 <= {round(tight_threshold * 0.6)} RETURN 1 FORCE\n\n"

        profile += "// Position-based adjustments\n"
        profile += f"WHEN (InButton OR InCutOff) AND handrank169 <= {round(squeeze_threshold * 0.8)} RETURN 2 FORCE\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(squeeze_threshold * 0.7)} RETURN 2 FORCE\n\n"

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
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(fourbet_threshold * 0.4)} RETURN 2 FORCE\n"
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(tight_threshold * 0.5)} RETURN 1 FORCE\n\n"

        profile += "// Middle position\n"
        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(fourbet_threshold * 0.5)} RETURN 2 FORCE\n"
        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(tight_threshold * 0.55)} RETURN 1 FORCE\n\n"

        profile += "// Late position\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(fourbet_threshold * 0.6)} RETURN 2 FORCE\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(tight_threshold * 0.6)} RETURN 1 FORCE\n\n"

        profile += "// Blinds\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(fourbet_threshold * 0.55)} RETURN 2 FORCE\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(tight_threshold * 0.55)} RETURN 1 FORCE\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 4Bet Before First Action
        profile += "##f$Facing4BetBeforeFirstAction##\n"
        profile += "// 4bet before Hero first action. Hero can 5Bet, ColdCall or Fold\n"
        profile += "WHEN f$Facing4BetBeforeFirstAction_Decision = 2 RETURN RaiseMax FORCE\n"
        profile += "WHEN f$Facing4BetBeforeFirstAction_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$Facing4BetBeforeFirstAction_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = 5-Bet (All-In)\n"
        profile += "// Very narrow 5-bet range, mostly premium hands\n"
        profile += "WHEN handrank169 <= 5 RETURN 2 FORCE  // AA, KK, QQ, AKs, AKo\n"
        profile += "WHEN handrank169 <= 20 RETURN 1 FORCE // Top ~12% hands\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 5Bet Before First Action
        profile += "##f$Facing5BetBeforeFirstAction##\n"
        profile += "// 5bet before Hero first action. Hero can Push, ColdCall or Fold\n"
        profile += "WHEN handrank169 <= 5 RETURN RaiseMax FORCE  // AA, KK, QQ, AKs, AKo\n"
        profile += "WHEN handrank169 <= 10 RETURN Call FORCE     // Top ~6% hands\n"
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
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(fourbet_threshold * 0.45)} RETURN 2 FORCE\n"
        profile += f"WHEN (InEarlyPosition1 OR InEarlyPosition2 OR InEarlyPosition3) AND handrank169 <= {round(tight_threshold * 0.55)} RETURN 1 FORCE\n\n"

        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(fourbet_threshold * 0.55)} RETURN 2 FORCE\n"
        profile += f"WHEN (InMiddlePosition1 OR InMiddlePosition2 OR InMiddlePosition3) AND handrank169 <= {round(tight_threshold * 0.6)} RETURN 1 FORCE\n\n"

        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(fourbet_threshold * 0.65)} RETURN 2 FORCE\n"
        profile += f"WHEN (InCutOff OR InButton) AND handrank169 <= {round(tight_threshold * 0.7)} RETURN 1 FORCE\n\n"

        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(fourbet_threshold * 0.6)} RETURN 2 FORCE\n"
        profile += f"WHEN (InSmallBlind OR InBigBlind) AND handrank169 <= {round(tight_threshold * 0.65)} RETURN 1 FORCE\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing Squeeze
        profile += "##f$FacingSqueeze##\n"
        profile += "// Hero is the Original Raiser and Facing Squeeze by an opponent. Hero can 4Bet, Call or Fold\n"
        profile += "WHEN f$FacingSqueeze_Decision = 2 RETURN RaisePot FORCE\n"
        profile += "WHEN f$FacingSqueeze_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$FacingSqueeze_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = 4-Bet\n"
        profile += "// Generally tighter than regular 3-bet defense\n"
        profile += f"WHEN handrank169 <= {round(fourbet_threshold * 0.5)} RETURN 2 FORCE\n"
        profile += f"WHEN handrank169 <= {round(tight_threshold * 0.55)} RETURN 1 FORCE\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 4Bet
        profile += "##f$Facing4Bet##\n"
        profile += "// Hero 3bet and facing 4bet. Hero can 5bet, Call or Fold\n"
        profile += "WHEN f$Facing4Bet_Decision = 2 RETURN RaiseMax FORCE\n"
        profile += "WHEN f$Facing4Bet_Decision = 1 RETURN Call FORCE\n"
        profile += "WHEN Others RETURN Fold FORCE\n\n"

        profile += "##f$Facing4Bet_Decision##\n"
        profile += "// 0 = Fold, 1 = Call, 2 = 5-Bet (All-In)\n"
        profile += "WHEN handrank169 <= 5 RETURN 2 FORCE  // AA, KK, QQ, AKs, AKo\n"
        profile += "WHEN handrank169 <= 15 RETURN 1 FORCE // Top ~9% hands\n\n"

        profile += "WHEN Others RETURN 0 FORCE\n\n"

        # Facing 5Bet
        profile += "##f$Facing5Bet##\n"
        profile += "// Hero 4bet and facing 5bet. Hero can Push, Call or Fold\n"
        profile += "WHEN handrank169 <= 5 RETURN RaiseMax FORCE  // AA, KK, QQ, AKs, AKo\n"
        profile += "WHEN handrank169 <= 8 RETURN Call FORCE      // Top ~5% hands\n"
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

        profile += "//*****************************************************************************\n"
        profile += "//\n"
        profile += "// END OF PREFLOP PROFILE\n"
        profile += "//\n"
        profile += "//*****************************************************************************"
        
        return profile