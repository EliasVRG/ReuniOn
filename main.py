from services.google_sheets import GoogleSheetsAPI
from services.reuniOn_manager import ReuniOnManager

API_URL = "https://script.google.com/macros/s/AKfycbxRyrpI1ftxqS-jcYZi3HhEHOTBq157bNH1Juouj_81rR40K9zxH3VDJiRqilT4bSVvnw/exec"

if __name__ == "__main__":
    sheets_api = GoogleSheetsAPI(API_URL)
    manager = ReuniOnManager(sheets_api)

    manager.load_reuniOns()
    
    print("Reuniões futuras:")
    for meeting in manager.get_upcoming_meetings():
        print(meeting)
