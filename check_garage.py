import torch
import pandas as pd
import gymnasium as gym

print(f"PyTorch Version: {torch.__version__}")
print(f"Pandas Version: {pd.__version__}")
print(f"Gymnasium Version: {gym.__version__}")

if torch.backends.mps.is_available():
    print("M4 GPU acceleration is ACTIVE!")