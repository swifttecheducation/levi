#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/styles_library.py — Thư Viện 105 Phong Cách Dựng Video Điện Ảnh (Styles Library Engine).
Kế thừa & tích hợp toàn diện từ Thư viện phong cách Xưởng dựng rảnh tay (siatruong.com).
Bao gồm 10 danh mục:
  [H] Mở đầu thu hút (10 styles)
  [C] Phụ đề an toàn né mặt (9 styles)
  [L] Bố cục chia khung & chiều sâu (9 styles)
  [P] Bằng chứng & Màn hình thực (7 styles)
  [V] Điểm nhấn hình ảnh & Huy hiệu (23 styles)
  [B] Cảnh minh họa động & B-roll (11 styles)
  [X] Hiệu ứng nổi bật (19 styles)
  [M] Chuyển động & Nhịp dựng (7 styles)
  [S] Âm thanh phát sóng (3 styles)
  [G] Màu sắc & Hoàn thiện (7 styles)
Tổng cộng: 105 phong cách.
"""

from typing import Dict, Any, List, Optional


STYLES_DATA: Dict[str, Any] = {
  "updated": "2026-10-19",
  "cats": [
    {
      "id": "H",
      "name": "Mở đầu thu hút",
      "blurb": "1–3 giây đầu tiên. Nội dung xuất hiện đầy đủ ngay từ khung hình đầu.",
      "items": [
        {
          "code": "H1",
          "name": "Tiêu đề lớn sau nhân vật",
          "what": "Dòng chữ trắng nghiêng nhỏ kết hợp tiêu đề vàng lớn viền nâu đậm. Chữ ở phía sau, nhân vật được tách nền và đứng phía trước."
        },
        {
          "code": "H2",
          "name": "Nhãn mở đầu kèm logo",
          "what": "Các nhãn trắng xếp chồng, viền đen dày, tên theo màu thương hiệu và logo tương ứng. Hợp nội dung so sánh."
        },
        {
          "code": "H3",
          "name": "Chữ máy đánh chữ tông ấm",
          "what": "Chữ in hoa màu kem xếp dòng, viền nâu đậm, dòng phụ màu caramel và nhãn emoji. Cảm giác ấm áp, gần gũi."
        },
        {
          "code": "H4",
          "name": "Chữ xếp lớp kiểu sổ lưu niệm",
          "what": "Dòng serif nghiêng mảnh nằm trên từ khóa đậm, tròn. Chữ thường, nhẹ nhàng như trang tạp chí."
        },
        {
          "code": "H5",
          "name": "Hộp tiêu đề trong 3 giây",
          "what": "Một hộp màu phẳng chứa câu mở đầu, biến mất sau 3 giây để trả lại khung hình thoáng."
        },
        {
          "code": "H6",
          "name": "Mở đầu ngay tại nơi có kết quả",
          "what": "Nói câu mở đầu tại chính nơi trải nghiệm diễn ra: chỗ ngồi, phòng chờ hoặc sự kiện. Bối cảnh làm bằng chứng trước khi giải thích."
        },
        {
          "code": "H7",
          "name": "Câu hỏi và logo bật lên",
          "what": "Câu hỏi xuất hiện ngay khung hình đầu, gần mép trên. Logo bật lên cùng lúc khi nhắc tên thương hiệu; chữ rời đi ở lần chuyển cảnh đầu."
        },
        {
          "code": "H8",
          "name": "Nét viết tay và chữ thường đậm",
          "what": "Dòng viết tay nhỏ trên tiêu đề chữ thường đậm, nền vàng phẳng. Video nằm trong thẻ bên dưới, kèm bong bóng bình luận thật."
        },
        {
          "code": "H9",
          "name": "Logo cũ bị gạch, logo mới giữ lại",
          "what": "Hai biểu tượng ứng dụng cạnh nhau ở phía trên. Logo công cụ cũ bị gạch đỏ, công cụ mới giữ nguyên để diễn tả sự thay thế."
        },
        {
          "code": "H10",
          "name": "Tiêu đề phối hai độ đậm",
          "what": "Dòng in hoa đậm phía trên, serif hẹp mảnh phía dưới. Căn giữa từ khung hình đầu và rời đi sau khoảng 3 giây."
        }
      ]
    },
    {
      "id": "C",
      "name": "Phụ đề",
      "blurb": "Cách lời nói xuất hiện trên hình. Luôn tránh khuôn mặt.",
      "items": [
        {
          "code": "C1",
          "name": "Cụm chữ và từ khóa vàng",
          "what": "Chữ như viết tay, hiện theo lời nói. Mỗi cụm có một từ khóa vàng phát sáng."
        },
        {
          "code": "C2",
          "name": "Từng từ đậm nổi bật",
          "what": "Chữ trắng in hoa lớn, hiện từng từ, bóng nhẹ. Nhịp nhanh và dứt khoát."
        },
        {
          "code": "C3",
          "name": "Không phụ đề",
          "what": "Khung hình thoáng, chỉ có tiêu đề và đồ họa. Hợp video nhẹ nhàng hoặc phong cách cao cấp."
        },
        {
          "code": "C4",
          "name": "Chữ nhỏ, từ khóa lớn",
          "what": "Phần lớn chữ thường nhỏ, xen một từ khóa lớn đậm bằng màu nhấn."
        },
        {
          "code": "C5",
          "name": "Cụm chữ và nhãn trắng",
          "what": "Cụm ngắn hiện theo lời nói, một từ khóa nằm trong nhãn trắng. Tối đa hai dòng trong vùng an toàn TikTok, tránh sản phẩm, logo và màn hình."
        },
        {
          "code": "C6",
          "name": "Dòng trắng và câu nhấn vàng",
          "what": "Dòng chữ thường trắng nhỏ, câu nhấn vàng lớn hiện bên dưới qua hiệu ứng mờ. Cả cụm mờ dần khi rời đi."
        },
        {
          "code": "C7",
          "name": "Chữ hoa giãn cách và serif lớn",
          "what": "Dòng in hoa nhỏ giãn chữ, sau đó là từ nhấn serif lớn. Các chữ đi lên qua lớp che; từ cuối có thể nghiêng. Cảm giác tạp chí."
        },
        {
          "code": "C8",
          "name": "Chữ hoa nhỏ dưới cằm",
          "what": "Một dòng in hoa ngắn, nhỏ ngay dưới cằm, giúp giao diện ở phía trên vẫn dễ đọc."
        },
        {
          "code": "C9",
          "name": "Phụ đề bậc thang",
          "what": "Từng từ xuất hiện chéo xuống thành 3–5 dòng rồi nhường chỗ cho cụm sau. Chữ trắng đậm kết hợp từ khóa serif nghiêng xanh nhạt và gạch chân tự vẽ. Tránh khuôn mặt."
        }
      ]
    },
    {
      "id": "L",
      "name": "Bố cục",
      "blurb": "Cách sắp xếp nhân vật và đồ họa trong khung hình.",
      "items": [
        {
          "code": "L1",
          "name": "Tách nhân vật tạo chiều sâu",
          "what": "Nhân vật đứng trước các thẻ, logo và tiêu đề nổi. Phòng phía sau được làm mờ."
        },
        {
          "code": "L2",
          "name": "Chia đôi màn hình",
          "what": "Bằng chứng hoặc cảnh minh họa ở nửa trên, người nói ở nửa dưới. Dùng cắt cảnh trực tiếp."
        },
        {
          "code": "L3",
          "name": "Bố cục sổ lưu niệm",
          "what": "Nền xanh dịu, nhân vật tách nền, các thẻ video viền trắng đặt nghiêng cùng nhãn dán."
        },
        {
          "code": "L4",
          "name": "Toàn khung và đồ họa nổi",
          "what": "Giữ cảnh quay bình thường, đồ họa xuất hiện ở khoảng trống phía trên nhân vật."
        },
        {
          "code": "L5",
          "name": "Dải kể chuyện phía trên",
          "what": "Nhân vật ở hai phần ba dưới; dải trên dành cho trích dẫn, ảnh cũ và bằng chứng. Luôn thấy rõ mặt."
        },
        {
          "code": "L6",
          "name": "Khoảng tường làm bảng chữ",
          "what": "Đặt nhân vật thấp, toàn bộ chữ nằm trên mảng tường trống phía trên đầu. Không đè lên cơ thể."
        },
        {
          "code": "L7",
          "name": "Luân phiên ba bố cục",
          "what": "Đổi giữa chia đôi có bằng chứng phía trên, khuôn mặt kèm từ khóa lớn và bằng chứng toàn màn hình. Chuyển khi sang ý mới."
        },
        {
          "code": "L8",
          "name": "Người kể trong khung ảnh nhỏ",
          "what": "Màn hình công cụ hoặc clip trước chỉnh sửa là nội dung chính. Người nói nằm trong khung ảnh nhỏ nghiêng ở góc, hợp trình bày quy trình."
        },
        {
          "code": "L9",
          "name": "Trước và sau cạnh nhau",
          "what": "Khung Trước nhỏ bên trái, khung Sau lớn bên phải, cùng phát trên nền họa tiết nhẹ và tiêu đề ghi người dựng."
        }
      ]
    },
    {
      "id": "P",
      "name": "Bằng chứng",
      "blurb": "Nguồn thật, màn hình thật để minh chứng cho điều bạn nói.",
      "items": [
        {
          "code": "P1",
          "name": "Bài viết và nét bút đánh dấu",
          "what": "Ảnh chụp bài viết thật phóng tới đúng trích dẫn, bút vàng quét qua, kèm nguồn và ngày."
        },
        {
          "code": "P2",
          "name": "Video demo chính thức",
          "what": "Đoạn 2–5 giây từ video ra mắt của chính đơn vị, có ghi nhãn nguồn."
        },
        {
          "code": "P3",
          "name": "Con số lớn đếm tăng",
          "what": "Con số lớn đếm tăng phía sau đầu khi bạn nhắc tới số liệu."
        },
        {
          "code": "P4",
          "name": "Thẻ bài đăng mạng xã hội",
          "what": "Bài đăng thật từ X, Threads hoặc LinkedIn xuất hiện dưới dạng thẻ nổi."
        },
        {
          "code": "P6",
          "name": "Tư liệu cá nhân",
          "what": "Video và ảnh cũ thật của bạn xuất hiện đúng lời kể: những video đầu, đội nhóm, sự kiện. Tạo kết nối bằng câu chuyện thật."
        },
        {
          "code": "P7",
          "name": "Con trỏ chỉ bằng chứng",
          "what": "Quay màn hình công cụ hoặc bảng thật, con trỏ chỉ đúng con số, có nhãn nguồn nhỏ."
        },
        {
          "code": "P8",
          "name": "Chỉ tay vào màn hình",
          "what": "Dùng điện thoại quay máy tính, ngón tay chỉ số dư hoặc kết quả thật trên màn hình."
        }
      ]
    },
    {
      "id": "V",
      "name": "Điểm nhấn hình ảnh",
      "blurb": "Hình ảnh giải thích hoặc minh chứng cho lời nói. Không cần thêm vào mọi câu.",
      "items": [
        {
          "code": "V1",
          "name": "Logo kèm vai trò",
          "what": "Logo chính thức bật lên đúng từ được nói, kèm nhãn vai trò ngắn như suy luận, hình ảnh hoặc âm nhạc."
        },
        {
          "code": "V2",
          "name": "Logo nối bằng mũi tên",
          "what": "Mũi tên được vẽ giữa các logo để thể hiện quan hệ hoặc chuyển đổi công cụ."
        },
        {
          "code": "V3",
          "name": "Một từ lớn đậm",
          "what": "Một từ hoặc cụm ngắn lớn xuất hiện ở câu hỏi hay điểm nhấn, như “Tại sao?” hoặc “Bất ngờ chưa”."
        },
        {
          "code": "V4",
          "name": "Đổi logo liên tiếp",
          "what": "Các logo thay nhanh trong cùng vị trí trước khi cụm chữ chính xuất hiện."
        },
        {
          "code": "V5",
          "name": "Xếp chồng thẻ so sánh",
          "what": "Thẻ sản phẩm lần lượt xếp chồng, kèm giá và đối tượng phù hợp."
        },
        {
          "code": "V6",
          "name": "Từ khóa chốt toàn khung",
          "what": "Một từ đậm cực lớn phủ ngang khung hình ở thời điểm chốt ý."
        },
        {
          "code": "V7",
          "name": "Thẻ chữ chuyển động",
          "what": "Câu toàn màn hình được dựng từng từ, xen biểu tượng emoji."
        },
        {
          "code": "V8",
          "name": "Thẻ trích dẫn",
          "what": "Khi trích lời người khác, nội dung được gõ vào dải trên, đặt trong dấu ngoặc kép."
        },
        {
          "code": "V9",
          "name": "Chuỗi cảnh đời thực",
          "what": "Chuyển toàn màn hình sang các clip sự kiện hoặc đời sống thật ở đoạn giàu cảm xúc."
        },
        {
          "code": "V10",
          "name": "Giao diện tài trợ phẳng",
          "what": "Luồng tương tác với nhà tài trợ được minh họa bằng thẻ đơn giản: bình luận, tin nhắn, email. Không phát sáng hay 3D."
        },
        {
          "code": "V11",
          "name": "Tiêu đề theo tiến trình",
          "what": "Tiêu đề cố định cập nhật theo danh sách hoặc từng nấc, giúp người xem biết đang đến đâu."
        },
        {
          "code": "V12",
          "name": "Logo bật sáng nhẹ",
          "what": "Logo và tên thương hiệu bật lên với quầng trắng dịu, nảy nhẹ và vệt sáng quét qua, kèm âm thanh hé lộ. Không đặt trong thẻ."
        },
        {
          "code": "V13",
          "name": "Đồng hồ vòng kiểu iOS",
          "what": "Vòng đếm mờ kính ở khoảng trống giữa khung hình, đếm tới số được nói trong khoảng 2 giây rồi biến mất."
        },
        {
          "code": "V14",
          "name": "Lịch lật năm",
          "what": "Ô lịch trắng kiểu iOS bật lên, lật về năm cũ khi nhảy thời gian. Cho hiệu ứng một khoảng riêng, không che người."
        },
        {
          "code": "V15",
          "name": "Thông báo iPhone",
          "what": "Dải thông báo kiểu iOS trượt xuống với nội dung vừa nói. Giữ gọn trong vùng an toàn."
        },
        {
          "code": "V16",
          "name": "Ô Trung tâm điều khiển",
          "what": "Các ô Wi-Fi và Điện thoại kiểu iPhone tắt đi đúng lời nói như “không mạng, không điện thoại”."
        },
        {
          "code": "V17",
          "name": "Lời mời bình luận chuyển sắc",
          "what": "Thẻ trắng có vòng màu Instagram bật lên ngay trước từ khóa. Gõ “Bình luận”, sau đó hiện từ khóa chuyển sắc lớn và giữ lại."
        },
        {
          "code": "V18",
          "name": "Ảnh chuyến đi kiểu Polaroid",
          "what": "Ảnh thật từ chuyến đi hoặc sự kiện rơi vào khung hình, kèm chớp sáng và tiếng màn trập."
        },
        {
          "code": "V19",
          "name": "Minh họa bình luận và theo dõi",
          "what": "Màn hình Instagram tối phía trước ngực: gõ từ khóa, đăng bình luận kèm tim, rồi chuyển sang hồ sơ và nhấn Theo dõi."
        },
        {
          "code": "V20",
          "name": "Bộ đếm theo danh sách",
          "what": "Tên chuỗi cố định phía trên, kèm bộ đếm như 01/10 trên nhãn vàng lớn của từng mục."
        },
        {
          "code": "V21",
          "name": "Ghi chú viết tay và mũi tên",
          "what": "Ghi chú nhỏ như “trước” cùng mũi tên vẽ tay chỉ vào thẻ, như đang tự chú thích tác phẩm."
        },
        {
          "code": "V22",
          "name": "Dòng bình luận ghim",
          "what": "Một dòng viết tay nhỏ được ghim ở đầu suốt video để lời mời hành động xuất hiện ngay từ giây đầu."
        },
        {
          "code": "V23",
          "name": "Lưới kết quả",
          "what": "Hai hàng kết quả “Video mới” và “Clip gốc” đổi mỗi giây, cho thấy nhiều ví dụ khác nhau."
        }
      ]
    },
    {
      "id": "B",
      "name": "Cảnh minh họa động",
      "blurb": "Tái hiện thao tác ứng dụng. Thay toàn bộ dữ liệu riêng tư trước khi dùng.",
      "items": [
        {
          "code": "B1",
          "name": "Tin nhắn hỏi và trả lời",
          "what": "Tin nhắn được gõ rồi gửi; câu trả lời của bot hiện dần."
        },
        {
          "code": "B2",
          "name": "Nhóm trò chuyện giữa các bot",
          "what": "Các bot nói chuyện với tên, ảnh đại diện và lượt nhắc @."
        },
        {
          "code": "B3",
          "name": "Từ chat sang lịch",
          "what": "Nhấn liên kết, mở Google Calendar và thêm sự kiện."
        },
        {
          "code": "B4",
          "name": "Từ chat qua Drive tới Sheets",
          "what": "Nhấn liên kết, mở Drive rồi các hàng bảng tính lần lượt hiện lên."
        },
        {
          "code": "B5",
          "name": "Nhóm chat iPhone",
          "what": "Cuộc trò chuyện kiểu iMessage trong khung iPhone."
        },
        {
          "code": "B6",
          "name": "Nhấn ứng dụng trên Dock",
          "what": "Phóng vào thanh Dock, nhấn biểu tượng, ứng dụng nảy lên rồi mở."
        },
        {
          "code": "B7",
          "name": "Thông báo tin nhắn",
          "what": "Ảnh đại diện xuất hiện kèm tiếng báo, bong bóng lời thoại bật trên cảnh quay."
        },
        {
          "code": "B8",
          "name": "Nhãn logo ứng dụng",
          "what": "Nhãn kính tối bo tròn chứa biểu tượng, tên ứng dụng, logo đơn vị phát triển và vệt sáng quét."
        },
        {
          "code": "B9",
          "name": "Giới thiệu nhân vật",
          "what": "Các gương mặt bật lên thành hàng, kèm nhãn tên."
        },
        {
          "code": "B10",
          "name": "Sơ đồ giải thích",
          "what": "Sơ đồ động đơn giản minh họa khái niệm, như máy tính đám mây hoặc các tài khoản kết nối."
        },
        {
          "code": "B11",
          "name": "Hé lộ logo điện ảnh",
          "what": "Tư liệu chính thức được quay chậm, chỉnh màu và kết hợp logo trượt vào."
        }
      ]
    },
    {
      "id": "X",
      "name": "Hiệu ứng nổi bật",
      "blurb": "Điểm nhấn ngắn khoảng một giây. Mỗi ý một hiệu ứng, tránh chồng lớp.",
      "items": [
        {
          "code": "X1",
          "name": "Thẻ video bay quanh người",
          "what": "Các thẻ màn hình bo tròn từ REEL khác bay vòng, đi cả sau và trước nhân vật đã tách nền."
        },
        {
          "code": "X2",
          "name": "Bức tường nội dung",
          "what": "Tường phía sau phủ ảnh thu nhỏ, bài đăng và ảnh chụp màn hình cũ. Nhân vật được tách nền ở phía trước."
        },
        {
          "code": "X3",
          "name": "Bước vào giao diện AI",
          "what": "Thay nền bằng ứng dụng chat trắng ngà. Thanh yêu cầu gõ nội dung ngay trên đầu bạn."
        },
        {
          "code": "X4",
          "name": "Bước ra khỏi khung",
          "what": "Cảnh quay thu nhỏ trong khung điện thoại bo tròn, nền tối mờ. Cơ thể vượt khỏi mép khung tạo cảm giác nổi 3D."
        },
        {
          "code": "X5",
          "name": "Phóng gần kỹ thuật số",
          "what": "Phóng nhanh từ toàn cảnh vào khuôn mặt đúng từ khóa, tối nhẹ góc ảnh. Chuyển dứt khoát, không làm mờ."
        },
        {
          "code": "X6",
          "name": "Điện thoại trượt vào",
          "what": "Mô hình điện thoại tối trượt từ mép vào cạnh nhân vật. Danh sách bước được điền rồi nút vàng chuyển thành “Xong”."
        },
        {
          "code": "X7",
          "name": "Danh sách lần lượt đánh dấu",
          "what": "Thẻ tối nhỏ ở mảng tường cạnh đầu. Ba bước lần lượt có dấu tích xanh theo lời nói."
        },
        {
          "code": "X8",
          "name": "Bức tường tiêu đề",
          "what": "Giấy ghi chú, thẻ trích dẫn và mẩu thanh tìm kiếm dán lên tường quanh đầu, hơi nghiêng, mỗi nhịp một mẩu."
        },
        {
          "code": "X9",
          "name": "Chuyển cảnh xuyên vùng tối",
          "what": "Máy quay lao vào vùng tối như áo khoác hay bóng đổ, màn hình đen rồi mở ra cảnh tiếp theo."
        },
        {
          "code": "X10",
          "name": "Biểu đồ vươn lên",
          "what": "Đường biểu đồ phát sáng được vẽ sau lưng, rồi vọt lên vàng neon ở con số chốt, để lại vệt sáng."
        },
        {
          "code": "X11",
          "name": "Lùi ra để lộ cửa sổ AI",
          "what": "Cảnh quay lùi ra, cho thấy video đang nằm trong cửa sổ AI Agent, cạnh danh sách tác vụ được đánh dấu và thanh kết xuất đang chạy."
        },
        {
          "code": "X12",
          "name": "Hai góc quay cùng lúc",
          "what": "Bạn ở dưới, phía trên là thẻ tối nhỏ chiếu cùng lượt quay từ góc khác, như một màn hình phía sau."
        },
        {
          "code": "X13",
          "name": "Nhân vật cắt giấy",
          "what": "Nhân vật viền trắng trên nền giấy xé ghép lớp, chữ cắt dán, nét sáp màu và băng dính."
        },
        {
          "code": "X14",
          "name": "Nét vẽ tay rung nhẹ",
          "what": "Viền trắng vẽ tay quanh nhân vật rung biến đổi từng khung hình. Tim và tia sáng vẽ tay bật gần đầu."
        },
        {
          "code": "X15",
          "name": "Hiệu ứng chóng mặt",
          "what": "Dolly zoom: nhân vật giữ nguyên kích thước trong khi căn phòng phía sau co giãn. Dùng ở câu hé lộ."
        },
        {
          "code": "X16",
          "name": "Trang bìa tạp chí",
          "what": "Khung hình thành bìa tạp chí: tên báo serif lớn mảnh sau đầu, tiêu đề phụ nhỏ ở góc và dòng nghiêng bên dưới."
        },
        {
          "code": "X17",
          "name": "Chữ kính mờ",
          "what": "Từ khổng lồ bằng kính mờ nằm sau đầu, khúc xạ hình căn phòng qua chữ."
        },
        {
          "code": "X18",
          "name": "Thẻ hình lật",
          "what": "Trong khung Sau, các thẻ kem lần lượt lật. Mỗi thẻ có một vật 3D bóng và nhãn serif: máy chữ cho phụ đề, máy quay cho cảnh minh họa, cuộn phim cho hoạt họa."
        },
        {
          "code": "X19",
          "name": "Màn hình trong phòng tối",
          "what": "Video giải thích phát trên màn hình trong phòng tối, bàn phím sáng, hình nét đơn giản và tiêu đề serif cố định bên dưới."
        }
      ]
    },
    {
      "id": "M",
      "name": "Chuyển động và nhịp dựng",
      "blurb": "Cách video chuyển cảnh, phóng gần và giữ nhịp.",
      "items": [
        {
          "code": "M1",
          "name": "Cắt cảnh phóng gần",
          "what": "Cắt trực tiếp kết hợp đổi cỡ khung ở đầu câu để hình ảnh liên tục thay đổi."
        },
        {
          "code": "M2",
          "name": "Chuyển cảnh phóng mờ",
          "what": "Phóng nhanh và làm mờ khi vào hoặc ra cảnh chèn, kèm vệt sáng ấm dịu."
        },
        {
          "code": "M3",
          "name": "Đổi hình nhanh",
          "what": "Cứ 2–3 giây có hình mới, không lặp cùng thủ pháp hai lần liên tiếp."
        },
        {
          "code": "M4",
          "name": "Chậm và tĩnh",
          "what": "Ít cắt, phóng chậm, có khoảng thở. Ít đồ họa hơn nhưng rõ điểm nhấn."
        },
        {
          "code": "M5",
          "name": "Cắt nhảy hai cỡ khung",
          "what": "Một lượt quay, luân phiên toàn và cận ở mỗi câu, cắt gọn khoảng dừng. Chỉ dùng cắt trực tiếp."
        },
        {
          "code": "M6",
          "name": "Phóng lấy mặt làm tâm",
          "what": "Câu nhấn ngắn phóng nhanh 115–120%; câu dài phóng chậm rồi lùi nhẹ. Luôn lấy mặt làm tâm."
        },
        {
          "code": "M7",
          "name": "Chuyển cảnh vòng tròn màu",
          "what": "Vòng tròn màu thương hiệu mở rộng từ thẻ để chuyển sang phần tiếp theo. Gọn, không làm mờ."
        }
      ]
    },
    {
      "id": "S",
      "name": "Âm thanh",
      "blurb": "Phối âm khoảng −14 LUFS, luôn để giọng nói nổi rõ hơn.",
      "items": [
        {
          "code": "S1",
          "name": "Âm thanh cho từng đồ họa",
          "what": "Tiếng bật, lướt, tích và nhấn theo từng hình, luôn nhỏ hơn giọng nói."
        },
        {
          "code": "S2",
          "name": "Hiệu ứng âm thanh nhẹ",
          "what": "Chỉ thêm hiệu ứng ở những điểm nhấn lớn."
        },
        {
          "code": "S3",
          "name": "Nhạc nền",
          "what": "Nhạc nhỏ dưới giọng nói. Chỉ dùng nhạc bạn có quyền sử dụng."
        }
      ]
    },
    {
      "id": "G",
      "name": "Màu sắc và hoàn thiện",
      "blurb": "Diện mạo và tông màu chung của video.",
      "items": [
        {
          "code": "G1",
          "name": "Điện ảnh tông ấm",
          "what": "Chỉnh màu ấm nhẹ, tối góc, làm mờ phòng phía sau các thẻ."
        },
        {
          "code": "G2",
          "name": "Sáng và gọn",
          "what": "Mảng trắng dịu, thanh màu nhấn mảnh, không emoji hay huy hiệu."
        },
        {
          "code": "G3",
          "name": "Xanh pastel nhẹ",
          "what": "Nền xanh pastel kèm nhãn dán vui mắt."
        },
        {
          "code": "G4",
          "name": "Gọn kiểu Apple",
          "what": "Thẻ iOS trắng, kính mờ, SF Pro và bóng dịu. Mỗi nhịp một màn hình; không chữ phát sáng, dấu đóng hay neon."
        },
        {
          "code": "G5",
          "name": "Tông ấm dịu cá tính",
          "what": "Màu nâu ấm nhẹ, chữ kem, một câu chốt serif nghiêng vàng bơ và ánh lấp lánh. Hợp hiệu ứng thẻ bay quanh người."
        },
        {
          "code": "G6",
          "name": "Tạp chí tông lạnh",
          "what": "Phòng tối hơn, nhân vật vẫn sáng. Tông xanh cổ vịt, tối góc, không hạt. Đan xen toàn cảnh và cận như phỏng vấn studio."
        },
        {
          "code": "G7",
          "name": "Nền vàng phẳng",
          "what": "Toàn video trên nền vàng bơ phẳng, chữ trắng và thẻ viền trắng. Tạo diện mạo nhận biết cho cả chuỗi."
        }
      ]
    }
  ]
}


CURATED_PRESETS: Dict[str, Dict[str, Any]] = {
    "editorial_luxe": {
        "name": "Tạp Chí Sang Trọng (Editorial Luxe)",
        "codes": ["H4", "C7", "L1", "X16", "M4", "S1", "G6"],
        "description": "Chữ serif cổ điển, bố cục chiều sâu tách nền, trang bìa tạp chí, nhịp dựng điềm tĩnh."
    },
    "apple_minimal": {
        "name": "Tối Giản Công Nghệ (Apple Minimal)",
        "codes": ["H10", "C8", "L4", "V15", "X6", "M1", "S1", "G4"],
        "description": "Thẻ iOS trắng kính mờ, SF Pro, chữ dưới cằm, trượt điện thoại, chuyển động dứt khoát chuẩn Apple."
    },
    "hands_off_reels": {
        "name": "Xưởng Dựng Rảnh Tay (Hands-Off Reels Triệu View)",
        "codes": ["H1", "C1", "L2", "V1", "X5", "M6", "S1", "G1"],
        "description": "Tiêu đề sau nhân vật, từ khóa vàng phát sáng, chia đôi bằng chứng, phóng gần lấy mặt làm tâm."
    },
    "viral_storyteller": {
        "name": "Kể Chuyện Truyền Cảm Hứng (Viral Storyteller)",
        "codes": ["H6", "C9", "L5", "P1", "V18", "X10", "M3", "S1", "G5"],
        "description": "Mở đầu tại nơi có kết quả, phụ đề bậc thang, dải kể chuyện trên, ảnh polaroid, biểu đồ vọt lên."
    },
    "gen_z_pop": {
        "name": "Năng Động Bùng Nổ (Gen Z Pop)",
        "codes": ["H8", "C2", "L3", "V7", "X14", "M1", "S1", "G3"],
        "description": "Nét viết tay trên nền phẳng, từng từ đậm nổi bật, sổ lưu niệm, viền vẽ tay rung nhẹ, nhịp nhanh."
    }
}


class StylesLibrary:
    def __init__(self):
        self.data = STYLES_DATA
        self.by_code: Dict[str, Dict[str, Any]] = {}
        self.by_cat: Dict[str, Dict[str, Any]] = {}
        for cat in self.data.get("cats", []):
            self.by_cat[cat["id"]] = cat
            for item in cat.get("items", []):
                item_copy = item.copy()
                item_copy["cat_id"] = cat["id"]
                item_copy["cat_name"] = cat["name"]
                self.by_code[item["code"]] = item_copy

    @property
    def total_count(self) -> int:
        return len(self.by_code)

    def get_style(self, code: str) -> Optional[Dict[str, Any]]:
        return self.by_code.get(code.upper().strip())

    def list_categories(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": cat["id"],
                "name": cat["name"],
                "blurb": cat.get("blurb", ""),
                "count": len(cat.get("items", []))
            }
            for cat in self.data.get("cats", [])
        ]

    def get_styles_in_category(self, cat_id: str) -> List[Dict[str, Any]]:
        cat = self.by_cat.get(cat_id.upper().strip())
        return cat.get("items", []) if cat else []

    def search_styles(self, keyword: str) -> List[Dict[str, Any]]:
        kw = keyword.lower().strip()
        results = []
        for code, item in self.by_code.items():
            if (kw in code.lower() or
                kw in item["name"].lower() or
                kw in item["what"].lower() or
                kw in item["cat_name"].lower()):
                results.append(item)
        return results

    def compose_mix_prompt(self, codes: List[str]) -> str:
        valid_items = [self.by_code[c.upper().strip()] for c in codes if c.upper().strip() in self.by_code]
        if not valid_items:
            return ""

        lines = ["Dựng video của tôi theo các phong cách sau:"]
        for it in valid_items:
            lines.append(f"- {it['code']} {it['name']}: {it['what']}")

        lines.append("\nCắt các khoảng im lặng. Giữ nội dung trong vùng an toàn TikTok và Reels, không che khuôn mặt. Cho tôi xem kế hoạch trước khi dựng.")
        return "\n".join(lines)

    def get_preset(self, preset_key: str) -> Optional[Dict[str, Any]]:
        return CURATED_PRESETS.get(preset_key.lower().strip())

    def list_presets(self) -> Dict[str, Dict[str, Any]]:
        return CURATED_PRESETS
