class ClassModel:
    # Kontruktor (bez argumentow tworzy pusty obiekt)
    def __init__(self, class_id=None, super_category="", name="", color=None):
        self.class_id = class_id
        self.super_category = super_category
        self.name = name
        self.color = color