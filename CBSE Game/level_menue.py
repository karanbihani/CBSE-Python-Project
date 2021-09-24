from level_menue_data import menue_level

class Menue():
    def __init__(self,menue_level ) :
        self.pos = menue_level[0]
        self.content = menue_level[1]
        self.max_level = menue_level[2]
        

    