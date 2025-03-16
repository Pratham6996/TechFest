import gspread
import pywhatkit as kit
import time

# Google Sheets API Authentication
gc = gspread.service_account(filename="d:/Web Projects/TechFest/TechFest/form-backend/credentials.json")

# Open Google Sheet
sheet = gc.open("TechFest").sheet1

# Fetch Data
data = sheet.get_all_records()

# Entry Fees Dictionary
entry_fees = {
    "BGMI": 100,
    "Tech Quiz": 200,
    "AI Pictionary": 300,
    "Treasure Hunt": 400,
    "Error Finding": 500
}

# Loop Through Each Participant
for row in data:
    name = row.get("Full Name", "").lstrip(":").strip()
    phone = f'+91{row.get("Phone Number", "").lstrip(":").strip()}'

    # Find the correct "Event" column (ignores spaces)
    event_key = next((key for key in row.keys() if key.strip().lower() == "event"), None)

    if event_key and row[event_key]:
        events_selected = [event.strip() for event in row[event_key].lstrip(":").split(",")]
        total_fee = sum(entry_fees.get(event, 0) for event in events_selected)

        # Message Template
        message = f"Hi {name},\nYou have selected {', '.join(events_selected)} games.\nYour total amount to pay is ₹{total_fee}. Please scan the UPI below to complete your payment."

        # Send Message + Image Together
        kit.sendwhats_image(phone, "d:/Web Projects/TechFest/TechFest/form-backend/upi.jpg", caption=message)

        time.sleep(20)  # Prevents spam & ensures WhatsApp Web loads properly

print("✅ Messages sent successfully with UPI image!")
