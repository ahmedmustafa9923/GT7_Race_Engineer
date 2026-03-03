import torch
import torch.nn as nn
from gt_telem import TurismoClient
import time
import os
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

# 1. Rebuild the Architecture
class RaceNet(nn.Module):
    def __init__(self):
        super(RaceNet, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(3, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        return self.network(x)


# 2. Load the "Saved Brain" onto the M4 GPU
device = torch.device("mps")
model = RaceNet().to(device)
model.load_state_dict(torch.load("my_trained_driver.pth"))
model.eval()  # Set to Evaluation Mode

# 3. Connect to PS5
tc = TurismoClient(heartbeat_type="B")
tc.playstation_ip = "192.XXX.X.XX"  # Your IP
tc.start()

print("AI ASSISTANT ACTIVE. Drive now...")

try:
    print("AI ASSISTANT ACTIVE. (Press Ctrl+C to stop)")
    while True:
        t = tc.telemetry

        # If we have data, process it
        if t and t.speed_mps > 0.1:
            speed = t.speed_mps * 3.6
            gear = getattr(t, 'current_gear', 0)
            rpm = getattr(t, 'engine_rpm', 0)

            # Simple Inference on CPU (Stable for M4 Live-Inference)
            input_data = torch.FloatTensor([[speed, gear, rpm]])
            with torch.no_grad():
                model.to("cpu")
                prediction = model(input_data)

            ai_thr, ai_brk = prediction[0][0].item(), prediction[0][1].item()
            real_thr = (t.throttle / 255) * 100

            # Keep the display clean
            print(f"SPEED: {speed:5.1f} | AI THR: {ai_thr:3.0f}% | YOUR THR: {real_thr:3.0f}%", end="\r")

        # If no data, just wait and keep trying instead of closing
        elif t:
            print(">>> STATUS: Standing still or in Menu...          ", end="\r")

        time.sleep(0.05)  # 20Hz update rate

except KeyboardInterrupt:
    print("\n[MANUAL STOP] Shutting down safely...")
    tc.stop()