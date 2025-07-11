import cv2
import face_recognition
import os
import pickle
import numpy as np
from vitals import get_vitals
#from meds import dispense_medication
from vitals import get_vitals, dispense_medication
DATA_PATH = "user_data.pkl"

def load_user_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "rb") as f:
            return pickle.load(f)
    return {}

def save_user_data(data):
    with open(DATA_PATH, "wb") as f:
        pickle.dump(data, f)

def recognize_face(known_encodings, encoding, tolerance=0.45):
    if not known_encodings:
        return None

    names = list(known_encodings.keys())
    encodings = [v["encoding"] for v in known_encodings.values()]
    #encodings = list(known_encodings.values())

    distances = face_recognition.face_distance(encodings, encoding)
    best_match_index = np.argmin(distances)

    if distances[best_match_index] < tolerance:
        return names[best_match_index]

    return None


def capture_face_embedding():
    video = cv2.VideoCapture(0)
    print("Capturing face. Press 'q' to capture.")
    face_encoding = None

    while True:
        ret, frame = video.read()
        if not ret or frame is None:
            print("❌ Failed to capture frame from webcam.")
            continue

        # Ensure it's 8-bit 3-channel image
        if frame.dtype != 'uint8' or len(frame.shape) != 3 or frame.shape[2] != 3:
            print(f"❌ Invalid image format: shape={frame.shape}, dtype={frame.dtype}")
            continue

        cv2.imshow("Capture", frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            try:
                rgb = np.ascontiguousarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                print("✅ Converted to RGB")
                print("RGB image shape:", rgb.shape)
                print("RGB image dtype:", rgb.dtype)

                boxes = face_recognition.face_locations(rgb)
                if boxes:
                    face_encoding = face_recognition.face_encodings(rgb, boxes)[0]
                    print("✅ Face detected and encoded.")
                    break
                else:
                    print("⚠️ No face detected. Try again.")
            except Exception as e:
                print("❌ Error during processing:", e)

    video.release()
    cv2.destroyAllWindows()
    return face_encoding


def main():
    user_data = load_user_data()
    print("user data: ", user_data)
    print("Initializing Kiosk Face Recognition...")
    encoding = capture_face_embedding()

    user_name = recognize_face(user_data, encoding)
    
    if user_name:
        print(f"✅ User recognized: {user_name}")
            # --- Ask for passkey ---
        stored_passkey = user_data[user_name]["passkey"]
        input_passkey = input("🔑 Enter your passkey: ")

        if input_passkey == stored_passkey:
            print("✅ Passkey correct. Access granted.")
            vitals = get_vitals()
            print("Vitals Report:", vitals)
            dispense_medication(vitals)
        else:
            print("❌ Invalid passkey. Access denied.")
    

    else:
        
        user_name = input("New user detected. Enter your name for registration: ")
        new_passkey = input(f"Create a passkey for {user_name}: ")

        # Save encoding and passkey
        user_data[user_name] = {
            "encoding": encoding,
            "passkey": new_passkey
        }
        save_user_data(user_data)
        print(f"✅ {user_name} registered successfully with passkey.")
        #print(f"Welcome back, {user_name}!")
        
        vitals = get_vitals()
        print("Vitals Report:", vitals)
        dispense_medication(vitals)

#else:
        #user_name = input("New user detected. Enter your name for registration: ")

        #user_data[user_name] = encoding
        #save_user_data(user_data)
        #print(f"{user_name} registered successfully.")

    

if __name__ == "__main__":
    main()