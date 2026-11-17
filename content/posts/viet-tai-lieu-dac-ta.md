---
title: Viết tài liệu đặc tả sao cho dev đọc một lần là hiểu
slug: viet-tai-lieu-dac-ta
date: '2026-10-28'
category: Phân tích nghiệp vụ
excerpt: Cấu trúc hóa User Story, Acceptance Criteria và sơ đồ luồng (Flowchart) để
  xóa bỏ khoảng cách giữa BA và đội ngũ kỹ thuật.
read: 9 phút đọc
hero_image: null
hero_alt: null
hero_caption: null
hero_icon: description
hero_label: Tài liệu · BA · Dev
featured_image: null
tags:
- Tài liệu
- Business Analysis
- Dev
---

Có một nỗi đau chung của BA và dev: BA viết tài liệu rất kỹ, dev đọc xong vẫn phải hỏi lại. Không phải vì dev lười đọc, mà vì tài liệu viết theo cảm nhận của người viết, không viết theo cái dev cần để làm. Tôi đã mất vài vòng hỏi đáp mới rút ra được cách viết mà dev đọc một lần là hiểu — và bài này ghi lại cách đó.

## Quy tắc của sếp tôi

Sếp tôi đặt một quy tắc cho mọi phản hồi gửi dev: chỉ viết ba thứ — hiện trạng quan sát được, trạng thái cần đạt kiểm chứng được, và căn cứ chính xác. Không viết theo cảm nhận chủ quan. Không dùng những từ như “như mong muốn”, “chưa hợp lý”, “tinh gọn”, “tối giản” — vì mỗi người hiểu những từ đó một kiểu.

Quy tắc này nghe thì khô, nhưng nó xóa được gần hết tranh cãi. Khi tôi viết “hiện trạng: màn hình A thiếu cột X; cần đạt: màn hình A có đủ 8 cột theo danh mục đính kèm; căn cứ: tài liệu v31 trang 4”, dev không cần hỏi lại tôi muốn gì. Mọi thứ cần để làm đều nằm trong ba dòng đó.

> Một khái niệm tiền chỉ được một tên.
>
> — Quy tắc đặt tên trong đặc tả

## Một khái niệm, một tên

Lỗi đặt tên là lỗi tốn kém nhất trong tài liệu. Tôi từng gọi cùng một khoản tiền bằng ba cái tên — phí tối thiểu, tiền cọc, tiền giữ — và dev làm ra ba nhãn khác nhau trên giao diện. Từ đó tôi giữ quy tắc: một khái niệm chỉ được một tên, dùng nhất quán ở mọi tài liệu, mọi màn hình, mọi cuộc họp. Tên section chỉ xuất hiện một lần thì phải xác nhận trước khi gửi.

Đặt tên chuẩn không phải là việc của riêng BA. Nó là hợp đồng giữa người viết và người đọc: từ này chỉ đúng một thứ, và cả hai bên đều đồng ý như vậy.

## Cấu trúc một đặc tả tốt

1. **User Story rõ vai trò và giá trị** — Ai làm gì, để được gì. Viết thiếu một trong ba thì dev không biết mình đang phục vụ ai.
2. **Acceptance Criteria kiểm chứng được** — Mỗi tiêu chí phải trả lời được bằng có hoặc không sau khi test. Tiêu chí mơ hồ thì test cũng mơ hồ.
3. **Sơ đồ luồng thay cho đoạn văn dài** — Một sơ đồ luồng nói rõ hơn ba đoạn văn mô tả quy trình. Người đọc nhìn sơ đồ là thấy đường đi của dữ liệu.
4. **Triage ba tầng khi rà soát** — Cái gây implement sai thì bắt buộc sửa. Cái nên sửa thì sửa nếu còn thời gian. Cái bỏ qua được thì nói thẳng là bỏ qua được.

## Khi nào tài liệu đủ để gửi

Câu hỏi khó nhất là: gửi cho sếp, cho dev được chưa? Tôi trả lời bằng phán quyết nhị phân kèm phạm vi: gửi để check tiến độ thì được, gửi như bản chốt thì chưa — và liệt kê đúng ba việc còn tồn đọng. Một phán quyết rõ ràng kèm ba việc tồn đọng thì người nhận biết mình đang cầm thứ gì trong tay.

Và có một kỷ luật tôi giữ rất chặt: mỗi bản gửi đi là một bản duy nhất. Không gửi hai bản cùng lúc, không sửa lén sau khi gửi. Bản nào đã gửi thì bản đó là căn cứ — muốn đổi thì gửi bản mới và nói rõ đổi chỗ nào.

## Kết luận

Viết tài liệu đặc tả không phải là viết văn hay. Nó là viết sao cho người khác làm đúng mà không cần hỏi lại. Muốn vậy thì từ ngữ phải chuẩn, cấu trúc phải rõ, và căn cứ phải chính xác. Làm được ba thứ đó thì tài liệu ngắn cũng đủ, tài liệu dài cũng không thừa.
