// GET /api/callback — GitHub trả code về đây sau khi user bấm cho phép.
// Đổi code lấy access token ở phía server (client_secret không bao giờ lộ ra
// trình duyệt), rồi gửi token về cho Decap qua postMessage + BroadcastChannel
// (dự phòng khi GitHub chặn window.opener bằng COOP: same-origin).
module.exports = async (req, res) => {
  const site = process.env.OAUTH_SITE_URL || 'https://blog.jackethee.dev';
  const code = (req.query && req.query.code) || '';
  let token = '';
  let error = '';
  try {
    const r = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        client_id: process.env.GITHUB_CLIENT_ID,
        client_secret: process.env.GITHUB_CLIENT_SECRET,
        code: code,
        redirect_uri: site + '/api/callback',
      }),
    });
    const data = await r.json();
    token = data.access_token || '';
    error = data.error || '';
  } catch (e) {
    error = 'token_exchange_failed';
  }
  const status = token ? 'success' : 'error';
  const content = token
    ? { token: token, provider: 'github' }
    : { error: error || 'unknown_error' };
  const page =
    '<!doctype html><html><head><meta charset="utf-8"><title>Decap CMS</title></head>'
    + '<body><p>'
    + (token
      ? 'Đăng nhập thành công, đang quay lại trang quản trị…'
      : 'Đăng nhập thất bại: ' + error)
    + '</p>'
    + '<script>(function(){'
    + 'var content=' + JSON.stringify(JSON.stringify(content)) + ';'
    + 'var status=' + JSON.stringify(status) + ';'
    + 'var sent=false;'
    + 'function send(){'
    + '  if(sent) return; sent=true;'
    + '  var msg="authorization:github:"+status+":"+content;'
    + '  try{ if(window.opener) window.opener.postMessage(msg,"*"); }catch(e){}'
    + '  try{ new BroadcastChannel("decap-cms-auth").postMessage(msg); }catch(e){}'
    + '}'
    + 'function onAck(){ send(); window.removeEventListener("message",onAck,false); }'
    + 'window.addEventListener("message",onAck,false);'
    + 'try{ if(window.opener) window.opener.postMessage("authorizing:github","*"); }catch(e){}'
    + 'try{ new BroadcastChannel("decap-cms-auth").postMessage("authorizing:github"); }catch(e){}'
    + 'setTimeout(send, 3000);'
    + '})();</script></body></html>';
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.status(200).send(page);
};
