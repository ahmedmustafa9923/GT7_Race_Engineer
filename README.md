# GT7_Race_Engineer
Current Features: Multi-Output Prediction: Processes input images to determine Steering, Throttle, and Braking values.
Weight Checkpoints: Includes .pth model state dictionaries containing learned parameters (weights and biases).
Data Logging: Supports .csv dataset structure for recording real-time driving telemetry.🛠️ Technical OverviewFramework: PyTorchData Structure: Tensors representing control vectors $[Steer, Throttle, Brake]$.
Status: Integrating braking logic into the training pipeline and addressing data imbalance in the CSV logs.
