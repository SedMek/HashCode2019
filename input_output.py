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
    s0 = c.Slide([photos[0]])
    s1 = c.Slide([photos[3]])
    s2 = c.Slide([photos[1], photos[2]])
    # show = c.SlideShow([s0, s1, s2], 0)
    # print(show.calc_interest())
    # photos = read("b_lovely_landscapes.txt")
    # slides = [c.Slide([photo]) for photo in photos]
    # show = c.SlideShow(slides, 0)
    sh1 = c.SlideShow([s1])
    sh2 = c.SlideShow([s2])
    # print(c.calc_interest(sh1,sh2))
    print(s1)
    print(s2)
    print("=================")
    print(c.calc_interest(sh1,sh2))