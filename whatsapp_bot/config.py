"""
Módulo de configuração do bot do WhatsApp
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Diretórios base
BASE_DIR = Path(__file__).parent.parent
PROFILES_DIR = BASE_DIR / "profiles"
MESSAGES_DIR = BASE_DIR / "messages"
IMAGES_DIR = BASE_DIR / "images"
LOGS_DIR = BASE_DIR / "logs"

# Criar diretórios se não existirem
for directory in [PROFILES_DIR, MESSAGES_DIR, IMAGES_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Arquivo de configuração
CONFIG_FILE = BASE_DIR / "config.json"


class Config:
    """Classe para gerenciar configurações do bot"""

    DEFAULT_CONFIG = {
        "browser": "chrome",  # Opções: chrome, edge, firefox
        "group_name": "",  # Nome do grupo do WhatsApp
        "send_time": "09:00",  # Horário de envio (HH:MM)
        "last_send_date": None,  # Data do último envio
        "headless": False,  # Executar em modo headless
        "minimize_window": True,  # Minimizar janela ao abrir
    }

    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        """Carrega configurações do arquivo JSON"""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Mesclar com valores padrão para garantir todas as chaves
                    return {**self.DEFAULT_CONFIG, **config}
            except Exception as e:
                print(f"Erro ao carregar configuração: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            return self.DEFAULT_CONFIG.copy()

    def save_config(self):
        """Salva configurações no arquivo JSON"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")

    def get(self, key, default=None):
        """Obtém valor de configuração"""
        return self.config.get(key, default)

    def set(self, key, value):
        """Define valor de configuração"""
        self.config[key] = value
        self.save_config()

    def update_last_send_date(self):
        """Atualiza a data do último envio"""
        self.set("last_send_date", datetime.now().strftime("%Y-%m-%d"))

    def should_send_today(self):
        """Verifica se deve enviar mensagem hoje"""
        last_send = self.get("last_send_date")
        today = datetime.now().strftime("%Y-%m-%d")
        return last_send != today

    def get_profile_path(self):
        """Retorna o caminho do perfil do navegador"""
        browser = self.get("browser", "chrome")
        return str(PROFILES_DIR / f"{browser}_profile")

    def setup_wizard(self):
        """Assistente de configuração inicial"""
        print("\n" + "="*50)
        print("CONFIGURAÇÃO INICIAL DO BOT DE WHATSAPP")
        print("="*50 + "\n")

        # Escolher navegador
        print("Escolha o navegador:")
        print("1. Chrome (padrão)")
        print("2. Edge")
        print("3. Firefox")
        choice = input("\nOpção (1-3) [1]: ").strip() or "1"

        browsers = {"1": "chrome", "2": "edge", "3": "firefox"}
        self.set("browser", browsers.get(choice, "chrome"))

        # Nome do grupo
        group_name = input("\nNome do grupo do WhatsApp: ").strip()
        if group_name:
            self.set("group_name", group_name)

        # Horário de envio
        send_time = input("\nHorário de envio (HH:MM) [09:00]: ").strip() or "09:00"
        try:
            datetime.strptime(send_time, "%H:%M")
            self.set("send_time", send_time)
        except ValueError:
            print("Horário inválido, usando padrão 09:00")
            self.set("send_time", "09:00")

        # Modo de execução
        minimize = input("\nMinimizar janela durante execução? (s/n) [s]: ").strip().lower() or "s"
        self.set("minimize_window", minimize == "s")

        print("\n" + "="*50)
        print("Configuração concluída!")
        print("="*50 + "\n")

        return self.config


# Instância global de configuração
config = Config()
