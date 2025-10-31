# TP 1

**Nom** **:** Damien Paszkiewicz

## Objectif général

Découvrir Docker en manipulant des images existantes, en conteneurisant un script Python très simple et en comprenant le cycle de vie d’un conteneur (build, run, inspect, logs, nettoyage).

## Prérequis

- Docker Desktop, Docker Engine ou Colima/Rancher Desktop opérationnel
- Accès à un terminal (bash/zsh) avec curl , python3
- Bases de CLI Linux (navigation, exécution de commandes)

## Compétences visées

- Vérifier l’installation et comprendre les informations principales du daemon Docker
- Télécharger et exécuter des images officielles
- Construire une image à partir d’un Dockerfile minimal
- Gérer les conteneurs (logs, stop, rm) et nettoyer l’environnement

## Fil rouge du TP

Tu vas transformer un script Python qui génère un message de bienvenue en image Docker indépendante. À chaque étape tu apprendras une commande clé pour passer de « je lance un script sur ma machine » à « je lance un conteneur portable ».
Arborescence recommandée : `~/workspace/docker-basic-1`

# **Étape 0 — Vérifier Docker**

```yaml
~$ sudo docker version
Client: Docker Engine - Community
 Version:           28.5.1
 API version:       1.51
 Go version:        go1.24.8
 Git commit:        e180ab8
 Built:             Wed Oct  8 12:17:26 2025
 OS/Arch:           linux/amd64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          28.5.1
  API version:      1.51 (minimum version 1.24)
  Go version:       go1.24.8
  Git commit:       f8215cc
  Built:            Wed Oct  8 12:17:26 2025
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          v1.7.28
  GitCommit:        b98a3aace656320842a23f4a392a33f46af97866
 runc:
  Version:          1.3.0
  GitCommit:        v1.3.0-0-g4ca628d1
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```

- Différences entre la partie Client et Server :
    - Le **Client Docker** est l’interface que j’utilise dans le terminal pour envoyer des commandes.
    - Le **Server Docker (daemon)** est le moteur qui reçoit ces commandes et gère concrètement les conteneurs et images.

| Élément | Version | Rôle |
| --- | --- | --- |
| **Client Docker** | 28.5.1 | Programme `docker` CLI |
| **Server (Engine)** | 28.5.1 | Démon Docker principal |
| **API version** | 1.51 | Version de communication Client ↔ Server |
| **Go version** | go1.24.8 | Langage utilisé pour compiler Docker |
| **containerd** | v1.7.28 | Gestionnaire de conteneurs |
| **runc** | 1.3.0 | Exécuteur bas niveau des conteneurs |
| **docker-init** | 0.19.0 | Petit binaire pour init dans les conteneurs |

```yaml
~$ sudo docker info
Client: Docker Engine - Community
 Version:    28.5.1
 Context:    default
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.29.1
    Path:     /usr/libexec/docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v2.40.3
    Path:     /usr/libexec/docker/cli-plugins/docker-compose

Server:
 Containers: 5
  Running: 0
  Paused: 0
  Stopped: 5
 Images: 1
 Server Version: 28.5.1
 Storage Driver: overlay2
  Backing Filesystem: extfs
  Supports d_type: true
  Using metacopy: false
  Native Overlay Diff: true
  userxattr: false
 Logging Driver: json-file
 Cgroup Driver: systemd
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local splunk syslog
 CDI spec directories:
  /etc/cdi
  /var/run/cdi
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: b98a3aace656320842a23f4a392a33f46af97866
 runc version: v1.3.0-0-g4ca628d1
 init version: de40ad0
 Security Options:
  apparmor
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 6.8.0-87-generic
 Operating System: Linux Mint 22.2
 OSType: linux
 Architecture: x86_64
 CPUs: 8
 Total Memory: 15.28GiB
 Name: rusty-ThinkPad-T490s
 ID: a2aeb713-09f6-42d5-ba91-5ae6388c18ec
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 Experimental: false
 Insecure Registries:
  ::1/128
  127.0.0.0/8
 Live Restore Enabled: false
```

- Storage Driver : `overlay2`
- Runtime par défaut : `runc`
- nombre d’images et de conteneurs déjà présents
    - Containers: 5
        - Running: 0
        - Paused: 0
        - Stopped: 5
    - Images: 1

## Étape 1 — Exécuter des images existantes

### Hello World

