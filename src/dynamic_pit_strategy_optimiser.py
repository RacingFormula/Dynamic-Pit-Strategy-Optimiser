import numpy as np
import pandas as pd
from itertools import combinations

class TyreModel:
    def __init__(self, base_grip=1.0, wear_rate=0.02, warmup_laps=1, compound_type="medium"):
        self.base_grip = base_grip
        self.wear_rate = wear_rate
        self.warmup_laps = warmup_laps
        self.compound_type = compound_type
        self.compound_properties = {
            "soft": {"grip_multiplier": 1.2, "durability": 0.8},
            "medium": {"grip_multiplier": 1.0, "durability": 1.0},
            "hard": {"grip_multiplier": 0.8, "durability": 1.5},
        }

    def calculate_grip(self, lap, tyre_age):
        properties = self.compound_properties[self.compound_type]
        grip_multiplier = properties["grip_multiplier"]
        durability = properties["durability"]

        if tyre_age < self.warmup_laps:
            return max(self.base_grip * grip_multiplier - 0.1 * (self.warmup_laps - tyre_age), 0)
        return max(self.base_grip * grip_multiplier - self.wear_rate * tyre_age / durability, 0)


class PitStopModel:
    def __init__(self, pit_time=20):
        self.pit_time = pit_time

    def get_pit_loss(self):
        return self.pit_time


class DynamicPitStrategyOptimiser:
    def __init__(self, laps=50, base_lap_time=90, degradation_penalty=2, track_conditions="dry"):
        self.laps = laps
        self.base_lap_time = base_lap_time
        self.degradation_penalty = degradation_penalty
        self.track_conditions = track_conditions
        self.tyre_model = None
        self.pit_stop_model = PitStopModel()
        self.track_condition_multiplier = 1.0 if track_conditions == "dry" else 1.2

    def simulate_lap_times(self, strategy, compound_type="medium"):
        self.tyre_model = TyreModel(compound_type=compound_type)
        tyre_age = 0
        lap_times = []

        for lap in range(1, self.laps + 1):
            if lap in strategy:
                # Pit stop logic
                lap_times.append(self.pit_stop_model.get_pit_loss())
                tyre_age = 0  # New tyres after a pit stop
            else:
                grip = self.tyre_model.calculate_grip(lap, tyre_age)
                lap_time = self.base_lap_time + self.degradation_penalty * (1 - grip) * self.track_condition_multiplier
                lap_times.append(lap_time)
                tyre_age += 1

        return lap_times

    def evaluate_strategy(self, strategy, compound_type="medium"):
        lap_times = self.simulate_lap_times(strategy, compound_type)
        return sum(lap_times)

    def find_optimal_strategy(self, max_stops=2, compound_type="medium"):
        best_time = float('inf')
        best_strategy = []

        # Generate all possible strategies with up to max_stops
        for stops in range(1, max_stops + 1):
            pit_laps = range(1, self.laps)  # Exclude final lap
            for strategy in combinations(pit_laps, stops):
                total_time = self.evaluate_strategy(strategy, compound_type)
                if total_time < best_time:
                    best_time = total_time
                    best_strategy = strategy

        return best_strategy, best_time


if __name__ == "__main__":
    optimiser = DynamicPitStrategyOptimiser(laps=50, base_lap_time=90, degradation_penalty=2, track_conditions="dry")

    # Define overcut and undercut strategies for comparison
    overcut_strategy = [20]  # Delay pit stop to gain advantage from tyre degradation
    undercut_strategy = [15]  # Early pit stop to benefit from fresh tyres

    # Evaluate strategies
    overcut_time = optimiser.evaluate_strategy(overcut_strategy, compound_type="medium")
    undercut_time = optimiser.evaluate_strategy(undercut_strategy, compound_type="medium")

    print(f"Overcut Strategy ({overcut_strategy}): Total Race Time = {overcut_time:.2f} seconds")
    print(f"Undercut Strategy ({undercut_strategy}): Total Race Time = {undercut_time:.2f} seconds")

    # Find optimal strategy
    best_strategy, best_time = optimiser.find_optimal_strategy(max_stops=2, compound_type="medium")
    print(f"Optimal Strategy: Pit at laps {best_strategy}, Total Race Time = {best_time:.2f} seconds")
