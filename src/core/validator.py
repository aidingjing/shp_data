"""
几何验证器模块
提供几何验证和修复功能
"""

from typing import Tuple, List
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection, shape


class GeometryValidator:
    """几何验证和修复类"""

    def __init__(self):
        """初始化验证器"""
        pass

    def fix_invalid_geometry(self, geom):
        """
        修复无效几何

        Args:
            geom: Shapely 几何对象

        Returns:
            修复后的几何对象
        """
        if geom.is_empty:
            return geom

        # 如果已经是有效的，直接返回
        if geom.is_valid:
            return geom

        # 使用 buffer(0) 技巧修复几何
        fixed = geom.buffer(0)

        # 如果修复后仍然无效，尝试进一步处理
        if not fixed.is_valid:
            # 尝试简化几何
            fixed = fixed.simplify(0.0001, preserve_topology=True)

        # 确保返回正确的几何类型
        if isinstance(fixed, GeometryCollection):
            # 如果是几何集合，提取最大的多边形
            polygons = [g for g in fixed.geoms if isinstance(g, (Polygon, MultiPolygon))]
            if polygons:
                # 返回面积最大的多边形
                fixed = max(polygons, key=lambda g: g.area)

        return fixed

    def validate_geometry(self, geom) -> Tuple[bool, List[str]]:
        """
        验证几何对象

        Args:
            geom: Shapely 几何对象

        Returns:
            (is_valid, error_messages): 验证结果和错误信息列表
        """
        errors = []

        # 检查是否为空
        if geom.is_empty:
            errors.append("几何对象为空")
            return False, errors

        # 检查是否有效
        if not geom.is_valid:
            errors.append(f"几何无效: {geom.is_valid}")

        # 检查是否为多边形
        if not isinstance(geom, (Polygon, MultiPolygon)):
            errors.append(f"几何类型错误: {type(geom).__name__}")

        return len(errors) == 0, errors

    def check_self_intersection(self, geom) -> bool:
        """
        检查几何是否有自相交

        Args:
            geom: Shapely 几何对象

        Returns:
            True 如果有自相交，False 否则
        """
        return not geom.is_valid
