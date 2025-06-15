# Ensure that your virtual environment is activated and that `pandas` is installed in the correct environment.
import pandas as pd
import numpy as np


def compute_total_sold(df):
    # Step 1: 填充缺失值，将 tax 列中 NaN 替换为 0
    df["tax"] = df["tax"].fillna(0)

    # Step 2: 过滤掉 units_sold_per_annum 小于 100 的行
    df = df[df["units_sold_per_annum"] >= 100]

    # Step 3: 计算每行的年度总销售额
    # 使用公式: price * units_sold_per_annum * (1 + tax)
    df["yearly_total_amount"] = (
        df["price"] * df["units_sold_per_annum"] * (1 + df["tax"])
    ).round()

    # Step 4: 按 car_company 汇总年度总销售额
    grouped = df.groupby("car_company")["yearly_total_amount"].sum().reset_index()

    # Step 5: 重命名列并将值转换为整数类型
    grouped = grouped.rename(
        columns={"yearly_total_amount": "yearly_total_amount_sold"}
    )
    grouped["yearly_total_amount_sold"] = grouped["yearly_total_amount_sold"].astype(
        int
    )

    # Step 6: 按 car_company 降序排序
    result = grouped.sort_values(by="car_company", ascending=False)

    return result


# 测试用例
if __name__ == "__main__":
    # 示例数据
    data = {
        "car_company": ["BMW", "BMW", "BMW", "TOYOTA", "FORD", "HYUNDAI", "HONDA"],
        "car_model": [
            "bmw_m1",
            "bmw_m15",
            "bmw_m2",
            "toyota_m1",
            "ford_m2",
            "hyundai_m14",
            "honda_m1",
        ],
        "price": [50000, 35000, 75543, 40000, 25000, 35000, 20000],
        "units_sold_per_annum": [200, 768, 95, 2600, 154, 1000, 4400],
        "tax": [0.01, np.nan, 0.029, 0.015, 0.023, 0.044, 0.032],
    }
    df = pd.DataFrame(data)

    # 调用函数
    result = compute_total_sold(df)
    print(result)