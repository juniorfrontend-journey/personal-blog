---
title: Tôi xây một công ty agent bằng AI như thế nào
slug: cong-ty-agent-ai
date: '2026-11-12'
category: AI
excerpt: Thử nghiệm phân phối công việc tự động cho các LLM agent phối hợp giải quyết
  bài toán nghiệp vụ phức tạp.
read: 7 phút đọc
hero_image: null
hero_alt: null
hero_caption: null
hero_icon: smart_toy
hero_label: AI · Agent · Automation
featured_image: null
tags:
- AI
- Agent
- Automation
---

Một buổi tối, tôi tự hỏi: nếu mỗi AI agent là một nhân viên, thì một mình tôi có thể điều hành cả một công ty không? Không phải công ty trên giấy, mà một guồng máy thật: có phòng ban, có bộ nhớ riêng từng người, có quy trình bàn giao, có sổ sách. Tôi bắt tay vào xây, và đây là những gì tôi học được sau vài tuần vận hành nó.

## Vì sao lại là công ty, không phải một trợ lý

Một trợ lý AI giỏi làm được nhiều việc, nhưng nó có một điểm yếu: mọi thứ dồn vào một đầu. Khi khối lượng việc tăng lên — vừa viết code, vừa kiểm thử, vừa nghiên cứu, vừa quản lý dữ liệu — một đầu mối duy nhất trở thành nút thắt. Chia việc cho nhiều agent chuyên trách thì khác: mỗi agent chỉ làm giỏi một thứ, và làm nó lặp đi lặp lại theo đúng quy trình của mình.

Tôi chia thành các phòng: Kỹ thuật viết code, QA kiểm thử, Thiết kế lo giao diện, Dữ liệu giữ sổ sách, Nghiên cứu đi tìm nguồn, Truyền thông lo kênh phụ. Mỗi phòng có tên riêng, có hồ sơ riêng, có cách làm việc riêng được ghi thành văn bản. Tôi chỉ nói chuyện với một người duy nhất — tổng điều phối — và người đó phân việc xuống các phòng.

## Bộ nhớ ba tầng

Vấn đề lớn nhất của agent là trí nhớ. Một subagent không tự nhớ được gì sau khi tắt. Nên tôi xây bộ nhớ thành ba tầng. Tầng một là hồ sơ riêng của từng agent: một file ghi nó là ai, làm gì, đã làm được gì, vấp ở đâu. Tầng hai là bộ nhớ chung: những quyết định, quy tắc và bài học mà mọi phòng đều phải biết. Tầng ba là nguồn thật: code trên GitHub, hàng đợi task trên Sheet, dữ liệu trên Drive. Agent không nhớ bằng đầu, agent nhớ bằng file — và file thì không bao giờ quên.

> Chẳng có sự giới hạn nào — mọi thứ liên kết với nhau qua Internet.
>
> — Nguyên tắc thiết kế hệ thống

## Luồng giao tiếp liên tục

Để các agent làm việc khi tôi ngủ, tôi cần một luồng giao tiếp không đứt. Mô hình tôi chọn rất đơn giản: một bảng tính làm hàng đợi task, một máy tính ở nhà chạy 24/7 để nhận task và làm, GitHub làm nơi lưu bằng chứng. Task đi qua đúng sáu trạng thái: chờ, đã nhận, đang làm, xong, lỗi, kẹt. Không có trạng thái thứ bảy. Một task kẹt quá lâu thì tự động được đưa lại hàng đợi để người khác nhận.

Nghe thì đơn giản, nhưng chính sự đơn giản này giữ cho cả hệ thống không rối. Khi có quá nhiều trạng thái, người ta sẽ không biết task đang ở đâu. Khi chỉ có sáu trạng thái, ai nhìn vào bảng cũng biết việc đang ở bước nào.

## Nguyên tắc không giới hạn

Có một nguyên tắc tôi chốt ngay từ đầu: không giới hạn account, không giới hạn nền tảng. Mọi thứ liên kết với nhau qua Internet, và giới hạn thật — quota, chi phí, điều khoản dịch vụ, bảo mật — không phải là tường ngăn mà là tài nguyên cần quản lý bằng sổ sách. Càng nhiều account thì sổ càng phải chặt: mỗi account có quota riêng, ngày reset riêng, ngày hết hạn riêng.

Dĩ nhiên, không giới hạn không có nghĩa là không cẩn thận. Có những đường đi vi phạm điều khoản dịch vụ — ví dụ tự động xoay tài khoản để né giới hạn — thì tôi không đi, dù nó làm được về mặt kỹ thuật. Một hệ thống bền là hệ thống sống được lâu, không phải hệ thống chạy nhanh nhất trong tuần đầu tiên rồi bị khóa hết tài khoản vào tuần thứ hai.

## Kết luận

Xây công ty agent dạy tôi một điều: quản lý AI cũng giống quản lý người. Bạn không cần agent thông minh nhất, bạn cần quy trình rõ nhất: ai làm gì, ghi ở đâu, bàn giao thế nào, sai thì ai chịu trách nhiệm. Khi quy trình đúng, những agent bình thường cũng làm ra kết quả tốt. Khi quy trình sai, agent giỏi nhất cũng chỉ tạo ra mớ hỗn độn nhanh hơn.
