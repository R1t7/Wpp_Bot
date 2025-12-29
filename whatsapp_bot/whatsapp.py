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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import io
from PIL import Image

logger = logging.getLogger(__name__)

# Importar biblioteca de clipboard baseado no sistema operacional
try:
    import win32clipboard
    from PIL import ImageGrab
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False
    logger.warning("win32clipboard não disponível. Instalando pywin32...")


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

    def copy_image_to_clipboard(self, image_path):
        """
        Copia uma imagem para a área de transferência (Windows)

        Args:
            image_path: Caminho para a imagem

        Returns:
            bool: True se a imagem foi copiada com sucesso
        """
        try:
            if not HAS_CLIPBOARD:
                logger.error("Biblioteca de clipboard não disponível")
                return False

            # Abrir imagem com PIL
            image = Image.open(image_path)

            # Converter para bitmap
            output = io.BytesIO()
            image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]  # Remove BMP header
            output.close()

            # Copiar para clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()

            logger.info("Imagem copiada para clipboard")
            return True

        except Exception as e:
            logger.error(f"Erro ao copiar imagem para clipboard: {e}")
            try:
                win32clipboard.CloseClipboard()
            except:
                pass
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
        logger.info(f"Enviando imagem via clipboard: {image_path}")

        try:
            # Verificar se o arquivo existe
            if not os.path.exists(image_path):
                logger.error(f"Arquivo não encontrado: {image_path}")
                return False

            # Copiar imagem para clipboard
            logger.info("Copiando imagem para clipboard...")
            if not self.copy_image_to_clipboard(image_path):
                logger.error("Falha ao copiar imagem para clipboard")
                return False

            # Encontrar caixa de mensagem
            logger.info("Procurando caixa de mensagem...")
            message_box = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            ))

            # Clicar na caixa de mensagem para focar
            message_box.click()
            time.sleep(1)

            # Colar imagem (Ctrl+V)
            logger.info("Colando imagem (Ctrl+V)...")
            message_box.send_keys(Keys.CONTROL, 'v')
            time.sleep(3)

            # Aguardar a imagem carregar
            logger.info("Aguardando preview da imagem...")
            time.sleep(3)

            # Enviar imagem sem legenda (legenda será enviada como mensagem separada depois)
            logger.info("Enviando imagem sem legenda...")

            # Procurar e clicar no botão de enviar da preview
            logger.info("Procurando botão de enviar da preview...")
            send_button = None
            send_selectors = [
                '//span[@data-icon="send"]',
                '//span[@data-testid="send"]',
                '//button[@aria-label="Enviar"]',
                '//div[@aria-label="Enviar"]',
                '//span[@data-icon="send-light"]'
            ]

            for selector in send_selectors:
                try:
                    logger.info(f"Tentando seletor: {selector}")
                    send_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    if send_button:
                        logger.info(f"Botão de enviar encontrado: {selector}")
                        break
                except:
                    continue

            if send_button:
                try:
                    # Tentar clicar com ActionChains
                    logger.info("Clicando no botão de enviar com ActionChains")
                    actions = ActionChains(self.driver)
                    actions.move_to_element(send_button).click().perform()
                    logger.info("Botão clicado via ActionChains")
                    time.sleep(4)
                except Exception as e:
                    logger.warning(f"ActionChains falhou: {e}, tentando JavaScript")
                    try:
                        self.driver.execute_script("arguments[0].click();", send_button)
                        logger.info("Botão clicado via JavaScript")
                        time.sleep(4)
                    except Exception as e2:
                        logger.error(f"Falha ao clicar no botão: {e2}")
                        return False
            else:
                logger.error("Botão de enviar não encontrado")
                return False

            logger.info("Imagem enviada com sucesso")

            # Se houver legenda, enviar como mensagem de texto separada
            if caption:
                logger.info("Enviando legenda como mensagem de texto...")
                time.sleep(2)  # Aguardar imagem ser processada

                if self.send_text_message(caption):
                    logger.info("Legenda enviada com sucesso")
                else:
                    logger.warning("Falha ao enviar legenda")

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
