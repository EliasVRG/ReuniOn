from models.reuniOn import ReuniOn
from services.google_sheets import GoogleSheetsAPI

class ReuniOnManager:
    def __init__(self, api: GoogleSheetsAPI):
        self.api = api
        self.reuniOns = []

    def load_reuniOns(self):
        """Carrega reuniões via API do Apps Script"""
        data = self.api.get_reuniOns()
        self.reuniOns = [ReuniOn(row["Data"], row["Hora"], row["Descrição"]) for row in data]

    def get_upcoming_reuniOns(self):
        """Retorna reuniões futuras"""
        return [reuniOns for reuniOns in self.reuniOns if not reuniOns.is_past()]
