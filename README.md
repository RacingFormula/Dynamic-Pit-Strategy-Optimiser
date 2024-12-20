# Dynamic Pit Strategy Optimiser

## Overview
This project models and optimises pit stop strategies in motorsport, including overcut and undercut scenarios. It uses advanced simulations to predict lap times, tyre degradation, and pit stop impacts under varying conditions.

## Features
- **Advanced Tyre Modelling**: Simulates grip loss based on tyre compound (soft, medium, hard), wear rate, and warm-up effects.
- **Dynamic Strategy Evaluation**: Compares overcut and undercut strategies by analysing lap times and pit stop timing.
- **Track Condition Effects**: Incorporates dry and wet track multipliers for realistic lap time predictions.
- **Optimal Strategy Finder**: Identifies the best pit stop timing for minimising total race time.
- **Customisable Parameters**: Supports configuration of race length, tyre properties, and track conditions.

## Usage
1. Define your race parameters (laps, base lap time, tyre compounds).
2. Choose a pit stop strategy or let the optimiser find the best strategy.
3. Run the simulation to evaluate the total race time and compare strategies.

## Example Output
```plaintext
Overcut Strategy ([20]): Total Race Time = 4500.25 seconds
Undercut Strategy ([15]): Total Race Time = 4520.78 seconds
Optimal Strategy: Pit at laps (20,), Total Race Time = 4498.10 seconds
```
