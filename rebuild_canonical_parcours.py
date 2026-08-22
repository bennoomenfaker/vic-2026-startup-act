import json
from pathlib import Path
from datetime import datetime, timezone

root=Path('/home/ubuntu/vic-2026-startup-act-4339943/public/data')
d=json.loads((root/'dashboard_data.json').read_text(encoding='utf-8'))
sessions=d['sessions']
yearly=d['yearly']
labels=sum(int(s.get('labels') or 0) for s in sessions)
pre=sum(int(s.get('preLabels') or 0) for s in sessions)
conv=sum(int(s.get('conversions') or 0) for s in sessions)
retraits=sum(int(s.get('retraits') or 0) for s in sessions)
direct=max(0,labels-conv)
restants=max(0,pre-conv)
out={
  'meta': {
    'totalConversions': conv,
    'totalNewPreLabels': pre,
    'totalNewLabels': direct,
    'totalRetraits': retraits,
    'totalLabels': labels,
    'convRate': round(conv/pre*100,1) if pre else None,
    'pctLabelsFromConversions': round(conv/labels*100,1) if labels else None,
    'manualSessions': [],
    'sessionsWithConversions': sum(1 for s in sessions if int(s.get('conversions') or 0)>0),
    'sessionsWithRetraits': sum(1 for s in sessions if int(s.get('retraits') or 0)>0),
    'preLabelsRestants': restants,
    'preLabelsRestantsPct': round(restants/pre*100,1) if pre else None,
    'definition': 'Les labels officiels incluent les conversions; totalNewLabels = labels directs hors conversions; les conversions ne sont pas additionnées au totalLabels.',
    'generated': datetime.now(timezone.utc).isoformat(),
  },
  'yearly': yearly,
  'sessions': []
}
for s in sessions:
  c=int(s.get('conversions') or 0); l=int(s.get('labels') or 0); p=int(s.get('preLabels') or 0)
  out['sessions'].append({
    'session': s.get('session'),
    'candidatures': int(s.get('candidatures') or 0),
    'labels': l,
    'preLabels': p,
    'conversions': c,
    'retraits': int(s.get('retraits') or 0),
    'labelsDirects': max(0,l-c),
    'pctConversions': round(c/p*100,1) if p else 0,
    'pctRetraits': round(int(s.get('retraits') or 0)/l*100,1) if l else 0,
  })
(root/'parcours.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out['meta'],ensure_ascii=False))
