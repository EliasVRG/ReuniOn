import requests

class GoogleSheetsAPI:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def get_reuniOns(self):
        """Obtém as reuniões do Google Sheets via Apps Script"""
        response = requests.get(self.api_url)
        print("Status Code:", response.status_code)
        print("Resposta da API:", response.text)  # 👀 Ver o que está vindo

        if response.status_code == 200:
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                raise Exception(f"Erro ao decodificar JSON. Resposta da API: {response.text}")
        else:
            raise Exception(f"Erro ao buscar dados: {response.status_code}")

