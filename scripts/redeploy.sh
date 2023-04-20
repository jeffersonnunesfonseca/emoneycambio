docker pull jefonseca/sum && docker rm -f emoneycambio && docker run -d -p 5656:5656 --network host --env-file /run/secrets/env_vars/emoney_prod.env --name emoneycambio jefonseca/sum:latest 
