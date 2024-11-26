<div align="center">

# Pedidos service

<img src="https://raw.githubusercontent.com/AstronautMarkus/MofuLunches-Web/refs/heads/dev/mofulunches-web/app/static/img/icon.png" alt="MofuLunches-logo" width="80">

</div>

## Pedidos service

Service in charge of the creation and modifications of **'pedidos'**, created based on letters provided together with the **cartas/alimentos** service.

This service is created with Flask, using [Requirements.txt](https://github.com/AstronautMarkus/MofuLunches-API/blob/dev/mofulunches-api/pedidos_service/requirements.txt) file, also needs a dotenv() file for run.

### dotenv() settings

```
MONGO_URI = "your-mongo-db-uri"
SECRET_KEY = "flask-secret-key"
```

## Pedidos service endpoints


### 1. Get all pedidos

**URL**: `/pedidos`

**Method**: `GET`

**Description**: Get full 'pedidos' list, with 

**Response**:

```json
[
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
    // more pedidos...
]
```

### 2. Get daily pedidos


**URL**: `/pedidos/diarios`

**Method**: `GET`

**Description**: Bring the complete list of 'pedidos', but only for the specific day, using the date of the machine.

**Response**:

(assuming today is 2024-11-22)

```json
[
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
    // more pedidos...
]
```

### 3. Get pedidos by RUT

**URL**: `/pedidos/<rut>`

**Method**: `GET`

**Description**: Bring the complete list of 'pedidos', using User's RUT.

**Response**:

(assuming user's RUT is "123456789")

```json
[
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
        "rut": "123456789"
    }
]
```

### 4. Get daily pedido by RUT

**URL**: `/pedidos/diarios/<rut>`

**Method**: `GET`

**Description**: Bring the complete list of 'pedidos', using User's RUT.

**Response**:

(assuming user's RUT is "123456789" and date is "2024-11-22")

```json
[
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
        "rut": "123456789"
    }
]
```

### 5. Create new pedido

**URL**: `/pedidos`

**Method**: `POST`

**Description**: Create a new pedido in database.

**Body**:

```json
[
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
]
```

**Response - Created pedido (201)**: 

```json
{
  "message": "Pedido creado exitosamente"
}
```

**Response - missing fields (400)**: 

```json
{
  "message": "Faltan campos obligatorios en el pedido: {fields}"
}
```

**Response - alimentos is not an arraylist (400)**: 

```json
{
  "message": "El campo 'alimentos' debe ser una lista de objetos."
}

```

**Response - alimentos list have an invalid object (400)**: 

```json
{
  "message": "Cada alimento debe ser un objeto con los campos 'id', 'nombre' y 'tipo'."
}
```

**Response - 'id', 'nombre' or 'tipo' in alimentos field are not strings (400)**: 

```json
{
  "message": "Los campos 'id', 'nombre' y 'tipo' de cada alimento deben ser cadenas de texto."
}
```

**Response - 'hora_retiro' format is invalid (400)**: 

```json
{
  "message": "El formato de 'hora_retiro' es inválido. Debe ser '%H:%M'."
}
```

**Response - An order with the same RUT already exists for the current date (400)**: 

```json
{
  "message": "El RUT ya tiene un pedido registrado para hoy."
}
```