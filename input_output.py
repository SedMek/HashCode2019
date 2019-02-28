import classes as c

PATH = 'input/'

def read(filename):
    with open(PATH + filename) as f:
        content = f.readline()
        N = int(content.strip())


        content = f.readlines()
        photos = []
        for line in content:
            line = line.strip().split(" ")
            photo = c.Photo(line[0], line[2:])
            photos.append(photo)
        return N, photos

if __name__ == "__main__":
    print(read("a_example.txt"))

