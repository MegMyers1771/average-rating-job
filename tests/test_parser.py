import pytest
from report import Parser

# FIXTURES

@pytest.fixture
def csv_content():
    return """name,brand,price,rating
ThinkPad T42,IBM,1850,4.5
PowerBook G4,Apple,2400,4.6
VAIO VGN-TX,SONY,2100,4.3
Latitude D610,Dell,1450,4.1
Pavilion zd8000,HP,1300,3.9
ThinkPad X60,Lenovo,1650,4.4
"""

@pytest.fixture
def tmp_csv_file(tmp_path, csv_content):
    file = tmp_path / "test.csv"
    file.write_text(csv_content, encoding="utf-8")
    return str(file)

# TESTS  _read_csv

def test_read_csv_success(tmp_csv_file):
    parser = Parser()
    data = parser._read_csv(tmp_csv_file)
    assert isinstance(data, list)
    assert len(data) == 6
    assert data[0]["brand"] == "IBM"
    assert data[1]["price"] == "2400"
    assert data[-1]["rating"] == "4.4"


def test_read_csv_file_not_found(capsys):
    parser = Parser()
    data = parser._read_csv("missing.csv")
    out = capsys.readouterr().out
    assert data is None
    assert "File not found" in out


def test_read_csv_empty_file(tmp_path):
    f = tmp_path / "empty.csv"
    f.write_text("", encoding="utf-8")
    parser = Parser()
    data = parser._read_csv(str(f))
    assert data == []

# TESTS create_rate_dict

def test_create_rate_dict_valid_data(tmp_csv_file):
    parser = Parser()
    laptops = parser.create_rate_dict(tmp_csv_file)
    assert "Apple" in laptops.keys()
    assert "Lenovo" in laptops.keys()
    assert isinstance(laptops["Apple"][0], tuple)
    assert laptops["Apple"][0][1] == pytest.approx(4.6, 0.01)
    assert len(laptops) == 6  # все бренды из файла


def test_create_rate_dict_with_invalid_rating(tmp_path, capsys):
    f = tmp_path / "bad.csv"
    f.write_text("name,brand,price,rating\nModel,HP,1300,abc\n", encoding="utf-8")
    parser = Parser()
    laptops = parser.create_rate_dict(str(f))
    out = capsys.readouterr().out
    assert "Error reading rating" in out
    assert laptops == {"HP": []}


def test_create_rate_dict_file_not_found(capsys):
    parser = Parser()
    laptops = parser.create_rate_dict("nonexistent.csv")
    out = capsys.readouterr().out
    assert laptops == {}
    assert "File not found" in out


def test_create_rate_dict_empty_file(tmp_path):
    f = tmp_path / "empty.csv"
    f.write_text("", encoding="utf-8")
    parser = Parser()
    laptops = parser.create_rate_dict(str(f))
    assert laptops == {}
