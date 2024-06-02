from urllib.parse import urljoin

import requests

from app.cache import redis_client
from app.config import settings


class EskizClient:
    host = settings.ESKIZ_HOST
    email = settings.ESKIZ_EMAIL
    password = settings.ESKIZ_PASSWORD
    token_key = settings.ESKIZ_TOKEN_KEY

    def request(self, method: str, uri: str, retry: int = 0, **kwargs):
        token = self.get_token()
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
        response = requests.request(method, urljoin(self.host, uri), headers=headers, **kwargs)
        if response.status_code == 401:
            self.get_token(renew=True)
            if retry < 2:
                self.request(method, uri, retry=retry + 1, **kwargs)
        response.raise_for_status()
        return response.json()

    def get_token(self, renew=False) -> str:
        token = redis_client.get(self.token_key)
        token = token if token else None
        if not token or renew:
            token = self.request_token()
            redis_client.set(self.token_key, token)
        return token

    def request_token(self) -> str:
        payload = {'email': self.email, 'password': self.password}
        response = requests.post(
            urljoin(self.host, 'api/auth/login'), headers={'Content-Type': 'application/json'}, json=payload,
        )
        return response.json()['data']['token']

    def send_sms(self, phone_number: str, message: str):
        payload = {
            'mobile_phone': phone_number,
            'country_code': 'UZ',
            'message': message,
        }
        response = self.request('POST', 'api/message/sms/send', json=payload)
        return response
