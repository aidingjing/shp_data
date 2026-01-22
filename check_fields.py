"""检查图层字段名冲突"""
import geopandas as gpd

source_path = "D:/图层/河南流域划分/新建文件夹/河南省流域治理单元矢量.shp"
target_path = "D:/图层/河南流域划分/新建文件夹/一级流域.shp"

print("正在检查字段名...")
print("=" * 60)

try:
    source_gdf = gpd.read_file(source_path)
    target_gdf = gpd.read_file(target_path)

    print(f"\n源图层字段 ({len(source_gdf.columns)} 个):")
    source_fields = [col for col in source_gdf.columns if col != 'geometry']
    for field in source_fields:
        print(f"  - {field}")

    print(f"\n目标图层字段 ({len(target_gdf.columns)} 个):")
    target_fields = [col for col in target_gdf.columns if col != 'geometry']
    for field in target_fields:
        print(f"  - {field}")

    # 检查重复字段
    common_fields = set(source_fields) & set(target_fields)
    if common_fields:
        print(f"\n⚠️ 发现重复字段 ({len(common_fields)} 个):")
        for field in common_fields:
            print(f"  - {field}")
    else:
        print("\n✅ 没有重复字段")

except Exception as e:
    print(f"\n❌ 错误: {e}")
