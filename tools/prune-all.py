# Apply tools/exclude.json to ia.json, lv.json, mg.json, books.json (keeps the library Reformed).
import json,re,sys
ex=json.load(open('tools/exclude.json'));DA=re.compile(ex['deny_au'],re.I);DT=re.compile(ex['deny_ti'],re.I)
AL=set(ex['allow_ia']);ALR=re.compile(ex['allow_ia_re'],re.I)
def compact(d,strict_idx=0):
    used=sorted({r[0] for r in d['b']});m={o:i for i,o in enumerate(used)}
    d['a']=[d['a'][o] for o in used]
    for r in d['b']:r[0]=m[r[0]]
    return d
def run(f,ia=False):
    d=json.load(open(f));n0=len(d['b']);A=d['a']
    keep=[]
    for r in d['b']:
        nm=A[r[0]]
        if isinstance(nm,list):nm=nm[0]
        if DA.search(nm) or DT.search(r[1]):continue
        if ia and not (nm in AL or ALR.search(nm)):continue
        keep.append(r)
    d['b']=keep
    if isinstance(A[0],str):d=compact(d)
    json.dump(d,open(f,'w'),ensure_ascii=False,separators=(',',':'))
    print(f,n0,'->',len(keep))
run('ia.json',True);run('lv.json',True)
m=json.load(open('mg.json'));n0=len(m['b'])
bad={i for i,a in enumerate(m['a']) if DA.search(a[0])};m['b']=[r for r in m['b'] if r[0] not in bad]
json.dump(m,open('mg.json','w'),ensure_ascii=False,separators=(',',':'));print('mg',n0,'->',len(m['b']),[m['a'][i][0] for i in bad])
b=json.load(open('books.json'));n=len(b['extra']);b['extra']=[e for e in b['extra'] if e.get('id') not in ex['deny_extra_ids']]
json.dump(b,open('books.json','w'),ensure_ascii=False,indent=1 if False else None,separators=(',',':'));print('extra',n,'->',len(b['extra']))
