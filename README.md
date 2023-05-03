# Configuração para windows

- criar ambiente virtual, vai ser utilizado o python que esta na máquina, nesse projeto estamos utilizando o python 3.10.6

- Download do python no windows
```
https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe
```

- Criando ambiente virtual
    - obs: se der erro abrir o power shell como admin e rodar o seguinte comando e confirmar
    ```
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    ```
```

python -m venv venv
```

- ativar o ambiente no windows com power shell
```
.\venv\Scripts\Activate.ps1
```
- Desativar o ambiente no windows com power shell
```
.\venv\Scripts\Activate.ps1
```

# Docker
python 3.9


# Gerar imagem
docker build -t 'emoneycambio' .

# rodar imagem
docker run -d -p 5656:5656 --name emoneycambio emoneycambio:latest

# dica pegar imagem google driver
- https://drive.google.com/u/0/uc?id=1LpuQ1RprZ4Do_WstWAIjeaFq_NQzc3Ai&export=download

# Docker installation
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04

# Configurando o docker hub
`docker login`
jefonseca
personal toke


`export DOCKER_USERNAME=jefonseca`
`export IP_SERVER=xxx.xxx.xx.xx`

# gera imagem e manda para o docker hub
`sh push.sh sum`

# baixa imagem do docker hub
docker pull jefonseca/sum


# tarefas cron

- atualiza moeda comercial
`*/5 * * * * docker exec emoneycambio python tools.py update_exchange_commercial_coin > /tmp/update_exchange_commercial_coin.log &`


- buscar dados da get money, sobre selenium, roda scrit, mata selenium
`*/12 * * * * /bin/sh get-money-cambio.sh > /tmp/get-money-cambio.sh.log &`

- buscar dados da frente-corretora, sobre selenium, roda scrit, mata selenium
`*/12 * * * * docker exec emoneycambio python tools.py get_coins_frente_corretora > get_coins_frente_corretora.log &`

- buscar dados da daycambio(frentecorretora), sobre selenium, roda scrit, mata selenium
`*/12 * * * * docker exec emoneycambio python tools.py get_coins_daycambio > get_coins_daycambio.log &`

# rodar selenium
`docker run -d -p 4444:4444 --shm-size="2g" --env-file .env --name selenium-server selenium/standalone-chrome:4.4.0-20220812`

# nginx base conf
`scp  -i ~/.ssh/id_rsa nginx-conf/www.emoneycambio.com.br.conf root@$IP_SERVER:/etc/nginx/conf.d/www.emoneycambio.com.br.conf`

# quando alterar o seo/sitemap.xml rodar o comando
`scp  -i ~/.ssh/id_rsa sitemap.xml root@$IP_SERVER:/var/www/html/sitemap.xml`

# quando alterar o seo/robots rodar o comando
`scp  -i ~/.ssh/id_rsa robots.txt root@$IP_SERVER:/var/www/html/robots.txt`


# classes de botoes para gtm
```
btn-search-home
btn-buy-search-result
btn-sell-search-result
btn-negotiation-tourism-step-1
btn-negotiation-tourism-step-2
negotiation-international-shipment-main
negotiation-international-shipment-pf-send-step1
negotiation-international-shipment-pf-send-step2
negotiation-international-shipment-pf-receive-step1
negotiation-international-shipment-pf-receive-step2
negotiation-international-shipment-pj-send-step1
negotiation-international-shipment-pj-send-step2
negotiation-international-shipment-pj-receive-step1
negotiation-international-shipment-pj-receive-step2
linkedin-link
instagram-link
aboutus-link
privacypolicy-link
termsuse-link
negotiation-international-shipment-link
negotiation-tourism-link
logo-header-negotiation-tourism-link
logo-footer-negotiation-tourism-link
faq-link
```
