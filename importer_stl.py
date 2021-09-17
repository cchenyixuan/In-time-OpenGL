import numpy as np
from multiprocessing import Pool
import os
import re


class CreateBufferSTL:
    def __init__(self, file: str):
        self.vertices = None
        self.indices = None
        self.name = re.findall(re.compile(r"_([0-9]+).stl", re.S), file)[0]
        self.fetch(file)
        self.save()

    def fetch(self, file: str) -> None:
        find_vertex = re.compile(r"vertex (.*) (.*) (.*)\n", re.S)
        find_normal = re.compile(r"normal (.*) (.*) (.*)\n", re.S)
        vertex = []
        normal = []
        with open(file, "r") as f:
            for row in f:
                try:
                    vertex.append([float(_) for _ in re.findall(find_vertex, row)[0]])
                except IndexError:
                    pass
                try:
                    normal.append([float(_) for _ in re.findall(find_normal, row)[0]])
                except IndexError:
                    pass
            f.close()
        for step in range(len(vertex)):
            vertex[step].extend(normal[step//3])
        self.vertices = np.array(vertex, dtype=np.float32)
        self.indices = np.array([[i*3, i*3+1, i*3+2] for i in range(len(vertex)//3)], dtype=np.uint32)
    
    def __call__(self):
        return self.vertices, self.indices
    
    def save(self):
        np.savez(self.name, vertices=self.vertices, indices=self.indices)


if __name__ == '__main__':
    file_dir = r"C:\PycharmProjects\stl\Handai_case02_STL/"
    pool = Pool()
    pool.map(CreateBufferSTL, [file_dir+item for item in os.listdir(file_dir)])

    