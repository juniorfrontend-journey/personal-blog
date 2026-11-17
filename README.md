# Blog cá nhân — Jackethee

Blog tĩnh tại **https://blog.jackethee.dev** (repo này, nhánh `main`, Vercel tự deploy
mỗi lần `main` đổi). Giao diện Jackey Editorial, dựng từ 3 màn hình Stitch.

## Thêm / sửa / xóa bài — không cần đụng code

Mở **https://blog.jackethee.dev/admin**, đăng nhập bằng tài khoản GitHub, sửa bài
trên form rồi bấm lưu. Luồng chạy:

1. Decap CMS ghi bài thành file Markdown trong `content/posts/`, commit lên GitHub.
2. GitHub Actions (`.github/workflows/build.yml`) chạy `python3 build.py --out .`
   để dựng lại các file HTML rồi commit về `main`.
3. Vercel thấy `main` đổi thì deploy lại. Bài mới/sửa/xóa hiện trên web sau
   khoảng 1–3 phút.

Xóa bài trong `/admin` cũng xóa luôn trang bài cũ (build.py dọn file HTML thừa).

## Cấu trúc repo

| Đường dẫn | Ghi chú |
| --- | --- |
| `content/posts/*.md` | Bài viết: frontmatter YAML + body Markdown. File tên theo slug. |
| `build.py` | Build site từ Markdown + template Stitch. |
| `stitch/` | Template HTML gốc từ Stitch + `image-map.json` (ảnh local). |
| `images/` | Ảnh bài viết (Decap tải ảnh mới vào đây). |
| `admin/` | Trang quản trị Decap (`index.html` + `config.yml`). |
| `api/auth.js`, `api/callback.js` | Cầu nối đăng nhập GitHub cho Decap (Vercel Functions). |
| `.github/workflows/build.yml` | Auto-rebuild sau mỗi lần bài đổi. |
| `index.html`, `bai-viet.html`, `gioi-thieu.html`, `rss.xml`, `bai-viet/` | File HTML đã build, Vercel phục vụ trực tiếp. |

Bài mới nhất (theo `date`) lên mục tiêu điểm ở trang chủ; các bài còn lại vào
lưới "Bài viết mới nhất" và trang danh sách.

## Build ở máy local

```bash
python3 -m venv .venv && .venv/bin/pip install markdown pyyaml
.venv/bin/python build.py            # ghi ra site/
.venv/bin/python build.py --out .    # ghi thẳng ra repo root (như CI chạy)
```

## Đăng nhập /admin cần gì (làm 1 lần)

1. Tạo **GitHub OAuth App** (Settings → Developer settings → OAuth Apps):
   - Application name: `Blog Jackethee CMS`
   - Homepage URL: `https://blog.jackethee.dev`
   - Authorization callback URL: `https://blog.jackethee.dev/api/callback`
2. Trên Vercel (project này → Settings → Environment Variables), thêm:
   - `GITHUB_CLIENT_ID` = Client ID của OAuth App
   - `GITHUB_CLIENT_SECRET` = Client Secret của OAuth App
3. Redeploy project Vercel 1 lần để nhận biến môi trường.

Không ghi client secret vào code hay chat — chỉ nhập trong dashboard Vercel.

## Ghi chú

- Body bài viết bằng Markdown: `##` là tiêu đề mục, `>` là trích dẫn,
  `1.` là danh sách đánh số (hiện thành thẻ có số). Sơ đồ tùy chỉnh trong 2 bài
  cũ (`tu-duy-hop-den`, `sinh-vien-cntt-den-ba-hevo-charge`) là khối HTML gốc —
  đừng sửa trong trình soạn thảo, chỉ sửa bằng code.
- `featured_image` để trống thì trang chủ dùng ảnh đại diện của bài.
- `content.py` cũ (7 bài dạng HTML helper) đã thay bằng `content/posts/*.md`,
  chỉ giữ lại local để đối chiếu, không dùng để build nữa.
