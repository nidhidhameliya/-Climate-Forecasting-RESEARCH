"""Compatibility entry point for all current verified visualizations.

The previous implementation read a missing legacy metrics.csv and could label
normalized, stale values as ConvLSTM. Use the saved corrected experiment outputs.
"""
from generate_verified_visualizations import main

if __name__ == "__main__":
    main()
