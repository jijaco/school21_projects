from modules.voight_kampff import VoightKampff
from modules.valid_params import BiologicalParametres
from json import JSONDecodeError
import pytest
from pathlib import Path
from pydantic import ValidationError

parent = str(Path(__file__).parent)+'/../'


def test_existence_of_file():
    with pytest.raises(FileNotFoundError):
        VoightKampff('nofile.json')


def test_emptyness_of_file():
    with pytest.raises(JSONDecodeError):
        VoightKampff(file_path=parent+'test1.json')


def test_number_of_questions():
    test = VoightKampff(file_path=parent+'test2.json')
    test._check_input()
    assert test.exception_msg == 'Not enough questions'


def test_invalid_numbers():
    test = VoightKampff(file_path=parent+'test2.json')
    with pytest.raises(ValidationError):
        test.list_of_bio_params.append(BiologicalParametres(
            respiration=1,
            heart_rate=2,
            blushing_level=3,
            pupillary_dilation=4
        ))


def test_number_of_health_parametres(monkeypatch):
    test = VoightKampff(file_path=parent+'test.json')
    monkeypatch.setattr('builtins.input', lambda: '1 2 3 4 5')
    test.replicant_test()
    assert test.exception_msg == 'Must be four values'
