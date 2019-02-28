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
        return photos

if __name__ == "__main__":
    photos = read("a_example.txt")
    s1 = c.Slide([photos[1]])
    s2 = c.Slide([photos[2], photos[3]])
    print(c.calc_interest(s1,s2))


