import pygame
from .obj import Obj
from .char import Char

class RotatingAlphabet(Obj):
    
    def __init__(self, xy=None, color=None):
        super().__init__(832, 30, xy if xy else [0, 0], True)
        self.alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Khởi tạo bảng chữ cái
        self.current_offset = 0  # Độ lệch hiện tại để hiển thị bảng chữ cái xoay
        self.arr_char = [Char(chr(i)) for i in range(65, 91)]
        if color != None:
            for i in self.arr_char:
                i.color = color

    def rotate_left(self):
        """
        Xoay bảng chữ cái sang trái một đơn vị.
        """
        self.current_offset = (self.current_offset + 1) % len(self.alphabet)

    def rotate_right(self):
        """
        Xoay bảng chữ cái sang phải một đơn vị.
        """
        self.current_offset = (self.current_offset - 1) % len(self.alphabet)

    def get_rotated_alphabet(self):
        """
        Lấy bảng chữ cái sau khi xoay với độ lệch hiện tại.
        :return: Danh sách các chữ cái đã xoay.
        """
        return self.alphabet[self.current_offset:] + self.alphabet[:self.current_offset]

    def update(self, xy=None):
        """
        Cập nhật giao diện bảng chữ cái xoay.
        """
        if xy is not None:
            self.xy = xy

        rotated_alphabet = self.get_rotated_alphabet()

        # Vẽ bảng chữ cái xoay trên surface
        for i in range(26):
            char=self.arr_char[i]
            char.char = rotated_alphabet[i]
            char.xy = [32*i, 0]
            self.draw(char.update())

        return [self.surface, (self.xy[0], self.xy[1])]

