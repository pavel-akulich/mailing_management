from django.core.cache import cache
from service_client.models import Client


def get_cached_clients():
    """
    Функция для кэширования количества клиентов на главной странице
    """
    # Создаем ключ для кэширования клиентов
    client_cache_key = 'clients_data_cache'
    cached_clients = cache.get(client_cache_key)

    if cached_clients:
        # Если данные есть в кэше, используем их
        return cached_clients
    else:
        # Если данных нет в кэше, выполняем запрос к базе данных
        clients = Client.objects.all()

        # Сохраняем результат запроса в кэше на определенное время(в моем случае 30 сек)
        cache.set(client_cache_key, clients, 30)

        return clients
