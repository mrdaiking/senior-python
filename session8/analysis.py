import pandas as pd


def main():
    # Đọc file CSV (giả sử có file sample.csv trong cùng thư mục)
    df = pd.read_csv("sample.csv")

    # Lọc user tuổi > 20
    adults = df[df["age"] > 20]
    print("Users age > 20:")
    print(adults)

    # Group by city, đếm số user mỗi thành phố
    city_counts = df.groupby("city")["id"].count()
    print("\nUser count by city:")
    print(city_counts)

    # Lọc user theo city, xuất ra file mới
    hanoi_users = df[df["city"] == "Hanoi"]
    hanoi_users.to_csv("hanoi_users.csv", index=False)
    print("\nExported Hanoi users to hanoi_users.csv")


if __name__ == "__main__":
    main()
