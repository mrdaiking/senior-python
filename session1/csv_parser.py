""" 
Pythonic Mindset vs Java
Goal: Understand the differences in programming paradigms between Python and Java.
    - Imperative style
    - Pythonic style (comprehensions, with, f-strings)
"""

import csv

def java_style_parser(file_path: str, min_age: int):
    """Imperative style similar to Java"""
    results = []
    f = open(file_path, 'r')
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        age = int(row[2])
        if age > min_age:
            results.append(row)
    f.close()
    return results

def pythonic_style_parser(file_path: str, min_age: int):
    """Pythonic style using context managers and list comprehensions"""
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        results = [row for row in reader if int(row[2]) > min_age]
    return results

if __name__ == "__main__":
    file_path = 'session1/sample.csv'
    print("Imperative Style Results:", java_style_parser(file_path, 30))
    print("Pythonic Style Results:", pythonic_style_parser(file_path, 30))
