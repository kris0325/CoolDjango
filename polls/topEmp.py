import pandas as pd


def topEmp(df):
    # 处理空 DataFrame，返回仅包含表头的空 DataFrame
    if df.empty:
        return pd.DataFrame(columns=["emp_id", "sales"])

    # 按 emp_id 汇总所有分部的销售额
    total_sales = df.groupby("emp_id", as_index=False)["sales"].sum()

    # 找到最高销售额
    max_sales = total_sales["sales"].max()

    # 找到拥有最高销售额的员工
    top_employee = total_sales[total_sales["sales"] == max_sales]

    return top_employee


# 测试数据
data = {
    "emp_id": [1, 1, 1, 2, 2, 2, 2, 2],
    "branch_code": ["b01", "b02", "b02", "b01", "b01", "b01", "b02", "b02"],
    "sales": [193, 151, 195, 114, 122, 128, 103, 142],
}

df = pd.DataFrame(data)

# 运行函数
result = topEmp(df)
print(result)
