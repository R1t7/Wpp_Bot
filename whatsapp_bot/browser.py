"""
Módulo para gerenciar o navegador Selenium
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from pathlib import Path

logger = logging.getLogger(__name__)


class BrowserManager:
    """Gerenciador do navegador Selenium"""

    def __init__(self, browser_type="chrome", profile_path=None, minimize=True, headless=False):
        """
        Inicializa o gerenciador do navegador

        Args:
            browser_type: Tipo de navegador (chrome, edge, firefox)
            profile_path: Caminho para o perfil do navegador
            minimize: Minimizar janela ao abrir
            headless: Executar em modo headless
        """
        self.browser_type = browser_type.lower()
        self.profile_path = profile_path
        self.minimize = minimize
        self.headless = headless
        self.driver = None

    def _get_chrome_driver(self):
        """Configura e retorna driver do Chrome"""
        options = ChromeOptions()

        # Perfil de usuário dedicado
        if self.profile_path:
            options.add_argument(f"--user-data-dir={self.profile_path}")

        # Configurações para execução discreta
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

        # Desabilitar notificações
        options.add_argument("--disable-notifications")
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
        }
        options.add_experimental_option("prefs", prefs)

        # Modo headless
        if self.headless:
            options.add_argument("--headless=new")

        # Minimizar janela
        if self.minimize and not self.headless:
            options.add_argument("--window-position=-2400,-2400")

        try:
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            logger.error(f"Erro ao iniciar Chrome: {e}")
            raise

    def _get_edge_driver(self):
        """Configura e retorna driver do Edge"""
        options = EdgeOptions()

        # Perfil de usuário dedicado
        if self.profile_path:
            options.add_argument(f"--user-data-dir={self.profile_path}")

        # Configurações para execução discreta
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

        # Desabilitar notificações
        options.add_argument("--disable-notifications")
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
        }
        options.add_experimental_option("prefs", prefs)

        # Modo headless
        if self.headless:
            options.add_argument("--headless=new")

        # Minimizar janela
        if self.minimize and not self.headless:
            options.add_argument("--window-position=-2400,-2400")

        try:
            driver = webdriver.Edge(options=options)
            return driver
        except Exception as e:
            logger.error(f"Erro ao iniciar Edge: {e}")
            raise

    def _get_firefox_driver(self):
        """Configura e retorna driver do Firefox"""
        options = FirefoxOptions()

        # Perfil de usuário dedicado
        if self.profile_path:
            profile = webdriver.FirefoxProfile(self.profile_path)
            options.profile = profile

        # Desabilitar notificações
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("dom.push.enabled", False)

        # Modo headless
        if self.headless:
            options.add_argument("--headless")

        try:
            driver = webdriver.Firefox(options=options)

            # Minimizar janela (Firefox não suporta window-position negativo)
            if self.minimize and not self.headless:
                driver.minimize_window()

            return driver
        except Exception as e:
            logger.error(f"Erro ao iniciar Firefox: {e}")
            raise

    def start(self):
        """Inicia o navegador"""
        logger.info(f"Iniciando navegador {self.browser_type}...")

        try:
            if self.browser_type == "chrome":
                self.driver = self._get_chrome_driver()
            elif self.browser_type == "edge":
                self.driver = self._get_edge_driver()
            elif self.browser_type == "firefox":
                self.driver = self._get_firefox_driver()
            else:
                raise ValueError(f"Navegador não suportado: {self.browser_type}")

            logger.info("Navegador iniciado com sucesso")
            return self.driver

        except Exception as e:
            logger.error(f"Erro ao iniciar navegador: {e}")
            raise

    def stop(self):
        """Fecha o navegador"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Navegador fechado")
            except Exception as e:
                logger.error(f"Erro ao fechar navegador: {e}")

    def minimize_window(self):
        """Minimiza a janela do navegador"""
        if self.driver and not self.headless:
            try:
                if self.browser_type in ["chrome", "edge"]:
                    self.driver.set_window_position(-2400, -2400)
                else:
                    self.driver.minimize_window()
                logger.info("Janela minimizada")
            except Exception as e:
                logger.error(f"Erro ao minimizar janela: {e}")

    def restore_window(self):
        """Restaura a janela do navegador"""
        if self.driver and not self.headless:
            try:
                self.driver.set_window_position(0, 0)
                self.driver.maximize_window()
                logger.info("Janela restaurada")
            except Exception as e:
                logger.error(f"Erro ao restaurar janela: {e}")

    def __enter__(self):
        """Context manager - entrada"""
        self.start()
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager - saída"""
        self.stop()
