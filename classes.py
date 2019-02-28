import input_output as io

class Photo:
    id_counter = 0

    def __init__(self, orientation, tags):
        self.id = Photo.id_counter
        Photo.id_counter += 1
        self.orientation = orientation
        self.tags = set(tags)

    def __repr__(self):
        return "id= {}, orientation= {}, tags= {}\n".format(self.id, self.orientation, self.tags)

    def __str__(self):
        return self.__repr__()


class Slide:
    def __init__(self, photos):

        self.photos = photos
        self.tags = set(photos[0].tags)
        if len(photos) > 1:
            self.tags = self.tags.union(photos[1].tags)
            self.id = (photos[0].id, photos[1].id)
        else:
            self.id = (photos[0].id,)

    def __repr__(self):
        return "id= {}, tags= {}".format(self.id, self.tags)

    def __str__(self):
        return self.__repr__()


def calc_interest(slide1, slide2):
    tags_s1 = slide1.tags
    tags_s2 = slide2.tags
    inter = len(tags_s1.intersection(tags_s2))
    diff12 = len(tags_s1.difference(tags_s2))
    diff21 = len(tags_s2.difference(tags_s1))
    return min(inter, diff12, diff21)


class SlideShow:

    def __init__(self,slides,id): # TODO Maybe remove id
        self.id = id
        self.slides = slides # Slides is a list of Slide objects

    def calc_interest(self):
        interest = 0
        for i in range(len(self.slides)-1):
            interest += calc_interest(self.slides[i], self.slides[i+1])

if __name__ == "__main__":
    N,  = io.read("a_example.txt")