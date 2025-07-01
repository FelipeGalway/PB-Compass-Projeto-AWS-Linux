# ⚙️ Configuração de Servidor Web com Nginx na AWS

> Este projeto foi desenvolvido como parte do programa de bolsas da Compass Uol e tem como objetivo configurar um servidor web na AWS utilizando **Nginx**, com **monitoramento automatizado** e **notificações via Discord**.  
> Ideal para praticar habilidades em **cloud computing**, **automação com cron** e **infraestrutura como serviço (IaaS)**.

---

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de que você tem:

- ✅ Conta ativa na AWS
- ✅ Chave SSH configurada para EC2
- ✅ Familiaridade com terminal / linha de comando
- ✅ Editor de texto (VS Code recomendado)

---

## 🚀 Tecnologias Utilizadas

Este projeto utiliza diversas ferramentas para garantir uma infraestrutura web monitorada e automatizada:

- 🧱 **Amazon VPC** — Criação de redes e sub-redes
- 💻 **Amazon EC2** — Instância virtual na nuvem
- 🐧 **Amazon Linux** — Sistema operacional da instância
- 🌐 **Nginx** — Servidor web leve e eficiente
- 🐍 **Python** — Script de monitoramento
- ⏱️ **cron** — Agendamento da verificação automática
- 🔔 **Discord Webhooks** — Envio de alertas de indisponibilidade

---

## 🛠️ Etapa 1: Configuração do Ambiente na AWS

### 🧭 1. Criando a VPC

- Vá em **VPC > Your VPCs > Create VPC**
- Crie com:
  - 2 sub-redes públicas
  - 2 sub-redes privadas

![VPC](/Prints%20de%20telas/Captura%20de%20tela%202025-02-24%20101838.png)

### 🌐 2. Internet Gateway

- Crie um Internet Gateway em **Internet Gateways > Create**
- Associe-o à VPC e sub-redes públicas criadas

### 🔐 3. Security Group

- Vá em **EC2 > Security Groups > Create**
- Regras de entrada:
  - HTTP (porta 80)
  - SSH (porta 22)
- Regras de saída:
  - All traffic para `0.0.0.0/0`

![Security group](/Prints%20de%20telas/Captura%20de%20tela%202025-02-24%20101922.png)

### 📦 4. Instância EC2

- Use **Amazon Linux 2023 AMI**
- Associe à VPC e sub-rede pública
- Vincule uma **chave .pem** e o **Security Group**

![Instância](/Prints%20de%20telas/Captura%20de%20tela%202025-02-24%20103201.png)

---

## 🔗 Etapa 2: Configuração do Servidor Web (Nginx)

### 📥 1. Instalação do Nginx

```bash
sudo yum install nginx -y
nginx -v
```

### ▶️ 2. Iniciando o serviço
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

### 🖥️ 3. Criando uma Página Web
```bash
sudo nano /usr/share/nginx/html/index.html
```

Acesse pelo IP público da instância para testar.

### ♻️ 4. Reinício automático do Nginx
Edite:

```bash
sudo nano /etc/systemd/system/multi-user.target.wants/nginx.service
```

Adicione:

```ini
Restart=always
RestartSec=30
```

Recarregue:

```bash
sudo systemctl daemon-reload
```

Teste matando o processo:

```bash
ps aux | grep nginx
sudo kill -9 <PID>
```

---

## 🛡️ Etapa 3: Monitoramento e Notificações

### 🐍 1. Script Python de Monitoramento

Crie o script:

```bash
sudo nano /home/ec2-user/monitoramento.py
```

Execute e visualize os logs:

```bash
python3 /home/ec2-user/monitoramento.py
tail -f /home/ec2-user/monitoramento.log
```

### ⏰ 2. Automatizando com cron

Instale e habilite:

```bash
sudo yum install cronie -y
sudo systemctl start crond
sudo systemctl enable crond
```

Configure o agendamento:

```bash
crontab -e
```

Adicione:

```bash
* * * * * /usr/bin/python3 /home/ec2-user/monitoramento.py
```

### 🔔 3. Notificações no Discord

Crie um Webhook no canal desejado

Edite o script com sua URL:

```python
webhook_url = "https://discord.com/api/webhooks/SEU_WEBHOOK"
```

---

## ⚙️ Etapa Alternativa: Configuração via User Data

Durante a criação da EC2:

- Vá em Advanced Details > User Data

- Cole o script automatizado (presente neste repositório)

Esse método agiliza toda a configuração inicial, incluindo Nginx, HTML e script Python.

---

## ✅ Conclusão

Este projeto mostrou como configurar um servidor web completo com Nginx na AWS, com monitoramento automatizado e alertas em tempo real via Discord.

Através do uso de ferramentas como EC2, VPC, cron e Python, foi possível montar um ambiente confiável, com alta disponibilidade e capacidade de auto-recuperação.