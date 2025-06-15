import requests


def get_all_data(base_url, per_page=10):
    all_data = []
    page = 1

    while True:
        url = f"{base_url}?page={page}&per_page={per_page}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error: Unable to fetch data. Status code: {response.status_code}")
            break

        data = response.json()
        all_data.extend(data["results"])
        all_data.append(data["results"])

        if page >= data["total_pages"]:
            break

        page += 1

    return all_data


# 示例使用
base_url = "https://api.example.com/data"
result = get_all_data(base_url)
print(result)
