import os

def mystemmize(dirpath, xmldirname, plaindirname):
    '''dirpath - path to dir with files need mystemming(needs to be within the dir with module,
xmldirname - name for dir with mystemmed xml files, plaindirname -
name for dir with mystemmed txt files; both output dirs will be located in the
same directory as the input dir. Mystem must be located in the same dir with mystemmer module'''
    bat = []
    cwd = os.getcwd()
    disk = cwd.split(os.sep)[0]
    mystempath = os.getcwd()+'\mystem.exe'
    for root, dirs, files in os.walk(dirpath):
        for d in dirs:
            dirp = os.path.join(cwd, root, d)
            xml_dirp = dirp.replace(dirpath, xmldirname)
            plain_dirp = dirp.replace(dirpath, plaindirname)
            os.makedirs(xml_dirp, exist_ok = True)
            os.makedirs(plain_dirp, exist_ok = True)

    bat.append(disk)
    d = (cwd + os.sep + dirpath).split(os.sep)
    c = d[len(d)-2]+os.sep
    d = os.sep.join(d[:len(d)-1])+os.sep
    xmldirname = xmldirname[xmldirname.find(c)+len(c):]+os.sep
    plaindirname = plaindirname[plaindirname.find(c)+len(c):]+os.sep
    bat.append('cd '+d)
    for root, dirs, files in os.walk(dirpath):
        for f in files:
            flnm = os.path.join(root,f)
            flnm = flnm[flnm.find(c)+len(c):]
            xmlnm = flnm.split(os.sep)
            xmlnm = xmldirname + os.sep.join(xmlnm[1:])
            xmlnm = xmlnm[:xmlnm.find('.txt')] + '.xml'
            plnnm = flnm.split(os.sep)
            plnnm = plaindirname + os.sep.join(plnnm[1:])
            cmd_request_xml = cwd + os.sep + 'mystem.exe -i -d --format xml '+flnm+' ' + xmlnm
            bat.append(cmd_request_xml)
            cmd_request_plain = cwd + os.sep + 'mystem.exe -i -d '+flnm+' '+ plnnm
            bat.append(cmd_request_plain)
    #сначала записываем всё в батник, потому что os.system передаёт аргумент в командную строку не в кодировке cp-866,
    #из-за чего система не может найти папку с кириллическими символами в пути:
    with open('./script.bat', 'w', encoding = 'cp866') as b:
        for i in range(len(bat)):
            if i==len(bat)-1:
                b.write(bat[i])
            else:
                b.write(bat[i]+'\n')
    os.system(disk)
    os.system(os.path.join(cwd,'script.bat'))
    #батник сделал своё дело, батник может уходить:
    os.remove('./script.bat')

def main():
    mystemmize(os.path.join('газета','plain'),os.path.join('газета','mystem-xml'),os.path.join('газета','mystem-plain'))

if __name__ == '__main__':
    main()
