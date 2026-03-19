search_cache = {}


def set_cache(user_id, data):
    search_cache[user_id] = data


def get_cache(user_id):
    return search_cache.get(user_id)
