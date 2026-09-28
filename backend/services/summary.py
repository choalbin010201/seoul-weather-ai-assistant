from statistics import mean,pstdev
def build_summary(rows):
 if not rows:return {"period":None,"count":0,"metrics":{"average":None,"max":None,"min":None,"std":None},"trend":"데이터 없음","latest":None}
 rows=sorted(rows,key=lambda r:r["date"]); vals=[float(r["value"]) for r in rows]
 if len(vals)>=14:
  delta=mean(vals[-7:])-mean(vals[-14:-7]); trend=("유지" if abs(delta)<.5 else "상승" if delta>0 else "하락")+f" (최근 7개 평균 변화 {delta:+.2f}°C)"
 else:
  delta=vals[-1]-vals[0]; trend="상승" if delta>0 else "하락" if delta<0 else "유지"
 mx=max(rows,key=lambda r:float(r["value"])); mn=min(rows,key=lambda r:float(r["value"]))
 return {"period":f'{rows[0]["date"]} ~ {rows[-1]["date"]}',"count":len(rows),"metrics":{"average":round(mean(vals),2),"max":round(float(mx["value"]),2),"max_date":mx["date"],"min":round(float(mn["value"]),2),"min_date":mn["date"],"std":round(pstdev(vals),2) if len(vals)>1 else 0},"trend":trend,"latest":{"date":rows[-1]["date"],"value":round(vals[-1],2)}}
