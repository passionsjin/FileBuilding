'''
usage : python make_file.py --size --part

size : 총 사이즈
unit : 사이즈에 대한 단위
part : 파일갯수

결과 : 지정한 파일갯수만큼 파일 생성. 만들어진 파일의 총 사이즈는 지정한 사이즈보다 같거나 큼.
'''
import argparse
import enum
import hashlib
import math
import os
import random
import string
from datetime import datetime

make_file_path = os.path.join(os.path.dirname(__file__), "test_file")


class UnitBytes(enum.Enum):
    B = 0
    KB = 1
    MB = 2
    GB = 3
    TB = 4


def convert_byte(_input: int, unit: UnitBytes):
    return int(_input * (1024 ** unit.value))


def get_random_to_md5(target: str):
    _target = str(target).join(str(datetime.now()) + str(random.randint(1, 1000)))
    return hashlib.md5(_target.encode('utf-8')).hexdigest()


def check_params(_size: float, _unit: str):
    if _unit not in UnitBytes.__members__:
        print('[ERROR] Unit param : unit(B, KB, MB, GB, TB)')
        return True

    if UnitBytes[_unit] == UnitBytes.B:
        if _size - int(_size):
            print('[ERROR] Byte 일경우 실수형이 올 수 없습니다.')
            return True


def cal_unit_file_size(_size, _unit, _part):
    '''
    하나의 파일당 용량 계산
    :param _size:
    :param _unit:
    :param _part:
    :return:
    '''
    c_size = convert_byte(_size, UnitBytes[_unit]) # size -> byte로 변환

    return math.ceil(c_size / _part)


def make_file(_size, filename):
    file_path = os.path.join(make_file_path, filename)
    with open(file_path, 'w') as f:
        for i in range(_size):
            f.write(random.choice(string.ascii_letters))
        f.close()

    print("size : %d -> %d" % (_size, os.path.getsize(file_path)))


def make_files(unit_size, _part):
    for i in range(_part):
        filename = get_random_to_md5(i)
        make_file(unit_size, filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CM File Maker.')
    parser.add_argument('--size', type=float, required=True, help='size')
    parser.add_argument('--unit', type=str, required=True, help='unit (B, KB, MB, GB, TB)')
    parser.add_argument('--part', type=int, required=True, help='partition')
    args = parser.parse_args()

    size = args.size
    unit = args.unit
    part = args.part
    if check_params(size, unit):
        exit(1)

    file_unit_size = cal_unit_file_size(size, unit, part)

    print("Total File Size : %f %s -> %s byte" % (size, unit, format(convert_byte(size, UnitBytes[unit]), ",")))
    print("Total File Amount : %s" % format(part, ","))
    print("-Unit File Amount: %s" % format(file_unit_size, ","))
    check_from_input = input("Continue? (y,n) : ")

    if check_from_input.lower() != 'y':
        print('Cancel...')
        exit(0)

    make_files(file_unit_size, part)


