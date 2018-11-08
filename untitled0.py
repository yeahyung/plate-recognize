import os

def search(dirname):
    filenames = os.listdir(dirname)
    for filename in filenames:
    #  print(filename)
      full_filename = os.path.join(dirname, filename);
      f = open(full_filename,"r")
      text = f.read()
      if text == '835322':
          print(filename)
          path = "C:\\Users\\yea\\Desktop\\Hyung Bin\\Wrong-\\"+filename
          g = open(path,"w")
          g.write(text)
          g.close()

      
     
search("C:\\Users\\yea\\Desktop\\Hyung Bin\\strings")

