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
    def _encode_field_name(field_name: str, prefix: str = 't_') -> str:
        """
        编码字段名为 ASCII 兼容格式（用于 Shapefile）

        Shapefile 限制：字段名最长 10 字符，只支持 ASCII

        Args:
            field_name: 原始字段名
            prefix: 字段前缀（默认 't_' 以节省空间）

        Returns:
            编码后的字段名（最长 10 字符）
        """
        # 完整字段名（带前缀）
        full_name = f"{prefix}{field_name}"

        # 如果已经是 ASCII 且长度 <= 10，直接返回
        try:
            full_name.encode('ascii')
            if len(full_name) <= 10:
                return full_name
        except UnicodeEncodeError:
            pass

        # 需要编码的情况：使用简短的前缀 + 拼音/编码
        # 常见中文到简短拼音映射（3-4个字符）
        pinyin_map = {
            '实施年': 'shinian',    # 实施年 -> shinian
            '建设': 'jian',         # 建设 -> jian
            '项目': 'xiang',         # 项目 -> xiang
            '名称': 'ming',          # 名称 -> ming
            '类型': 'typ',           # 类型 -> typ
            '编号': 'no',            # 编号 -> no
            '单位': 'unit',          # 单位 -> unit
            '流域': 'luyu',          # 流域 -> luyu
            '河流': 'riv',           # 河流 -> riv
            '面积': 'area',          # 面积 -> area
            '长度': 'len',           # 长度 -> len
            '省份': 'prov',          # 省份 -> prov
            '城市': 'city',          # 城市 -> city
            '区县': 'cnty',          # 区县 -> cnty
            '地址': 'addr',           # 地址 -> addr
            '位置': 'loc',           # 位置 -> loc
            '坐标': 'crd',            # 坐标 -> crd
            '时间': 'time',          # 时间 -> time
            '日期': 'date',          # 日期 -> date
            '金额': 'amt',            # 金额 -> amt
            '数量': 'qty',            # 数量 -> qty
            '年份': 'yr',             # 年份 -> yr
            '月份': 'mo',             # 月份 -> mo
            '日期': 'dt',             # 日期 -> dt
        }

        # 检查是否有映射
        if field_name in pinyin_map:
            mapped = pinyin_map[field_name]
            result = f"{prefix}{mapped}"
            # 确保不超过 10 字符
            return result[:10] if len(result) > 10 else result

        # 如果没有映射，使用更激进的编码
        # 使用 unicode 转换 + 简化
        import unicodedata
        simplified = unicodedata.normalize('NFKD', field_name).encode('ascii', 'ignore').decode('ascii')
        # 移除非字母数字字符
        cleaned = ''.join(c if c.isalnum() else '_' for c in simplified)
        result = f"{prefix}{cleaned}"[:10]

        # 如果结果太短，至少保留前缀
        if len(result) < 3:
            result = f"{prefix}cnv"[:10]  # conventional

        return result

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
                    # 添加目标属性（使用短前缀以节省空间）
                    for key, value in result['target_attributes'].items():
                        # 使用短前缀 't_' 而不是 'target_' 以节省空间
                        col_name = self._encode_field_name(key, prefix='t_')

                        # 调试信息（可以删除）
                        if col_name == key:  # 仍然是中文名，编码失败
                            print(f"⚠️ 警告: 字段 '{key}' 未能正确编码")

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
