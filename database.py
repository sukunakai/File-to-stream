import os
import firebase_admin
from firebase_admin import credentials, firestore

class Database:
    def __init__(self):
        self.db = None

    async def connect(self):
        if not firebase_admin._apps:
            cred_path = "/etc/secrets/serviceAccountKey.json"
            if not os.path.exists(cred_path):
                cred_path = "serviceAccountKey.json"

            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            else:
                print("Firebase secret file nahi mili, temporary memory chalegi.")
                return

        self.db = firestore.client()
        print("✅ Firebase Database connected successfully.")

    async def save_link(self, unique_id: str, message_id: int):
        if self.db:
            doc_ref = self.db.collection("links").document(unique_id)
            doc_ref.set({"message_id": message_id})

    async def get_link(self, unique_id: str):
        if self.db:
            doc = self.db.collection("links").document(unique_id).get()
            if doc.exists:
                return doc.to_dict().get("message_id")
        return None

db = Database()
