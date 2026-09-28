from fastapi import APIRouter,HTTPException
from ..firebase import get_db
from ..schemas import DataCreate,DataUpdate
from ..services.summary import build_summary
router=APIRouter(prefix="/api/data",tags=["data"])
def all_rows():
 return sorted([{"id":d.id,**d.to_dict()} for d in get_db().collection("data").stream()],key=lambda r:r["date"])
@router.post("")
def create_data(p:DataCreate):
 ref=get_db().collection("data").document(); x=p.model_dump(mode="json"); ref.set(x); return {"id":ref.id,**x}
@router.get("")
def list_data():return all_rows()
@router.get("/summary")
def summary():return build_summary(all_rows())
@router.put("/{item_id}")
def update_data(item_id:str,p:DataUpdate):
 ref=get_db().collection("data").document(item_id)
 if not ref.get().exists:raise HTTPException(404,"데이터를 찾을 수 없습니다.")
 patch={k:v for k,v in p.model_dump(mode="json").items() if v is not None}
 if patch:ref.update(patch)
 return {"id":item_id,**ref.get().to_dict()}
@router.delete("/{item_id}")
def delete_data(item_id:str):
 ref=get_db().collection("data").document(item_id)
 if not ref.get().exists:raise HTTPException(404,"데이터를 찾을 수 없습니다.")
 ref.delete(); return {"message":"삭제 완료","id":item_id}
