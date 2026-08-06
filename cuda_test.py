import torch
import time

# 1. Check if the code can see your NVIDIA GPU
if torch.cuda.is_available():
    print(" SUCCESS: CUDA is active and working!")
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
    device = torch.device("cuda")
else:
    print(" FAILURE: CUDA not found. Code is running on your CPU.")
    device = torch.device("cpu")

# 2. Run a lightning-fast heavy math test on your GPU
print("\nTesting GPU speed (Matrix Multiplication)...")
size = 8000
x = torch.randn(size, size, device=device)
y = torch.randn(size, size, device=device)

start = time.time()
result = torch.matmul(x, y)
torch.cuda.synchronize() # Wait for GPU to finish
end = time.time()

print(f" Calculated millions of data points in {end - start:.4f} seconds!")
