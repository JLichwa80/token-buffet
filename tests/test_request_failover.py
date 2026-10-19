import io
import json
import logging
import sys
import threading
import tempfile
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch
from cli_llm_bridge import local_router as router
from cli_llm_bridge import cli_proxy_server as proxy
from cli_llm_bridge import log_config

class RequestTests(unittest.TestCase):
    def setUp(self):
        level_patch=patch.object(proxy,'TRACE_LEVEL','DEBUG')
        level_patch.start()
        self.addCleanup(level_patch.stop)

    def start_server(self, handler):
        server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return server.server_port

    def request(self, port, model='fast', stream=False, request_id=None):
        headers={'Content-Type':'application/json'}
        if request_id: headers['X-Request-ID']=request_id
        req = urllib.request.Request(f'http://127.0.0.1:{port}/v1/responses', data=json.dumps({'model':model,'input':[], 'stream':stream}).encode(), headers=headers)
        return urllib.request.urlopen(req, timeout=10)

    def test_proxy_failure_nonstream_and_stream(self):
        config={'execution':{'cmd_template':[sys.executable,'-c', 'import sys; print(\'quota exhausted\',file=sys.stderr); sys.exit(1)']},'stream':{}}
        with tempfile.TemporaryDirectory() as temp, patch.object(proxy,'LOG_DIR',Path(temp)), patch.object(proxy,'PROVIDER','verification'), patch.object(proxy,'load_provider_config',return_value=config):
            port=self.start_server(proxy.ProxyHandler)
            with self.assertRaises(urllib.error.HTTPError) as caught:
                self.request(port)
            self.assertEqual(caught.exception.code,502)
            self.assertIn(b'quota exhausted',caught.exception.read())
            with self.request(port,stream=True,request_id='streamfailure') as response:
                wire=response.read()
            self.assertIn(b'response.failed',wire)
            self.assertNotIn(b'response.completed',wire)
            captured=Path(temp)/'verification/proxy/raw_responses'
            self.assertEqual((next(captured.glob('*streamfailure.raw'))).read_bytes(),wire)
            self.assertIn('quota exhausted',(next(captured.glob('*streamfailure.provider.stderr.log'))).read_text())
            self.assertIn('Proxy Error: quota exhausted',(next((Path(temp)/'verification/proxy/sessions').glob('*streamfailure.log'))).read_text())

    def test_declared_error_even_with_zero_exit(self):
        config={'execution':{'cmd_template':[sys.executable,'-c','print(\'{"type":"error","message":"quota exhausted"}\')']},'stream':{'error_extractors':[{'matches':{'type':'error'},'path':'message'}]}}
        with patch.object(proxy,'PROVIDER','verification'), patch.object(proxy,'load_provider_config',return_value=config):
            port=self.start_server(proxy.ProxyHandler)
            with self.assertRaises(urllib.error.HTTPError) as caught: self.request(port)
            self.assertEqual(caught.exception.code,502)

    def test_empty_success_is_a_failure(self):
        config={'execution':{'cmd_template':[sys.executable,'-c','print("unmatched event")']},'stream':{}}
        with patch.object(proxy,'PROVIDER','verification'), patch.object(proxy,'load_provider_config',return_value=config):
            port=self.start_server(proxy.ProxyHandler)
            with self.assertRaises(urllib.error.HTTPError) as caught: self.request(port)
            self.assertEqual(caught.exception.code,502)
            self.assertIn(b'no text',caught.exception.read())
            with self.request(port,stream=True) as response: wire=response.read()
            self.assertIn(b'response.failed',wire)
            self.assertNotIn(b'response.completed',wire)

    def test_agy_result_event_yields_text(self):
        config=json.loads((Path(__file__).resolve().parents[1]/'registered_providers/agy/config.json').read_text())
        config['execution']={'cmd_template':[sys.executable,'-c','print(\'{"event":"result","result":{"status":"SUCCESS","response":"OK"}}\')']}
        with tempfile.TemporaryDirectory() as temp, patch.object(proxy,'LOG_DIR',Path(temp)), patch.object(proxy,'PROVIDER','verification'), patch.object(proxy,'load_provider_config',return_value=config):
            port=self.start_server(proxy.ProxyHandler)
            with self.request(port,request_id='capturetest') as response: body=json.load(response)
            self.assertEqual(body['output'][0]['content'][0]['text'],'OK')
            files=list((Path(temp)/'verification/proxy/raw_responses').glob('*capturetest*'))
            self.assertEqual(len(files),3)
            stdout=next(p for p in files if p.name.endswith('.provider.stdout.log'))
            http=next(p for p in files if p.name.endswith('.raw'))
            self.assertIn('"status":"SUCCESS"',stdout.read_text())
            self.assertEqual(json.loads(http.read_text()),body)
            session=next((Path(temp)/'verification/proxy/sessions').glob('*capturetest.log'))
            self.assertIn('CHUNK: ',session.read_text())
            self.assertIn('Raw payload: ',session.read_text())
            self.assertIn('Output received: ',session.read_text())
            extracted=next((Path(temp)/'verification/llm_provider/raw_responses').glob('*capturetest.txt'))
            self.assertEqual(extracted.read_text(),'OK')

    def test_info_keeps_summary_without_raw_content(self):
        config={'execution':{'cmd_template':[sys.executable,'-c','print(\'{"text":"OK"}\')']},'stream':{'text_extractors':[{'path':'text'}]}}
        with tempfile.TemporaryDirectory() as temp, patch.object(proxy,'LOG_DIR',Path(temp)), patch.object(proxy,'TRACE_LEVEL','INFO'), patch.object(proxy,'PROVIDER','verification'), patch.object(proxy,'load_provider_config',return_value=config):
            port=self.start_server(proxy.ProxyHandler)
            with self.request(port,request_id='infosummary') as response: body=json.load(response)
            self.assertEqual(body['output'][0]['content'][0]['text'],'OK')
            session=next((Path(temp)/'verification/proxy/sessions').glob('*infosummary.log'))
            trace=session.read_text()
            self.assertIn('Request parsed:',trace)
            self.assertIn('Output received:',trace)
            self.assertNotIn('Raw payload:',trace)
            self.assertNotIn('CHUNK:',trace)
            self.assertFalse((Path(temp)/'verification/proxy/raw_responses').exists())

    def test_config_level_and_debug_override(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(log_config,'REPO_ROOT',Path(temp)):
            config_dir=Path(temp)/'config'
            config_dir.mkdir()
            (config_dir/'logging.json').write_text('{"level":"INFO"}')
            self.assertEqual(log_config.resolve_log_level(),'INFO')
            self.assertEqual(log_config.resolve_log_level(debug=True),'DEBUG')
            self.assertEqual(log_config.resolve_log_level('DEBUG'),'DEBUG')

    def test_router_retries_http_and_partial_stream_failure(self):
        attempts=[]
        class Backend(BaseHTTPRequestHandler):
            def log_message(self,*args): pass
            def do_POST(self):
                payload=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                model=payload['model']; attempts.append(model)
                if model=='a':
                    self.send_response(502); body=b'{"error":{"message":"quota exhausted"}}'
                elif model=='b':
                    self.send_response(200); body=b'data: {"type":"response.output_text.delta","delta":"discard me"}\n\ndata: {"type":"response.failed","response":{"error":{"message":"failed midstream"}}}\n\n'
                else:
                    self.send_response(200); body=b'{"output_text":"success"}'
                self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
        backend_port=self.start_server(Backend)
        tiers={'fast':[{'provider':p,'model':p} for p in 'abc']}
        with patch.multiple(router,TIERS=tiers,ALL_MODELS={'a':'a'},MODE='custom',CUSTOM_ORDER=list('abc'),USAGE={}), patch.object(router,'running_port',return_value=backend_port):
            port=self.start_server(router.RouterHandler)
            with self.request(port,model='a',stream=True) as response: body=response.read()
            self.assertEqual(attempts,list('abc'))
            self.assertEqual(body,b'{"output_text":"success"}')

    def test_provider_first_mapping(self):
        tiers={'fast':[{'provider':'a','model':'exact-a'}], 'medium':[{'provider':'a','model':'exact-b'},{'provider':'b','model':'exact-c'}]}
        self.assertEqual(router.tiers_from_providers(router.providers_from_tiers(tiers)),tiers)

if __name__=='__main__': unittest.main()
