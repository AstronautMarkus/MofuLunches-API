<div align="center">

# MofuLunches-API 

<img src="https://raw.githubusercontent.com/AstronautMarkus/MofuLunches-Web/refs/heads/dev/mofulunches-web/app/static/img/icon.png" alt="MofuLunches-logo" width="120">

</div>

MofuLunches-API is the backend system for the [MofuLunches platform](https://github.com/topics/mofulunches), a student project designed to manage and serve core API services for the totem, mobile app, and admin web portal. This repository follows a Service-Oriented Architecture (SOA) and includes various independent services such as user management, order processing, and menu management, all coordinated through an API Gateway.

## Features:

- Centralized API Gateway to route and manage requests
- Independent user, order, and menu services for modular functionality
- Built with Flask, utilizing RESTful principles for service interactions
- Structured for scalability and future integration with other modules

## Intended Use:

MofuLunches-API is part of the MofuLunches ecosystem, designed to support backend operations for the platform's applications. It is suitable for deployment in both cloud and local environments, providing a seamless, distributed backend architecture for the MofuLunches experience.

> Note:
This project is a learning initiative, and while it is student-developed, the code is open for use if it aligns with any positive objectives you may have. Contributions and feedback are welcome to help improve its functionality and reach.

## Repository paths

Search for documentation of specific services:

<div align="center">

[![Usuarios](https://img.shields.io/badge/Mofulunches-Usuarios-blue?style=for-the-badge&logo=github)](#usuarios)
[![Cartas](https://img.shields.io/badge/Structure-Cartas-green?style=for-the-badge&logo=github)](#cartas)
[![Alimentos](https://img.shields.io/badge/Mofulunches-Alimentos-orange?style=for-the-badge&logo=github)](#alimentos)



</div>

---


## Usuarios service

Main service, in charge of creating users, modifying attributes, assigning roles, also in charge of the **/login** system, allowing the functionality of the rest of the services.

This service is created with Flask, using [Requirements.txt](https://github.com/AstronautMarkus/MofuLunches-API/blob/dev/mofulunches-api/usuarios_service/requirements.txt) file, also needs a dotenv() file for run.

### dotenv() settings

```
MONGO_URI = "your-mongo-db-uri"
SECRET_KEY = "flask-secret-key"
JWT_SECRET_KEY = "jwt-secret-key"
JWT_ACCESS_TOKEN_EXPIRES = 3600 // (default 1h)
```

## Usuarios service endpoints

### 1. Get users list

**URL**: `/usuarios`

**Method**: `GET`

**Description**: Get all users list, names, last names, email, "RUTs",  roles and RFID codes.

**Response**:

```json
[
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
        "tipo_usuario": "cocinero"
    }
]
```

### 2. Get user by rut

**URL**: `/usuarios/<rut>`

**Method**: `GET`

**Description**: Get an user data by its rut.

**Response**:

```json
[
    {
        "apellido": "Markihnos",
        "codigo_RFID": "111111111",
        "correo": "astronautmarkus@gmail.com",
        "nombre": "Astronauta",
        "rut": "111111111",
        "tipo_usuario": "admin"
    }
]
```

**Response - User not found (404)**:

```json
[
    {
    "error": "Usuario no encontrado."
    }
]
```


### 3. Create new user

**URL**: `/usuarios`

**Method**: `POST`

**Description**: Create a new user, using name, last name, email, "RUT", role, RFID code and password. 

**Body**:

```json
[
    {
        "apellido": "Hakurei",
        "codigo_RFID": "123456789",
        "correo": "reimugaming@gmail.com",
        "contrasena":"ReimuGamingAdmin.",
        "nombre": "Reimu",
        "rut": "123456789",
        "tipo_usuario": "admin"
    }
]
```

**Response - Created (201)**:

```json
[
    {
    "message": "Usuario creado exitosamente."
    }
]
```

**Response - Missing fields (400)**:

```json
{
    "error": "Campos faltantes: {fields}"
}
```

**Response - RUT already exists (400)**:

```json
{
    "error": "El RUT ya existe."
}
```

### 4. Update user full

**URL**: `/usuarios/<rut>`

**Method**: `PUT`

**Description**: Updates full data of a user, name, rut, RFID code, etc. Without password field.

**Body**:

```json
[
    {
        "apellido": "Hakurei",
        "codigo_RFID": "123456789",
        "correo": "reimugaming@gmail.com",
        "nombre": "Reimu",
        "rut": "123456789",
        "tipo_usuario": "admin"
    }
]
```

**Response - Updated (200)**:

```json
[
    {
    "message": "Usuario actualizado exitosamente."
    }
]
```

**Response - User not found (404)**:

```json
[
    {
    "error": "Usuario no encontrado."
    }
]
```

**Response - Missing fields (400)**:

```json
[
{
    "error": "Faltan campos obligatorios.",
    "missing_fields": [
        "{fields}"
    ]
}
]
```

### 5. update user partially

**URL**: `/usuarios/<rut>`

**Method**: `PATCH`

**Description**: Updates partially data of a user with its RUT.

**Body**:

```json
[
    {
        "apellido": "Hakurei",
        "codigo_RFID": "123456789",
        "correo": "reimugaming@gmail.com",
        "nombre": "Reimu",
        "rut": "123456789",
        "tipo_usuario": "admin"
    }
]
```

You can put one or more characters as you prefer.

**Response - Updated (200)**:

```json
[
    {
    "message": "Usuario actualizado exitosamente."
    }
]
```

**Response - User not found (404)**:

```json
[
    {
    "error": "Usuario no encontrado."
    }
]
```


### 6. Login User

**URL**: `/login`

**Method**: `POST`

**Description**: Authenticates a user using their RUT and password.

**Body**:

```json
{
    "rut": "123456789",
    "contrasena": "yourpassword"
}
```

**Responses**:

- **Success (200)**:

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
Headers:
- `Authorization: Bearer <access_token>`
- `Refresh-Token: <refresh_token>`

- **Validation Error (400)**:

```json
{
    "error": "RUT y contraseña son requeridos."
}
```

- **User Not Found (404)**:

```json
{
    "error": "Usuario no encontrado."
}
```

- **Incorrect Password (401)**:

```json
{
    "error": "Contraseña incorrecta."
}
```


---


## Cartas service

Service in charge of serving the menus, fed by the Alimentos service, in charge of creating, modifying, deleting, adding/removing food to the menus. Cartas service is located in the /alimentos-service folder next to Alimentos service.

This service is created with Flask, using [Requirements.txt](https://github.com/AstronautMarkus/MofuLunches-API/blob/dev/mofulunches-api/alimentos_service/requirements.txt) file, also needs a dotenv() file for run.

### dotenv() settings

```
MONGO_URI = "your-mongo-db-uri"
SECRET_KEY = "flask-secret-key"
```

## Cartas service endpoints

### 1. Get all Cartas

**URL**: `/cartas`

**Method**: `GET`

**Description**: Get all cartas list, rates and food content.

**Response**:

```json
[
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
]
```


### 2. Get all Cartas by id

**URL**: `/cartas/<id>`

**Method**: `GET`

**Description**: Get a carta by ID, full content.

**Response**:

```json
[
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
]
```


**Response - No cartas in ID (404)**:

```json
[
    {
        "message": "Carta no encontrada."
    }
]
```

### 3. Create new carta

**URL**: `/cartas`

**Method**: `POST`

**Description**: Create a carta.

**Body**

```json
{
    "id": "1",
    "fecha": "2024-11-21",
    "alimentos":[
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
    ]
}
```

**Response - Created carta (200)**:

```json
{
    "message": "Carta creada exitosamente."
}
```


**Response - ID already exists (409)**:

```json
{
    "message": "Ya existe una carta con este ID."
}
```

**Response - Alimentos field are not arraylist (400)**:

```json
{
    "message": "El campo 'alimentos' debe ser una lista con 'id' y 'nombre' en cada elemento."
}
```

**Response - Missing fields (400)**:

```json
{
    "message": "Campos faltantes: {fields}"
}
```

**Response - Other error (500)**:

```json
{
    "message": "Error al crear la carta: {errors}"
}
```

### 4. Create new carta

**URL**: `/cartas/<id>/calificar`

**Method**: `POST`

**Description**: Rate a carta, from 0 to 5.

**Body**

```json
{
    "calificacion":5
}
```

**Response - Created carta (200)**:

```json
{
    "message": "Calificación registrada."
}
```

**Response - If calificacion is more than 5 or less than 0 (400)**:

```json
{
    "message": "La calificación debe ser un número entre 1 y 5."
}
```

**Response - Carta not exists (404)**:

```json
{
    "message": "Carta no encontrada."
}
```

### 5. Modify carta

**URL**: `/cartas/<string:id>/alimentos`

**Method**: `PUT`

**Description**: Modify the list of alimentos in a carta by adding or deleting an item.

**Body**

```json
  {
    "operation": "{operation}", // add or delete
    "alimento": {
      "id": "{alimento_id}",
      "nombre": "{alimento_nombre}"
    }
  }
```

**Response - Alimento added (200)**:

```json
{
  "message": "Alimento agregado exitosamente."
}
```

**Response - Alimento deleted (200)**:

```json
{
  "message": "Alimento eliminado exitosamente."
}
```

**Response - Operation is invalid (400)**:

```json
{
  "message": "Operación inválida. Usa 'add' o 'delete'."
}
```

**Response - Missing fields (400)**:

```json
{
  "message": "Datos del alimento inválidos o faltantes ('id' y 'nombre' son obligatorios)."
}
```

**Response - Carta not found (404)**:

```json
{
  "message": "Carta no encontrada."
}
```

**Response - Alimento not exists in carta (404)**:

```json
{
  "message": "El alimento no existe en la carta."
}
```
**Response - If trying to add an alimento that already exists in the carta (409)**:

```json
{
  "message": "El alimento ya existe en la carta."
}
```
**Response - Other errors (500)**:

```json
{
  "message": "Error al modificar los alimentos: <error_message>."
}

```

