from datetime import datetime

class ReuniOn:
    def __init__(self, date: str, time: str, description: str):
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.time = time
        self.description = description

    def __str__(self):
        return f"{self.date.strftime('%d/%m/%Y')} às {self.time} - {self.description}"

    def is_past(self):
        """Verifica se a reunião já passou"""
        return self.date < datetime.today()
