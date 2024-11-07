#Model klas
class ClassModel:
    def __init__(self, class_id=None, super_category="", name="", color=(0, 0, 0)):
        self.class_id = class_id
        self.super_category = super_category
        self.name = name
        self.color = color #Jako (r,g,b)