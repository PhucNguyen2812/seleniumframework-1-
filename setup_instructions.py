import os

project_dir = r"c:\Users\TonyTonyChopper\Desktop\lab_9.7"

def write(path, content):
    full_path = os.path.join(project_dir, path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

write("HuongDan_ChamDiem_Bai1.txt", """Hướng dẫn test và chụp kết quả Bài 1 (1.5 điểm) - GitHub Actions CI/CD cơ bản
--------------------------------------------------------------------------------
1. Yêu cầu 1: Pipeline chạy thành công (Log màu xanh)
   - Đẩy (push) code mới nhất lên branch 'main' của repository trên GitHub.
   - Truy cập vào tab 'Actions' trên repository của bạn.
   - Nhấp vào workflow "Selenium Test Suite" đang chạy.
   - Đợi đến khi workflow hoàn thành xuất hiện dấu tick màu xanh lá (Success).
   => **Chụp ảnh 1**: Màn hình tổng quan của tab Actions hiển thị dấu tick màu xanh của job vừa chạy.

2. Yêu cầu 2: Pipeline thất bại khi test sai (Log màu đỏ)
   - Mở một file test bất kỳ (ví dụ: LoginTest.java) và cố tình sửa sai 1 assertion (VD: Assert.assertEquals(1, 2);).
   - Push code lên GitHub.
   - Vào lại tab 'Actions', đợi workflow chạy xong và báo lỗi màu đỏ (Failed).
   => **Chụp ảnh 2**: Màn hình Actions hiển thị dấu tích chéo màu đỏ báo job thất bại.

3. Yêu cầu 3: Xem ảnh chụp màn hình trong log artifact
   - Mở log của job bị fail (bước 2), cuộn xuống cuối phần 'Artifacts'.
   - Nhấp vào 'test-results-chrome' (hoặc artifact tương ứng) để tải về.
   - Giải nén file zip, mở thư mục 'target/screenshots' và mở ảnh chụp lỗi.
   => **Chụp ảnh 3**: Màn hình mở ảnh screenshot chứng minh test fail được lưu thành công trong artifact.
""")

write("HuongDan_ChamDiem_Bai2.txt", """Hướng dẫn test và chụp kết quả Bài 2 (1.0 điểm) - Matrix Strategy
--------------------------------------------------------------------------------
1. Yêu cầu 1: Hai job Chrome và Firefox chạy song song
   - Đảm bảo file .github/workflows/selenium-ci.yml đã thêm cấu trúc 'matrix: browser: [chrome, firefox]'.
   - Push code lên GitHub và truy cập tab 'Actions'.
   - Nhấp vào workflow đang chạy. Bạn sẽ thấy ở cột bên trái xuất hiện 2 job: 'run-tests (chrome)' và 'run-tests (firefox)' hoặc tương tự.
   => **Chụp ảnh 1**: Màn hình hiển thị cả 2 job Chrome và Firefox đang chạy cùng một lúc (In progress).

2. Yêu cầu 2: Ghi nhận thời gian so sánh
   - Mở log của một lần chạy chỉ có Chrome (trước khi thêm matrix) hoặc xem log file cũ. Ghi lại thời gian hoàn thành.
   - Mở log của lần chạy dùng matrix (cả Chrome và Firefox). Ghi lại thời gian hoàn thành.
   - Tạo một bảng hoặc note nhỏ ghi chú so sánh thời gian.
   => **Chụp ảnh 2**: Bảng so sánh thời gian chạy tuần tự vs song song minh chứng được việc dùng Strategy giúp tiết kiệm thời gian CI.
""")

write("HuongDan_ChamDiem_Bai3.txt", """Hướng dẫn test và chụp kết quả Bài 3 (1.0 điểm) - GitHub Secrets
--------------------------------------------------------------------------------
1. Yêu cầu 1: Không có hardcode password trong code (Lệnh grep)
   - Mở Terminal (Bash/PowerShell) tại thư mục project trên máy tính của bạn.
   - Chạy lệnh: grep -r 'secret_sauce' src/ (nếu dùng PowerShell: Select-String -Path "src\*" -Pattern "secret_sauce" -Recurse)
   - Đảm bảo kết quả trả về là rỗng (không tìm thấy gì).
   => **Chụp ảnh 1**: Màn hình console hiển thị lệnh tìm kiếm và trả về kết quả rỗng (không có password trong file code).

2. Yêu cầu 2: Logs Pipeline ẩn mật khẩu qua variable
   - Trên GitHub, vào tab 'Settings' > 'Secrets and variables' > 'Actions', tạo 2 Repository secrets: SAUCEDEMO_USERNAME và SAUCEDEMO_PASSWORD.
   - Chạy tab Actions, mở mục 'Run Selenium Tests' để xem log chi tiết.
   - Bạn sẽ thấy giá trị của thư mục biến môi trường đã được che lại bằng dấu '***'.
   => **Chụp ảnh 2**: Ảnh chụp log của Actions hiển thị APP_PASSWORD=*** thay vì password thật.
""")

write("HuongDan_ChamDiem_Bai4.txt", """Hướng dẫn test và chụp kết quả Bài 4 (2.0 điểm) - Selenium Grid với Docker
--------------------------------------------------------------------------------
1. Yêu cầu 1: 3 node đăng ký thành công trên Hub
   - Mở Terminal, gõ lệnh: docker-compose up -d
   - Mở trình duyệt truy cập: http://localhost:4444
   - Chuyển sang tab 'Nodes' (nếu có) trên Grid UI, bạn sẽ thấy 2 node Chrome và 1 node Firefox hiển thị trạng thái Ready.
   => **Chụp ảnh 1**: Màn hình Selenium Grid UI (http://localhost:4444) hiển thị 3 Node đang online.

2. Yêu cầu 2: Các session chạy đồng thời
   - Mở một Terminal khác, chạy lệnh: mvn test -Dgrid.url=http://localhost:4444 -DsuiteXmlFile=testng-grid.xml
   - Nhanh chóng quay lại tab trình duyệt http://localhost:4444, ở phần Session UI sẽ thấy nhiều ô vuông có chữ Chrome màu xám chuyển sang trạng thái đang chạy (Active 4 session).
   => **Chụp ảnh 2**: Màn hình Grid UI (http://localhost:4444) hiển thị 4 session đang hoạt động đồng thời (có logo Chrome/Firefox).

3. Yêu cầu 3: Bảng so sánh tiến độ thời gian
   - Chạy test local bình thường qua Maven và ghi lại thời gian hoàn thành (Ví dụ: thread-count=1).
   - Chạy Grid qua 2 thread và 4 thread, ghi lại thời gian.
   - Điền vào file Word bảng kết quả chi tiết.
   => **Chụp ảnh 3**: Hình chụp bảng thời gian đo được từ việc sử dụng các hệ số tăng tốc Grid tuần tự và song song.
""")

write("HuongDan_ChamDiem_Bai5.txt", """Hướng dẫn test và chụp kết quả Bài 5 (1.0 điểm) - Allure Report
--------------------------------------------------------------------------------
1. Yêu cầu: Xem Allure Report giao diện đầy đủ
   - Chạy các test case local: mvn clean test
   - Chạy lệnh render report Allure: mvn allure:serve
   - Trình duyệt sẽ tự động mở trang web giao diện Allure Report (localhost:X).
   - Kiểm tra các phần:
      + Biểu đồ tổng quan (Overviews chart: Pass/Fail)
      + Tính năng step-by-step (Click vào một test case để xem chi tiết từng Step log)
      + Xem ảnh đính kèm: Click vào một test case bị FAIL (tạo lỗi cố ý như ở bài 1), mở rộng phần 'Teardown' hoặc 'Attachments' sẽ thấy ảnh chụp.
   => **Chụp ảnh 1**: Màn hình tổng quan biểu đồ Allure Report có Pass và Fail.
   => **Chụp ảnh 2**: Màn hình chi tiết một test case showing các Step by step và file Screenshot đính kèm (cho test fail).
""")

write("HuongDan_ChamDiem_Bai6.txt", """Hướng dẫn test và chụp kết quả Bài 6 (1.5 điểm) - Allure trên GitHub Pages
--------------------------------------------------------------------------------
1. Yêu cầu 1: Report hiển thị thành công trên Github Pages
   - Vào Settings repository > Pages > Gán Source deploy vào nhánh 'gh-pages', chọn Save.
   - Đợi Actions tab có job deploy pages thành công (màu xanh).
   - Mở trình duyệt truy cập URL Github Pages của bạn, dạng 'https://<username>.github.io/<tên-repo>/'.
   => **Chụp ảnh 1**: Màn hình trình duyệt hiển thị giao diện cấu trúc của trang Allure Report với đường dẫn URL là từ domain github.io.

2. Yêu cầu 2: README.md có Github Badge
   - Vào trang chủ repository của bạn (chuyển sang tab Code).
   - Cuộn xuống phần preview file README.md, nhìn thấy 2 badge (Test Status xanh hoặc đỏ, và Allure Report).
   => **Chụp ảnh 2**: Ảnh chụp giao diện Github Repository hiển thị file README có chứa 2 nút Badge.
""")

write("HuongDan_ChamDiem_Bai7.txt", """Hướng dẫn test và chụp kết quả Bài 7 (2.0 điểm) - Test Strategy và Test Plan
--------------------------------------------------------------------------------
1. Yêu cầu: Viết Test Strategy & Plan thực tế
   - Sinh viên cần nộp một tài liệu Word (hoặc PDF) trình bày chi tiết văn bản Chiến lược.
   - Mục tài liệu cần phải bao gồm đầy đủ:
      1. Phạm vi kiểm thử (Scope có liệt kê các module In / Out)
      2. Tỉ lệ và phân loại Automation Test.
      3. Definition of Done (DoD).
      4. Bảng quản lý rủi ro thực tiễn sprint.
      5. Lịch trình thời gian kiểm thử Pipeline.
      6. Phân tích rủi ro Test Case Thanh Toán (Liệt kê 5 Blockers)
      7. Bảng thiết kế 15 Test Case có đầy đủ TC-ID, Priority, Expected Result.
   => **Cách nộp 1**: Xuất nội dung tài liệu thành dạng file PDF để nộp cho giáo viên (nên đặt tên: Lab11_MSSV_TestPlan.pdf). Không áp dụng ảnh chụp.
""")

print("Done creating instruction files!")
