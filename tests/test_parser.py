import pytest
import os
from src.parser import extract_text_from_file

def test_extract_text_from_txt(tmp_path):
    # Create a dummy text file
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("Hello World", encoding="utf-8")
    
    content = extract_text_from_file(str(p))
    assert "Hello World" in content

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        extract_text_from_file("non_existent_file.txt")
