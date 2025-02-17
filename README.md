# Projeto de Configuração de Servidor Web com Nginx na AWS

Este projeto foi desenvolvido no programa de bolsas da Compass Uol. Tem como objetivo configurar uma instância EC2 na AWS para hospedar uma página web utilizando o servidor Nginx.

## Etapa 1: Configuração do Ambiente

### 1. Criação de uma VPC na AWS
- Crie uma VPC com 2 sub-redes públicas e 2 sub-redes privadas na seção **VPC**, no campo **Your VPCs**.
- Configure um **Internet Gateway** para vincular às sub-redes públicas, na mesma seção.

### 2. Criação de uma Instância EC2
- Crie uma instância EC2 na seção **EC2**, no campo **Instances**. A instância de exemplo foi criada com uma AMI baseada no **Amazon Linux**.
- Adicione as tags necessárias e associe a instância à VPC criada anteriormente, além de colocá-la em uma sub-rede pública.
- Crie e vincule uma chave `.pem` à instância.

### 3. Configuração do Acesso à Instância EC2
- Associe um **Security Group** à instância, permitindo tráfego de entrada nas seguintes portas:
  - **HTTP** (porta 80)
  - **SSH** (porta 22)
- Nas regras de saída, configure **All Traffic**, permitindo acesso ao IP `0.0.0.0/0`.

### 4. Acesso à Instância EC2 via SSH
- Acesse a instância EC2 via SSH para iniciar as configurações necessárias.
- A conexão foi realizada utilizando o **Visual Studio Code**.
- Para isso, selecione a instância na AWS, clique em **Connect**, copie o comando exibido no campo **SSH Client** e cole no terminal do VS Code. Substitua "nome_da_chave" pelo caminho correto da chave, que deve estar localizado na pasta `C:\Users\seu_usuario\.ssh`.

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

- Teste a página acessando a instância pelo seu **IP público** no navegador. Se tudo estiver configurado corretamente, a página HTML será exibida.

### 4. Configuração para Reinício Automático do Nginx
- Configure o Nginx para reiniciar automaticamente em caso de pausa: