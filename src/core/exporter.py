"""
结果导出器模块
提供处理结果导出功能
"""

from typing import List, Dict, Any, Tuple
import geopandas as gpd
import pandas as pd
import os
import urllib.parse


class ResultExporter:
    """结果导出器类"""

    def __init__(self):
        """初始化导出器"""
        pass

    @staticmethod
    def _encode_field_name(field_name: str) -> str:
        """
        编码字段名为 ASCII 兼容格式（用于 Shapefile）

        Args:
            field_name: 原始字段名

        Returns:
            编码后的字段名
        """
        # 如果已经是 ASCII，直接返回
        try:
            field_name.encode('ascii')
            return field_name
        except UnicodeEncodeError:
            # 包含非 ASCII 字符，进行 URL 编码
            encoded = urllib.parse.quote_plus(field_name)
            # 截断到 10 个字符（Shapefile 限制）
            return encoded[:10] if len(encoded) > 10 else encoded

    def export_to_shapefile(
        self,
        source_gdf: gpd.GeoDataFrame,
        results: List[Dict[str, Any]],
        output_path: str,
        field_prefix: str = 'target_'
    ) -> Tuple[bool, List[str]]:
        """
        导出为 Shapefile

        Args:
            source_gdf: 源图层 GeoDataFrame
            results: 处理结果列表
            output_path: 输出文件路径
            field_prefix: 目标字段前缀

        Returns:
            (success, error_messages): 是否成功和错误信息列表
        """
        errors = []

        try:
            # 复制源图层
            output_gdf = source_gdf.copy()

            # 添加目标字段
            for idx, result in enumerate(results):
                # 找到对应的源要素（按顺序）
                if idx < len(output_gdf):
                    # 添加目标属性（带前缀）
                    for key, value in result['target_attributes'].items():
                        # 编码字段名为 ASCII 兼容格式
                        encoded_key = self._encode_field_name(key)
                        col_name = f"{field_prefix}{encoded_key}"

                        if col_name not in output_gdf.columns:
                            output_gdf[col_name] = None
                        output_gdf.at[idx, col_name] = value

                    # 添加关联信息字段
                    output_gdf.at[idx, 'relation_type'] = result['relation_type']
                    if 'intersection_area' not in output_gdf.columns:
                        output_gdf['intersection_area'] = None
                    output_gdf.at[idx, 'intersection_area'] = result['intersection_area']

                    if 'overlap_ratio' not in output_gdf.columns:
                        output_gdf['overlap_ratio'] = None
                    output_gdf.at[idx, 'overlap_ratio'] = result['overlap_ratio']

            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # 保存为 Shapefile
            output_gdf.to_file(output_path)

            return True, []

        except Exception as e:
            errors.append(f"导出失败: {str(e)}")
            return False, errors

    def export_to_csv(
        self,
        results: List[Dict[str, Any]],
        output_path: str
    ) -> Tuple[bool, List[str]]:
        """
        导出为 CSV 报告

        Args:
            results: 处理结果列表
            output_path: 输出文件路径

        Returns:
            (success, error_messages): 是否成功和错误信息列表
        """
        errors = []

        try:
            # 转换为 DataFrame
            rows = []
            for result in results:
                row = {
                    'source_id': result['source_id'],
                    'target_id': result['target_id'],
                    'relation_type': result['relation_type'],
                    'intersection_area': result['intersection_area'],
                    'overlap_ratio': result['overlap_ratio'],
                }

                # 添加源属性
                for key, value in result['source_attributes'].items():
                    row[f'source_{key}'] = value

                # 添加目标属性
                for key, value in result['target_attributes'].items():
                    row[f'target_{key}'] = value

                rows.append(row)

            df = pd.DataFrame(rows)

            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # 保存为 CSV
            df.to_csv(output_path, index=False, encoding='utf-8-sig')

            return True, []

        except Exception as e:
            errors.append(f"导出失败: {str(e)}")
            return False, errors
