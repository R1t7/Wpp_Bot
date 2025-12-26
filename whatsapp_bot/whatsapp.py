"""
Módulo para interação com WhatsApp Web
"""

import time
import logging
import os
from datetime import datetime
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)


class WhatsAppBot:
    """Bot para envio de mensagens no WhatsApp Web"""

    WHATSAPP_URL = "https://web.whatsapp.com"

    def __init__(self, driver):
        """
        Inicializa o bot do WhatsApp

        Args:
            driver: Instância do WebDriver do Selenium
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 30)

    def open_whatsapp(self):
        """Abre o WhatsApp Web"""
        logger.info("Abrindo WhatsApp Web...")
        self.driver.get(self.WHATSAPP_URL)

    def wait_for_login(self, timeout=120):
        """
        Aguarda o login no WhatsApp Web (scan do QR Code ou carregamento do perfil)

        Args:
            timeout: Tempo máximo de espera em segundos
        """
        logger.info("Aguardando login no WhatsApp Web...")

        try:
            # Espera pela caixa de pesquisa aparecer (indica que está logado)
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            ))
            logger.info("Login realizado com sucesso!")
            time.sleep(3)  # Pequena pausa para garantir carregamento completo
            return True

        except TimeoutException:
            logger.error("Timeout ao aguardar login")
            return False

    def search_group(self, group_name):
        """
        Busca e abre um grupo pelo nome

        Args:
            group_name: Nome do grupo a ser buscado

        Returns:
            bool: True se o grupo foi encontrado e aberto
        """
        logger.info(f"Buscando grupo: {group_name}")

        try:
            # Clicar na caixa de pesquisa
            search_box = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            ))
            search_box.clear()
            time.sleep(1)
            search_box.send_keys(group_name)
            time.sleep(2)

            # Clicar no primeiro resultado
            group_xpath = f'//span[@title="{group_name}"]'
            group = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, group_xpath)
            ))
            group.click()
            time.sleep(2)

            logger.info(f"Grupo '{group_name}' encontrado e aberto")
            return True

        except TimeoutException:
            logger.error(f"Grupo '{group_name}' não encontrado")
            return False
        except Exception as e:
            logger.error(f"Erro ao buscar grupo: {e}")
            return False

    def send_text_message(self, message):
        """
        Envia uma mensagem de texto

        Args:
            message: Texto da mensagem (pode conter emojis)

        Returns:
            bool: True se a mensagem foi enviada com sucesso
        """
        logger.info("Enviando mensagem de texto...")

        try:
            # Encontrar a caixa de mensagem
            message_box = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            ))

            # Dividir mensagem por linhas e enviar
            lines = message.split('\n')
            for i, line in enumerate(lines):
                message_box.send_keys(line)
                if i < len(lines) - 1:
                    message_box.send_keys(Keys.SHIFT + Keys.ENTER)

            time.sleep(1)

            # Enviar mensagem
            message_box.send_keys(Keys.ENTER)
            time.sleep(2)

            logger.info("Mensagem de texto enviada com sucesso")
            return True

        except Exception as e:
            logger.error(f"Erro ao enviar mensagem de texto: {e}")
            return False

    def send_image_with_caption(self, image_path, caption=""):
        """
        Envia uma imagem com legenda

        Args:
            image_path: Caminho para a imagem
            caption: Legenda da imagem (opcional)

        Returns:
            bool: True se a imagem foi enviada com sucesso
        """
        logger.info(f"Enviando imagem: {image_path}")

        try:
            # Verificar se o arquivo existe
            if not os.path.exists(image_path):
                logger.error(f"Arquivo não encontrado: {image_path}")
                return False

            # Converter para caminho absoluto
            abs_image_path = os.path.abspath(image_path)
            logger.info(f"Caminho absoluto: {abs_image_path}")

            # Tentar múltiplos seletores para o botão de anexo
            attach_button = None
            attach_selectors = [
                '//div[@title="Anexar"]',
                '//div[@aria-label="Anexar"]',
                '//span[@data-icon="plus"]',
                '//span[@data-icon="attach-menu-plus"]',
                '//button[@aria-label="Anexar"]'
            ]

            for selector in attach_selectors:
                try:
                    logger.info(f"Tentando seletor: {selector}")
                    attach_button = self.driver.find_element(By.XPATH, selector)
                    if attach_button:
                        logger.info(f"Botão de anexo encontrado com: {selector}")
                        break
                except NoSuchElementException:
                    continue

            if not attach_button:
                logger.error("Botão de anexo não encontrado")
                return False

            attach_button.click()
            logger.info("Botão de anexo clicado")
            time.sleep(2)

            # Tentar múltiplos seletores para o input de arquivo
            file_input = None
            input_selectors = [
                '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]',
                '//input[@type="file"]',
                '//input[@accept*="image"]'
            ]

            for selector in input_selectors:
                try:
                    logger.info(f"Tentando seletor de input: {selector}")
                    file_input = self.driver.find_element(By.XPATH, selector)
                    if file_input:
                        logger.info(f"Input de arquivo encontrado com: {selector}")
                        break
                except NoSuchElementException:
                    continue

            if not file_input:
                logger.error("Input de arquivo não encontrado")
                return False

            file_input.send_keys(abs_image_path)
            logger.info("Caminho da imagem enviado para input")
            time.sleep(3)

            # Se houver legenda, adicionar
            if caption:
                logger.info("Tentando adicionar legenda")
                try:
                    caption_box = self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
                    ))

                    # Dividir legenda por linhas
                    lines = caption.split('\n')
                    for i, line in enumerate(lines):
                        caption_box.send_keys(line)
                        if i < len(lines) - 1:
                            caption_box.send_keys(Keys.SHIFT + Keys.ENTER)

                    logger.info("Legenda adicionada")
                    time.sleep(1)
                except Exception as e:
                    logger.warning(f"Erro ao adicionar legenda: {e}")

            # Tentar múltiplos seletores para o botão de enviar
            send_button = None
            send_selectors = [
                '//span[@data-icon="send"]',
                '//button[@aria-label="Enviar"]',
                '//span[@data-testid="send"]',
                '//div[@aria-label="Enviar"]'
            ]

            for selector in send_selectors:
                try:
                    logger.info(f"Tentando seletor de envio: {selector}")
                    send_button = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if send_button:
                        logger.info(f"Botão de enviar encontrado com: {selector}")
                        break
                except:
                    continue

            if not send_button:
                logger.error("Botão de enviar não encontrado")
                return False

            # Tentar clicar usando JavaScript para evitar element intercepted
            try:
                logger.info("Tentando clicar com JavaScript")
                self.driver.execute_script("arguments[0].click();", send_button)
                logger.info("Botão de enviar clicado via JavaScript")
            except:
                logger.info("JavaScript falhou, tentando clique normal")
                send_button.click()
                logger.info("Botão de enviar clicado")

            time.sleep(3)

            logger.info("Imagem enviada com sucesso")
            return True

        except Exception as e:
            logger.error(f"Erro ao enviar imagem: {e}", exc_info=True)
            return False

    def get_message_for_today(self, messages_dir):
        """
        Obtém a mensagem programada para hoje baseada no dia da semana

        Args:
            messages_dir: Diretório onde estão os arquivos de mensagens

        Returns:
            dict: Dicionário com 'text' e opcionalmente 'image' e 'caption'
        """
        today = datetime.now()

        # Mapear dia da semana (0=segunda, 6=domingo)
        weekdays = {
            0: 'segunda',
            1: 'terca',
            2: 'quarta',
            3: 'quinta',
            4: 'sexta',
            5: 'sabado',
            6: 'domingo'
        }

        weekday = today.weekday()
        weekday_name = weekdays[weekday]

        # Arquivo de mensagem do dia da semana
        message_file = Path(messages_dir) / f"{weekday_name}.txt"

        logger.info(f"Procurando mensagem para: {weekday_name}")

        # Se não existir arquivo específico, usar mensagem padrão
        if not message_file.exists():
            default_file = Path(messages_dir) / "default.txt"
            if default_file.exists():
                logger.warning(f"Arquivo {weekday_name}.txt não encontrado, usando default.txt")
                message_file = default_file
            else:
                logger.warning("Nenhum arquivo de mensagem encontrado")
                return None

        try:
            with open(message_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            result = {'text': content, 'image': None, 'caption': None}

            # Verificar se existe imagem para o dia da semana
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            for ext in image_extensions:
                image_file = Path(messages_dir).parent / "images" / f"{weekday_name}{ext}"
                if image_file.exists():
                    result['image'] = str(image_file)
                    result['caption'] = content  # Usar o texto como legenda
                    result['text'] = None  # Não enviar texto separado
                    logger.info(f"Imagem encontrada: {weekday_name}{ext}")
                    break

            return result

        except Exception as e:
            logger.error(f"Erro ao ler mensagem: {e}")
            return None

    def send_daily_message(self, group_name, messages_dir):
        """
        Envia a mensagem diária programada

        Args:
            group_name: Nome do grupo
            messages_dir: Diretório de mensagens

        Returns:
            bool: True se a mensagem foi enviada com sucesso
        """
        try:
            # Abrir WhatsApp
            self.open_whatsapp()

            # Aguardar login
            if not self.wait_for_login():
                logger.error("Falha no login do WhatsApp")
                return False

            # Buscar grupo
            if not self.search_group(group_name):
                logger.error("Falha ao encontrar o grupo")
                return False

            # Obter mensagem do dia
            message_data = self.get_message_for_today(messages_dir)
            if not message_data:
                logger.error("Nenhuma mensagem configurada para hoje")
                return False

            # Enviar imagem com legenda OU mensagem de texto
            if message_data.get('image'):
                success = self.send_image_with_caption(
                    message_data['image'],
                    message_data.get('caption', '')
                )
            else:
                success = self.send_text_message(message_data['text'])

            if success:
                logger.info("Mensagem diária enviada com sucesso!")
            else:
                logger.error("Falha ao enviar mensagem diária")

            return success

        except Exception as e:
            logger.error(f"Erro ao enviar mensagem diária: {e}")
            return False
