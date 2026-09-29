"""Check regional report consistency; research and translation still need human/agent review."""
import argparse
from datetime import datetime, timedelta
import json, math, re
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

def validate_config(config):
    region=config['region']
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*',region['id']):
        raise ValueError('region.id must be a lowercase slug')
    if not re.fullmatch(r'[A-Z]{2}',region['country']):
        raise ValueError('country must be ISO two-letter code')
    ZoneInfo(region['timezone'])
    if not region['discoveryLanguages'] or not config['contentLanguage']:
        raise ValueError('Language configuration is required')
    if not config['stateDir']:
        raise ValueError('stateDir is required')
    return config

def state_path(config, config_file):
    validate_config(config)
    return (Path(config_file).resolve().parent/config['stateDir']/config['region']['id']).resolve()

def week_window(config, now):
    validate_config(config)
    if now.tzinfo is None:raise ValueError('now must have a timezone')
    local=now.astimezone(ZoneInfo(config['region']['timezone']))
    end=(local-timedelta(days=local.weekday())).replace(hour=0,minute=0,second=0,microsecond=0)
    return (end-timedelta(days=7)).isoformat(),end.isoformat()

def baseline_growth(values):
    # Caller must verify all 35 daily observations share region/query/normalization.
    if len(values)!=35 or any(type(x) not in (int,float) or not math.isfinite(x) or x<0 for x in values):return None
    baseline=sum(values[:28])/28
    return None if baseline==0 else (sum(values[28:])/7/baseline-1)*100

def valid_url(value):
    try:
        u=urlsplit(value)
        return u.scheme in ('http','https') and bool(u.hostname) and not u.username and not u.password
    except (ValueError,TypeError):return False

def audit(config,report):
    validate_config(config);errors=[]
    if report.get('region_id')!=config['region']['id']:errors.append('Report belongs to another region')
    history=set(report.get('history_topic_ids',[]));seen=set()
    for t in report.get('topics',[]):
        ident=t.get('topic_id')
        if not ident or ident in seen:errors.append('Missing or duplicate topic_id')
        seen.add(ident)
        kind=t.get('kind')
        if kind not in ('new','old','continuation','watch'):errors.append(f'{ident}: invalid kind')
        if kind=='new' and ident in history:errors.append(f'{ident}: old topic labeled new')
        if kind in ('old','continuation') and ident not in history:errors.append(f'{ident}: no historical topic')
        urls=t.get('source_urls',[])
        if not urls or not all(valid_url(u) for u in urls):errors.append(f'{ident}: missing/invalid source URL')
        if kind=='continuation':
            if not t.get('previous_stage') or not t.get('stage') or t['previous_stage']==t['stage']:
                errors.append(f'{ident}: no actual stage change')
            new_urls=t.get('new_evidence_urls',[])
            if not new_urls or not all(valid_url(u) and u in urls for u in new_urls):errors.append(f'{ident}: missing linked stage evidence')
        facts=t.get('facts'); status=t.get('evidence_status')
        if not isinstance(facts,dict) or not status:errors.append(f'{ident}: facts/status required')
        for lang in ('zh','en'):
            translated=t.get(lang,{})
            for key,value in [('topic_id',ident),('facts',facts),('evidence_status',status)]:
                if translated.get(key)!=value:errors.append(f'{ident}: {lang} {key} mismatch')
        for key in ('local_term','target_keywords','headline'):
            if t.get('zh',{}).get(key)!=t.get('en',{}).get(key):errors.append(f'{ident}: shared {key} differs')
    return errors

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('config');p.add_argument('report');args=p.parse_args()
    config=json.loads(Path(args.config).read_text());report=json.loads(Path(args.report).read_text())
    errors=audit(config,report)
    print(json.dumps({'ok':not errors,'errors':errors},ensure_ascii=False,indent=2))
    raise SystemExit(bool(errors))
