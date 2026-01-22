"""
测试图层加载器
"""

import pytest
import geopandas as gpd
import tempfile
import os
from shapely.geometry import Polygon
from src.core.loader import ShapefileLoader


def test_load_valid_shapefile():
    """测试加载有效的 Shapefile"""
    # 创建一个临时的 Shapefile
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建测试数据
        poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        gdf = gpd.GeoDataFrame(
            {'id': [1, 2], 'name': ['A', 'B']},
            geometry=[poly, poly],
            crs='EPSG:4326'
        )

        # 保存为 Shapefile
        shp_path = os.path.join(tmpdir, 'test.shp')
        gdf.to_file(shp_path)

        # 加载
        loader = ShapefileLoader()
        loaded_gdf, errors = loader.load_layer(shp_path)

        assert len(errors) == 0
        assert len(loaded_gdf) == 2
        assert 'id' in loaded_gdf.columns
        assert 'name' in loaded_gdf.columns


def test_load_invalid_path():
    """测试加载不存在的文件"""
    loader = ShapefileLoader()
    gdf, errors = loader.load_layer('/nonexistent/file.shp')

    assert gdf is None
    assert len(errors) > 0


def test_get_layer_info():
    """测试获取图层信息"""
    with tempfile.TemporaryDirectory() as tmpdir:
        poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        gdf = gpd.GeoDataFrame(
            {'id': [1, 2], 'name': ['A', 'B']},
            geometry=[poly, poly],
            crs='EPSG:4326'
        )

        shp_path = os.path.join(tmpdir, 'test.shp')
        gdf.to_file(shp_path)

        loader = ShapefileLoader()
        loaded_gdf, _ = loader.load_layer(shp_path)

        info = loader.get_layer_info(loaded_gdf)

        assert info['feature_count'] == 2
        assert info['crs'] == 'EPSG:4326'
        assert info['geometry_type'] in ['Polygon', 'MultiPolygon']
