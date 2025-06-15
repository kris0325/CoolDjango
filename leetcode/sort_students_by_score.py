from typing import List, Dict


def sort_students_by_score(students: List[dict[str, int]]) -> List[dict[str, int]]:
    """
    1. Sort an array of student records by score in descending order.
    """
    return sorted(students, key=lambda x: x["score"], reverse=True)


if __name__ == "__main__":
    students: List[Dict[str, int]] = [
        {"name": "Alice", "score": 85},
        {"name": "Bob", "score": 92},
        {"name": "Charlie", "score": 78},
        {"name": "David", "score": 95},
        {"name": "Eve", "score": 88},
    ]

    sort_students: List[Dict[str, int]] = sort_students_by_score(students)

    for student in sort_students:

        print(f"name: {student['name']}, socre: {student['score']}")
