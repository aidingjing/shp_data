"""
测试结果导出器
"""

import pytest
import geopandas as gpd
import tempfile
import os
from shapely.geometry import Polygon
from src.core.exporter import ResultExporter


def test_export_to_shapefile():
    """测试导出为 Shapefile"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建测试数据
        poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        source_gdf = gpd.GeoDataFrame(
            {'id': [1], 'name': ['A']},
            geometry=[poly],
            crs='EPSG:4326'
        )

        # 处理结果
        results = [{
            'source_id': 1,
            'source_attributes': {'id': 1, 'name': 'A'},
            'target_id': 'Z01',
            'target_attributes': {'zone_id': 'Z01', 'zone_name': 'Zone A'},
            'relation_type': 'contained',
            'intersection_area': 1.0,
            'overlap_ratio': 1.0,
        }]

        output_path = os.path.join(tmpdir, 'output.shp')

        # 导出
        exporter = ResultExporter()
        success, errors = exporter.export_to_shapefile(
            source_gdf,
            results,
            output_path
        )

        assert success
        assert len(errors) == 0
        assert os.path.exists(output_path)

        # 验证导出的数据（注意：Shapefile 字段名限制为10字符）
        exported_gdf = gpd.read_file(output_path)
        assert len(exported_gdf) == 1
        # 检查截断后的字段名
        assert 'target_zon' in exported_gdf.columns  # target_zone_id 被截断
        assert 'relation_t' in exported_gdf.columns   # relation_type 被截断
        # 验证数据值（使用截断后的字段名）
        assert exported_gdf['target_zon'][0] == 'Z01'


def test_export_to_csv():
    """测试导出为 CSV"""
    with tempfile.TemporaryDirectory() as tmpdir:
        results = [{
            'source_id': 1,
            'source_attributes': {'id': 1, 'name': 'A'},
            'target_id': 'Z01',
            'target_attributes': {'zone_id': 'Z01', 'zone_name': 'Zone A'},
            'relation_type': 'contained',
            'intersection_area': 1.0,
            'overlap_ratio': 1.0,
        }]

        output_path = os.path.join(tmpdir, 'report.csv')

        exporter = ResultExporter()
        success, errors = exporter.export_to_csv(results, output_path)

        assert success
        assert len(errors) == 0
        assert os.path.exists(output_path)
