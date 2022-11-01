from typing import List

__all__ = ['ArrayUtil']


class ArrayUtil:
    """数组工具类"""

    @staticmethod
    def list_to_tree(arr: List[dict], id_: str, pid: str, child: str) -> List[dict]:
        """
        字典列表转树形结构

        Args:
            arr: 对象列表
            id_: 主键字段名
            pid: 上级字段名
            child: 子级字段名

        Returns:
            树形结构字典列表
        """
        dict_list = []
        # 遍历以id_为key生成map
        id_dict_map = {i.get(id_): i for i in arr}
        # 遍历
        for i in arr:
            # 获取父节点
            p_node = id_dict_map.get(i.get(pid))
            # 有父节点则添加到父节点子集
            if p_node:
                if child in p_node:
                    p_node[child].append(i)
                else:
                    p_node[child] = [i]
            else:
                dict_list.append(i)
        return dict_list
