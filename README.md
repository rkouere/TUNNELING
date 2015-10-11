# TUNNELING

Bonnes info
http://www.binarytides.com/python-socket-programming-tutorial/

# Web côté maison
## Connection avec le serveur
Lance un serveur qui écoute sur le port 80 tous les packets venant de l'addresse IP de l'entreprise
Lorsqu'il reçoit une requette, il accepte la demande de connection et initialise une connection TCP avec le serveur

## Lancement de commande SSH 
Le script python écoute sur le port ssh 22 du localhost et "copie" les instructions et les encapsule dans en tant que data dans une requette POST de http
Il les envoit ensuite vers l'ip

# Web côté entreprise
## Connection à la maison
Envoit d'une requette SYN à interval régulié vers l'ip/l'adresse de la maison
Lorsqu'une connection a été accepté, il envoit son identifiant (ip, nom de machine etc...)

## Lancement de commande SSG
Le script écoute ensuite sur le port 22 du localhost et renvoit les réponse de ssh dans un POST
Lorsque le script reçoit des POST, il récupère le contenu du message body et effectue un requette ssh sur le port 22 de locahost

Chaque requette doit avoir une expiry date de quelques millisecondes/dans le passé si possible

# Formation des paquets
Pour éviter que le proxy ne garde la page en cache
```
response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
response.headers["Pragma"] = "no-cache" # HTTP 1.0.
response.headers["Expires"] = "0" # Proxies.
```
Le content sera en text/html
```
Content-Type:text/html
```
Il faudra utiliser la taille de contenu
```
"Content-Length:" TailleDuContenu 
```

# Test
Depuis la racine
```
python3 -m unittest
```
