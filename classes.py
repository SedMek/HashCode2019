class Photo:
    id_counter = 0

    def __init__(self, orientation, tags):
        self.id = Photo.id_counter
        Photo.id_counter += 1
        self.orientation = orientation
        self.tags = set(tags)


class Slide:
    def __init__(self, photos):

        self.photos = photos
        self.tags = set(photos[0].tags)
        if len(photos) > 1:
            self.tags = self.tags.union(photos[1].tags)
            self.id = (photos[0].id, photos[1].id)
        else:
            self.id = (photos[0].id,)

def calc_interest(slide1, slide2):
    pass


class SlideShow:

    def __init__(self,slides,id): # TODO Maybe remove id
        self.id = id
        self.slides = slides # Slides is a list of Slide objects

    def calc_interest(self):
        interest = 0
        for i in range(len(self.slides)-1):
            interest += calc_interest(self.slides[i], self.slides[i+1])
