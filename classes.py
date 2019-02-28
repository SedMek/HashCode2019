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
            if photos[0].orientation == 'H' or photos[1].orientation == 'H':
                raise ValueError('Slides with 2 photos cannot contain a horizontal photo')

            self.tags = self.tags.union(photos[1].tags)
            self.id = (photos[0].id, photos[1].id)
        else:
            if photos[0].orientation == 'V':
                raise ValueError('Slides with 1 photo must contain 1 horizontal photo')
            self.id = (photos[0].id,)

    def distance(self, slide):
        return - (calc_interest(self, slide) + 1)

    def __repr__(self):
        return "id= {}, tags= {}".format(self.id, self.tags)

    def __str__(self):
        return self.__repr__()

    def __add__(self, other):
        return SlideShow([self, other])

    def __len__(self):
        return len(self.photos)

    def distance(self, other):
        return calc_interest(self, other)


def calc_interest(slide1, slide2):
    if isinstance(slide1, SlideShow):
        slide1 = slide1.last_slide()
        slide2 = slide2.first_slide()
    tags_s1 = slide1.tags
    tags_s2 = slide2.tags
    inter = len(tags_s1.intersection(tags_s2))
    diff12 = len(tags_s1.difference(tags_s2))
    diff21 = len(tags_s2.difference(tags_s1))
    return min(inter, diff12, diff21)


class SlideShow:

    def distance(self,other):
        return calc_interest(self,other)

    def __init__(self,slides,id=0): # TODO Maybe remove id
        self.id = id
        self.slides = slides # Slides is a list of Slide objects

    def calc_interest(self):
        interest = 0
        for i in range(len(self.slides)-1):
            interest += calc_interest(self.slides[i], self.slides[i+1])
        return interest

    def __add__(self, other):
        return self.slides.extend(other.slides)

    def __len__(self):
        return len(self.slides)

    def first_slide(self):
        return self.slides[0]

    def last_slide(self):
        return self.slides[-1]

if __name__ == "__main__":
    pass
