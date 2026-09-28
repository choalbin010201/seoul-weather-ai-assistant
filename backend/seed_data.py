import csv
from pathlib import Path
from backend.firebase import get_db
CSV=Path(__file__).resolve().parents[1]/"data"/"seoul_weather_data.csv"
def main():
 db=get_db(); rows=list(csv.DictReader(CSV.open(encoding="utf-8-sig"))); batch=db.batch(); n=0
 for r in rows:
  ref=db.collection("data").document(r["date"]);batch.set(ref,{"date":r["date"],"value":float(r["value"]),"memo":r["memo"]});n+=1
  if n%400==0:batch.commit();batch=db.batch()
 if n%400:batch.commit()
 print(f"{n}개 데이터를 Firestore에 저장했습니다.")
if __name__=="__main__":main()