```
~$ sudo docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

- Le client contacte le démon Docker
- Téléchargement de l’image (pull)
- Création et exécution du conteneur
- Affichage du résultat dans le terminal

### Shell éphémère en Alpine

```
~$ sudo docker run -it --rm alpine:3.20 sh
Unable to find image 'alpine:3.20' locally
3.20: Pulling from library/alpine
5311e7f182d0: Pull complete 
Digest: sha256:765942a4039992336de8dd5db680586e1a206607dd06170ff0a37267a9e01958
Status: Downloaded newer image for alpine:3.20
/ # ls /
bin    etc    lib    mnt    proc   run    srv    tmp    var
dev    home   media  opt    root   sbin   sys    usr
/ # touch testfile.txt
/ # ls
bin           lib           proc          srv           usr
dev           media         root          sys           var
etc           mnt           run           testfile.txt
home          opt           sbin          tmp
/ # exit
~$ sudo docker run -it --rm alpine:3.20 sh
/ # ls
bin    etc    lib    mnt    proc   run    srv    tmp    var
dev    home   media  opt    root   sbin   sys    usr
/ # exit
```

```bash
~$ sudo docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                      PORTS     NAMES
32b7947c2195   hello-world   "/hello"   31 minutes ago   Exited (0) 31 minutes ago             silly_rubin
f00cd93f4e46   hello-world   "/hello"   36 minutes ago   Exited (0) 36 minutes ago             hopeful_galileo
8d0df217e112   hello-world   "/hello"   4 weeks ago      Exited (0) 4 weeks ago                romantic_goldstine
942188aafcd1   hello-world   "/hello"   4 weeks ago      Exited (0) 4 weeks ago                funny_brattain
b255b0ca29ef   hello-world   "/hello"   4 weeks ago      Exited (0) 4 weeks ago                heuristic_keller
7ca962422da9   hello-world   "/hello"   4 weeks ago      Exited (0) 4 weeks ago                mystifying_carver
~$ sudo docker rm 7ca962422da9
7ca962422da9
...
~$ sudo docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

# Étape 2 — Préparer le projet Python

```python
mkdir -p ~/Documents/B3dev/Docker/docker-basic-1 && cd ~/Documents/B3dev/Docker/docker-basic-1
git init .
cat > welcome.py <<'PY'
import datetime
import platform
def banner() -> str:
return (
"Bonjour Docker !\n"
f"Date et heure : {datetime.datetime.utcnow().isoformat()}Z\n"
f"Système : {platform.system()} {platform.release()}"
)
if __name__ == "__main__":
print(banner())
PY
```

Vérifie l’exécution locale

```python
python3 welcome.py
```

```python
~/Documents/B3dev/Docker/docker-basic-1$ python3 welcome.py
Bonjour Docker !
Date et heure : 2025-10-31T10:02:13.557552Z
Système : Linux 6.8.0-87-generic
```

# Étape 3 — Écrire un Dockerfile minimal

1. Crée Dockerfile 
    
    ```python
    # syntax=docker/dockerfile:1
    FROM python:3.12-slim
    WORKDIR /app
    COPY welcome.py .
    CMD ["python", "welcome.py"]
    ```
    
