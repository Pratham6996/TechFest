import gspread
import pywhatkit as kit
import time

# Google Sheets API Authentication
gc = gspread.service_account(filename="d:/Web Projects/TechFest/TechFest/form-backend/credentials.json")

# Open Google Sheet
sheet = gc.open("TechFest").sheet1  # Ensure "TechFest" is the correct sheet name

# Fetch Data
data = sheet.get_all_records()

# Entry Fees Dictionary with Emojis
entry_fees = {
    "BGMI": (100, "🎯"),
    "Tech Quiz": (200, "🧠"),
    "AI Pictionary": (300, "🎨"),
    "Treasure Hunt": (400, "🗺️"),
    "Error Finding": (500, "🐞")
}

# Loop Through Each Participant
for row in data:
    name = row.get("Full Name", "").lstrip(":").strip()
    phone = f'+91{row.get("Phone Number", "").lstrip(":").strip()}'

    # Find the correct "Event" column (ignores spaces & case differences)
    event_key = next((key for key in row.keys() if key.strip().lower() == "event"), None)

    if event_key and row[event_key]:
        events_selected = [event.strip() for event in row[event_key].lstrip(":").split(",") if event.strip() in entry_fees]
        
        if not events_selected:
            print(f"⚠️ No valid events found for {name}. Skipping...")
            continue

        total_fee = sum(entry_fees[event][0] for event in events_selected)

        # Format selected events as a numbered list with emojis
        formatted_events = "\n".join([f"{i+1}. {event} {entry_fees[event][1]}" for i, event in enumerate(events_selected)])

        # Message Template
        message = f"""Hey {name},  
Great to see you participating in TechSagar 2025! 🎉  

You have selected the following events:  
{formatted_events}  

Your total entry fee for the above events is ₹{total_fee}.  

Please scan the QR below to complete your payment and share the transaction screenshot here.  

Thank you, and we’re excited to see you at the event! 🚀🎭  
"""

        # Send WhatsApp Message with Image
        kit.sendwhats_image(phone, "d:/Web Projects/TechFest/TechFest/form-backend/upi.jpg", caption=message)

        # Wait to prevent spam detection
        time.sleep(20)

print(" Messages sent successfully with UPI image!")
