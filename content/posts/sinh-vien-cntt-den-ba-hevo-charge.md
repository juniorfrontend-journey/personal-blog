---
title: 'Từ sinh viên CNTT đến BA hệ thống trạm sạc: những gì tôi học được ở HEVO Charge'
slug: sinh-vien-cntt-den-ba-hevo-charge
date: '2026-11-15'
category: Phân tích nghiệp vụ
excerpt: Hành trình chuyển giao từ tư duy code sang phân tích kiến trúc trạm sạc xe
  điện, giao thức OCPP và trải nghiệm người dùng trạm sạc.
read: 8 phút đọc
hero_image: /images/featured-hop-den.jpg
hero_alt: Kiến trúc hệ thống trạm sạc
hero_caption: 'Một hệ thống trạm sạc nhìn từ phía nghiệp vụ: trụ, cổng, phiên sạc
  và dòng tiền.'
hero_icon: null
hero_label: null
featured_image: null
tags:
- HEVO Charge
- OCPP
- Business Analysis
---

Tôi học CNTT, quen đọc code. Khi bắt đầu làm Business Analyst cho hệ thống trạm sạc HEVO Charge, tôi mang theo đúng thói quen đó: mở mã nguồn ra, dò từng hàm, cố hiểu mọi thứ vận hành ra sao. Và tôi bị ngợp. Một hệ thống sạc xe điện không chỉ có code — nó có trụ sạc ngoài trời, có giao thức OCPP, có tiền giữ, tiền điện, tiền hoàn, có đối tác chia doanh thu, có ngân hàng đối soát. Không ai hiểu hết mọi lớp cùng lúc. Tôi phải học cách làm BA thật sự, và ba bài học dưới đây là những gì ở lại lâu nhất.

## Từ đọc code sang đọc hợp đồng

Bước ngoặt đầu tiên đến khi sếp tôi nói một câu rất ngắn: tài liệu chỉ đặt hợp đồng, cách firmware áp dụng là việc nội bộ của họ. Nghĩa là tôi không cần biết ruột của trụ sạc viết gì. Tôi chỉ cần định nghĩa rõ ranh giới: trụ gửi gì lên server, server trả gì về, sự kiện nào thì phiên sạc bắt đầu, sự kiện nào thì quyết toán. OCPP 1.6 là ngôn ngữ của ranh giới đó — một bản hợp đồng mà cả hai phía đều tuân theo.

Khi tôi thôi cố hiểu ruột máy và chuyển sang vẽ ranh giới, mọi thứ bỗng gọn lại. Một phiên sạc không còn là hàng trăm dòng code nữa. Nó là một chuỗi sự kiện: cắm phích, chọn ổ, quẹt NFC, server tạo phiên, sạc, dừng, quyết toán. Mỗi sự kiện có một thời điểm, một bằng chứng, một trạng thái. Đó là tất cả những gì BA cần nắm.

## Tiền thực chất là dữ liệu

Bài học thứ hai khó hơn, vì nó đụng tới tiền. Trong hệ thống sạc, tiền không phải là một con số ai đó gõ tay vào. Tiền là dữ liệu đi qua một chuỗi biến đổi: cảm biến đo được số điện, số điện thành gói tin MeterValues, gói tin thành kWh, kWh thành tiền theo bảng giá, tiền thành bút toán. Độ đúng của tiền bằng độ đúng của dòng dữ liệu. Sai ở một mắt xích thì sai cả chuỗi.

Vì vậy mỗi khi có lỗi về tiền, tôi không hỏi “số này đúng hay sai” mà hỏi “nó sai ở điểm chuyển giao nào”. Dữ liệu gì đi qua điểm đó, khóa khớp là gì, mất hoặc trùng thì sao, bằng chứng lưu ở đâu. Cách hỏi này tìm ra lỗi nhanh hơn nhiều so với việc rà lại toàn bộ hệ thống.

> Tiền thực chất là dữ liệu — số đo thành MeterValues, thành kWh, thành tiền theo bảng giá, thành bút toán.
>
> — Nguyên tắc dòng tiền HEVO Charge