2. Construis l’image : 
    
    ```python
    ~/Documents/B3dev/Docker/docker-basic-1$ sudo docker build -t welcome:1.0.0 .
                
    [+] Building 7.0s (10/10) FINISHED                                    docker:default
     => [internal] load build definition from Dockerfile                            0.0s
     => => transferring dockerfile: 148B                                            0.0s
     => resolve image config for docker-image://docker.io/docker/dockerfile:1       1.2s
     => docker-image://docker.io/docker/dockerfile:1@sha256:b6afd42430b15f2d2a4c5a  0.6s
     => => resolve docker.io/docker/dockerfile:1@sha256:b6afd42430b15f2d2a4c5a02b9  0.0s
     => => sha256:77246a01651da592b7bae79e0e20ed3b4f2e4c00a1b54b 13.57MB / 13.57MB  0.4s
     => => sha256:b6afd42430b15f2d2a4c5a02b919e98a525b785b1aaff167 8.40kB / 8.40kB  0.0s
     => => sha256:62b0eac4b38b65f257ba2525a1bc87978b5e339d6133b5daef1b 850B / 850B  0.0s
     => => sha256:6742480c08d7878bbb82a5f5b55d7cb17c5dea60d2068cb2 1.33kB / 1.33kB  0.0s
     => => extracting sha256:77246a01651da592b7bae79e0e20ed3b4f2e4c00a1b54b7c921c9  0.1s
     => [internal] load metadata for docker.io/library/python:3.12-slim             1.5s
     => [internal] load .dockerignore                                               0.0s
     => => transferring context: 2B                                                 0.0s
     => [1/3] FROM docker.io/library/python:3.12-slim@sha256:e97cf9a2e84d604941d99  3.1s
     => => resolve docker.io/library/python:3.12-slim@sha256:e97cf9a2e84d604941d99  0.0s
     => => sha256:324231aabbd84383faa67463fb653f94cfab52b71ec3a56f 5.58kB / 5.58kB  0.0s
     => => sha256:38513bd7256313495cdd83b3b0915a633cfa475dc2a070 29.78MB / 29.78MB  1.0s
     => => sha256:f2a111092025316a53c811d958b8c96faf9e98f6245c9a9c 1.29MB / 1.29MB  0.6s
     => => sha256:79f2dc6dd7d858f8963f236b2ab93a0f607fc2e3554e19 12.11MB / 12.11MB  0.6s
     => => sha256:e97cf9a2e84d604941d9902f00616db7466ff302af4b1c 10.37kB / 10.37kB  0.0s
     => => sha256:408ad54fa40b7a4fff7cb21ce6e1b74eb5154bfc6c0fbd0a 1.75kB / 1.75kB  0.0s
     => => sha256:d2876f169c021dd03855501cad6f7f8d06701774c8fbbff1b13e 250B / 250B  0.9s
     => => extracting sha256:38513bd7256313495cdd83b3b0915a633cfa475dc2a07072ab2c8  0.7s
     => => extracting sha256:f2a111092025316a53c811d958b8c96faf9e98f6245c9a9cc1b7d  0.1s
     => => extracting sha256:79f2dc6dd7d858f8963f236b2ab93a0f607fc2e3554e19e244b3c  0.9s
     => => extracting sha256:d2876f169c021dd03855501cad6f7f8d06701774c8fbbff1b13e7  0.0s
     => [internal] load build context                                               0.0s
     => => transferring context: 322B                                               0.0s
     => [2/3] WORKDIR /app                                                          0.1s
     => [3/3] COPY welcome.py .                                                     0.1s
     => exporting to image                                                          0.1s
     => => exporting layers                                                         0.0s
     => => writing image sha256:e96a6cd6a18ce49fcbaeb4c115ca817d6453b47ea60f2ee36b  0.0s
     => => naming to docker.io/library/welcome:1.0.0                                0.0s
    ```
    
3. Exécute et compare : 
    
    ```python
    ~/Documents/B3dev/Docker/docker-basic-1$ sudo docker run --rm welcome:1.0.0
    Bonjour Docker !
    Date et heure : 2025-10-31T10:12:12.468712Z
    Système : Linux 6.8.0-87-generic
    ```
    

| Élément | Exécution locale | Conteneur | Explication |
| --- | --- | --- | --- |
| Date / heure | 2025-10-31T10:02:13Z | 2025-10-31T10:12:12Z | L’horodatage est généré à l’exécution, donc il change à chaque run |
| Système | Linux 6.8.0-87-generic | Linux 6.8.0-87-generic | Le conteneur utilise **le même noyau que l’hôte** mais son système de fichiers et les binaires sont isolés |
| Plateforme | Linux Mint 22.2 | Debian slim (conteneur) | La distribution à l’intérieur du conteneur est différente (Python et librairies viennent de l’image) |

# Étape 4 — Personnaliser l’exécution

Objectif : comprendre CMD vs arguments

1. Passe un message personnalisé en variable d’environnement :
    
    ```python
    import datetimeimport platformimport os
    def banner() -> str:    name = os.getenv("WELCOME_NAME", "Docker")    return (        f"Bonjour {name} !\n"        f"Date et heure : {datetime.datetime.utcnow().isoformat()}Z\n"        f"Système : {platform.system()} {platform.release()}"    )
    if __name__ == "__main__":    print(banner())
    ```
    
    ```python
    ~/Documents/B3dev/Docker/docker-basic-1$ sudo docker run --rm -e WELCOME_NAME="Alice" welcome:1.0.0
    Bonjour Alice !
    Date et heure : 2025-10-31T10:19:18.520504Z
    Système : Linux 6.8.0-87-generic
    ```
    
2. Surcharge la commande au run :
    
    ```python
    ~/Documents/B3dev/Docker/docker-basic-1$ sudo docker run --rm welcome:1.0.0 python -c "print('Commande override')"
    Commande override
    ```
    

