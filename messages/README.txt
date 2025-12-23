COMO CONFIGURAR MENSAGENS
=========================

O bot envia uma mensagem diferente para cada dia da semana!

1. MENSAGEM PADRÃO (default.txt):
   - Será enviada quando não houver mensagem específica para o dia
   - Edite o arquivo default.txt com sua mensagem

2. MENSAGENS POR DIA DA SEMANA:
   - Crie/edite arquivos com o nome do dia:
     • segunda.txt  - Mensagem de segunda-feira
     • terca.txt    - Mensagem de terça-feira
     • quarta.txt   - Mensagem de quarta-feira
     • quinta.txt   - Mensagem de quinta-feira
     • sexta.txt    - Mensagem de sexta-feira
     • sabado.txt   - Mensagem de sábado
     • domingo.txt  - Mensagem de domingo

   - O bot enviará automaticamente a mensagem correspondente ao dia

3. MENSAGENS COM IMAGEM:
   - Coloque a imagem na pasta images/
   - Use o mesmo nome do dia: segunda.jpg, terca.jpg, etc.
   - Formatos aceitos: .jpg, .jpeg, .png, .gif
   - Exemplos:
     • images/segunda.jpg
     • images/sexta.png
     • images/domingo.gif

   - O texto do arquivo .txt será usado como legenda da imagem

4. EMOJIS:
   - Você pode usar emojis normalmente nos arquivos de texto
   - Certifique-se de salvar os arquivos com codificação UTF-8

EXEMPLOS:
---------

Mensagem simples de segunda-feira:
  messages/segunda.txt → "Bom dia! Segunda-feira! 💪"

Mensagem com imagem na sexta-feira:
  messages/sexta.txt → "Sextou! 🎉"
  images/sexta.jpg → [sua imagem]

  Resultado: Imagem com legenda "Sextou! 🎉"

CICLO SEMANAL:
--------------

O bot enviará as 7 mensagens em ciclo:
  Segunda → Terça → Quarta → Quinta → Sexta → Sábado → Domingo → Segunda...

Basta configurar uma vez e o bot repete automaticamente toda semana!

HORÁRIO DE ENVIO:
-----------------

Configure o horário de envio durante a configuração inicial:
  python main.py --setup

Ou edite manualmente o arquivo config.json:
  "send_time": "09:00"  (formato HH:MM)
