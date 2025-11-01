import argparse
import csv
from typing import List, Dict 

TDictReader = csv.DictReader
CSVDataDict = Dict[str, List[tuple[str, float]]]
CSVDataList = Dict[str, List[List]]

from pprint import pprint
    
class ReportGenerator:
    """Generates and displays reports based on RateObject data."""

    def __init__(self):
        self._header = [" ", "brand", "rating"]
        self.reports: Dict[str, List[List]] = {}

    def _get_max_row_width(self, report: List) -> list[int]:
        
        # добавляем хэдер к общему списку рейтингов
        report.insert(0, self._header)
        
        # считаем максимальную длину строки
        return [max(len(str(row[i])) for row in report) for i in range(len(self._header))]
    
    def _get_separator(self, col_widths: list[int]) -> str:
        
        # генерируем разделитель
        return '+' + '+'.join('-' * (w+2) for w in col_widths) + '+'
    
    def _get_formatted_raw(self, row: List, col_widths: list[int]) -> str:
        
        # форматируем строку на основе максимальной длины
        return '|' + '|'.join(f' {str(row[i]).ljust(col_widths[i])} ' for i in range(len(self._header))) + '|'
    
    def add(self, file_path: str, data: CSVDataDict):
        avg_rate_dict = {}
        
        # создаем словарь {brand: avg_rate}
        for brand, products in data.items():
            rate_list = [rate[1] for rate in products]
            avg_rate_dict[brand] = float(f"{sum(rate_list) / len(rate_list):.2f}")
            
        # создаем список из модели и сортируем по убыванию рейтинга
        avg_rate_list = sorted(list(avg_rate_dict.items()), key=lambda x: x[1], reverse=True)
        self.reports[file_path] = []
        
        # добавляем индекс ко всем позициям начиная с 1
        for i, item in enumerate(avg_rate_list):
            self.reports[file_path].append([str(i), *item])
        
        

    def display(self):
        if not self.reports:
            print("No reports generated.")
            return

        
        for file, items in self.reports.items():
            if not items:
                print(f"\n{file}: no data found.")
                continue
            
            max_row = self._get_max_row_width(items)
            separator = self._get_separator(max_row)
            
            print(f"+-- Report for {file} --+")
            print(separator)
            print(self._get_formatted_raw(self._header, max_row))
            print(separator)
            for item in items[1:]:
                print(self._get_formatted_raw(item, max_row))
                print(separator)
            print("\n")
            # print(separator)
        
class Parser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument("--files", nargs='+', required=True, help="The paths to files with ratings")
        self.add_argument("--report", type=str, default="Main report", help="Report average rating of data")
    
    def _read_csv(self, file_path) -> List[dict[str, str]] | None:
        # Функция для чтения csv файлов
        # Вовзвращает список из dict[str, str] вместо DictReader для получения всех элементов без построчной итерации
        
        try:
            print(f"Reading CSV file: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None

    def create_rate_dict(self, file_path) -> CSVDataDict:
        
        # Создаем словарь с брэндами
        csv_dict: CSVDataDict = {}
        
        # Читаем csv файл и получаем ридер
        csv_data = self._read_csv(file_path)
        
        if not csv_data:
            return {}
        
        for row in csv_data:
            # Создаем ключ брэнда в словаре, если он инициализирующий
            if row['brand'] not in csv_dict.keys():
                csv_dict[row['brand']] = []
            
            # Добавляем элемент с моделью с рейтингом
            
            try:
                row_rating = float(row['rating'])
                csv_dict[row['brand']].append(
                    (row['name'], row_rating)
                )
                
            except ValueError:
                print(f"Error reading rating for {row['name']}: {row['rating']}")
        
        
        return csv_dict


        
    