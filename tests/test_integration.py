"""
集成测试
测试完整的处理流程
"""

import pytest
import geopandas as gpd
from shapely.geometry import Polygon
from src.core.loader import ShapefileLoader
from src.core.processor import SpatialJoinProcessor
from src.core.validator import GeometryValidator
from src.core.exporter import ResultExporter
import tempfile
import os


def test_full_workflow():
    """测试完整工作流"""
    # 创建测试数据
    source_poly = Polygon([(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5), (0.5, 0.5)])
    source_gdf = gpd.GeoDataFrame(
        {'id': [1], 'name': ['Source A']},
        geometry=[source_poly],
        crs='EPSG:4326'
    )

    target_poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
    target_gdf = gpd.GeoDataFrame(
        {'zone_id': ['Z01'], 'zone_name': ['Zone A']},
        geometry=[target_poly],
        crs='EPSG:4326'
    )

    # 处理
    validator = GeometryValidator()
    processor = SpatialJoinProcessor(validator)
    results = processor.process(source_gdf, target_gdf)

    # 验证结果
    assert len(results) == 1
    assert results[0]['relation_type'] == 'contained'

    # 导出
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, 'output.shp')
        exporter = ResultExporter()
        success, errors = exporter.export_to_shapefile(
            source_gdf,
            results,
            output_path
        )

        assert success
        assert os.path.exists(output_path)

        # 验证导出的数据
        exported_gdf = gpd.read_file(output_path)
        assert len(exported_gdf) == 1
        assert 'target_zone' in exported_gdf.columns or 'target_zon' in exported_gdf.columns
