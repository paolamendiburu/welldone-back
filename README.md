# Welldonde-back
Welldone API


## Start server:
```
python manage.py runserver
```

## Mail Local Server:
```
python -m smtpd -n -c DebuggingServer localhost:1025
```

## API:

### Token:
Loguearse para obtener token (post)
```
http://127.0.0.1:8000/api/v1/login
```

### Usuarios:
Listado de usuarios
```
http://127.0.0.1:8000/api/v1/users
```

Búsqueda
```
http://127.0.0.1:8000/api/v1/users?search=palabra
http://127.0.0.1:8000/api/v1/users?username=palabra
http://127.0.0.1:8000/api/v1/users?email=palabra

output:
    username
    first_name
    last_name
    email
    articles (listado de articulos)
```

Búsqueda por usuario
```
http://127.0.0.1:8000/api/v1/users/username (solo el propio usuario puede ver sus datos completos)
```

Listado de articulos (solo articulos ya publicados)

```
http://127.0.0.1:8000/api/v1/articles/

output:
    -articleid
    -title
    -introduction
    -owner
    -first_name
    -last_name
    -category
    -publish_Date
    -slug
    -full_text
    -small_image
    -large_image
    -media

```

Articulo especifico

```
http://127.0.0.1:8000/api/v1/articles/slug del articulo
```

Listado de mis articulos(para usuario registrado)

```
http://127.0.0.1:8000/api/v1/my-articles/
```

Detalle de mis articulos(para usuario registrado)

```
http://127.0.0.1:8000/api/v1/my-articles/slug del articulo
```

Listado de comentarios

```
http://127.0.0.1:8000/api/v1/comments/

output:
    -id
    -text
    -article
    -owner
```

Comentario especifico

```
http://127.0.0.1:8000/api/v1/comments/id del comentario
```

Listado de follows

```
http://127.0.0.1:8000/api/v1/follows/

output:
    - id
    -owner
    -user_followed
```

Follow especifico

```
http://127.0.0.1:8000/api/v1/follows/id del follow

```


Listado de favoritos

```
http://127.0.0.1:8000/api/v1/favorites/

output:
    - id
    -owner
    -favorite_article
```

Favorito especifico

```
http://127.0.0.1:8000/api/v1/favorites/id del favorite

```
