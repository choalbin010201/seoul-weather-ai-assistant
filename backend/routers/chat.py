from fastapi import APIRouter,HTTPException
from firebase_admin import firestore
from ..firebase import get_db
from ..schemas import ChatRequest
from ..services.ai import answer_question
router=APIRouter(prefix="/api/chat",tags=["chat"])
@router.post("")
def chat(p:ChatRequest):
 db=get_db(); rows=[{"id":d.id,**d.to_dict()} for d in db.collection("data").stream()]
 if not rows:raise HTTPException(400,"먼저 Firestore에 데이터를 저장하세요.")
 try:ans=answer_question(p.message,rows)
 except Exception as e:raise HTTPException(500,f"AI 호출 실패: {e}")
 ref=db.collection("conversations").document(p.conversation_id) if p.conversation_id else None
 if ref is None or not ref.get().exists: ref=db.collection("conversations").document(); msgs=[]; title=p.message[:40]
 else:
  cur=ref.get().to_dict(); msgs=cur.get("messages",[]); title=cur.get("title",p.message[:40])
 msgs += [{"role":"user","content":p.message},{"role":"assistant","content":ans}]
 ref.set({"title":title,"messages":msgs,"updated_at":firestore.SERVER_TIMESTAMP},merge=True)
 return {"answer":ans,"conversation_id":ref.id}
