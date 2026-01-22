"""
测试辅助函数
"""

import pytest
from src.utils.helpers import (
    validate_shapefile_path,
    format_number,
    calculate_overlap_ratio,
)


def test_validate_shapefile_path_not_exist():
    """测试文件不存在的验证"""
    is_valid, errors = validate_shapefile_path("/nonexistent/file.shp")
    assert is_valid is False
    assert len(errors) > 0
    assert "文件不存在" in errors[0]


def test_validate_shapefile_path_wrong_extension():
    """测试错误文件扩展名"""
    # 测试当前目录（存在）但扩展名错误
    is_valid, errors = validate_shapefile_path(".")
    assert is_valid is False
    assert len(errors) > 0


def test_format_number():
    """测试数字格式化"""
    assert format_number(3.14159, 2) == "3.14"
    assert format_number(100.0, 1) == "100.0"
    assert format_number(0.123456, 4) == "0.1235"


def test_calculate_overlap_ratio():
    """测试重叠比例计算"""
    assert calculate_overlap_ratio(50, 100) == 0.5
    assert calculate_overlap_ratio(100, 100) == 1.0
    assert calculate_overlap_ratio(0, 100) == 0.0
    assert calculate_overlap_ratio(150, 100) == 1.0  # 不超过1.0
    assert calculate_overlap_ratio(50, 0) == 0.0    # 防止除零
