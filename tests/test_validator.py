"""
测试几何验证器
"""

import pytest
from shapely.geometry import Polygon, Point
from src.core.validator import GeometryValidator


def test_fix_invalid_geometry():
    """测试修复无效几何"""
    # 创建一个自相交的多边形（无效几何）
    # 简化的自相交示例： bowed shape
    coords = [
        (0, 0), (2, 2), (0, 2), (2, 0), (0, 0)
    ]
    invalid_polygon = Polygon(coords)

    validator = GeometryValidator()
    fixed = validator.fix_invalid_geometry(invalid_polygon)

    assert fixed.is_valid
    assert isinstance(fixed, Polygon)


def test_fix_valid_geometry():
    """测试修复有效几何（应保持不变）"""
    # 创建一个有效的多边形
    coords = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    valid_polygon = Polygon(coords)

    validator = GeometryValidator()
    fixed = validator.fix_invalid_geometry(valid_polygon)

    assert fixed.is_valid
    assert fixed.equals(valid_polygon)


def test_validate_geometry_valid():
    """测试验证有效几何"""
    coords = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    valid_polygon = Polygon(coords)

    validator = GeometryValidator()
    is_valid, errors = validator.validate_geometry(valid_polygon)

    assert is_valid is True
    assert len(errors) == 0


def test_validate_geometry_invalid():
    """测试验证无效几何"""
    # 自相交的多边形
    coords = [(0, 0), (2, 2), (0, 2), (2, 0), (0, 0)]
    invalid_polygon = Polygon(coords)

    validator = GeometryValidator()
    is_valid, errors = validator.validate_geometry(invalid_polygon)

    assert is_valid is False
    assert len(errors) > 0


def test_validate_geometry_empty():
    """测试验证空几何"""
    empty_polygon = Polygon()

    validator = GeometryValidator()
    is_valid, errors = validator.validate_geometry(empty_polygon)

    assert is_valid is False
    assert len(errors) > 0
