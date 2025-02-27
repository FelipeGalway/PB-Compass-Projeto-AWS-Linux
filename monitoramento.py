import requests
import logging
from datetime import datetime

logging.basicConfig(filename='/home/ec2-user/monitoramento.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

url = "http://localhost"

def enviar_notificacao_discord(mensagem):
    webhook_url = "https://discord.com/api/webhooks/SEU_WEBHOOK_AQUI"
    data = {"content": mensagem}
    requests.post(webhook_url, json=data)

def monitorar_site():
    try:
        resposta = requests.get(url, timeout=10)
        status = resposta.status_code
    except requests.exceptions.RequestException as e:
        status = None
        mensagem = f"⚠️ O site {url} está INDISPONÍVEL devido a um erro de rede."
        logging.error(mensagem)
        enviar_notificacao_discord(f"ALERTA: O site {url} está INDISPONÍVEL!")
        return

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if status != 200:
        mensagem = f"⚠️ O site {url} está INDISPONÍVEL (Código HTTP: {status})."
        logging.error(mensagem)
        enviar_notificacao_discord(f"ALERTA: O site {url} está INDISPONÍVEL!")
    else:
        mensagem = f"✅ O site {url} está DISPONÍVEL."
        logging.info(mensagem)

if __name__ == "__main__":
    monitorar_site()
