"""
空间关联处理器模块
实现核心的空间关联算法
"""

from typing import List, Dict, Any, Optional
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from .validator import GeometryValidator


class SpatialJoinProcessor:
    """空间关联处理器类"""

    def __init__(self, validator: GeometryValidator):
        """
        初始化处理器

        Args:
            validator: 几何验证器实例
        """
        self.validator = validator

    def process(
        self,
        source_gdf: gpd.GeoDataFrame,
        target_gdf: gpd.GeoDataFrame,
        source_id_field: str = None,
        target_id_field: str = None
    ) -> List[Dict[str, Any]]:
        """
        执行空间关联处理

        Args:
            source_gdf: 源图层 GeoDataFrame
            target_gdf: 目标图层 GeoDataFrame
            source_id_field: 源图层ID字段名（默认使用索引）
            target_id_field: 目标图层ID字段名（默认使用索引）

        Returns:
            处理结果列表，每个元素包含关联信息
        """
        results = []

        # 确定ID字段
        if source_id_field is None:
            source_ids = source_gdf.index.tolist()
        else:
            source_ids = source_gdf[source_id_field].tolist()

        if target_id_field is None:
            target_ids = target_gdf.index.tolist()
        else:
            target_ids = target_gdf[target_id_field].tolist()

        # 遍历源要素
        for idx, source_geom in enumerate(source_gdf.geometry):
            source_id = source_ids[idx]
            source_attrs = source_gdf.iloc[idx].to_dict()

            # 移除几何字段（避免序列化问题）
            source_attrs.pop('geometry', None)

            # 修复几何错误
            if not source_geom.is_valid:
                source_geom = self.validator.fix_invalid_geometry(source_geom)

            # 优先级1：检查是否完全落入某个目标面
            contained_target = None
            for target_idx, target_geom in enumerate(target_gdf.geometry):
                # 修复目标几何
                if not target_geom.is_valid:
                    target_geom = self.validator.fix_invalid_geometry(target_geom)

                # 检测完全包含
                if source_geom.within(target_geom):
                    contained_target = {
                        'index': target_idx,
                        'id': target_ids[target_idx],
                        'geometry': target_geom,
                        'attributes': target_gdf.iloc[target_idx].to_dict()
                    }
                    break  # 找到第一个包含的面就停止

            # 如果完全包含，直接关联
            if contained_target:
                target_attrs = contained_target['attributes'].copy()
                target_attrs.pop('geometry', None)

                results.append({
                    'source_id': source_id,
                    'source_attributes': source_attrs,
                    'target_id': contained_target['id'],
                    'target_attributes': target_attrs,
                    'relation_type': 'contained',
                    'intersection_area': source_geom.area,
                    'overlap_ratio': 1.0,
                })
                continue

            # 优先级2：计算相交面积，找最大的
            intersects = []
            for target_idx, target_geom in enumerate(target_gdf.geometry):
                # 修复目标几何
                if not target_geom.is_valid:
                    target_geom = self.validator.fix_invalid_geometry(target_geom)

                # 检测相交
                if source_geom.intersects(target_geom):
                    # 计算相交面积
                    intersection = source_geom.intersection(target_geom)
                    area = intersection.area

                    if area > 0:  # 忽略面积为0的相交
                        target_attrs = target_gdf.iloc[target_idx].to_dict()
                        target_attrs.pop('geometry', None)

                        intersects.append({
                            'target_id': target_ids[target_idx],
                            'area': area,
                            'attributes': target_attrs
                        })

            # 如果有相交，选择面积最大的
            if intersects:
                best_match = max(intersects, key=lambda x: x['area'])

                results.append({
                    'source_id': source_id,
                    'source_attributes': source_attrs,
                    'target_id': best_match['target_id'],
                    'target_attributes': best_match['attributes'],
                    'relation_type': 'partial_overlap',
                    'intersection_area': best_match['area'],
                    'overlap_ratio': best_match['area'] / source_geom.area if source_geom.area > 0 else 0,
                })
            else:
                # 无相交
                # 获取目标图层的所有字段
                target_fields = {k: None for k in target_gdf.columns if k != 'geometry'}

                results.append({
                    'source_id': source_id,
                    'source_attributes': source_attrs,
                    'target_id': None,
                    'target_attributes': target_fields,
                    'relation_type': 'no_intersection',
                    'intersection_area': 0,
                    'overlap_ratio': 0,
                })

        return results

    def get_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        获取处理统计信息

        Args:
            results: 处理结果列表

        Returns:
            统计信息字典
        """
        total = len(results)

        contained = sum(1 for r in results if r['relation_type'] == 'contained')
        partial_overlap = sum(1 for r in results if r['relation_type'] == 'partial_overlap')
        no_intersection = sum(1 for r in results if r['relation_type'] == 'no_intersection')

        return {
            'total': total,
            'contained': contained,
            'partial_overlap': partial_overlap,
            'no_intersection': no_intersection,
            'success_rate': (contained + partial_overlap) / total if total > 0 else 0,
        }
