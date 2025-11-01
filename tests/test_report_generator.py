from report import ReportGenerator

# TESTS ReportGenerator

def test_add_and_sort_report():
    rg = ReportGenerator()
    data = {
        "Apple": [("PowerBook G4", 4.6)],
        "IBM": [("ThinkPad T42", 4.5)],
        "SONY": [("VAIO VGN-TX", 4.3)],
        "Dell": [("Latitude D610", 4.1)],
        "HP": [("Pavilion zd8000", 3.9)],
        "Lenovo": [("ThinkPad X60", 4.4)],
    }
    rg.add("laptops.csv", data)

    assert "laptops.csv" in rg.reports
    report = rg.reports["laptops.csv"]

    # Проверим сортировку по убыванию рейтинга
    brands = [row[1] for row in report]
    assert brands == ["Apple", "IBM", "Lenovo", "SONY", "Dell", "HP"]

    # Проверим, что рейтинг округлён до двух знаков
    for row in report:
        assert len(str(row[2]).split('.')[-1]) <= 2


def test_get_max_row_width():
    rg = ReportGenerator()
    report = [["0", "Apple", "4.8"], ["12", "Lenovo", "4.32"]]
    widths = rg._get_max_row_width(report)
    assert widths == [2, 6, 6]


def test_get_separator():
    rg = ReportGenerator()
    sep = rg._get_separator([3, 4, 5])
    assert sep.startswith("+")
    assert sep.endswith("+")
    assert "-" in sep


def test_get_formatted_raw():
    rg = ReportGenerator()
    row = ["1", "Apple", "4.8"]
    col_widths = [2, 6, 3]
    formatted = rg._get_formatted_raw(row, col_widths)
    assert formatted.startswith("| ")
    assert "Apple" in formatted
    assert formatted.endswith("|")


def test_display_no_reports(capsys):
    rg = ReportGenerator()
    rg.display()
    out = capsys.readouterr().out
    assert "No reports generated" in out


def test_display_with_data(capsys):
    rg = ReportGenerator()
    rg.reports = {
        "laptops.csv": [
            ["0", "Apple", "4.6"],
            ["1", "IBM", "4.5"],
        ]
    }
    rg.display()
    out = capsys.readouterr().out
    assert "Report for laptops.csv" in out
    assert "Apple" in out
    assert "+" in out
