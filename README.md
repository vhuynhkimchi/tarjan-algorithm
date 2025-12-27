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
   - **Bảng Disc/Low**: Hiển thị `(Đỉnh, Disc, Low, Cha)`
   - **Danh sách Cầu**: Liệt kê tất cả cầu tìm được
   - **Các bước DFS**: Log chi tiết quá trình
   - **Kiểm chứng**: Xác nhận kết quả qua BFS

5. **Làm mới:**
   - Click "Reset" để xóa dữ liệu và bắt đầu lại

## Thuật toán Tarjan

### Nguyên lý
Thuật toán Tarjan sử dụng DFS để tìm cầu:
- **disc[u]**: Thời điểm khám phá đỉnh u
- **low[u]**: Giá trị disc thấp nhất có thể đạt được từ cây con của u
- **Cầu**: Cạnh (u,v) là cầu nếu `low[v] > disc[u]` (không thể quay lại u từ cây con của v)

### Các bước chính
1. Khởi tạo disc, low, parent cho tất cả đỉnh
2. Duyệt DFS từ mỗi đỉnh chưa thăm
3. Khi gặp cạnh ngược, cập nhật `low[u] = min(low[u], disc[v])`
4. Khi quay lui, kiểm tra `low[v] > disc[u]` để xác định cầu

### Độ phức tạp
- **Thời gian**: O(V + E) - duyệt mỗi đỉnh và cạnh một lần
- **Không gian**: O(V) - lưu disc, low, parent

## Ví dụ

**Input:**
```
1 2
1 3
2 3
3 4
4 5
4 6
5 6
```

**Output:**
```
Đỉnh: 6 | Cạnh: 7 | Cầu tìm thấy: 1
Cầu: 3 - 4
```

Giải thích: Cạnh (3,4) là cầu vì nó là cách duy nhất kết nối nhóm {1,2,3} với nhóm {4,5,6}.

## Cấu trúc code

| Hàm | Mục đích |
|-----|---------|
| `run_tarjan_visual(G, pos)` | Chạy thuật toán Tarjan với visualization |
| `dfs(u)` | Hàm DFS đệ quy trong Tarjan |
| `update_canvas_step()` | Cập nhật vẽ đồ thị sau mỗi bước |
| `verify_bridges_with_bfs()` | Xác nhận cầu bằng cách xóa cạnh |
| `start_processing()` | Xử lý nhập liệu và chạy thuật toán |
| `clear_all()` | Làm mới giao diện |
| `main()` | Tạo giao diện GUI với Tkinter |

## Tùy chỉnh

- **Tốc độ animation**: Thay đổi biến `ANIMATION_SPEED` (đơn vị: giây)
- **Vị trí đồ thị**: Sửa tham số `seed` trong `nx.spring_layout()`
- **Màu sắc**: Chỉnh sửa giá trị trong `node_colors` và `edge_colors`

## Lưu ý

- Ứng dụng hỗ trợ đồ thị vô hướng không có cạnh song song
- Cạnh được nhập theo định dạng `đỉnh1 đỉnh2` (cách nhau bởi khoảng trắng)
- Visualization chỉ hoạt động tốt với đồ thị có ≤ 20 đỉnh

## Tác giả
Sinh viên: Võ Huỳnh Kim Chi
MSSV: 65130306
Thời gian hoàn thành: Tháng 12/2025
Phát triển bằng Python, NetworkX, Matplotlib, và Tkinter
