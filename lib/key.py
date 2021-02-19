from random import randint

class Key:
    length = 20 # Length of a key
    
    def random_letter(self, i: bool) -> str:
        '''
        Randomize a key letter A-Z a-z
        '''
        if i:
            return chr(randint(65, 90))
        return chr(randint(97, 122))

    def build_key(self) -> str:
        '''
        Create a key
        '''
        return ''.join([self.random_letter(randint(0,1)) for i in range(0,self.length)])
