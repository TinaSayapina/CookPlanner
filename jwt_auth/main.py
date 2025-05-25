from authx import AuthXConfig, AuthX
from datetime import timedelta
config = AuthXConfig()
# время действия токена
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
# создаем ключ
config.JWT_SECRET_KEY = "MY_SECRET_KEY2213312"
# определяем где будет храниться токен
config.JWT_TOKEN_LOCATION = ["cookies"]
# называем название нашего куки-файла
config.JWT_ACCESS_COOKIE_NAME = "my_projects_token"
# объект для генерации токенов
security = AuthX(config=config)