class Gamification:
    def __init__(self):
        self.xp = 0
        self.levels = {
            "Ученик": 0,
            "Мастер пергаментов": 50,
            "Архимаг документов": 100
        }

    def add_xp(self, amount):
        self.xp += amount
        return self.xp

    def get_level(self):
        current_level = "Ученик"
        for level, req_xp in sorted(self.levels.items(), key=lambda x: x[1]):
            if self.xp >= req_xp:
                current_level = level
        return current_level

    def get_progress(self):
        return min(self.xp, 100)
