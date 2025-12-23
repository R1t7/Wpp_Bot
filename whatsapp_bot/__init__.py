"""
WhatsApp Bot - Bot para envio automático de mensagens no WhatsApp Web
"""

__version__ = "1.0.0"
__author__ = "WhatsApp Bot"

from .config import Config, config
from .browser import BrowserManager
from .whatsapp import WhatsAppBot

__all__ = ['Config', 'config', 'BrowserManager', 'WhatsAppBot']
