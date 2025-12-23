# Bot de WhatsApp - Mensagens Automáticas

Bot simples para enviar mensagens automáticas diárias no WhatsApp Web usando Python e Selenium.

Ideal para grupos onde você precisa enviar lembretes, mensagens motivacionais ou avisos diários de forma automatizada. Funciona com ciclo semanal (uma mensagem diferente para cada dia da semana).

## 🎯 O que faz

Envia automaticamente 1 mensagem por dia em um grupo do WhatsApp Web no horário que você configurar. O bot usa um sistema de ciclo semanal - você configura 7 mensagens (uma para cada dia) e ele repete automaticamente toda semana.

**Exemplo de uso:**
- Segunda: "Bom dia! Vamos começar a semana! 💪"
- Sexta: "Sextou! 🎉" + imagem

## 📋 Características

- ✅ **Ciclo semanal** - 7 mensagens diferentes (segunda a domingo)
- ✅ **Horário configurável** - Defina quando enviar
- ✅ **Texto + Imagens** - Suporte a emojis e imagens com legenda
- ✅ **Sessão persistente** - QR Code apenas na primeira execução
- ✅ **Execução em background** - Roda minimizado
- ✅ **Logs detalhados** - Histórico completo de envios
- ✅ **Windows** - Configurado para rodar no Agendador de Tarefas

## 🔧 Requisitos

- Windows
- Python 3.7+
- Chrome, Edge ou Firefox

## 📦 Instalação Rápida

### 1. Instalar dependências

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar

```cmd
python main.py --setup
```

Responda:
- Navegador: **1** (Chrome)
- Nome do grupo: **"Seu Grupo"**
- Horário: **09:00**
- Minimizar janela: **s**

### 3. Login no WhatsApp (primeira vez)

```cmd
python main.py --first-run
```

1. Escaneie o QR Code
2. Aguarde confirmação
3. Pressione Enter

Pronto! A sessão está salva.

### 4. Configurar mensagens

Edite os arquivos em `messages\`:

```
messages\
├── segunda.txt   - Segunda-feira
├── terca.txt     - Terça-feira
├── quarta.txt    - Quarta-feira
├── quinta.txt    - Quinta-feira
├── sexta.txt     - Sexta-feira
├── sabado.txt    - Sábado
└── domingo.txt   - Domingo
```

**Com imagens (opcional):**
- Adicione: `images\segunda.jpg`, `images\sexta.png`, etc.
- O texto vira legenda automaticamente

### 5. Testar

```cmd
python main.py --test
```

### 6. Agendar (Agendador de Tarefas do Windows)

1. Pressione `Win + R` → digite `taskschd.msc`
2. **Criar Tarefa Básica**
3. Nome: `WhatsApp Bot`
4. Gatilho: **Diariamente** no horário configurado (ex: 09:00)
5. Ação: **Iniciar programa**
6. Programa: Caminho completo para `run_bot.bat`
   ```
   C:\Users\SeuUsuario\Documents\Script_Bot\run_bot.bat
   ```
7. Iniciar em: Diretório do projeto
   ```
   C:\Users\SeuUsuario\Documents\Script_Bot
   ```
8. Concluir

**Via PowerShell (alternativa):**

```powershell
$action = New-ScheduledTaskAction -Execute "C:\caminho\completo\run_bot.bat" -WorkingDirectory "C:\caminho\completo\Script_Bot"
$trigger = New-ScheduledTaskTrigger -Daily -At 9:00AM
Register-ScheduledTask -TaskName "WhatsApp Bot" -Action $action -Trigger $trigger
```

## 📖 Uso

### Comandos

```cmd
python main.py --setup      # Configuração inicial
python main.py --first-run  # Login no WhatsApp (primeira vez)
python main.py --test       # Testar envio (não atualiza data)
python main.py              # Enviar mensagem do dia
```

### Estrutura de Arquivos

```
Script_Bot\
├── main.py              # Script principal
├── config.json          # Configurações (gerado automaticamente)
├── run_bot.bat          # Executar bot (usar no agendador)
├── ativar_venv.bat      # Ativar ambiente virtual
├── whatsapp_bot\        # Código do bot
├── messages\            # Mensagens (7 arquivos .txt)
├── images\              # Imagens opcionais
├── profiles\            # Sessão do WhatsApp
└── logs\                # Logs de execução
```

### Como Funciona

O bot identifica o dia da semana e envia a mensagem correspondente:

```
Segunda  →  messages\segunda.txt
Terça    →  messages\terca.txt
Quarta   →  messages\quarta.txt
Quinta   →  messages\quinta.txt
Sexta    →  messages\sexta.txt
Sábado   →  messages\sabado.txt
Domingo  →  messages\domingo.txt
```

Ciclo se repete automaticamente toda semana!

### Configuração do Horário

**Via setup:**
```cmd
python main.py --setup
```

**Manual (config.json):**
```json
{
    "send_time": "09:00"
}
```

## 📝 Exemplos de Mensagens

### Texto simples

`messages\segunda.txt`:
```
Bom dia! Segunda-feira! 💪
Vamos começar a semana!
```

### Com imagem

`messages\sexta.txt`:
```
Sextou! 🎉
```

`images\sexta.jpg` → (sua imagem)

Resultado: Imagem enviada com legenda "Sextou! 🎉"

## 🔍 Logs

Logs em: `logs\bot_YYYY-MM-DD.log`

Ver log:
```cmd
type logs\bot_2025-12-23.log
```

## 🐛 Solução de Problemas

### "python não é reconhecido"
- Reinstale Python e marque "Add to PATH"

### "Navegador não abre"
- Verifique se Chrome/Edge está instalado
- Execute: `pip install --upgrade selenium`
- Tente outro navegador: `python main.py --setup`

### "Grupo não encontrado"
- Verifique nome exato do grupo (maiúsculas/minúsculas)
- Fixe o grupo no WhatsApp Web

### "QR Code não aparece"
- Delete pasta `profiles\`
- Execute: `python main.py --first-run`

### "Mensagem não enviada"
- Veja logs: `type logs\bot_*.log`
- Execute: `python main.py --test`

### "Sessão expirou"
- Execute: `python main.py --first-run`
- Escaneie QR Code novamente

### Verificar tarefas agendadas
```cmd
schtasks /query /tn "WhatsApp Bot"
```

### Executar tarefa manualmente
```cmd
schtasks /run /tn "WhatsApp Bot"
```

### Remover tarefa
```cmd
schtasks /delete /tn "WhatsApp Bot" /f
```

## ⚙️ Configurações (config.json)

```json
{
    "browser": "chrome",           // chrome, edge ou firefox
    "group_name": "Meu Grupo",     // Nome do grupo
    "send_time": "09:00",          // Horário de envio (HH:MM)
    "last_send_date": "2025-12-23",
    "headless": false,
    "minimize_window": true
}
```

## ⚠️ Importante

- Uso pessoal e educacional
- Apenas 1 mensagem por dia
- Não compartilhe a pasta `profiles\` (contém sua sessão)
- Mantenha backup das mensagens

## 📞 Suporte

1. Veja os logs: `logs\`
2. Execute: `python main.py --test`
3. Refaça login: `python main.py --first-run`

---

**Python + Selenium** 🐍✨
