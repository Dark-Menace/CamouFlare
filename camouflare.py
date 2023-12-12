import cv2 as cv
import os

class Steganography:
    def __init__(self,choice_bool,img)->None:
        self.img=img
        self.row_len=self.img.shape[0]
        self.col_len=self.img.shape[1]
        if choice_bool:
            self.hide_data()
        else:
            self.extract_data()
    
    def hide_data(self)->None:

        self.data_ip=input("Enter the data to be encrypted:")
        self.data_len=len(self.data_ip)
        if self.data_len*3 >( self.col_len * self.row_len):
            print("Data to be encrypted is too big.")
            exit()
        newimg=self.encode()
        new_path=input("Enter the path to store the new image:")
        if not os.path.exists(new_path):
            print("Invalid file path.")
            exit
        final_img=cv.write(new_path,newimg)
        print("Data encoded successfully!")

# encoding data into the image
    def encode(self)->list:
        
        pixel=iter([row for col in self.img for row in col])
        
        binary_value=[ format((ord(data)),'08b') for data in self.data_ip]
        pix_list=self.data_len*[None]*3
        final_pix=self.row_len*self.col_len*[None]
        for i in range(self.data_len):
            pix_list[i]=[next(pixel)]+[next(pixel)]+[next(pixel)]
            for j in range(0,8):
            
                if (binary_value[i][j]=="0") and  (pix_list[i][j]%2!=0): # bgr value to be even, when bin value=0
                    pix_list[i][j]-=1
                elif(binary_value[i][j]=="1") and (pix_list[i][j]%2==0): #bgr value to be odd, when bin value=1
                    if(pix_list[i][j]!=0):
                        pix_list[i][j]-=1
                    else:
                        pix_list[i][j]+=1
            
# last value(r value) in the 3rd pixel to be updated to indicate whether data is to be further read or not, while decoding. 
            if(i==self.data_len-1):
                if (pix_list[i][-1]%2==0): #if all values of the given data has been encoded, (r value)= odd value
                    if(pix_list[i][-1]!=0):
                        pix_list[i][-1]-=1
                    else:
                        pix_list[i][-1]+=1    
            else:#if some values are yet to be encoded, (r value)= even value
                if(pix_list[i][-1]%2!=0):
                    pix_list[i][-1]-=1

# pix_list set into right format(final_pix) to push the list for restructuring the image
        for i in range(self.data_len):
                final_pix.append(pix_list[i][0:3])
                final_pix.append(pix_list[i][3:6])
                final_pix.append(pix_list[i][6:9])
        while True:
            try: 
                final_pix.append(next(pixel))        
            except:
                break

        return self.restructure(final_pix)   

    def restructure(self,pix)->list:
        pix_count=0
        image=self.row_len*[None]
        for i in self.row_len:
            for j in self.col_len:
                image[i][j]=pix[pix_count]
                pix+=1
        return image
            
        




    def decode(self):
        pass
print("Enter 1 for encoding data into the image.")
print("Enter 2 for decoding data from the image.")
choice=int(input("Enter your choice:"))

img_path=input("Enter the image's path:")
if not os.path.exists(img_path):
    print("File path invalid")
    exit()
if choice==1 or choice==2:
    img_obj=cv.imread(img_path)
    
    obj=Steganography(choice%2,img_obj)
else:
    print("Wrong choice")

















