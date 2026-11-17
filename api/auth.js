// GET /api/auth — bắt đầu đăng nhập GitHub cho Decap CMS.
// Chuyển hướng sang trang cấp quyền của GitHub. Client id đọc từ biến môi
// trường GITHUB_CLIENT_ID trên Vercel (không ghi cứng trong code).
module.exports = (req, res) => {
  const site = process.env.OAUTH_SITE_URL || 'https://blog.jackethee.dev';
  const clientId = process.env.GITHUB_CLIENT_ID;
  if (!clientId) {
    res.status(500).send('Thiếu GITHUB_CLIENT_ID. Thêm biến môi trường trên Vercel.');
    return;
  }
  const params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: site + '/api/callback',
    scope: 'repo',
  });
  res.redirect('https://github.com/login/oauth/authorize?' + params.toString());
};
