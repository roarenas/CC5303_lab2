# CC5303 Laboratorio 2

En el siguiente laboratorio tomaremos como base al **laboratirio 1**, al cual le iremos realizando modificaciones para terminar en un ambiente distribuido revisando lo problemas que estos conllevan.
Cada commit es el inicio de una nueva etapa dentro del laboratorio, en cada etapa iremos revisando sus implicancias en el SD.

En este laboratorio utilizaremos un nuevo archivo llamado *docker-compose.yaml*, este archivo nos permite definir un proyecto de servicios prestados por contenedores, los requisitos de los mismoas, asi como la dependencia que estos pueden tener de recursos (ej. *red, disco, etc*) o de otros servicios.

El conjunto de servicios y recursos que componen este proyecto se le denomina *compose* (componer en español).

## Paso 0

- [ ] Crear el archivo *docker-compose.yaml*
- [ ] Crear en el directorio local la carpeta log y el archivo log.txt
```bash
mkdir log
touch log/log.txt
```
- [ ] Ejecutar *docker compose build*
- [ ] Ejecutar *docker compose up*
> [!Observe] La ejecución de los contenedores no posee un orden por defecto
- [ ] Revisar el contenido del archivo log.txt
```bash
cat log/log.txt
```

## Paso 1

Dado que los contenedores parten sin un orden especifico, impondremos un orden de inicio mediante el uso de la dependencia, es decir, *client* depende de que *webapp* este atendiendo clientes en el servicio que presta.
Para ello agregaremos en el archivo *docker-compose.yaml* en la seccion del servicio *webapp* lo siguiente.
```yaml
healthcheck:
      test: [ "CMD-SHELL", "curl http://127.0.0.1:8000/random" ]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 5s
```
La caracteristica de *healtcheck* nos permite evaluar la salud del contenedor.
Luego en la seccion del servicio agregamos
```yaml
depends_on:
      webapp:
        condition: service_healthy
```
Con esta caracteristica le indicamos al demonio de docker que este contenedor debe esperar a que el estado de salud del contenedor que aloja *webapp* sea saludable.

Luego ampliaremos el funcionamiento del cliente para que consulte cada 1 segundo por el servicio

```bash
while true; do
  echo -n "\$MY_NAME ">>\$MY_LOG_FILE;
  curl -s http://webapp:8000/random 2>&1 >> \$MY_LOG_FILE;
  sleep 1;
  done
```
Ahora proceguimos con
- [ ] Ejecutar *docker compose build*
- [ ] Ejecutar *docker compose up*
- [ ] Revisar el contenido del archivo log.txt en una terminal exclusiva
```bash
tail -f log/log.txt
```

Finalmente generaremos una nuevo container con la imagen *lab2-client* mientras monitoreamos */tmp/log/log.txt*

```bash
docker run --rm --name test-app -v ./log:/tmp/log --network lab2_intranet1 lab2-client:latest
```

## Comandos utiles

### Comandos nuevos
```bash
    docker compose ls
``` 

El comando *compose ls* permite revisar los "*compose*"s que estan en ejecución.

```bash
    docker compose build
``` 
El comando *compose build* permite la construcción de las imagenes asociadas al *compose* siguiendo el archivo docker-compose.yaml alojado en el directorio en el cual nos encontramos (*./*).
Asumamos que el nombre de nuestro *compose* es *lab2*, entonces luego de generar las imagenes correctamente si revisamos las imagenes disponible mediante *docker image ls*, podremos constatar que las imagenes del lab1 ahora se llaman lab2-webapp:version, por ejemplo *lab2-webapp:latest*
```bash
    docker compose up
``` 
El comando *compose up* procede levantar los *servicios* y crear aquellos recursos requeridos para que los servicios operen de forma correcta.
Nota: la salida estandar o *stdout* de los contenedores queda conectada a la terminal donde se ejecuta este comando. Para salir de este comando y parar la ejecución del *compose* debe presionar *CTRL-C*.

```bash
    docker compose start
``` 

El comando *compose start* es equivalente a *compose up* con la excepción que la *stdout* no queda conectada al a terminal.

```bash
    docker compose stop
``` 

El comando *compose stop* permite terminar la ejecución del compose levantado mediante *compose start*


### Comandos anteriores

```bash
    docker ps
``` 
El comando *ps* permite ver que contenedores estan corriendo (*run*) o que se ejecutaron recientemente.
```bash
docker pull IMAGE
```
El comando *pull* permite descargar desde dockerhub la imagen IMAGE para ser almacenada y utilizada localmente.
```bash
docker image ls
```
El comando *image ls* lista las imagenes tenemos descargadas localmente, los *tags* que tiene asociados y las distintas versiones que poseen, si el ID es el mismo entoces es la misma imagen con un *tag* de referencia distinto.
Ejemplo:

| IMAGE | ID | DISK USAGE | CONTENT SIZE | EXTRA |
|--|--|--|--|--|
alpine:latest | 5b10f432ef3d | 13.1MB | 3.95MB|
|busybox:latest | fd8d9aa63ba2 | 6.81MB | 2.23MB|
|debian:latest | 4ae67669760b | 186MB | 52.5MB

```bash
docker network ls
```
El comando *network ls* lista las redes existentes en docker y los modos en que estan funcionado.
```bash
docker build -t tag:version
```
El comando *build* permite crear una imagen con el "nombre" o *tag:version*, utilizando el archivo *Dockerfile* almacenado en el directorio desde el cual ejecutamos el comando.\
```bash
docker run -it --rm --name NOMBRE --network RED tag:version [COMANDO]
```
El comando *run* crea un contenedor denominado *NOMBRE* utilizando la imagen *tag:version* y lo deja conectado a la red RED. Las siguientes opciones realizan:
*-it* : permite ejecutar el comando COMANDO de forma interctiva y alojado en el contenedor.
*--rm* : permite que al terminar la ejecución del contenedor, el volumen utilizado sea eliminado.
*COMANDO* : el contenedor una vez que se levanta correctamente ejecutará el comando predefinido en la imagen o en su lugar el indicado
```bash
docker exec -it [NOMBRE|ID] COMANDO
```
El comando *exec* permite ejecutar el *COMANDO* al interior del contenedor identificado por el *NOMBRE* o el *ID* generado al momento de su creación.
