classes = [
    'Colleges & Schools',
    'Environmental',
    'World',
    'Entertainment',
    'Media',
    'Politics & Government',
    'Regional News',
    'Religion',
    'Sports',
    'Technology',
    'Traffic',
    'Weather',
    'Economic & Corp',
    'Advertisements',
    'Crime',
    'Other',
    'Magazine'
]

def convertToNum():
    with open('./text.csv', 'r') as f:
        lines = f.readlines()
        with open ('./newtext.csv', 'w') as n:        
            for line in lines:  
                t = line.split(',')
                for i in range(0, len(classes)):
                    if(t[0]==classes[i]):
                        t[0] = str(i+1)
                        n.write(','.join(t))
                        break
            
if __name__ == '__main__':
    convertToNum()