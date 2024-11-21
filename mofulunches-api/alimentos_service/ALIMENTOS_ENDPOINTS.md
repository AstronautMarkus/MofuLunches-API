<div align="center">

# Alimentos/Cartas service

<img src="https://raw.githubusercontent.com/AstronautMarkus/MofuLunches-Web/refs/heads/dev/mofulunches-web/app/static/img/icon.png" alt="MofuLunches-logo" width="80">

</div>


## Aimentos/Cartas service

Multipurpose service, in charge of serving Alimentos, modifying, deleting and creating new ones, Accompanying the brother service of Cartas, in order to create, list, modify and delete these, filling it with Alimentos.


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

### 6. Get all Alimentos

**URL**: `/alimentos`

**Method**: `GET`

**Description**: Get all alimentos list, ids and data.

**Response**:

```json
[
    {
        "id": "1",
        "nombre": "Pure de patatas",
        "tipo": "almuerzo"
    },
    {
        "id": "2",
        "nombre": "Ensalada cesar",
        "tipo": "ensalada"
    },
    {
        "id": "3",
        "nombre": "Coca cola",
        "tipo": "bebestible"
    }
]
```


### 7. Create new alimento

**URL**: `/alimentos`

**Method**: `POST`

**Description**: Create a new alimento.

**Body**:

```json
[
    {
        "id":"",
        "nombre":"",
        "tipo":""
    }
]
```


**Response - Created alimento (200)**:

```json
[
    {
        "message": "Alimento creado exitosamente."
    }
]
```

**Response - id exists (400)**:

```json
[
    {
        "message": "El ID ya existe."
    }
]
```

**Response - Missing fields (400)**:

```json
[
    {
        "message": "Campos faltantes: {campos}"
    }
]
```

### 8. Updates alimento

**URL**: `/alimentos/<id>`

**Method**: `PUT`

**Description**: Updates specific data or all data for an Alimento.

**Body (you can put one or all of the data)**:

```json
[
    {
        "id":"",
        "nombre":"",
        "tipo":""
    }
]
```


**Response - Updated alimento (200)**:

```json
{
    "message": "Alimento actualizado exitosamente."
}
```

**Response - No data provided (400)**:

```json
{
    "message": "Datos no proporcionados."
}
```

**Response - Alimento id not exists (404)**:

```json
{
    "message": "Alimento no encontrado."
}
```

