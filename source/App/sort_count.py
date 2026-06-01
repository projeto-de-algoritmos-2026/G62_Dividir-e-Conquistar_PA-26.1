from typing import Any


class SortCount:
    @staticmethod
    def merge_count(left_items, right_items) -> tuple[int, list[Any]]:
        left_len = len(left_items)
        right_len = len(right_items)
        left_idx = right_idx = inv = 0
        merged = []
        while left_idx < left_len and right_idx < right_len:
            if right_items[right_idx] < left_items[left_idx]:
                merged.append(right_items[right_idx])
                right_idx += 1
                inv += left_len - left_idx
            else:
                merged.append(left_items[left_idx])
                left_idx += 1

        if left_idx < left_len:
            merged.extend(left_items[left_idx:])
        if right_idx < right_len:
            merged.extend(right_items[right_idx:])

        return (inv, merged)

    @staticmethod
    def run(items) -> tuple[int, list[Any]]:
        items_len = len(items)
        if items_len <= 1:
            return (0, list(items))

        middle_idx = items_len >> 1

        left_count, left_sorted = SortCount.run(items[:middle_idx])
        right_count, right_sorted = SortCount.run(items[middle_idx:])
        count, merged = SortCount.merge_count(left_sorted, right_sorted)

        return (left_count + right_count + count, merged)
