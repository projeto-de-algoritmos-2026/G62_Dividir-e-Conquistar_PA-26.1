from typing import Any, Optional

from App import sort_count as sc


class SortCountUtil:
    @staticmethod
    def kendall_tau_2(inv_num: int, len: int) -> float:
        if (len == 0) or (len == 1):
            raise ValueError(f"len ({len}) deve ser maior do que 1")
        return 2 * inv_num / (len * (len - 1))

    @staticmethod
    def kendall_tau(items: list[Any], sorted: Optional[list] = None) -> float:
        items_len = len(items)
        if (items_len == 0) or (items_len == 1):
            raise ValueError("items deve ter mais de 1 elemento")

        inv_num, sorted_items = sc.SortCount.run(items)
        tau = SortCountUtil.kendall_tau_2(inv_num, items_len)
        if sorted is not None:
            sorted = sorted_items
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

        inv_num, sorted_items = sc.SortCount.run(items)
        rs = SortCountUtil.spearman_2(inv_num, items_len)
        if sorted is not None:
            sorted = sorted_items
        return rs
