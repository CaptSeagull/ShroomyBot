#this is the function that will contain all the "cat grammar" that makes this actually work
#it's messy as hell and i'm an idiot
def Cat(string):
    split = string.split()
    gogyo = [words.replace('go', 'gyo') for words in split]
    GoGyo = [words.replace('Go', 'Gyo') for words in gogyo]
    onnyon = [words.replace('on', 'nyon') for words in GoGyo]
    OnNyon = [words.replace('On', 'Nyon') for words in onnyon]
    anya = [words.replace('ya', 'nya') for words in OnNyon]
    AnYa = [words.replace('Ya', 'Nya') for words in anya]
    WhNy = [words.replace('Wh', 'Ny') for words in AnYa]
    whny = [words.replace('wh', 'ny') for words in WhNy]
    nyo = [words.replace('no','nyo') for words in whny]
    Nyo = [words.replace('No', 'Nyo') for words in nyo]
    nya = [words.replace('na', 'nya') for words in Nyo]
    Nya = [words.replace('Na', 'Nya') for words in nya]
    ni = [words.replace('ni', 'nyi') for words in Nya]
    Ni = [words.replace('Ni', 'Nyi') for words in ni]
    nnya = [words.replace('nnya', 'nya') for words in Ni]
    w = [words.replace('r', 'w') for words in nnya]
    W = [words.replace('R', 'W') for words in w]
    finale = [words for words in W]
    return ' '.join(finale)


#this is the function that makes the pirate stuff work
#it is far more simple because i don't know that much about speaking like a pirate. just add argh!
def Pirate(string):
    split = string.split()
    ye = [words.replace('you', 'ye') for words in split]
    Ye = [words.replace('You', 'Ye') for words in ye]
    matey = [words.replace('friend', 'matey') for words in Ye]
    Matey = [words.replace('Friend', 'Matey') for words in matey]
    mateys = [words.replace('friends', 'mateys') for words in Matey]
    Mateys = [words.replace('Friends', 'Mateys') for words in mateys]
    aye = [words.replace('yes', 'aye') for words in mateys]
    Aye = [words.replace('Yes', 'Aye') for words in aye]
    joint = ' '.join(Aye)
    if 'One Piece' in joint:
        split2 = joint.split()
        nakama = [words.replace('matey', 'nakama') for words in Aye]
        Nakama = [words.replace('Matey', 'Nakama') for words in nakama]
        nakamas = [words.replace('nakamas', 'nakama-tachi') for words in Nakama]
        Nakamas = [words.replace('Nakamas', 'Nakama-tachi') for words in nakamas]
        arghed = "Argh! " + ' '.join(Nakamas)
        return arghed
    else:
        arghy = "Argh! " + joint
        return arghy


#in order to convert, type Converter('What text you want goes here', 'mode'), where 'mode' is either 'cat' or 'pirate'
def Converter(string, mode):
    if mode == 'Cat' or mode == 'cat':
        return Cat(string)
    elif mode == 'Pirate' or mode == 'pirate':
            return Pirate(string)
    else:
        print("Error. Please check your input again. The first input should be your string in quotes. The second should be the mode 'cat' or 'pirate', again in quotes.")
