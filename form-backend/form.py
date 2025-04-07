import gspread
import pywhatkit as kit
import pyautogui
import time

# Load Google Sheets data
gc = gspread.service_account(filename="D:/Web Projects/TechFest/TechFest/form-backend/credentials.json")
sheet = gc.open("TechFest").sheet1 
data = sheet.get_all_records()

# Entry fees and event icons
entry_fees = {
    "BGMI": (200, "🎯"),
    "Tech Quiz": (80, "🧠"),
    "Treasure Hunt": (100, "🗺"),
    "Error Finding": (400, "🐞"),
    "Project Competition": (300, "🏆"),
    "Paper Presentation": (300, "📄"),
    "Poster Presentation": (300, "🖼")      
}

# Iterate through each participant
for row in data:
    name = str(row.get("Full Name", "")).strip()
    phone = f'+91{str(row.get("Phone Number", "")).strip()}'
    event_key = next((key for key in row.keys() if key.strip().lower() == "event"), None)

    if event_key and row[event_key]:
        events_selected = [event.strip() for event in str(row[event_key]).split(",") if event.strip() in entry_fees]
        
        if not events_selected:
            print(f"⚠ No valid events found for {name}. Skipping...")
            continue

        total_fee = sum(entry_fees[event][0] for event in events_selected)
        formatted_events = "\n".join([f"{i+1}. {event} {entry_fees[event][1]}" for i, event in enumerate(events_selected)])

        message = f"""Hey {name},  
Great to see you participating in TechSagar 2025! 🎉  

You have selected the following events:  
{formatted_events}  

Your total entry fee for the above events is ₹{total_fee}.  

Please scan the QR above to complete your payment and share the transaction screenshot here.  

Thank you, and we’re excited to see you at the event! 🚀🎭  
"""

        # Send WhatsApp message with image
        kit.sendwhats_image(phone, "D:/Web Projects/TechFest/TechFest/form-backend/upi.jpg", caption=message)

        # Wait for WhatsApp Web to open
        time.sleep(10)  # Adjust as needed

        # Press "Enter" to send the message automatically
        pyautogui.press("enter")
        time.sleep(5)  # Small delay before sending the next message

print(""
" Messages sent successfully with UPI image!")
