import argparse
import csv
from typing import List, Dict

RateType = tuple[int | str, str, float | str]
    
class ReportGenerator:
    """Generates and displays reports based on RateObject data."""

    def __init__(self):
        self._headers = (" ", "brand", "rating")
        self.reports: Dict[str, List[RateType]] = {}

    def _get_max_row_width(self, report: List[RateType]) -> list[int]:
        
        report.insert(0, self._headers)
        return [max(len(str(row[i])) for row in report) for i in range(len(self._headers))]
    
    def _get_separator(self, col_widths: list[int]) -> str:
        return '+' + '+'.join('-' * (w+2) for w in col_widths) + '+'
    
    def _get_formatted_raw(self, row: RateType, col_widths: list[int]) -> str:
        return '|' + '|'.join(f' {str(row[i]).ljust(col_widths[i])} ' for i in range(len(self._headers))) + '|'
    
    def add(self, file_path: str, data: List[RateType]):
        self.reports[file_path] = data

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
            
            print(separator)
            print(self._get_formatted_raw(self._headers, max_row))
            print(separator)
            for item in items[1:]:
                print(self._get_formatted_raw(item, max_row))
            print(separator)
        
class Parser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument("--files", nargs='+', default=["untitled.csv"], help="The paths to files with ratings")
        self.add_argument("--report", type=str, default="Main report", help="report average rating of laptops")
        # self.reports = {}
          
    def create_rate_list(self, file_path) -> list[RateType]:
        print(f"Reading CSV file: {file_path}")
        laptops = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    brand = row['brand'].strip()
                    try:
                        rating = float(row['rating'])
                    except ValueError:
                        print(f"Invalid rating value for {brand}: {row['rating']}")
                        rating = "N/A"
                    
                    # rate_obj = RateObject(brand, 
                    #                       rating)
                    
                    laptops.append((brand, rating))
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []
        
        laptops.sort(key=lambda x: x[1], reverse=True)
        for i, item in enumerate(laptops):
            laptops[i] = (i + 1, item[0], item[1])
            
        return laptops.copy()
    


if __name__ == "__main__":
    parser = Parser()
    
    args = parser.parse_args()
    # report_generator = ReportGenerator()
    
    print(f"Report: {args}")
    print(f"Input files: {args.files}")
    
    if args.report:
        print(f"Generating report for: {args.files}")
        # Здесь будет ваша логика обработки файлов
        for file_path in args.files:
            rate_list = parser.create_rate_list(file_path)
            report_generator = ReportGenerator()
            report_generator.add(file_path, rate_list)
            report_generator.display()
            # print(f"Report of {file_path}: {rate_list}")
            # report_generator._calculate_max_row_width(rate_list)
            # print(rate_object)
    
    # parser.start()
    # parser.display_report()


        
    