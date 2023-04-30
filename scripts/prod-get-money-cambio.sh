echo "remove selenium-server"
sudo docker rm -f selenium-server
echo "sobe selenium-server"
sudo docker run -d -p 4444:4444 --shm-size="2g" --network host --env-file /home/${USER}/.secrets/.env --name selenium-server selenium/standalone-chrome:4.4.0-20220812 
echo "aguarda 10 sec ..."
sleep 10
echo "roda python script"
sudo docker exec emoneycambio python tools.py get_coins_get_money_corretora
echo "remove selenium-server"
sudo docker rm -f selenium-server 
echo "fim"