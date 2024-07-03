import requests


class HTTPClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint='', params=None, headers=None):
        url = self._build_url(endpoint)
        response = requests.get(url, params=params, headers=headers)
        return self._handle_response(response)

    def post(self, endpoint='', data=None, json=None, headers=None):
        url = self._build_url(endpoint)
        response = requests.post(url, data=data, json=json, headers=headers)
        return self._handle_response(response)

    def put(self, endpoint='', data=None, json=None, headers=None):
        url = self._build_url(endpoint)
        response = requests.put(url, data=data, json=json, headers=headers)
        return self._handle_response(response)

    def delete(self, endpoint='', headers=None):
        url = self._build_url(endpoint)
        response = requests.delete(url, headers=headers)
        return self._handle_response(response)

    def _build_url(self, endpoint):
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def _handle_response(self, response):
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.content


# Пример использования класса
if __name__ == "__main__":
    base_url = 'https://jsonplaceholder.typicode.com'
    client = HTTPClient(base_url)

    # Пример GET-запроса
    content = client.get('/posts/1')
    print(content)

    # Пример POST-запроса
    new_post = {
        'title': 'foo',
        'body': 'bar',
        'userId': 1
    }
    content = client.post('/posts', json=new_post)
    print(content)
