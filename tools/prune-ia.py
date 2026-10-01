# Remove off-mission items (Roman Catholic devotional/apologetic authors, Mormon/cult, non-theology) from ia.json
import json,re
AU=re.compile(r"liguori|ligouri|aquinas|newman|pohle|catholic church|frassinetti|nageleisen|spirago|de sales|john of the cross|theresa|bonaventure|duns scotus|francis of assisi|loyola|bellarmine|batiffol|henry edward manning|frederick william faber|edouard de lehen|fielding smith|joseph smith|brigham young|mormon|latter[- ]day|mary baker|eddy|watchtower|blavatsky|theosoph|swedenborg|machiavelli|propagation of|knights of columbus|cardinal",re.I)
TI=re.compile(r"\b(rosary|purgatory|novena|parish priest|mormon|latter[- ]day|book of mormon|breviary|benediction|sacred heart|our lady|immaculate|stations of the cross|roman missal|summa|spiritualis[mt]|theosoph|christian science|gout|coins|arithmetic|cookery|geography|railway|agricultur|veterinar|surgery|medicine|diseases|rheumat\w*)\b",re.I)
d=json.load(open('ia.json'));A=d['a']
keep=[x for x in d['b'] if not (AU.search(A[x[0]]) or TI.search(x[1]))]
print('before',len(d['b']),'after',len(keep))
d['b']=keep
json.dump(d,open('ia.json','w'),ensure_ascii=False,separators=(',',':'))
