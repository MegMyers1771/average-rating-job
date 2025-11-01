from report import ReportGenerator
from report import Parser

if __name__ == "__main__":
    parser = Parser()
    
    args = parser.parse_args()
    report_generator = ReportGenerator()

    if args.report:
        print(f"Generating report '{args.report}' for: {args.files}")
        # Здесь будет ваша логика обработки файлов
        for file_path in args.files:
            rate_dict = parser.create_rate_dict(file_path)
            
            if not rate_dict:
                continue
        
            report_generator.add(file_path, rate_dict)

    report_generator.display()