import json, firebase_admin
from firebase_admin import credentials, firestore
from .config import FIREBASE_SERVICE_ACCOUNT_JSON
_db=None
def get_db():
 global _db
 if _db is not None:return _db
 if not firebase_admin._apps:
  if not FIREBASE_SERVICE_ACCOUNT_JSON: raise RuntimeError("FIREBASE_SERVICE_ACCOUNT_JSON 환경변수가 비어 있습니다.")
  firebase_admin.initialize_app(credentials.Certificate(json.loads(FIREBASE_SERVICE_ACCOUNT_JSON)))
 _db=firestore.client(); return _db