➜ Explique la différence entre CMD dans le Dockerfile et les arguments passés au docker run .

| Élément | Explication |
| --- | --- |
| **CMD** dans Dockerfile | Commande par défaut à exécuter lorsque tu lances le conteneur sans arguments supplémentaires. |
| **Arguments passés à `docker run`** | Ils **remplacent CMD** pour cette exécution seulement. Le Dockerfile reste inchangé. |

# Étape 5 — Inspecter, logger, nettoyer

1. Lance le conteneur en arrière-plan :
    
    ```python
    ~/Documents/B3dev/Docker/docker-basic-1$ sudo docker run -d --name welcome_app welcome:1.0.0 sleep 60
    bf28dd47b5236d57dec430194a8c2e2cd2199cbae9e9ada4d63f19479b46cd54
    ```
    
2. Observe les métadonnées :
    
    ```python
    ~/Documents/B3dev/Docker/docker-basic-1$ sudo docker inspect welcome_app | jq '.[0].Config.Env'
    [
      "PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
      "LANG=C.UTF-8",
      "GPG_KEY=7169605F62C751356D054A26A821E680E5FA6305",
      "PYTHON_VERSION=3.12.12",
      "PYTHON_SHA256=fb85a13414b028c49ba18bbd523c2d055a30b56b18b92ce454ea2c51edc656c4"
    ]
    ```
    
    ```python
    ~/Documents/B3dev/Docker/docker-basic-1$ sudo docker logs welcome_app
    ```
    
    ```python
    ~/Documents/B3dev/Docker/docker-basic-1$ sudo docker top welcome_app
    UID                 PID                 PPID                C                   STIME               TTY                 TIME                CMD
    root                34742               34719               0                   11:31               ?                   00:00:00            sleep 300
    ```
    
3. Stoppe et supprime :
    
    ```python
    
    ~/Documents/B3dev/Docker/docker-basic-1$ sudo docker stop welcome_app
    
    ```
    
    ```python
    ~/Documents/B3dev/Docker/docker-basic-1$ sudo docker rm welcome_app
    ```
    
4. Nettoie les images inutilisées :
    
    ```python
    ~/Documents/B3dev/Docker/docker-basic-1$ sudo docker image prune
    WARNING! This will remove all dangling images.
    Are you sure you want to continue? [y/N] y
    Deleted Images:
    deleted: sha256:e96a6cd6a18ce49fcbaeb4c115ca817d6453b47ea60f2ee36b820dcbacfc5c3c
    
    Total reclaimed space: 0B
    
    ```
    

| Action | Objet ciblé | Effet |
| --- | --- | --- |
| `docker rm` | Conteneur | Supprime une **instance** en cours ou arrêtée, l’image reste |
| `docker image rm` | Image | Supprime un **template** pour créer des conteneurs, mais n’affecte pas les conteneurs déjà créés |

# Bilan du TP

- Ce qui change entre l’exécution locale et conteneurisée

| Aspect | Exécution locale | Exécution conteneurisée | Explication |
| --- | --- | --- | --- |
| **Environnement Python** | Utilise Python installé sur l’hôte | Utilise Python de l’image Docker (`python:3.12-slim`) | Le conteneur a son propre environnement isolé et portable |
| **Système / OS** | Linux Mint 22.2 avec noyau 6.8.0-87-generic | Debian slim (conteneur) avec noyau du host | Le conteneur partage le **noyau de l’hôte**, mais le reste est isolé (libs, fichiers système) |
| **Fichiers et dossier de travail** | Directement sur ton disque local | Isolé dans le conteneur (`/app`) | Tout ce qui est créé dans le conteneur reste dedans sauf volumes partagés |
| **Horodatage et sortie** | Généré au moment de l’exécution locale | Généré à l’exécution du conteneur | Chaque exécution est indépendante et produit des timestamps différents |
| **Installation de dépendances** | Déjà sur ton système (pip, librairies) | Dépend des packages présents dans l’image | Les dépendances doivent être ajoutées dans le Dockerfile pour être portables |
| **Portabilité** | Limitée à ton système | Très portable : peut être exécuté sur n’importe quel système avec Docker | L’image encapsule tout ce qui est nécessaire à l’exécution du script |
- Les commandes Docker nouvelles pour toi
    - C’est la première fois que j’utilise Docker. Toutes les commandes sont pour moi nouvelle.
- Les difficultés rencontrées
    - Pas de difficulté en particulier. Utilisation de commandes simple.