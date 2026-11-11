import io,json,unittest
from unittest.mock import Mock
from urllib.error import HTTPError
import probe_model as p
class ProbeTests(unittest.TestCase):
 def test_normalizes_endpoint(self):
  self.assertEqual(p.endpoint('https://model.example/v1/'),'https://model.example/v1/chat/completions')
  self.assertEqual(p.endpoint('https://model.example'),'https://model.example/v1/chat/completions')
 def test_rejects_unsafe_url(self):
  for x in ['http://model.example','https://secret@model.example','https://model.example/?token=x','https://model.example/#key','https://model.example/other']:
   with self.assertRaises(ValueError):p.endpoint(x)
 def response(self,data):
  r=Mock();r.status=200;r.headers={};r.read.return_value=json.dumps(data).encode();r.__enter__=Mock(return_value=r);r.__exit__=Mock(return_value=False);return r
 def test_success_no_output_secret(self):
  send=Mock(return_value=self.response({'choices':[{'message':{'content':'private reply'}}],'usage':{'total_tokens':12}}))
  result=p.probe('https://model.example','m','synthetic-test-token',send)
  self.assertTrue(result['ok']);self.assertNotIn('private reply',json.dumps(result));self.assertNotIn('synthetic-test-token',json.dumps(result));self.assertEqual(send.call_count,1)
 def test_200_error_is_failure(self):
  self.assertFalse(p.probe('https://model.example','m','x',Mock(return_value=self.response({'error':{'message':'private'}})))['ok'])
 def test_empty_completion_is_failure(self):
  self.assertFalse(p.probe('https://model.example','m','x',Mock(return_value=self.response({'choices':[{'message':{'content':''}}]})))['ok'])
 def test_http_error_does_not_echo_body(self):
  send=Mock(side_effect=HTTPError('https://model.example',401,'unauthorized',{},io.BytesIO(b'secret-token')))
  out=p.probe('https://model.example','m','x',send);self.assertEqual(out['http_status'],401);self.assertNotIn('secret-token',json.dumps(out));self.assertEqual(send.call_count,1)
 def test_redirect_is_not_followed(self):
  with self.assertRaises(HTTPError):p.NoRedirect().redirect_request(None,None,302,'redirect',{},'https://other.example')
 def test_tokens_are_raw(self):
  for token in ['', 'Bearer abc', 'API_KEY=abc','abc def','"abc"']:
   with self.assertRaises(ValueError):p.probe('https://model.example','m',token,Mock())
if __name__=='__main__':unittest.main()
