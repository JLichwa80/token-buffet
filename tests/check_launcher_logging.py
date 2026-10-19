"""Verify the Windows launch scripts expose request/failure lines without vendor calls."""
import json, os, shutil, socket, subprocess, sys, tempfile, time, urllib.request, urllib.error
from pathlib import Path

root = Path(__file__).resolve().parents[1]
def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0)); return sock.getsockname()[1]

with tempfile.TemporaryDirectory(prefix='bridge-launcher-test-') as temp:
    temp=Path(temp); package=temp/'src/cli_llm_bridge'; package.mkdir(parents=True)
    for name in ['__init__.py','cli_proxy_server.py','local_router.py','logged_run.py','log_paths.py']:
        shutil.copy(root/'src/cli_llm_bridge'/name,package/name)
    (temp/'scripts').mkdir()
    for name in ['start_all_proxies.ps1','start_router.ps1']:
        shutil.copy(root/'scripts'/name,temp/'scripts'/name)
    providers={name:free_port() for name in ('fake','bravo','charlie','delta')}
    router_port=free_port()
    for name, provider_port in providers.items():
        folder=temp/'registered_providers'/name; folder.mkdir(parents=True)
        config={'server':{'port':provider_port},'execution':{'cmd_template':[sys.executable,'-c','import sys; print("synthetic quota failure",file=sys.stderr); sys.exit(1)']},'stream':{}}
        (folder/'config.json').write_text(json.dumps(config))
        status=temp/'data/providers_status'; status.mkdir(parents=True,exist_ok=True)
        (status/f'{name}_models.json').write_text(json.dumps({'models':{'available':[{'id':f'{name}-model'}]}}))
    (temp/'config').mkdir()
    (temp/'config/router_config.json').write_text(json.dumps({'mode':'custom','custom_order':['fake'],'providers':{'fake':{'tiers':{'fast':'test'}}}}))
    processes=[]; handles=[]
    try:
        for name,args in [('start_all_proxies.ps1',['-TimeoutSeconds','10']),('start_router.ps1',['-Port',str(router_port),'-RefreshInterval','0'])]:
            handle=(temp/(name+'.out')).open('w',encoding='utf-8'); handles.append(handle)
            processes.append(subprocess.Popen(['pwsh','-NoProfile','-File',str(temp/'scripts'/name),*args],cwd=temp,stdout=handle,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW))
        deadline=time.monotonic()+25
        while time.monotonic()<deadline:
            try:
                for port in [*providers.values(),router_port]:
                    with socket.create_connection(('127.0.0.1',port),timeout=.3): pass
                break
            except OSError: time.sleep(.2)
        else: raise AssertionError('Launchers failed to bind')
        for name, provider_port in providers.items():
            with urllib.request.urlopen(f'http://127.0.0.1:{provider_port}/v1/models',timeout=3) as response:
                models=json.load(response)['data']
            assert [entry['id'] for entry in models]==[f'{name}-model']
        req=urllib.request.Request(f'http://127.0.0.1:{router_port}/v1/responses',data=b'{"model":"fast","input":[]}')
        try: urllib.request.urlopen(req,timeout=10); raise AssertionError('Expected failure')
        except urllib.error.HTTPError as exc: assert exc.code==503
        deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            outputs=[(temp/(name+'.out')).read_text(encoding='utf-8') for name in ['start_all_proxies.ps1','start_router.ps1']]
            if all('REQUEST id=' in text and 'FAIL id=' in text and 'synthetic quota failure' in text for text in outputs): break
            time.sleep(.2)
        else: raise AssertionError(outputs)
        print('PASS: fleet starts four providers with model catalogs; fleet and router print one-line request failures')
    finally:
        for process in processes:
            subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            process.wait(timeout=10)
        for handle in handles: handle.close()
