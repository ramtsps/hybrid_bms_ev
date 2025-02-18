from core.models import EVStation

evStations = [
    {"name": "GreenCharge Anna Nagar", "location": "Anna Nagar, Chennai", "latitude": 13.0827, "longitude": 80.2785, "slots": 5},
    {"name": "EcoVolt OMR Hub", "location": "OMR IT Expressway, Chennai", "latitude": 12.9056, "longitude": 80.0931, "slots": 4},
    {"name": "PowerPlug T. Nagar", "location": "T. Nagar, Chennai", "latitude": 13.0432, "longitude": 80.2333, "slots": 6},
    {"name": "ChargeGrid Gandhipuram", "location": "Gandhipuram, Coimbatore", "latitude": 11.0168, "longitude": 76.9558, "slots": 4},
    {"name": "ElectraCharge Avinashi", "location": "Avinashi Road, Coimbatore", "latitude": 11.0236, "longitude": 76.9736, "slots": 3},
    {"name": "RapidCharge RS Puram", "location": "RS Puram, Coimbatore", "latitude": 11.0046, "longitude": 76.9635, "slots": 6},
    {"name": "VoltBoost Periyar", "location": "Periyar Bus Stand, Madurai", "latitude": 9.9197, "longitude": 78.1194, "slots": 5},
    {"name": "SwiftCharge Mattuthavani", "location": "Mattuthavani, Madurai", "latitude": 9.9391, "longitude": 78.1217, "slots": 4},
    {"name": "EV QuickStop Anna Nagar", "location": "Anna Nagar, Madurai", "latitude": 9.9293, "longitude": 78.1414, "slots": 3},
    {"name": "GridX Trichy Central", "location": "Central Bus Stand, Trichy", "latitude": 10.7905, "longitude": 78.7047, "slots": 6},
    {"name": "EVGo Srirangam", "location": "Srirangam, Trichy", "latitude": 10.8622, "longitude": 78.6923, "slots": 4},
    {"name": "ChargeTech Thillai Nagar", "location": "Thillai Nagar, Trichy", "latitude": 10.8121, "longitude": 78.6984, "slots": 3},
    {"name": "PowerUp Salem Fort", "location": "Fort Area, Salem", "latitude": 11.6647, "longitude": 78.1460, "slots": 5},
    {"name": "VoltZone Hasthampatti", "location": "Hasthampatti, Salem", "latitude": 11.6758, "longitude": 78.1469, "slots": 4},
    {"name": "EVCharge Suramangalam", "location": "Suramangalam, Salem", "latitude": 11.6855, "longitude": 78.1410, "slots": 3},
    {"name": "EcoStation Erode Bus Stand", "location": "Bus Stand, Erode", "latitude": 11.3404, "longitude": 77.7172, "slots": 4},
    {"name": "VoltX Perundurai", "location": "Perundurai Road, Erode", "latitude": 11.3202, "longitude": 77.7255, "slots": 5},
    {"name": "SwiftVolt Thindal", "location": "Thindal, Erode", "latitude": 11.3461, "longitude": 77.7332, "slots": 3},
    {"name": "ChargeZone Palayamkottai", "location": "Palayamkottai, Tirunelveli", "latitude": 8.7139, "longitude": 77.7567, "slots": 4},
    {"name": "HyperCharge Junction", "location": "Tirunelveli Junction", "latitude": 8.7265, "longitude": 77.7047, "slots": 5},
    {"name": "EV Plug Vannarpettai", "location": "Vannarpettai, Tirunelveli", "latitude": 8.7253, "longitude": 77.7508, "slots": 3},
    {"name": "SuperVolt New Bus Stand", "location": "New Bus Stand, Thoothukudi", "latitude": 8.7642, "longitude": 78.1348, "slots": 4},
    {"name": "ChargeBay Bryant Nagar", "location": "Bryant Nagar, Thoothukudi", "latitude": 8.7658, "longitude": 78.1367, "slots": 5},
    {"name": "EVSpot Kovilpatti", "location": "Kovilpatti, Thoothukudi", "latitude": 9.1730, "longitude": 77.8720, "slots": 3},
    {"name": "ElectroGrid Vellore Bus Stand", "location": "Bus Stand, Vellore", "latitude": 12.9165, "longitude": 79.1325, "slots": 4},
    {"name": "ChargeHub Katpadi", "location": "Katpadi, Vellore", "latitude": 12.9489, "longitude": 79.1414, "slots": 5},
    {"name": "Energize Gandhinagar", "location": "Gandhinagar, Vellore", "latitude": 12.9508, "longitude": 79.1542, "slots": 3},
    {"name": "GreenVolt Kanchipuram", "location": "Varadharaja Temple, Kanchipuram", "latitude": 12.8473, "longitude": 79.7036, "slots": 4},
    {"name": "EcoCharge Bus Stand", "location": "Bus Stand, Kanchipuram", "latitude": 12.8372, "longitude": 79.7031, "slots": 5},
    {"name": "HyperPlug Ekambaranathar", "location": "Ekambaranathar Temple, Kanchipuram", "latitude": 12.8479, "longitude": 79.6999, "slots": 3},
    {"name": "QuickCharge Dindigul", "location": "Bus Stand, Dindigul", "latitude": 10.3656, "longitude": 77.9768, "slots": 4},
    {"name": "BoostVolt Palani Road", "location": "Palani Road, Dindigul", "latitude": 10.3627, "longitude": 77.9769, "slots": 5},
    {"name": "EVSnap Nagal Nagar", "location": "Nagal Nagar, Dindigul", "latitude": 10.3697, "longitude": 77.9752, "slots": 3},
    {"name": "EVNext Pudukkottai", "location": "Bus Stand, Pudukkottai", "latitude": 10.3797, "longitude": 78.8206, "slots": 4},
    {"name": "AmpCharge Sivakasi", "location": "Bus Stand, Sivakasi", "latitude": 9.4493, "longitude": 77.7960, "slots": 4},
    {"name": "SmartPlug Kanyakumari", "location": "Beach Road, Kanyakumari", "latitude": 8.0883, "longitude": 77.5410, "slots": 4}
]


for station in evStations:
    EVStation.objects.create(**station)

print("EV Stations added successfully!")
