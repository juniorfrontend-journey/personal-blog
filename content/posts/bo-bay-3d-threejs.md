---
title: 'Bò Bay 3D: làm game web bằng Three.js và tài nguyên miễn phí'
slug: bo-bay-3d-threejs
date: '2026-11-09'
category: Game
excerpt: Bài học tối ưu hiệu năng render đồ họa 3D trực tiếp trên trình duyệt từ một
  dự án game thử nghiệm vui nhộn.
read: 5 phút đọc
hero_image: null
hero_alt: null
hero_caption: null
hero_icon: flight
hero_label: Game · Three.js · Web 3D
featured_image: null
tags:
- Three.js
- Game
- Web
---

Bò Bay 3D là một game web nhỏ tôi làm để thử nghiệm: một con bò bay trên hòn đảo nổi, xuyên qua 10 vòng vàng, làm nhiệm vụ, ngắm cảnh. Nghe thì đơn giản, nhưng để nó chạy mượt 60 khung hình/giây trên trình duyệt, không cần cài đặt, tôi phải học khá nhiều thứ — và bài học lớn nhất không nằm ở code, mà nằm ở cách tìm tài nguyên.

## Chỉ dùng tài nguyên thật, miễn phí

Ngay từ đầu tôi đặt một quy tắc cho chính mình: texture, âm thanh và model chỉ lấy thật từ nguồn miễn phí, không tự bịa. Texture cỏ, đá, gỗ lấy từ Poly Haven và ambientCG. Âm thanh — tiếng rống, chuông cổ, tiếng gió — lấy từ Kenney và Pixabay. Con bò lấy từ model Quaternius, giấy phép CC0. Tất cả đều miễn phí và không cần ghi nguồn.

Quy tắc này nghe có vẻ gò bó, nhưng nó làm game đẹp lên rất nhiều. Một texture cỏ thật chụp từ đời thực luôn hơn một màu xanh tôi tự tô. Một tiếng rống thật luôn hơn một âm thanh tôi tự tổng hợp. Công việc của tôi không phải là sáng tạo ra mọi thứ từ con số 0, mà là đi tìm đúng nguồn và áp dụng cho đúng chỗ.

## Con bò biến mất — và lỗi bị nuốt lặng

Bài học kỹ thuật nhớ nhất là lần con bò mới không chịu hiện lên. Tôi đã thay model bò tự vẽ bằng model Quaternius, kiểm tra code thấy mọi thứ đều đúng, nhưng trên màn hình vẫn là con bò cũ. Mãi sau tôi mới phát hiện: bộ nạp model tải từ một máy chủ khác với thư viện Three.js, và khi tải lỗi, lỗi bị nuốt lặng không báo gì. Không có thông báo, không có dấu vết — chỉ có sự im lặng.

Tôi sửa bằng cách nhúng bộ nạp vào chung một file với game, và bắt lỗi phải hiện ra rõ ràng. Từ đó tôi giữ một nguyên tắc: lỗi nào cũng phải kêu lên. Một lỗi kêu to thì sửa trong năm phút. Một lỗi im lặng thì mất cả buổi chiều để tìm.

1. **Chiều cao mặt đất theo đúng địa hình** — Đảo có 8 ngọn đồi. Va chạm và độ cao của bò phải tính theo hàm chiều cao mặt đất H(x,z), không phải một mặt phẳng. Tính sai là bò bay xuyên đồi.
2. **Nước làm chậm** — Bay thấp qua mặt nước thì tốc độ giảm tới 62%. Một chi tiết nhỏ nhưng làm cảm giác bay thật hơn hẳn.
3. **Cơ chế flare khi hạ cánh** — Bay thấp dưới 6 mét mà đang chìm, kéo cần lên đúng lúc thì tốc độ chìm giảm tối đa 30%. Kéo sớm quá thì mất điểm, kéo đúng lúc thì hạ cánh mềm.

## Nhiệm vụ làm game có chiều sâu

Một game chỉ bay vòng vòng thì chán sau năm phút. Nên tôi thêm 20 nhiệm vụ: tuần tra cối xay gió, chở giỏ hàng, bay chậm qua cầu. Mỗi nhiệm vụ có luật riêng, có sao đánh giá, có HUD hiển thị tốc độ và độ cao. Nhiệm vụ không làm game khó hơn — nó làm người chơi có lý do để bay tiếp.

Và có một điều tôi vẫn chưa làm được trọn vẹn: kiểm chứng bằng mắt và tai. Mọi thứ đến nay mới được kiểm tra bằng code và mô phỏng. Game có thật sự đẹp, âm thanh có thật sự hay, cảm giác bay có thật sự đã hay không — chỉ người chơi thử mới trả lời được. Tôi vẫn đang chờ lượt chơi thử đầu tiên.

## Kết luận

Bò Bay 3D dạy tôi rằng làm game web không cần ngân sách lớn. Cần một thư viện 3D tốt, vài nguồn tài nguyên miễn phí đáng tin, và kỷ luật kiểm chứng từng thứ mình đắp vào. Còn lại là kiên nhẫn: mỗi ngày một cải tiến nhỏ, và đừng bao giờ để một lỗi im lặng.
