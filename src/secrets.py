# src/secrets.py
import os
from dotenv import load_dotenv
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class SecretsManager:
    """Secure secrets management with environment variables"""
    
    def __init__(self, env_file=".env"):
        # Load .env file
        env_path = Path(env_file)
        if env_path.exists():
            load_dotenv(env_path)
            logger.info(f"Loaded secrets from {env_file}")
        else:
            logger.warning(f"{env_file} not found, using system environment")
    
    def get_secret(self, key, default=None, required=False):
        """Get secret value"""
        value = os.getenv(key, default)
        
        if required and value is None:
            raise ValueError(f"Required secret '{key}' not found")
        
        return value
    
    def get_model_config(self):
        """Get model configuration"""
        return {
            'model_path': self.get_secret('MODEL_PATH', './models/best_unet_model.pth'),
            'input_size': (512, 512),
            'num_classes': 2,  # background + house
            'device': 'cuda' if self._check_cuda() else 'cpu'
        }
    
    def _check_cuda(self):
        try:
            import torch
            return torch.cuda.is_available()
        except:
            return False

secrets = SecretsManager()
