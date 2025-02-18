# Projeto de Configuração de Servidor Web com Nginx na AWS

Este projeto foi desenvolvido como parte do programa de bolsas da Compass Uol e tem como objetivo configurar uma instância EC2 na AWS para hospedar uma página web utilizando o servidor **Nginx**.

---

## Etapa 1: Configuração do Ambiente de Tarefas

### 1. Criação de uma VPC na AWS
- Crie uma **VPC** com **2 sub-redes públicas** e **2 sub-redes privadas** na seção **VPC** em **Your VPCs**.
- Configure um **Internet Gateway** e vincule-o às sub-redes públicas.

### 2. Criação de uma Instância EC2
- Crie uma instância EC2 na seção **EC2** em **Instances**. A instância de exemplo será criada com uma **AMI baseada no Amazon Linux**.
- Adicione as tags necessárias e associe a instância à VPC criada anteriormente, colocando-a em uma sub-rede pública.
- Crie e vincule uma chave `.pem` à instância.

### 3. Configuração do Acesso à Instância EC2
- Associe um **Security Group** à instância, permitindo tráfego de entrada nas seguintes portas:
  - **HTTP** (porta 80)
  - **SSH** (porta 22)
- Nas regras de saída, configure **All Traffic**, permitindo acesso ao IP `0.0.0.0/0`.
- Acesse a instância via SSH para realizar as configurações necessárias.
- A conexão pode ser realizada utilizando o **Visual Studio Code**. Para isso, selecione a instância na AWS, clique em **Connect**, copie o comando exibido no campo **SSH Client** e cole no terminal do VS Code. Substitua "nome_da_chave" pelo caminho correto da chave, que deverá estar em `C:\Users\seu_usuario\.ssh`.

---

## Etapa 2: Configuração do Servidor Web (Nginx)

### 1. Instalação do Nginx
- Instale o servidor **Nginx** utilizando o gerenciador de pacotes do Amazon Linux:

  ```bash
  sudo yum install nginx -y
  ```

- Verifique se o Nginx foi instalado corretamente:

  ```bash
  nginx -v
  ```

### 2. Configuração do Nginx
- Configure o Nginx para iniciar automaticamente com a instância EC2:

  ```bash
  sudo systemctl start nginx
  sudo systemctl enable nginx
  ```

- Verifique se o Nginx está funcionando corretamente:

  ```bash
  sudo systemctl status nginx
  ```

### 3. Criação de uma Página Web Simples
- Crie uma página HTML para ser exibida:

  ```bash
  sudo nano /usr/share/nginx/html/index.html
  ```

- Personalize a página conforme necessário. Após a edição, salve e saia do editor.
- A página usada neste teste pode ser encontrada neste repositório.
- Teste a página acessando a instância pelo seu **IP público** no navegador. Se tudo estiver configurado corretamente, a página HTML será exibida.

### 4. Configuração para Reinício Automático do Nginx
Para garantir que o Nginx seja reiniciado automaticamente em caso de falha, siga os seguintes passos:

1. **Edite o arquivo de serviço do Nginx:**

   ```bash
   sudo nano /etc/systemd/system/multi-user.target.wants/nginx.service
   ```

2. **Adicione as seguintes linhas à seção `[Service]`:**

   ```bash
   Restart=always
   RestartSec=30
   ```

   - **Restart=always**: Garante que o Nginx reinicie sempre que ele falhar.
   - **RestartSec=30**: Define o tempo de espera (em segundos) antes de tentar reiniciar o Nginx.

3. **Salve e saia do editor.**

4. **Recarregue o `systemd` para aplicar as alterações:**

   ```bash
   sudo systemctl daemon-reload
   ```

5. **Teste se a reinicialização automática funcionou simulando uma falha.**

   - **Obtenha o ID do processo (PID) do Nginx** com o comando:

     ```bash
     ps aux | grep nginx
     ```

   - O PID do processo mestre do Nginx será o número exibido antes de `nginx: master process`.

6. **Mate o processo do Nginx** (simulando uma falha) com o comando:

   ```bash
   sudo kill -9 <PID>
   ```

   Substitua `<PID>` pelo ID do processo mestre do Nginx (o número obtido no passo anterior).

7. **Verifique o status do Nginx**:

   ```bash
   sudo systemctl status nginx
   ```

   O `systemd` deverá detectar que o processo foi morto e tentará reiniciar automaticamente.

---

## Etapa 3: Monitoramento e Notificações

### 1. Criando o Script de Monitoramento
- Foi criado um script Python para monitorar a disponibilidade do site. O script está disponível neste repositório.
- Adicione o script à pasta `/home/ec2-user`:

  ```bash
    sudo nano /home/ec2-user/monitoramento.py
  ```

- Copie e cole o conteúdo do script no arquivo, altere o URL para o seu site e salve.
- Verifique se o script do Python está registrando as mensagens de disponibilidade do site no arquivo `/var/log/monitoramento.log`. Você pode monitorar esse arquivo para ver os logs das execuções do script:

  ```bash
  tail -f /var/log/monitoramento.log
  ```

- Caso esteja registrando corretamente e o NGINX estiver ativado, receberá uma mensagem informando que o site está disponível, juntamente com data e hora.
- Se quiser testar com o site indisponível, pare a execução do NGINX:

  ```bash
  sudo systemctl stop nginx
  ```

- Após, execute novamente o comando para verificar as mensagens de disponibilidade. Dessa vez, constará que o site está indisponível. Talvez seja necessário aguardar um pouco para atualizar, já que o monitoramento é feito a cada um minuto.
- Alternativamente, pode testar manualmente o status HTTP do site usando o comando `curl`, para garantir que o código HTTP retornado está correto quando o Nginx está parado:

  ```bash
  curl -I http://34.205.81.108/
  ```

- Quando o Nginx estiver parado, você deverá ver algo como:

  ```bash
  curl: (7) Failed to connect to 34.205.81.108 port 80: Connection refused
  ```

### 2. Configurando o Script para Execução Automática
- Configure o script para rodar automaticamente a cada minuto, editando o arquivo crontab. Caso o crontab não esteja instalado, instale-o com os seguintes comandos:

  ```bash
  sudo yum install cronie -y
  ```

- Inicie e habilite o cron:

  ```bash
  sudo systemctl start crond
  sudo systemctl enable crond
  ```

- Verifique se o cron está funcionando:

  ```bash
  sudo systemctl status crond
  ```

- Após feitas a instalação e a verificação, execute o seguinte comando para editar o arquivo crontab:

  ```bash
  crontab -e
  ```

- Adicione a seguinte linha para agendar a execução do script a cada minuto:

  ```bash
  * * * * * /usr/bin/python3 /home/ec2-user/monitoramento.py
  ```

- Salve e saia do editor. O script agora será executado automaticamente a cada minuto.
```
