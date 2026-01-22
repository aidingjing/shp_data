"""
测试空间关联处理器
"""

import pytest
import geopandas as gpd
from shapely.geometry import Polygon, box
from src.core.processor import SpatialJoinProcessor
from src.core.validator import GeometryValidator


def create_test_polygon(coords, **attributes):
    """创建测试用的多边形要素"""
    poly = Polygon(coords)
    return {'geometry': poly, **attributes}


def test_processor_contained_case():
    """测试完全包含情况"""
    # 源要素：小多边形
    source_poly = Polygon([(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5), (0.5, 0.5)])
    source_gdf = gpd.GeoDataFrame(
        {'id': [1], 'name': ['source1']},
        geometry=[source_poly],
        crs='EPSG:4326'
    )

    # 目标要素：大多边形（完全包含源要素）
    target_poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
    target_gdf = gpd.GeoDataFrame(
        {'zone_id': ['Z01'], 'zone_name': ['Zone A']},
        geometry=[target_poly],
        crs='EPSG:4326'
    )

    processor = SpatialJoinProcessor(GeometryValidator())
    result = processor.process(source_gdf, target_gdf, source_id_field='id', target_id_field='zone_id')

    assert len(result) == 1
    assert result[0]['source_id'] == 1
    assert result[0]['target_id'] == 'Z01'
    assert result[0]['relation_type'] == 'contained'
    assert result[0]['overlap_ratio'] == 1.0


def test_processor_partial_overlap():
    """测试部分重叠（相交面积最大）"""
    # 源要素
    source_poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    source_gdf = gpd.GeoDataFrame(
        {'id': [1], 'name': ['source1']},
        geometry=[source_poly],
        crs='EPSG:4326'
    )

    # 目标要素1：相交面积较小 (x: -0.2 to 0.3)
    target1 = Polygon([(-0.2, -0.5), (0.3, -0.5), (0.3, 1.5), (-0.2, 1.5), (-0.2, -0.5)])
    # 目标要素2：相交面积较大 (x: 0.3 to 1.5)
    target2 = Polygon([(0.3, -0.5), (1.5, -0.5), (1.5, 1.5), (0.3, 1.5), (0.3, -0.5)])

    target_gdf = gpd.GeoDataFrame(
        {'zone_id': ['Z01', 'Z02'], 'zone_name': ['Zone A', 'Zone B']},
        geometry=[target1, target2],
        crs='EPSG:4326'
    )

    processor = SpatialJoinProcessor(GeometryValidator())
    result = processor.process(source_gdf, target_gdf, source_id_field='id', target_id_field='zone_id')

    assert len(result) == 1
    assert result[0]['target_id'] == 'Z02'  # 应该关联到相交面积更大的
    assert result[0]['relation_type'] == 'partial_overlap'


def test_processor_no_intersection():
    """测试无相交情况"""
    # 源要素
    source_poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    source_gdf = gpd.GeoDataFrame(
        {'id': [1], 'name': ['source1']},
        geometry=[source_poly],
        crs='EPSG:4326'
    )

    # 目标要素：不相交
    target_poly = Polygon([(5, 5), (6, 5), (6, 6), (5, 6), (5, 5)])
    target_gdf = gpd.GeoDataFrame(
        {'zone_id': ['Z01'], 'zone_name': ['Zone A']},
        geometry=[target_poly],
        crs='EPSG:4326'
    )

    processor = SpatialJoinProcessor(GeometryValidator())
    result = processor.process(source_gdf, target_gdf)

    assert len(result) == 1
    assert result[0]['target_id'] is None
    assert result[0]['relation_type'] == 'no_intersection'
    assert result[0]['intersection_area'] == 0


def test_processor_auto_fix():
    """测试自动修复几何错误"""
    # 创建一个自相交的无效几何
    invalid_coords = [(0, 0), (2, 2), (0, 2), (2, 0), (0, 0)]
    invalid_poly = Polygon(invalid_coords)

    source_gdf = gpd.GeoDataFrame(
        {'id': [1], 'name': ['source1']},
        geometry=[invalid_poly],
        crs='EPSG:4326'
    )

    target_poly = Polygon([(0, 0), (3, 0), (3, 3), (0, 3), (0, 0)])
    target_gdf = gpd.GeoDataFrame(
        {'zone_id': ['Z01'], 'zone_name': ['Zone A']},
        geometry=[target_poly],
        crs='EPSG:4326'
    )

    processor = SpatialJoinProcessor(GeometryValidator())
    result = processor.process(source_gdf, target_gdf)

    # 应该成功处理（自动修复后）
    assert len(result) == 1
