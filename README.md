# MofuLunches-API

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

### Project structure

```
└── 📁MofuLunches-API
    └── 📁mofulunches-api
        └── 📁alimentos_service
            └── app.py
        └── 📁api_gateway
            └── app.py
        └── 📁pedidos_service
            └── app.py
        └── 📁usuarios_service
            └── 📁blueprints
                └── 📁users
                    └── __init__.py
                    └── usuarios_routes.py
                └── __init__.py
            └── 📁utils
                └── __init__.py
                └── db_utils.py
            └── app.py
            └── config.py
            └── requirements.txt
    └── README.md
```


