"""One authorized inference request. No redirects, retries, or response text output."""
import argparse
import getpass
import json
import os
import ssl
import sys
from datetime import datetime, timezone
from urllib.parse import urlsplit
from urllib.request import Request, HTTPRedirectHandler, HTTPSHandler, build_opener
from urllib.error import HTTPError, URLError

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise HTTPError(newurl, code, 'Redirect refused', headers, None)

def endpoint(value):
    u = urlsplit(value)
    if u.scheme != 'https' or not u.hostname or u.username or u.password or u.query or u.fragment:
        raise ValueError('Use a verified HTTPS model endpoint without credentials, query or fragment.')
    path = u.path.rstrip('/')
    if path not in ('', '/v1'):
        raise ValueError('Use the model base endpoint, optionally ending in /v1.')
    return value.rstrip('/') + ('/chat/completions' if path == '/v1' else '/v1/chat/completions')

def probe(base, model, token, send=None):
    url = endpoint(base)
    token = token.strip()
    if not token or any(c.isspace() for c in token) or token.startswith(('Bearer ', 'API_KEY=', '"', "'")):
        raise ValueError('Expected a nonempty raw token, without assignments, quotes or internal whitespace.')
    if not model or len(model) > 256:
        raise ValueError('Supply the verified deployed model identifier.')
    payload = json.dumps({'model':model,'messages':[{'role':'user','content':'Reply with OK.'}],'max_tokens':32,'stream':False}).encode()
    request = Request(url, data=payload, headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'},method='POST')
    if send is None:
        send = build_opener(NoRedirect(),HTTPSHandler(context=ssl.create_default_context())).open
    result = {'ok':False,'checked_at':datetime.now(timezone.utc).isoformat(),'http_status':None,'test':'single text completion'}
    try:
        with send(request, timeout=30) as response:
            result['http_status']=response.status
            raw=response.read(1024*1024+1)
            if len(raw)>1024*1024:
                result['category']='response_too_large';return result
            data=json.loads(raw)
            choices=data.get('choices',[]) if isinstance(data,dict) else []
            content=choices[0].get('message',{}).get('content') if choices and isinstance(choices[0],dict) else None
            result['ok']=response.status==200 and not data.get('error') and isinstance(content,str) and bool(content.strip())
            result['category']='completion_received' if result['ok'] else 'empty_or_error_response'
            usage=data.get('usage',{}) if isinstance(data,dict) else {}
            if isinstance(usage,dict):
                result['usage']={k:v for k,v in usage.items() if k in ('prompt_tokens','completion_tokens','total_tokens') and type(v) is int and v>=0}
            # Do not echo arbitrary headers: retain only a documented cache verdict.
            verdict=response.headers.get('x-cache','').lower()
            if verdict in ('hit','miss'):result['cache']=verdict
    except HTTPError as error:
        result['http_status']=error.code
        result['category']='redirect_refused' if 300<=error.code<400 else 'http_error'
        # Error bodies can echo submitted secrets. Do not read or print them.
    except (URLError,TimeoutError,OSError):result['category']='connection_error'
    except (ValueError,TypeError,AttributeError,IndexError):result['category']='invalid_response'
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--endpoint',required=True,help='Verified Capella model base URL')
    parser.add_argument('--model',required=True,help='Verified model identifier')
    args=parser.parse_args()
    try:
        endpoint(args.endpoint)
        key=os.environ.get('CB_MODEL_TOKEN')
        if not key:
            if not sys.stdin.isatty():
                raise ValueError('Use a protected environment variable or interactive terminal for secret input.')
            key=getpass.getpass('Model Service token (hidden): ')
        result=probe(args.endpoint,args.model,key)
    except ValueError as error:
        print(json.dumps({'ok':False,'category':'configuration_error','message':str(error)}));return 2
    except (EOFError,KeyboardInterrupt):
        print(json.dumps({'ok':False,'category':'cancelled'}));return 2
    print(json.dumps(result,indent=2));return 0 if result['ok'] else 1
if __name__=='__main__':raise SystemExit(main())
