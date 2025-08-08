для развертывания выполните команды: 
1. git clone https://github.com/Code408/Secunda_app.git
2. docker compose up --build

Доступны два интерфейса:
- HTML интерфейс для пользователей (web/organizations/)
- JSON ответы (organizations/)

оба доступны через префикс /api/v1

ссылки для тестирования:
- http://127.0.0.1:8000/api/v1/docs
- http://127.0.0.1:8000/api/v1/redoc
- http://127.0.0.1:8000/api/v1/organizations/nearby/?lat=55.77&lon=37.6176&radius=1
- http://127.0.0.1:8000/api/v1/organizations/?activity_id=3&radius=1
- http://127.0.0.1:8000/api/v1/organizations/?building_id=1
- http://127.0.0.1:8000/api/v1/organizations/?name=%D0%94%D0%B5%D1%80%D0%B5%D0%B2
- http://127.0.0.1:8000/api/v1/web/organizations/1
- http://127.0.0.1:8000/api/v1/web/organizations/?name=%D0%94%D0%B5%D1%80%D0%B5%D0%B2%D0%B5%D0%BD%D1%8C%D0%BA%D0%B0