<!-- Sơ đồ tùy chỉnh (HTML gốc) — đừng sửa trong trình soạn thảo, chỉ sửa bằng code -->
<div class="my-10 p-6 bg-surface-container-lowest border border-surface-container-highest rounded-xl text-center"><span class="block font-label-sm text-label-sm uppercase tracking-wider text-secondary mb-4">Luồng dữ liệu thành tiền</span><div class="flex flex-col sm:flex-row items-center justify-center gap-3 md:gap-4 my-2"><div class="px-4 py-2.5 rounded-lg border border-surface-container-highest bg-surface-container-low text-secondary font-label-md text-label-md w-full sm:w-auto">Cảm biến đo điện</div><span class="material-symbols-outlined text-secondary hidden sm:inline" data-icon="arrow_forward">arrow_forward</span><span class="material-symbols-outlined text-secondary sm:hidden" data-icon="arrow_downward">arrow_downward</span><div class="px-6 py-4 rounded-lg bg-inverse-surface text-inverse-on-surface border border-outline font-headline-sm text-headline-sm font-semibold tracking-wide flex flex-col items-center w-full sm:w-auto"><span>MeterValues</span></div><span class="material-symbols-outlined text-secondary hidden sm:inline" data-icon="arrow_forward">arrow_forward</span><span class="material-symbols-outlined text-secondary sm:hidden" data-icon="arrow_downward">arrow_downward</span><div class="px-4 py-2.5 rounded-lg border border-surface-container-highest bg-surface-container-low text-secondary font-label-md text-label-md w-full sm:w-auto">kWh theo bảng giá</div><span class="material-symbols-outlined text-secondary hidden sm:inline" data-icon="arrow_forward">arrow_forward</span><span class="material-symbols-outlined text-secondary sm:hidden" data-icon="arrow_downward">arrow_downward</span><div class="px-4 py-2.5 rounded-lg border border-surface-container-highest bg-surface-container-low text-secondary font-label-md text-label-md w-full sm:w-auto">Bút toán quyết toán</div></div><p class="font-body-sm text-body-sm text-secondary mt-5 max-w-md mx-auto">Mỗi điểm chuyển giao là một nơi lỗi có thể ẩn nấp — và là nơi bằng chứng phải được lưu lại.</p></div>

## Một khái niệm, một tên

Bài học thứ ba là về từ ngữ. Trong một đợt làm việc, nhóm tôi từng gọi cùng một khoản tiền bằng ba cái tên khác nhau: phí tối thiểu, tiền cọc, tiền giữ. Kết quả là dev hiểu thành ba thứ khác nhau và làm ra ba nhãn khác nhau trên giao diện. Từ đó tôi giữ một quy tắc sắt: một khái niệm tiền chỉ được một tên. Khoản tiền khách phải có trước khi sạc gọi là “Phí tối thiểu”, và chỉ gọi như vậy, ở mọi tài liệu, mọi màn hình, mọi cuộc họp.

Nghe thì nhỏ, nhưng đây là thứ phân biệt một bản đặc tả đọc một lần là hiểu với một bản đặc tả phải hỏi lại ba vòng. Từ ngữ chuẩn không phải là văn hay chữ đẹp. Nó là một hợp đồng: cả người viết lẫn người đọc đều đồng ý rằng từ này chỉ đúng một thứ.

## Kết luận

Làm BA hệ thống trạm sạc dạy tôi rằng công việc của BA không phải là biết nhiều nhất, mà là vẽ ranh giới rõ nhất. Ranh giới giữa hợp đồng và nội bộ. Ranh giới giữa dữ liệu và tiền. Ranh giới giữa một tên gọi và một khái niệm. Vẽ đúng ranh giới thì dev làm đúng, sếp đọc hiểu, và hệ thống chạy được. Đó cũng là lý do tôi viết blog này: ghi lại những ranh giới mình đã vẽ, để lần sau khỏi vẽ lại từ đầu.
