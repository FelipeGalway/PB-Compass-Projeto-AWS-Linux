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

- Edite o arquivo de serviço do Nginx:

   ```bash
   sudo nano /etc/systemd/system/multi-user.target.wants/nginx.service
   ```

- Adicione as seguintes linhas à seção `[Service]`:

   ```bash
   Restart=always
   RestartSec=30
   ```

   - **Restart=always**: Garante que o Nginx reinicie sempre que ele falhar.
   - **RestartSec=30**: Define o tempo de espera (em segundos) antes de tentar reiniciar o Nginx.

- Salve e saia do editor.

- Recarregue o sistema para aplicar as alterações:

   ```bash
   sudo systemctl daemon-reload
   ```

- Teste se a reinicialização automática funcionou simulando uma falha.

   - Obtenha o ID do processo (PID) do Nginx com o comando:

     ```bash
     ps aux | grep nginx
     ```

   - O PID do processo mestre do Nginx será o número exibido antes de `nginx: master process`.

- Mate o processo do Nginx (simulando uma falha) com o comando:

   ```bash
   sudo kill -9 <PID>
   ```

    - Substitua `<PID>` pelo ID do processo mestre do Nginx (o número obtido no passo anterior).

- Verifique o status do Nginx:

   ```bash
   sudo systemctl status nginx
   ```

- O `systemd` deverá detectar que o processo foi morto e tentará reiniciar automaticamente.

---

## Etapa 3: Monitoramento e Notificações

### 1. Criando o Script de Monitoramento
- Um script em Python foi desenvolvido para monitorar a disponibilidade do site. O script pode ser encontrado neste repositório.
- Para utilizar o script, adicione-o na pasta `/home/ec2-use` com o comando:

  ```bash
    sudo nano /home/ec2-user/monitoramento.py
  ```

- Em seguida, copie e cole o conteúdo do script no arquivo, substitua o URL pelo endereço do seu site e salve o arquivo.
- Verifique se o script do Python está registrando as mensagens de disponibilidade do site no arquivo `/home/ec2-user/monitoramento.log` com o seguinte comando:

  ```bash
  python3 /home/ec2-user/monitoramento.py
  tail -f /home/ec2-user/monitoramento.log
  ```

- O script exibirá uma mensagem informando se o site está disponível ou indisponível, juntamente com a data e hora da verificação.

### 2. Configurando o Script para Execução Automática
- Para garantir que o script seja executado automaticamente a cada minuto, será necessário configurá-lo no **cron**. Caso o **cron** ainda não esteja instalado, faça isso com o comando:

  ```bash
  sudo yum install cronie -y
  ```

- Após a instalação, inicie e habilite o serviço do **cron** para que ele inicie automaticamente com o sistema:

  ```bash
  sudo systemctl start crond
  sudo systemctl enable crond
  ```

- Verifique se está funcionando corretamente com:

  ```bash
  sudo systemctl status crond
  ```

- Agora, edite o arquivo **crontab** para adicionar o agendamento de execução do script a cada minuto:

  ```bash
  crontab -e
  ```

- Adicione a seguinte linha no arquivo para rodar o script a cada minuto:

  ```bash
  * * * * * /usr/bin/python3 /home/ec2-user/monitoramento.py
  ```

- Salve e feche o editor. Agora, o script será executado automaticamente a cada minuto.

- Para testar, verifique novamente os logs do script com o comando: 

  ```bash    
    tail -f /home/ec2-user/monitoramento.log
    ```

- A cada minuto, um novo log será registrado, indicando se o site está disponível ou não naquele momento. Você pode alterar o estado do Nginx entre "disponível" e "indisponível" para testar, lembrando que o script faz a verificação a cada minuto, então será necessário aguardar um pouco para ver a atualização nos logs.
