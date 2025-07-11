import random

def get_vitals():
    return {
        'heart_rate': random.randint(60, 100),
        'temperature': round(random.uniform(36.5, 37.5), 1),
        'blood_pressure': f"{random.randint(110, 130)}/{random.randint(70, 85)}"
    }

'''def check_passkey(input_passkey, actual_passkey):
    
        """Compares the input passkey to the stored passkey.
    Returns True if it matches, False otherwise."""
    
if input_passkey == actual_passkey:
    print("✅ Passkey correct.")
    #return True
else:
    print("❌ Invalid passkey.")
    #return False '''

def dispense_medication(vitals):
    medications = []

    # Temperature check
    if vitals['temperature'] > 37.2:
        medications.append("Paracetamol")
        medications.append("ORS")
        print("🛑 Detected high temperature (possible fever).")

    # Heart rate check
    if vitals['heart_rate'] > 95:
        medications.append("Beta Blocker (Mild Dose)")
        print("🛑 Elevated heart rate detected.")

    # Blood pressure check
    systolic, diastolic = map(int, vitals['blood_pressure'].split("/"))
    if systolic > 125 or diastolic > 80:
        medications.append("Amlodipine")
        print("🛑 High blood pressure detected.")

    if not medications:
        medications.append("Multivitamin")  # Default for healthy vitals
        print("✅ All vitals are normal.")

    print("💊 Based on your vitals, the following medications are dispensed:")
    for med in medications:
        print(f"- {med}")
    print("✅ Medication dispensing complete.")

    
 
