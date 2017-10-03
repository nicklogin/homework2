import os

def mkdirs_by_month(year1, year2, folder):
    for year in range(year1, year2+1):
        for month in range(1,13):
            path = folder+str(year)+'/'+str(month)+'/'
            os.makedirs(path, exist_ok = True)

##if __name__ == '__main__':
##    mkdirs_by_month(2007,2017,r'./газета/')
##    print('ok')
    
    
