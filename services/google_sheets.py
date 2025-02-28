import requests

class GoogleSheetsAPI:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def get_reuniOns(self):
        """Obtém as reuniões do Google Sheets via Apps Script"""
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro ao buscar dados: {response.status_code}")
