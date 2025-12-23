#!/usr/bin/env python3
"""
Script principal do bot de WhatsApp
"""

import sys
import logging
import argparse
from datetime import datetime
from pathlib import Path

# Adicionar o diretório do projeto ao path
sys.path.insert(0, str(Path(__file__).parent))

from whatsapp_bot import config, BrowserManager, WhatsAppBot

# Configurar logging
log_file = Path(__file__).parent / "logs" / f"bot_{datetime.now().strftime('%Y-%m-%d')}.log"
log_file.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def setup():
    """Executa o assistente de configuração inicial"""
    print("\n" + "="*60)
    print(" BOT DE WHATSAPP - CONFIGURAÇÃO INICIAL")
    print("="*60)

    config.setup_wizard()

    print("\n✓ Configuração salva com sucesso!")
    print(f"\nPróximos passos:")
    print("1. Execute o bot pela primeira vez: python main.py --first-run")
    print("2. Escaneie o QR Code do WhatsApp Web")
    print("3. Configure suas mensagens diárias")
    print("\n")


def first_run():
    """Primeira execução - Login no WhatsApp Web"""
    print("\n" + "="*60)
    print(" PRIMEIRA EXECUÇÃO - LOGIN NO WHATSAPP WEB")
    print("="*60 + "\n")

    # Verificar se há configuração
    if not config.get("group_name"):
        print("⚠ Configuração não encontrada. Execute primeiro: python main.py --setup")
        return False

    browser_type = config.get("browser", "chrome")
    profile_path = config.get_profile_path()

    print(f"Navegador: {browser_type}")
    print(f"Perfil: {profile_path}\n")

    browser_manager = BrowserManager(
        browser_type=browser_type,
        profile_path=profile_path,
        minimize=False,  # Não minimizar na primeira execução
        headless=False
    )

    try:
        print("Iniciando navegador...")
        driver = browser_manager.start()

        bot = WhatsAppBot(driver)
        bot.open_whatsapp()

        print("\n" + "="*60)
        print(" ESCANEIE O QR CODE DO WHATSAPP WEB")
        print("="*60)
        print("\n1. Abra o WhatsApp no seu celular")
        print("2. Vá em Configurações > Aparelhos conectados")
        print("3. Toque em 'Conectar um aparelho'")
        print("4. Escaneie o QR Code exibido no navegador\n")

        if bot.wait_for_login(timeout=180):
            print("\n✓ Login realizado com sucesso!")
            print("✓ Sessão salva no perfil do navegador")
            print("\nA partir de agora, o bot usará esta sessão automaticamente.")
            print("\nPressione Enter para fechar o navegador...")
            input()
            return True
        else:
            print("\n✗ Timeout ao aguardar login")
            print("Tente novamente executando: python main.py --first-run")
            return False

    except Exception as e:
        logger.error(f"Erro na primeira execução: {e}")
        print(f"\n✗ Erro: {e}")
        return False

    finally:
        browser_manager.stop()


def send_message():
    """Envia a mensagem diária"""
    logger.info("="*60)
    logger.info("BOT DE WHATSAPP - INICIANDO ENVIO")
    logger.info("="*60)

    # Verificar configuração
    group_name = config.get("group_name")
    if not group_name:
        logger.error("Nome do grupo não configurado. Execute: python main.py --setup")
        return False

    # Verificar se já enviou hoje
    if not config.should_send_today():
        logger.info("Mensagem já foi enviada hoje")
        print("✓ Mensagem já foi enviada hoje")
        return True

    # Configurações do navegador
    browser_type = config.get("browser", "chrome")
    profile_path = config.get_profile_path()
    minimize = config.get("minimize_window", True)
    headless = config.get("headless", False)

    browser_manager = BrowserManager(
        browser_type=browser_type,
        profile_path=profile_path,
        minimize=minimize,
        headless=headless
    )

    try:
        logger.info(f"Iniciando navegador {browser_type}...")
        driver = browser_manager.start()

        # Criar bot e enviar mensagem
        bot = WhatsAppBot(driver)
        messages_dir = Path(__file__).parent / "messages"

        success = bot.send_daily_message(group_name, messages_dir)

        if success:
            # Atualizar data do último envio
            config.update_last_send_date()
            logger.info("Mensagem enviada e data atualizada")
            print("✓ Mensagem enviada com sucesso!")
            return True
        else:
            logger.error("Falha ao enviar mensagem")
            print("✗ Falha ao enviar mensagem")
            return False

    except Exception as e:
        logger.error(f"Erro ao enviar mensagem: {e}", exc_info=True)
        print(f"✗ Erro: {e}")
        return False

    finally:
        browser_manager.stop()
        logger.info("="*60)


def test_message():
    """Modo de teste - envia mensagem sem verificar data"""
    logger.info("="*60)
    logger.info("BOT DE WHATSAPP - MODO DE TESTE")
    logger.info("="*60)

    group_name = config.get("group_name")
    if not group_name:
        logger.error("Nome do grupo não configurado. Execute: python main.py --setup")
        return False

    browser_type = config.get("browser", "chrome")
    profile_path = config.get_profile_path()

    browser_manager = BrowserManager(
        browser_type=browser_type,
        profile_path=profile_path,
        minimize=False,  # Não minimizar no modo teste
        headless=False
    )

    try:
        logger.info(f"Iniciando navegador {browser_type}...")
        driver = browser_manager.start()

        bot = WhatsAppBot(driver)
        messages_dir = Path(__file__).parent / "messages"

        success = bot.send_daily_message(group_name, messages_dir)

        if success:
            print("✓ Teste concluído - Mensagem enviada!")
            print("\n⚠ ATENÇÃO: Isso foi um teste.")
            print("A data do último envio NÃO foi atualizada.")
            return True
        else:
            print("✗ Teste falhou - Erro ao enviar mensagem")
            return False

    except Exception as e:
        logger.error(f"Erro no teste: {e}", exc_info=True)
        print(f"✗ Erro: {e}")
        return False

    finally:
        print("\nPressione Enter para fechar o navegador...")
        input()
        browser_manager.stop()
        logger.info("="*60)


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="Bot de WhatsApp para envio diário de mensagens",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py --setup          Configuração inicial
  python main.py --first-run      Primeira execução (login no WhatsApp)
  python main.py                  Enviar mensagem diária
  python main.py --test           Testar envio sem atualizar data
        """
    )

    parser.add_argument('--setup', action='store_true',
                        help='Executar assistente de configuração inicial')
    parser.add_argument('--first-run', action='store_true',
                        help='Primeira execução - Login no WhatsApp Web')
    parser.add_argument('--test', action='store_true',
                        help='Modo de teste - Envia mensagem sem atualizar data')

    args = parser.parse_args()

    try:
        if args.setup:
            setup()
        elif args.first_run:
            first_run()
        elif args.test:
            test_message()
        else:
            # Execução normal - enviar mensagem
            send_message()

    except KeyboardInterrupt:
        print("\n\n✗ Operação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
        print(f"\n✗ Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
