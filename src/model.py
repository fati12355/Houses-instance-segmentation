# src/model.py
import torch
import torch.nn as nn
import segmentation_models_pytorch as smp

class UNet(nn.Module):
    def __init__(self, in_channels=3, out_channels=1):
        super().__init__()
        self.model = smp.Unet(
            encoder_name='resnet34',
            encoder_weights=None,  # No pretrained weights for inference
            in_channels=in_channels,
            classes=out_channels,
            activation='sigmoid'
        )
    
    def forward(self, x):
        return self.model(x)