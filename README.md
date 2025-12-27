# Advanced Bridge Finder: Tarjan's Algorithm with Visualization & Verification

## Mô tả

Ứng dụng Python sử dụng **Thuật toán Tarjan** để tìm tất cả các **"cầu"** (bridge edges) trong một đồ thị vô hướng. 

**Cầu** là một cạnh mà khi xóa nó, đồ thị sẽ bị tách thành nhiều thành phần liên thông hơn. Ứng dụng cung cấp:
- **Visualization động**: Hình hoá quá trình DFS theo từng bước
- **Bảng Disc/Low**: Hiển thị giá trị khám phá (disc) và giá trị thấp nhất (low) của mỗi đỉnh
- **Danh sách cầu**: Liệt kê tất cả các cầu tìm được
- **Kiểm chứng BFS**: Xác nhận kết quả bằng cách xóa từng cạnh và đếm thành phần liên thông

## Cài đặt

### Yêu cầu
- Python 3.7+
- tkinter: Tạo giao diện GUI (cửa sổ ứng dụng, nút, text box)
- networkx: Tạo và quản lý đồ thị, cung cấp các hàm đồ thị
- matplotlib: Vẽ và hiển thị đồ thị trực quan trên canvas

### Bước cài đặt
```bash
pip install networkx matplotlib
```

## Cách sử dụng

1. **Chạy chương trình:**
   ```bash
   python main.py
   ```

2. **Nhập dữ liệu:**
   - Nhập cạnh vào trường "Danh sách cạnh" theo định dạng: `đỉnh1 đỉnh2`
   - Mỗi cạnh trên một dòng (ví dụ: `1 2`, `2 3`, `3 4`)
   - Tuỳ chọn: Nhập số đỉnh trong trường "Số đỉnh (Opt)" để thêm đỉnh lẻ

3. **Chạy thuật toán:**
   - Click nút "CHẠY (VISUALIZE)" để bắt đầu
   - Quan sát quá trình DFS:
     - **Vàng**: Đang duyệt đỉnh
     - **Xanh lá**: Đã duyệt xong
     - **Đỏ**: Cạnh là cầu

4. **Xem kết quả:**
   - **Bảng Disc/Low**: Hiển thị `(2025

Phát triển bằng Python, NetworkX, Matplotlib, và Tkinter
