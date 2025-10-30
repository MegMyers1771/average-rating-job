import csv

def parse_csv(file_path):
    laptops = []
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Конвертируем числовые поля
            row['price'] = float(row['price'])
            row['rating'] = float(row['rating'])
            laptops.append(row)
    return laptops

# Использование
laptops = parse_csv("laptops_rating.csv")
for laptop in laptops:
    print(f"{laptop['name']} - {laptop['brand']} - ${laptop['price']} - Rating: {laptop['rating']}")