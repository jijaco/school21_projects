"""
Module that contains tools for passing VoightKampff test.
"""
import sys
import os
from pathlib import Path
HERE = Path(__file__)
sys.path.append(
    '/home/joyasisk/school21/APP/Bootcamp/Python_Bootcamp.Day_07-1/src/modules')
from valid_params import BiologicalParametres
import json
from pydantic import PydanticSchemaGenerationError, ValidationError


class VoightKampff:
    """
    Test used by the LAPD's Blade Runners to assist in determining
    whether or not an individual was a replicant.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize a VoightKampff class that helps to reveal repliacnt

        :param file_path: Path to a JSON file with questions for test.
        :type file_path: str 
        """
        try:
            with open(file_path, "r") as fp:
                try:
                    self.test: dict = json.load(fp=fp)
                except json.JSONDecodeError as e:
                    print('Worng JSON')
                    raise json.JSONDecodeError(e.msg, e.doc, e.pos)
            self.list_of_bio_params: list[BiologicalParametres] = []
        except FileNotFoundError:
            print('File doesn\'t exist')
            raise FileNotFoundError
            # exit(1)
        self.exception_msg: str = ''

    def _check_input(self) -> None:
        if len(self.test) < 10:
            self.exception_msg = 'Not enough questions'
            print(self.exception_msg)

    def _check_params(self) -> bool:
        result_1 = self.list_of_bio_params[0]
        return result_1.respiration == 12 or result_1.heart_rate < 60 or\
            result_1.blushing_level == 0 or result_1.pupillary_dilation == 2

    def replicant_test(self) -> bool:
        """
        The test itself. You need to write four biological parameters for each answer.
        Amount of questions is at least 10. 
        """
        self._check_input()
        if self.exception_msg != '':
            return
        for question in self.test.keys():
            print(question)
            print("Choose from following answers:", end=' ')
            print(*self.test[question], sep=', ')
            try:
                respiration, heart_rate, blushing_level, pupillary_dilation = list(
                    map(int, input().split()))
            except ValueError:
                self.exception_msg = 'Must be four values'
                print(self.exception_msg)
                return
            try:
                bio_params = BiologicalParametres(
                    respiration=respiration,
                    heart_rate=heart_rate,
                    blushing_level=blushing_level,
                    pupillary_dilation=pupillary_dilation
                )
            except ValidationError:
                print('Impossible numbers')
                return
            self.list_of_bio_params.append(bio_params)

        print(self._check_params())
