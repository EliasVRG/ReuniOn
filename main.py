from services.google_sheets import GoogleSheetsAPI
from services.reuniOn_manager import ReuniOnManager

API_URL = "https://script.google.com/macros/s/AKfycbxjtYsBAhu5PsH2NjiP-XD-fs0s8kXJyFKpvTbF_uPPrahxfxru-q2FpQq8hWhU83MI/exec"

if __name__ == "__main__":
    sheets_api = GoogleSheetsAPI(API_URL)
    manager = ReuniOnManager(sheets_api)

    manager.load_reuniOns()
    
    print("Reuniões futuras:")
    for meeting in manager.get_upcoming_meetings():
        print(meeting)
