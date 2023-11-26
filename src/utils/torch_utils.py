import torch

def get_device():
    """Return the device."""
    return torch.device("cuda:0" if torch.cuda.is_available() else "cpu")