import torch
import torch.nn as nn
import torch.optim as optim

# 1. Define the 'Neural Network' Architecture
class RaceNet(nn.Module):
    def __init__(self):
        super(RaceNet, self).__init__()
        # Input: 4 sensors (Speed, Gear, Throttle, Brake)
        # Hidden Layer: 128 neurons (The 'thinking' space)
        # Output: 1 value (Steering Angle)
        self.network = nn.Sequential(
            nn.Linear(4, 128),
            nn.ReLU(),         # The 'activation' that lets it learn complex curves
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)    # Final steering output
        )

    def forward(self, x):
        return self.network(x)

# 2. Move the Brain to the M4 GPU
device = torch.device("mps")
model = RaceNet().to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# --- SECTION 3: THE DATA ---
# (Later, this is where we plug in the PS5/GT7 data)
fake_telemetry = torch.randn(100, 4).to(device)
target_steering = torch.randn(100, 1).to(device)

# --- SECTION 4: THE TRAINING LOOP ---
for epoch in range(100):
    optimizer.zero_grad()
    outputs = model(fake_telemetry)
    loss = criterion(outputs, target_steering)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f"Lap {epoch + 1} - Loss: {loss.item():.4f}")

        # Save the trained weights to a file
        torch.save(model.state_dict(), "race_engineer_v1.pth")
        print("Model weights saved to race_engineer_v1.pth")

        # To load it later in a new file:
        # model.load_state_dict(torch.load("race_engineer_v1.pth"))
        # model.eval() # Puts the brain in 'Prediction Mode'