from typing import Iterator, Callable

def log_line_generator(filepath: str) -> Iterator[str]:
    """Generator: yield từng dòng trong file log lớn."""
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.rstrip('\n')

def filter_error(lines: Iterator[str]) -> Iterator[str]:
    """Chỉ yield các dòng chứa 'ERROR'."""
    return (line for line in lines if 'ERROR' in line)

def transform(lines: Iterator[str], func: Callable[[str], str]) -> Iterator[str]:
    """Áp dụng hàm func cho từng dòng."""
    return (func(line) for line in lines)

# Ví dụ sử dụng pipeline:
# for line in transform(filter_error(log_line_generator('biglog.txt')), str.upper):
#     print(line)

"""
Giải thích lazy evaluation:
- Generator chỉ sinh ra giá trị khi cần (khi được duyệt), không load toàn bộ dữ liệu vào bộ nhớ.
- Giúp xử lý file lớn, tiết kiệm RAM.
- Tương tự Java Stream API: đều xử lý dữ liệu theo pipeline, lười (lazy), chỉ thực thi khi cần kết quả.
- Khác biệt: Generator là native Python, đơn giản hơn, không có nhiều toán tử như Stream API nhưng dễ dùng và linh hoạt.

Bài tập nhỏ:
- Viết hàm count_warning(lines: Iterator[str]) trả về số dòng chứa 'WARNING' trong file log (dùng pipeline generator).
"""
