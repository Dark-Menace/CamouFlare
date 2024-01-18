#import statements
import cv2 as cv
import os
import numpy as np

class Steganography:
    
    def __init__(self,choice_bool)->None:
        img_path=self.path_checker(1)
        self.img=cv.imread(img_path)
        self.pixel_count=np.size(self.img)
        self.row_len=self.img.shape[0]
        self.col_len=self.img.shape[1]
        
        if choice_bool:
            self.hide_data()
        else:
            self.extract_data()
        
    def path_checker(self,path_bool)->str: #Checks the path validity
        fpath=input("Enter the path to store the new image(with new image name and extension):")
        self.extension=["png"]
        if path_bool==1:
            if not os.path.exists(fpath):
                raise Exception("Invalid file path.")
        else:
            
            path_check=fpath.split("/")
            path_ck="/".join(path_check[:-1])
            ext=path_check[-1].split(".")
            if not os.path.exists(path_ck):
                raise Exception("Invalid file path.")
            if ext[-1] not in self.extension:
                raise Exception("Invalid file extension(only .png is valid)!!")
        return fpath
    
    def hide_data(self)->None: # Evoke encode method and create a new image instance with data encoded. 

        self.data_ip=input("Enter the data to be encrypted:")
        self.data_len=len(self.data_ip)

        if self.data_len*3 > self.pixel_count:
            raise Exception("Data to be encrypted is too big.")
        elif self.data_len==0:
            raise Exception("Data length is 0.")
      
        self.encode()

        new_path=self.path_checker(2)
        final_img=cv.imwrite(new_path,self.img)
        print("Data encoded successfully!")
    
    def extract_data(self)->None: # Evoke decode method and print the hidden data.
        bin_decode=self.decode()
        hidden_data=""
        for value in bin_decode:
            ord_value=int(value,2)
            hidden_data+=chr(ord_value)
        print("Data decoded.")
        print(f"Hidden data is:{hidden_data}")   

    def encode(self)->None:# encoding data into the image
        current_data_len:int=0
        row:int=0  
        col:int=0
        binary_value=[ format((ord(data)),'08b')for data in self.data_ip]


        for data in binary_value:
            for i in range(0,8):
                if (data[i]=="0" and self.img[row,col,i%3]%2!=0 ):# bgr value to be even, when bin value=0
                    self.img[row,col,i%3]-=1
                elif  (data[i]=="1" and self.img[row,col,i%3]%2==0 ):#bgr value to be odd, when bin value=1
                    if(self.img[row,col,i%3]!=0):
                        self.img[row,col,i%3]-=1
                    else:
                        self.img[row,col,i%3]+=1
                if i in [2,5]: #row upadation after each pixel
                    if col < self.col_len:
                        col+=1
                    else:
                        row+=1
                        col=0
                
# last value(r value) in the 3rd pixel to be updated to indicate whether data is to be further read or not   
            if current_data_len == self.data_len-1:
                if (self.img[row,col,2]%2==0 ):#if all values of the given data has been encoded, (r value)= odd value
                    if (self.img[row,col,2]!=0):
                        self.img[row,col,2]-=1
                    else:
                        self.img[row,col,2]+=1
                
            else:#if some values are yet to be encoded, (r value)= even value
                if (self.img[row,col,2]%2!=0 ):
                    self.img[row,col,2]-=1
                
#column updation after each row           
                if col < self.col_len:
                        col+=1
                else:
                        row+=1
                        col=0
            current_data_len+=1
        
       


    def decode(self)->list:
        binary_list=[]
        data=""
        row:int=0  
        col:int=0
        while True:
            for i in range(0,8):
                if self.img[row,col,i%3]%2==0:#if bgr value is even, bin value=0
                    data+="0"
                else:#if bgr value is odd, bin value=1
                    data+="1"
                if i in [2,5]: #row upadation after each pixel
                    if col < self.col_len:
                        col+=1
                    else:
                        row+=1
                        col=0
            binary_list.append(data)
            data=""
            if self.img[row,col,2]%2!=0:
                break
            else:
                if col < self.col_len:
                        col+=1
                else:
                        row+=1
                        col=0
        return binary_list
        

# Main program
print("Enter 1 for encoding data into the image.")
print("Enter 2 for decoding data from the image.")
choice=int(input("Enter your choice:"))

if choice==1 or choice==2:    
    obj=Steganography(choice%2)
else:
    print("Wrong choice")
    

