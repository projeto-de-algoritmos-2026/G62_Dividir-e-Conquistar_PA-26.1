from typing import Any, Optional

from App import sort_count as sc


class SortCountUtil:
    @staticmethod
    def kendall_tau_2(inv_num: int, len: int) -> float:
        if (len == 0) or (len == 1):
            raise ValueError(f"len ({len}) deve ser maior do que 1")
        # Kendall's tau for a permutation: tau = 1 - 4 * inv_num / (n*(n-1))
        return 1.0 - (4.0 * inv_num) / (len * (len - 1))

    @staticmethod
    def kendall_tau(items: list[Any], sorted: Optional[list] = None) -> float:
        items_len = len(items)
        if (items_len == 0) or (items_len == 1):
            raise ValueError("items deve ter mais de 1 elemento")

        inv_num, sorted_items = sc.SortCount.run(items)
        tau = SortCountUtil.kendall_tau_2(inv_num, items_len)
        if sorted is not None:
            # populate caller-provided list with the sorted result
            sorted.clear()
            sorted.extend(sorted_items)
        return tau

    @staticmethod
    def spearman_2(inv_num: int, len: int) -> float:
        if (len == 0) or (len == 1):
            raise ValueError(f"len ({len}) deve ser maior do que 1")
        return 6 * inv_num / (len * (len * len - 1))

    @staticmethod
    def spearman(items: list[Any], sorted: Optional[list] = None) -> float:
        items_len = len(items)
        if (items_len == 0) or (items_len == 1):
            raise ValueError("items deve ter mais de 1 elemento")

        # compute sorted items and handle ties by assigning average ranks
        _, sorted_items = sc.SortCount.run(items)
        positions: dict[Any, list[int]] = {}
        for idx, val in enumerate(sorted_items, start=1):
            positions.setdefault(val, []).append(idx)

        avg_rank: dict[Any, float] = {}
        for val, pos_list in positions.items():
            avg_rank[val] = sum(pos_list) / len(pos_list)

        sum_d2 = 0.0
        for i, val in enumerate(items, start=1):
            rank = avg_rank[val]
            d = i - rank
            sum_d2 += d * d

        rho = 1.0 - (6.0 * sum_d2) / (items_len * (items_len * items_len - 1))
        if sorted is not None:
            sorted.clear()
            sorted.extend(sorted_items)
        return rho
