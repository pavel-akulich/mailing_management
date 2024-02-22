from django.core.cache import cache
from service_client.models import Client


def get_cached_clients():
    """
    Function to cache the number of clients on the homepage.

    Returns:
        QuerySet: QuerySet containing Client objects.
    """
    # Create a key for caching clients
    client_cache_key = 'clients_data_cache'
    cached_clients = cache.get(client_cache_key)

    if cached_clients:
        # If data is in cache, use it
        return cached_clients
    else:
        # If data is not in cache, perform a database query
        clients = Client.objects.all()

        # Save the query result in the cache for a certain time (in this case, 30 seconds)
        cache.set(client_cache_key, clients, 30)

        return clients
