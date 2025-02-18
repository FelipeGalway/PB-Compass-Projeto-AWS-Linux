import requests
import logging
from datetime import datetime

logging.basicConfig(filename='/var/log/monitoramento.log', level=logging.INFO)

url = "seu_site_aqui"

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
        logging.error(f"{datetime.now()} - Erro ao tentar acessar o site: {e}")
        mensagem = f"{datetime.now()} - Site {url} está INDISPONÍVEL devido a erro de rede: {e}"
        logging.error(mensagem)
        enviar_notificacao_discord(f"ALERTA: O site {url} está INDISPONÍVEL devido a erro de rede: {e}")
        return  

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if status != 200:
        mensagem = f"{data_hora} - Site {url} está INDISPONÍVEL (Código HTTP: {status})"
        logging.error(mensagem)
        enviar_notificacao_discord(f"ALERTA: O site {url} está INDISPONÍVEL! (Código HTTP: {status})")
    else:
        mensagem = f"{data_hora} - Site {url} está DISPONÍVEL (Código HTTP: {status})"
        logging.info(mensagem)

if __name__ == "__main__":
    monitorar_site()
