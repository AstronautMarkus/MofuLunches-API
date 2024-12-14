<div align="center">

# API Gateway

<img src="https://raw.githubusercontent.com/AstronautMarkus/MofuLunches-Web/refs/heads/dev/mofulunches-web/app/static/img/icon.png" alt="MofuLunches-logo" width="80">

</div>


## API Gateway

This is the centralized API that is responsible for communicating with the three services: Alimentos/Cartas, Usuarios, and Pedidos. This API sends and receives information from the services, and systems that work with MofuLunches should only connect to the API and not directly to the services.



### dotenv() settings

```
MONGO_URI = "your-mongo-db-uri"
```



Before we start, we clarify that if you need to see the precise documentation of each endpoint per service (error codes, statuses, etc.) review them in their respective Markdown, here below you can find them:

<div align="center">

[![Usuarios](https://img.shields.io/badge/Mofulunches-Usuarios-blue?style=for-the-badge&logo=github)](https://github.com/AstronautMarkus/MofuLunches-API/blob/dev/mofulunches-api/usuarios_service/USUARIOS_ENDPOINTS.md)
[![Pedidos](https://img.shields.io/badge/Structure-Pedidos-green?style=for-the-badge&logo=github)](https://github.com/AstronautMarkus/MofuLunches-API/blob/dev/mofulunches-api/pedidos_service/PEDIDOS_ENDPOINTS.md)
[![Alimentos/Cartas](https://img.shields.io/badge/Mofulunches-Alimentos%20&%20Cartas-orange?style=for-the-badge&logo=github)](https://github.com/AstronautMarkus/MofuLunches-API/blob/dev/mofulunches-api/alimentos_service/ALIMENTOS_ENDPOINTS.md)

</div>

---

## Endpoints - Usuarios


### 1. Get all users

**URL**: `/api/usuarios`

**Method**: `GET`

**Description**: Get all users list, names, last names, email, "RUTs", roles and RFID codes.

**Response**:

```json

    {
        "apellido": "Markihnos",
        "codigo_RFID": "111111111",
        "correo": "astronautmarkus@gmail.com",
        "nombre": "Astronauta",
        "rut": "111111111",
        "tipo_usuario": "admin"
    },
    {
        "apellido": "Jackson",
        "codigo_RFID": "222222222",
        "correo": "sevenjackson@gmail.com",
        "nombre": "Seven",
        "rut": "222222222",
        "tipo_usuario": "cocineros"
    }

```


### 2. Get users by rut

**URL**: `/api/usuarios/<rut>`

**Method**: `GET`

**Description**: Get specific user using RUT.

**Response**:

```json

    {
        "apellido": "Markihnos",
        "codigo_RFID": "111111111",
        "correo": "astronautmarkus@gmail.com",
        "nombre": "Astronauta",
        "rut": "111111111",
        "tipo_usuario": "admin"
    }

```

### 3. Create new user

**URL**: `/api/usuarios`

**Method**: `POST`

**Description**: Create a new user, using name, last name, email, "RUT", role, RFID code and password. 

**Body**:

```json

    {
        "apellido": "Hakurei",
        "codigo_RFID": "123456789",
        "correo": "reimugaming@gmail.com",
        "contrasena":"ReimuGamingAdmin.",
        "nombre": "Reimu",
        "rut": "123456789",
        "tipo_usuario": "admin"
    }

```

**Response**:

```json

    {
    "message": "Usuario creado exitosamente."
    }

```

### 4. Update user fully

**URL**: `/api/usuarios/<rut>`

**Method**: `PUT`

**Description**: Updates full data of a user, name, rut, RFID code, etc. Without password field.

**Body**:

```json

    {
        "apellido": "Hakurei",
        "codigo_RFID": "123456789",
        "correo": "reimugaming@gmail.com",
        "nombre": "Reimu",
        "rut": "123456789",
        "tipo_usuario": "admin"
    }

```

**Response - Updated (200)**:

```json

    {
    "message": "Usuario actualizado exitosamente."
    }

```

### 5. Update user partially

**URL**: `/api/usuarios/<rut>`

**Method**: `PATCH`

**Description**: Updates partially data of a user with its RUT.

**Body**:

```json

    {
        "apellido": "Hakurei",
        "codigo_RFID": "123456789",
        "correo": "reimugaming@gmail.com",
        "nombre": "Reimu",
        "rut": "123456789",
        "tipo_usuario": "admin"
    }

```

You can put one or more characters as you prefer.

**Response**:

```json

    {
    "message": "Usuario actualizado exitosamente."
    }

```

# 6. Login user

**URL**: `/api/usuarios`

**Method**: `POST`

**Description**: Log user, using RUT and 'contrasena'

**Body**:

```json
{
    "rut": "123456789",
    "contrasena": "yourpassword"
}
```

**Response - Updated (200)**:

```json
{
    "message": "Login exitoso.",
    "user": {
        "rut": "123456789",
        "nombre": "Juan",
        "apellido": "Perez",
        "correo": "juan.perez@example.com",
        "tipo_usuario": "admin"
    }
}
```

### 7. Delete user

**URL**: `/api/usuarios/<rut>`

**Method**: `DELETE`

**Description**: Deletes a user by its RUT.

**Response - Deleted (200)**:

```json
{
    "message": "Usuario eliminado exitosamente."
}
```

**Response - User not found (404)**:

```json
{
    "error": "Usuario no encontrado."
}
```

---


## Endpoints - Alimentos/Cartas


### 1. Gell all alimentos

**URL**: `/api/alimentos`

**Method**: `GET`

**Description**: Get full alimentos list.

**Response**:

```json

    {
        "alimentos": [
            {
                "id": "101",
                "nombre": "Pizza de pepperoni"
            },
            {
                "id": "102",
                "nombre": "Ensalada César"
            },
            {
                "id": "105",
                "nombre": "Coca cola"
            }
        ],
        "calificaciones": {
            "promedio": 4.6,
            "total_calificaciones": 5
        },
        "fecha": "2024-11-20",
        "id": "1"
    }

```

### 2. Create alimento

**URL**: `/api/alimentos`

**Method**: `POST`

**Description**: Get full alimentos list.

**Body**:

```json

    {
        "nombre":"",
        "tipo":""
    }

```


**Response - Created alimento (200)**:

```json

    {
        "message": "Alimento creado exitosamente."
    }

```

### 3. Update alimento by id

**URL**: `/api/alimentos/<id>`

**Method**: `PUT`

**Description**: Get full alimentos list.

**Body**:

```json

    {
        "nombre":"",
        "tipo":""
    }

```


**Response - Created alimento (200)**:

```json

    {
        "message": "Alimento actualizado exitosamente."
    }

```


### 4. Get all cartas

**URL**: `/api/cartas`

**Method**: `GET`

**Description**: Get all cartas list.

**Response**:

> Note:
For this endpoint, you can filter by date using query params, in this case using desde=YYYY-MM-DD and hasta=YYYY-MM-DD.

```json

    {
        "alimentos": [
            {
                "id": "101",
                "nombre": "Pizza de pepperoni"
            },
            {
                "id": "102",
                "nombre": "Ensalada César"
            },
            {
                "id": "105",
                "nombre": "Coca cola"
            }
        ],
        "calificaciones": {
            "promedio": 4.6,
            "total_calificaciones": 5
        },
        "fecha": "2024-11-20",
        "id": "1"
    }

```


### 5. Get carta by id 

**URL**: `/api/cartas/<id>`

**Method**: `GET`

**Description**: Get specific carta using ID.

**Response**:

```json

    {
        "alimentos": [
            {
                "id": "101",
                "nombre": "Pizza de pepperoni"
            },
            {
                "id": "102",
                "nombre": "Ensalada César"
            },
            {
                "id": "105",
                "nombre": "Coca cola"
            }
        ],
        "calificaciones": {
            "promedio": 4.6,
            "total_calificaciones": 5
        },
        "fecha": "2024-11-20",
        "id": "1"
    }

```

### 6. Create carta

**URL**: `/api/cartas`

**Method**: `POST`

**Description**: Create a carta using Body.

**Body**:

```json
{
    "fecha": "2024-11-21",
    "alimentos":[
        {
            "id": "101",
            "tipo":"almuerzo",
            "nombre": "Pizza de pepperoni"
        },
        {
            "id": "102",
            "tipo":"ensalada",
            "nombre": "Ensalada César"
        },
        {
            "id": "105",
            "tipo":"refresco",
            "nombre": "Coca cola"
        }
    ]
}
```

**Response**:

```json
{
    "message": "Carta creada exitosamente."
}
```

### 7. Modify carta by id 

**URL**: `/api/cartas/<id>/alimentos`

**Method**: `PUT`

**Description**: Modify part of a carta.

**Body**:

```json
  {
    "operation": "{operation}", // add or delete
    "alimento": {
      "id": "{alimento_id}",
      "nombre": "{alimento_nombre}"
    }
  }
```

**Response**:

```json
{
  "message": "Alimento agregado exitosamente."
}
```


### 8. Rate carta by id

**URL**: `/api/cartas/<id>/calificar`

**Method**: `POST`

**Description**: Rate a carta using starts system, from 0 to 5.

**Body**:

```json
{
    "calificacion":5
}
``

**Response**:

```json
{
    "message": "Calificación registrada."
}
```

---

## Endpoints - Pedidos

### 1. Get all pedidos

**URL**: `/api/pedidos`

**Method**: `GET`

**Description**: Get all pedidos list. You can filter by date using query params `desde` and `hasta`.

**Query Parameters**:
- `desde` (optional): Start date in YYYY-MM-DD format.
- `hasta` (optional): End date in YYYY-MM-DD format.

**Response**:

```json

    {
        "apellido": "Markihnos",
        "codigo_RFID": "111111111",
        "correo": "astronautmarkus@gmail.com",
        "nombre": "Astronauta",
        "rut": "111111111",
        "tipo_usuario": "admin"
    }

```

### 2. Get daily pedidos

**URL**: `/api/pedidos/diarios`

**Method**: `GET`

**Description**: Get only daily pedidos.

**Response**:

```json

    {
        "_id": "67422eff0ea32bd70cacd2a6",
        "alimento": [
            {
                "id": "101",
                "nombre": "Pizza de pepperoni"
            },
            {
                "id": "102",
                "nombre": "Ensalada César"
            }
        ],
        "cod_diario": "001",
        "cod_unico": "00001",
        "estado": "Listo para recoger",
        "fecha_pedido": "2024-11-22", 
        "hora_retiro": "13:00",
        "rut": "12345678-9"
    }

```

### 3. Get daily pedidos

**URL**: `/api/pedidos/diarios`

**Method**: `GET`

**Description**: Get only daily pedidos.

> Note:
Let's assume today is 2024-11-22.

**Response**:

```json

    {
        "_id": "67422eff0ea32bd70cacd2a6",
        "alimento": [
            {
                "id": "101",
                "nombre": "Pizza de pepperoni"
            },
            {
                "id": "102",
                "nombre": "Ensalada César"
            }
        ],
        "cod_diario": "001",
        "cod_unico": "00001",
        "estado": "Listo para recoger",
        "fecha_pedido": "2024-11-22", 
        "hora_retiro": "13:00",
        "rut": "12345678-9"
    }

```

### 4. Get pedidos by RUT

**URL**: `/api/pedidos/<rut>`

**Method**: `GET`

**Description**: Get all pedidos from an user, using its RUT.


**Response**:

```json

    {
        "_id": "67422eff0ea32bd70cacd2a6",
        "alimento": [
            {
                "id": "101",
                "nombre": "Pizza de pepperoni"
            },
            {
                "id": "102",
                "nombre": "Ensalada César"
            }
        ],
        "cod_diario": "001",
        "cod_unico": "00001",
        "estado": "Listo para recoger",
        "fecha_pedido": "2024-11-22", 
        "hora_retiro": "13:00",
        "rut": "12345678-9"
    },
    {
        "_id": "67422eff0ea32bd70cacd2a7",
        "alimento": [
            {
                "id": "103",
                "nombre": "Hamburguesa"
            },
            {
                "id": "104",
                "nombre": "Papas fritas"
            }
        ],
        "cod_diario": "002",
        "cod_unico": "00002",
        "estado": "En preparación",
        "fecha_pedido": "2024-11-23", 
        "hora_retiro": "12:30",
        "rut": "12345678-9"
    },
    {
        "_id": "67422eff0ea32bd70cacd2a8",
        "alimento": [
            {
                "id": "105",
                "nombre": "Sushi"
            },
            {
                "id": "106",
                "nombre": "Té verde"
            }
        ],
        "cod_diario": "003",
        "cod_unico": "00003",
        "estado": "Entregado",
        "fecha_pedido": "2024-11-24", 
        "hora_retiro": "14:00",
        "rut": "12345678-9"
    }

```

### 5. Get daily pedido by RUT

**URL**: `/api/pedidos/diarios/<rut>`

**Method**: `GET`

**Description**: Get daily pedido from an user, using its RUT.

> Note:
Let's assume today is 2024-11-22 and user RUT is 12345678-9.


**Response**:

```json

    {
        "_id": "67422eff0ea32bd70cacd2a6",
        "alimento": [
            {
                "id": "101",
                "nombre": "Pizza de pepperoni"
            },
            {
                "id": "102",
                "nombre": "Ensalada César"
            }
        ],
        "cod_diario": "001",
        "cod_unico": "00001",
        "estado": "Listo para recoger",
        "fecha_pedido": "2024-11-22", 
        "hora_retiro": "13:00",
        "rut": "12345678-9"
    }

```

### 6. Create pedido

**URL**: `/api/pedidos`

**Method**: `POST`

**Description**: Create a new pedido, using a Body

**Body**:
```json

    {
        "rut":"",
        "alimentos":[
            {
                "id":"",
                "nombre":""
            }
        ]
        "hora_retiro":""
    }

```

**Response**:

```json
{
  "message": "Pedido creado exitosamente"
}
```

### 7. Update pedido status using cod_unico

**URL**: `/api/pedidos/<cod_unico>`

**Method**: `PUT`

**Description**: Updates pedido status, using the cod_unico.

**Body**:
```json

{
  "hora_retiro": "14:50",
  "estado": "listo_para_retiro"
}


```

**Response**:

```json
{
  "message": "Pedido actualizado exitosamente",
  "pedido": {
    "cod_unico": "12345",
    "hora_retiro": "15:30",
    "estado": "listo_para_retiro",
    "hora_modificacion": "14:50"
  }
}
```



