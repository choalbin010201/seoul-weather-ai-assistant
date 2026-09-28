from fastapi import APIRouter,HTTPException
from firebase_admin import firestore
from ..firebase import get_db
from ..schemas import ConversationCreate
router=APIRouter(prefix="/api/conversations",tags=["conversations"])
@router.post("")
def create_conversation(p:ConversationCreate):
 ref=get_db().collection("conversations").document(); x=p.model_dump(); ref.set({**x,"created_at":firestore.SERVER_TIMESTAMP,"updated_at":firestore.SERVER_TIMESTAMP}); return {"id":ref.id,**x}
@router.get("")
def list_conversations():
 return [{"id":d.id,"title":d.to_dict().get("title","새 대화"),"messages":d.to_dict().get("messages",[])} for d in get_db().collection("conversations").stream()]
@router.get("/{cid}")
def get_conversation(cid:str):
 d=get_db().collection("conversations").document(cid).get()
 if not d.exists:raise HTTPException(404,"대화를 찾을 수 없습니다.")
 return {"id":d.id,**d.to_dict()}
@router.delete("/{cid}")
def delete_conversation(cid:str):
 ref=get_db().collection("conversations").document(cid)
 if not ref.get().exists:raise HTTPException(404,"대화를 찾을 수 없습니다.")
 ref.delete();return {"message":"대화 삭제 완료","id":cid}
