import torch
from control_voltron import extract_lora

def test_extract_lora_shapes():
    up, down = extract_lora(torch.randn(32, 24), 8)
    assert up.shape == (32, 8)
    assert down.shape == (8, 24)

def test_extract_conv_shapes():
    up, down = extract_lora(torch.randn(16, 8, 3, 3), 4)
    assert up.shape == (16, 4, 1, 1)
    assert down.shape == (4, 8, 3, 3)
