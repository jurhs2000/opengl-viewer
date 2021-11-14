# Charges an OBJ file

class Obj(object):
  def __init__(self, filename):
    with open(filename, "r") as f:
      self.lines = f.read().splitlines()

    self.vertices = []
    self.textcoords = []
    self.normals = []
    self.faces = []
    self.read()

  def read(self):
    for line in self.lines:
      if line:
        try:
          prefix, value = line.split(" ", 1)
        except:
          continue
        if prefix == "v": # Vertex
          self.vertices.append(list(map(float, value.split(" "))))
        elif prefix == "vt": # Text coordinate
          self.textcoords.append(list(map(float, value.split(" "))))
        elif prefix == "vn": # Normal vector
          self.normals.append(list(map(float, value.split(" "))))
        elif prefix == "f": # Face
          self.faces.append([ list(map(int, vertex.split("/"))) for vertex in value.split(" ") ])
