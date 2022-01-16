# NBA Tracker

Nba Tracker es una aplicación web que basa su contenido en datos de equipos y jugadores de la NBA. Este contenido se obtiene mediante el scrapping de las paginas web oficiales. El contenido es indexado mediante Whoosh y se pueden realizar búsquedas a gran velocidad. Además, en función de la navegación y búsquedas del usuario, se recomiendan ciertos jugadores y equipos que concuerdan con las estadísticas medias de las busquedas de los jugadores o con las etiquetas de los mismos.

![image](https://user-images.githubusercontent.com/47798577/149675737-068fc704-37e9-481c-a56d-63f4a83dc107.png)


## Objetivos

### Usuarios

La mayor parte del uso de pruebas dado a la aplicación se ha realizado con un usuario administrador. Sin embargo, para dar sentido al uso de las recomendaciones en el sistema, se debe implementar la utilidad de login/logout y registro de usuarios.

### Vista de líderes

Se busca ofrecer una vista inicial a modo de _dashboard_ donde cualquier usuario puede ver:

- jugadores líderes en la liga según puntos, rebotes, tapones, asistencias por partido.
- la tabla de clasificación de equipos por conferencia.

### Búsqueda y Resultados

Se deben poder buscar jugadores y equipos de forma sencilla y rápida.

Los resultados de la búsqueda serán equipos o jugadores y se mostraran de forma amigable, con imagenes, etiquetas y datos básicos.

Los resultados podrán ser clickeados para realizar una búsqueda detallada del elemento y mostrar las estadísticas de un jugador o el conjunto de jugadores de un equipo.

### Recomendaciones

Cuando un usuario esté logeado, irá generando datos de búsqueda, concretamente de búsquedas detalladas. Cuando entre en la vista detallada de un equipo o jugador esto será registrado.

Se darán recomendaciones de jugadores y equipos en función de los registros de búsquedas del usuario.

Se recomendaran:

- **Jugadores** según las estadísticas de los mismos haciendo uso de la distancia Manhattan.
- **Jugadores** según las etiquetas de los mismos haciendo uso del coeficiente de Dice.
- **Equipos** según los equipos vistos en detalle y los equipos de los jugadores visitados.

### Panel de Administración

Se debe poder gestionar el populado (incluyendo scrapping) de la base de datos y el indexado de los mismos en whoosh de forma directa desde la aplicación.

Para poder realizar estas acciones el usuario debe estar logueado como administrador.

## Arquitectura

### Django

#### DB

Se hace uso de la base de datos por defecto, sqlite.

#### Modelos

Se han creado los siguientes modelos:

- Conferencia
- Division
- Equipo
- Jugador
- Etiqueta
- Profile
- Search Counters (jugadores y equipos)
- Partido (no implementado)

#### Views

Puesto que se ha implementado un frontend basado en React, se han creado vistas RESTful para dar servicio a las peticiones HTTP realizadas por el frontend.

El index.html inicial de react, en el que esta todo el código js inyectado, se ha usado a forma de template. Se ha servido a través de la vista en `frontend/views.py`.

La API REST se ha implementado en `tracker/views.py` y se ha encargado de servir controladores para:

- populate
- indexado
- gestión de login/logout y resgisto
- búsqueda
- recomendación
- consultas concretas a la bd

### React

Como ya se ha comentado, se ha hecho uso de react para elaborar un frontend SPA ligero.

Las paginas han sido enrutadas y por tanto es fácilmente navegable mediante los botones de "alante" y "atras" del navegador.

Se ha escrito en typescript para que el frontend sea más fácil de mantener. Se ha hecho uso de diversas librerías de funcionalidad y componentes.

## Scrapping

Se ha hecho uso de BeautifulSoup para realizar el scrapping de las páginas web de la NBA. Además, puesto que estas contenían js que no podía ser precargado, se ha realizado la toma de html con Selenium.

El scrapping puede ejecutarse individualmente para testearlo, vaya al archivo `tracker/scrapping.py`, descomente las líneas de `"__main__"` que considere y ejecute el archivo con python. (debe tener las dependencias instaladas, selenium y beautifulsoup)

Se ha hecho scrapping a:

- official_nba_url = "https://es.global.nba.com/"
- official_nba_standings_url = "https://www.nba.com/standings?GroupBy=div&Season=2021-22&Section=overall"
- official_nba_stats_url = "https://www.nba.com/stats/players/traditional/?sort=PLAYER_NAME&dir=-1"
- nba_teams_url = official_nba_url + "teamindex/"
- official_nba_players_url = "https://www.nba.com/players"

Y se han obtenido datos interrelacionados de conferencias, divisiones, equipos, jugadores ..., destacando las imagenes y estadísticas detalladas.

En el caso de los jugadores se han realizado 2 scrappings, para poder obtener estadísticas e imagenes de paginas diferentes.

> Véase admin en el manual de uso.

## Whoosh

Se han indexado jugadores y equipos en whoosh para poder realizar búsquedas "full text" y encontrar jugadores de forma sencilla.

La configuración y funciones de búsqueda e indexado de whoosh pueden encontrarse en `tracker/sarch.py`. El index puede encontrarse en `tracker/search_index`.

En el caso de los equipos las búsquedas son sencillas y poco relevantes, por nombre, abreviatura, conferencia o division.

En el caso de los jugadores, se pueden encontrar jugadores por nombre, nombre/abreviatura de equipo, posicion, dorsal, país, ...

> Véase searchbar en el manual de uso.

## Sistema de Recomendación

Se ha implementado un sistema de recomendación principalmente basado en búsquedas pasadas.

Para ello, se ha tomado recuento de búsquedas en detalle sobre equipos y jugadores. Una vez recopilados esos datos, se han realizado tres procesos de recomendación diferentes:

### Jugadores por estadística

Se han elaborado medias de estadísticas de los jugadores buscados por el usuario, bonificando los que se han buscado en mas ocasiones.

Se ha calculado la distancia entre los jugadores existentes en la base de datos y la media de búsqueda del usuario y finalmente, se han tomado los 8 con mayor semejanza (según la distancia manhattan).

### Jugadores por etiqueta

Se han etiquetado a los jugadores según sus estadísticas.

Se ha calculado el coeficiente de dice entre el conjunto de etiquetas de búsqueda del usuario y las etiquetas de cada jugador en la base de datos, finalmente, se han tomado los 8 con mayor semejanza.

### Equipos por búsqueda

La recomendacion de equipos está basada en la recomendación de jugadores, se toman los equipos de los jugadores mayormente recomendados y se toman las búsquedas de equipo para introducir equipos buscados frecuentemente.

## Uso

### Instalación

1. clone el repositorio o descargue el código fuente.
2. abra el proyecto y cree un virtual env si lo considera.
3. instale dependencias `cd nbaTracker && pip install -r requirements.txt`
4. asegurese de tener npm (preferiblemente `v6.14.12`) instalado en su ordenador
5. construya el frontend `cd nbaTracker/frontend && npm install && npm run build`
6. inicialice django `cd nbaTracker && python manage.py makemigrations && python manage.py migrate && python manage.py runserver`
7. visite la app en `http://localhost:8000/standings` [click aquí](http://localhost:8000/standings)

### Funcionalidad

Se recomienda iniciar sesión como administrador desde el inicio de las pruebas de la app.

- Puede crear un superusuario mediante `python manage.py createsuperuser`.
- En la base de datos debe existir un usuario admin de pruebas:

```
user: "admin"
password: "admin"
```

#### Navegación

- Se puede hacer uso del menú lateral (standings, search, recoommend y admin)
- Se puede desloguear mediante el botón de logout al final del menu lateral.
- Puede hacerse uso de las herramientas de navegación del navegador web.

#### Dashboard

- /standings
- [click aquí](http://localhost:8000/standings)

1. Pueden verse las estadísticas de los equipos y jugadores.
2. Arriba se visualiza la barra de búsqueda del sistema.
3. Los jugadores mostrados y los equipos en la tabla pueden ser clickados para verlos en detalle.

#### Admin

- http://localhost:8000/admin
- [click aquí](http://localhost:8000/admin)

> Nota: si no está logueado, hagalo como administrador.

Nota: la db se ha subido, estos pasos no son obligatorios pero prueban que el populate y el indexado funcionan y son funcionalidades de administración.

1. Se visualizan 3 acciones
2. Clicke en populate y espere
3. Clicke en index y espere

#### Búsqueda

- /results o /404
- [click aquí](http://localhost:8000/404)

> Nota: los resultados también son clickables y llevaran a la vista detallada del jugador o equipo.

> Nota: tenga en cuenta que la búsqueda esta seteada por defecto a teams, puede cambiarla y es posible que tenga que cambiarla en ciertas ocasiones sin navega a otras paginas y quiere volver a buscar jugadores.

##### teams

1. Verá un 404 y un mensaje que indica que puede buscar.
2. Deje Team seleccionado como tipo de búsqueda en la barra.
3. Busque por ejemplo: GSW, Brooklyn, Timberwolves, Trail ...
4. Busque por ejemplo: Eastern, Western.
5. Busque por ejemplo: Atlantic, Central ...

##### players

1. Mantengase en la página de busquedas
2. Seleccione Player como tipo de búsqueda en la barra.
3. Busque por ejemplo: Curry, James, Lebron ...
4. Busque por ejemplo: 30
5. Busque por ejemplo: C, G, F, ...
6. Busque por ejemplo: STAR, ANOTADOR, ...
7. Busque por ejemplo: Spain, USA, ...
8. Busque por ejemplo: GSW, BKN, Bucks

#### Recomendación

Tras haber realizado busquedas con un usuario logueado, visite la página de recomendación.

- /recommendations
- [click aquí](http://localhost:8000/recommendations)

1. Debe visualizar equipos y jugadores recomendados.
2. Existen, equipos según búsqueda, jugadores según stats y jugadores según etiquetas.
3. Todos son clickables y llevaran a la vista en detalle.

#### Enrutado

Puesto que la app es enrutada, se ha configurado el enrutado para transportar los parámetros de búsqueda.

1. pruebe búsqueda de equipo por url: [click aquí](http://localhost:8000/results/team/Eastern)
2. pruebe búsqueda de jugador por url: [click aquí](http://localhost:8000/results/team/Curry)
3. pruebe vista en detalle por url: [click aquí](http://localhost:8000/results/player/Stephen%20Curry)
