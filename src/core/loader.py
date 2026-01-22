"""
图层加载器模块
提供 Shapefile 图层加载功能
"""

from typing import Tuple, List, Dict, Any, Optional
import geopandas as gpd
import os
from ..utils.helpers import validate_shapefile_path


class ShapefileLoader:
    """Shapefile 图层加载器类"""

    def __init__(self):
        """初始化加载器"""
        pass

    def load_layer(self, file_path: str) -> Tuple[Optional[gpd.GeoDataFrame], List[str]]:
        """
        加载 Shapefile 图层

        Args:
            file_path: Shapefile 文件路径

        Returns:
            (geo_dataframe, error_messages): GeoDataFrame 和错误信息列表
        """
        # 验证文件路径
        is_valid, errors = validate_shapefile_path(file_path)
        if not is_valid:
            return None, errors

        try:
            # 读取 Shapefile
            gdf = gpd.read_file(file_path)

            # 验证几何类型
            if not self._validate_geometry_type(gdf, errors):
                return None, errors

            return gdf, []

        except Exception as e:
            errors.append(f"读取文件失败: {str(e)}")
            return None, errors

    def _validate_geometry_type(self, gdf: gpd.GeoDataFrame, errors: List[str]) -> bool:
        """
        验证几何类型

        Args:
            gdf: GeoDataFrame
            errors: 错误信息列表

        Returns:
            True 如果验证通过，False 否则
        """
        # 检查是否为空
        if len(gdf) == 0:
            errors.append("图层不包含任何要素")
            return False

        # 检查几何类型
        geom_types = set(gdf.geometry.geom_type)
        valid_types = {'Polygon', 'MultiPolygon'}

        if not geom_types.issubset(valid_types):
            errors.append(f"图层包含非面要素: {geom_types}")
            return False

        return True

    def get_layer_info(self, gdf: gpd.GeoDataFrame) -> Dict[str, Any]:
        """
        获取图层信息

        Args:
            gdf: GeoDataFrame

        Returns:
            图层信息字典
        """
        geom_types = gdf.geometry.geom_type.value_counts().to_dict()

        return {
            'feature_count': len(gdf),
            'crs': str(gdf.crs) if gdf.crs else '未定义',
            'geometry_type': list(geom_types.keys())[0] if geom_types else '未知',
            'geometry_counts': geom_types,
            'fields': list(gdf.columns),
            'field_count': len(gdf.columns),
            'bounds': gdf.total_bounds.tolist(),
        }
