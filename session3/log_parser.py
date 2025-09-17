import itertools
from typing import Iterator, Callable

def read_log_lines(filepath: str) -> Iterator[str]:
    """Generator: yield each line in a large log file. 
    Args:
        filepath (str): Path to the log file.
    Yields:
        str: Each line in the log file, stripped of trailing newline characters.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.rstrip('\n')

def filter_errors(lines: Iterator[str]) -> Iterator[str]:
    """Yield lines containing 'ERROR'.
    Args:
        lines (Iterator[str]): An iterator of log lines.
    Yields:
        str: Lines that contain the substring 'ERROR'.
    """
    return (line for line in lines if 'ERROR' in line)

def transform_lines(lines: Iterator[str], func: Callable[[str], str]) -> Iterator[str]:
    """Apply func to each line.
    Args:
        lines (Iterator[str]): An iterator of log lines.
        func (Callable[[str], str]): A function to transform each line.
    Yields:
        str: Transformed lines.
    """
    return (func(line) for line in lines)

def aggregate_count(lines: Iterator[str]) -> int:
    """Count the number of lines.
    Args:
        lines (Iterator[str]): An iterator of log lines.
    Returns:
        int: The count of lines."""
    return sum(1 for _ in lines)

if __name__ == "__main__":
    # Example usage of the pipeline
    filepath = "biglog.log"  # Change to the actual log file
    lines = read_log_lines(filepath)
    error_lines = filter_errors(lines)
    upper_lines = transform_lines(error_lines, str.upper) # Transform to uppercase
    # Count the number of error lines
    count = aggregate_count(itertools.tee(upper_lines, 2)[0])
    # Print the first 5 error lines (transformed)
    for line in itertools.islice(upper_lines, 5):
        print(line)
    print(f"Total number of error lines: {count}")
