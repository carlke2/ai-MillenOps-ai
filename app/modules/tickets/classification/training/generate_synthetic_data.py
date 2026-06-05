import pandas as pd
import random
import os

# Categories for tickets
CATEGORIES = {
    "IT/Network": ["wifi is down", "internet is slow", "cannot connect to vpn", "router is blinking red", "dns failure"],
    "IT/Hardware": ["laptop screen broken", "keyboard missing keys", "mouse not working", "printer jammed", "monitor flickering"],
    "Facility/Plumbing": ["leaking tap in kitchen", "toilet is blocked", "water heater not working", "low water pressure", "clogged drain"],
    "Facility/HVAC": ["room is too cold", "ac is making noise", "ventilation not working", "heater smells like burning", "thermostat broken"],
    "Facility/Cleaning": ["spill in hallway", "bin is overflowing", "restroom needs cleaning", "carpet is stained", "window is dirty"]
}

def generate_ticket_data(n=200):
    data = []
    for _ in range(n):
        cat = random.choice(list(CATEGORIES.keys()))
        phrase = random.choice(CATEGORIES[cat])
        
        data.append({
            "title": phrase.capitalize(),
            "description": f"The {phrase} in our department is causing delays.",
            "department": random.choice(["Engineering", "HR", "Sales", "Marketing", "Finance"]),
            "roomName": f"Room {random.randint(101, 505)}",
            "bookingLinked": random.choice([True, False]),
            "finalCategory": cat
        })
    return pd.DataFrame(data)

def main():
    print("Generating synthetic training data...")
    
    # Ticket Classification Data
    df_tickets = generate_ticket_data(300)
    path = "app/modules/tickets/classification/training/datasets/tickets.csv"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df_tickets.to_csv(path, index=False)
    print(f"Created {path} with {len(df_tickets)} samples.")

if __name__ == "__main__":
    main()
