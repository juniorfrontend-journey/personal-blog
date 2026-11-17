# Blog cá nhân — Jackethee

Blog cá nhân tiếng Việt của Nguyễn Hùng Mạnh (Jackethee): công nghệ, phân tích
nghiệp vụ, AI, game và học tập. Website tĩnh, không cần backend, deploy thẳng
lên Vercel.

## Nguồn gốc thiết kế

- Thiết kế gốc sinh bằng **Google Stitch** (project `Blog cá nhân — Jackethee`,
  id `6271780814624335218`, design system **Jackey Editorial**): 3 màn hình
  trang chủ, trang bài viết, trang giới thiệu.
- Atlas chuyển thành website đa trang hoàn thiện: giữ nguyên hệ thiết kế
  (Nunito Sans, nền trắng, chữ gần đen, điểm nhấn cam `#F17C55`, bo góc nhỏ,
  không gradient), nối link thật giữa các trang, viết đầy đủ nội dung 7 bài.

## Cấu trúc

```
index.html            Trang chủ (bài tiêu điểm + 6 bài mới nhất + đăng ký email)
bai-viet.html         Danh sách tất cả 7 bài viết
gioi-thieu.html       Giới thiệu tác giả, hành trình, liên hệ
bai-viet/*.html       7 trang bài viết đầy đủ nội dung
images/               Ảnh của Stitch, đã tải về local (không hotlink)
rss.xml               Feed RSS (7 bài)
```

## Deploy lên Vercel

1. Import repo này tại vercel.com/new.
2. Framework Preset: **Other**. Không cần Build Command, không cần Output
   Directory (site nằm ở root).
3. Deploy. Mỗi lần push lên `main` sẽ tự deploy lại.

## Thêm bài mới

Cách đúng: sửa `content.py` (thêm 1 mục vào `POSTS`, viết body bằng các
helper `LEAD`/`P`/`H2`/`QUOTE`/`NUM_LIST`), chạy `python3 build.py`, rồi
commit thư mục `site/` (kèm `stitch/` và `content.py` để lần sau build lại).

## Lưu ý

- Tailwind dùng qua CDN (`cdn.tailwindcss.com`) + config inline trong từng
  trang, nên không cần bước build CSS.
- Ảnh đã tải về local. Muốn đổi ảnh đại diện thì thay file trong `images/`
  và chạy lại `build.py`.
- `rss.xml` đang dùng base URL `https://blog.jackethee.dev` (blog chạy ở
  subdomain `blog.jackethee.dev` của `jackethee.dev`). Nếu blog chạy ở
  domain khác thì sửa biến `SITE_URL` trong `build.py` rồi chạy lại.
- Form đăng ký email trên trang chủ hiện chỉ là giao diện (chưa nối backend).
