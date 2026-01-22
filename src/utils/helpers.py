"""
辅助函数模块
提供常用的辅助功能
"""

import os
from typing import List, Tuple


def validate_shapefile_path(file_path: str) -> Tuple[bool, List[str]]:
    """
    验证 Shapefile 文件路径

    Args:
        file_path: Shapefile 文件路径

    Returns:
        (is_valid, error_messages): 验证结果和错误信息列表
    """
    errors = []

    # 检查文件是否存在
    if not os.path.exists(file_path):
        errors.append(f"文件不存在: {file_path}")
        return False, errors

    # 检查文件扩展名
    if not file_path.lower().endswith('.shp'):
        errors.append("文件格式错误，必须是 .shp 文件")
        return False, errors

    # 检查关联文件
    base_path = os.path.splitext(file_path)[0]
    required_extensions = ['.shx', '.dbf', '.prj']

    for ext in required_extensions:
        if not os.path.exists(base_path + ext):
            errors.append(f"缺少关联文件: {os.path.basename(base_path + ext)}")

    return len(errors) == 0, errors


def format_number(value: float, decimals: int = 2) -> str:
    """
    格式化数字显示

    Args:
        value: 数值
        decimals: 小数位数

    Returns:
        格式化后的字符串
    """
    return f"{value:.{decimals}f}"


def calculate_overlap_ratio(intersection_area: float, source_area: float) -> float:
    """
    计算重叠比例

    Args:
        intersection_area: 相交面积
        source_area: 源要素面积

    Returns:
        重叠比例（0-1）
    """
    if source_area == 0:
        return 0.0
    return min(intersection_area / source_area, 1.0)
