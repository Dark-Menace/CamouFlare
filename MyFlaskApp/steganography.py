#import statements
import cv2 as cv
import numpy as np


class Steganography:
    
    def __init__(self,choice_bool,file_path,input_msg="")->None:
        self.data_ip=input_msg
        self.img_path=file_path
        self.img=cv.imread(self.img_path)
        self.pixel_count=np.size(self.img)
        self.row_len=self.img.shape[0]
        self.col_len=self.img.shape[1]
        
        if choice_bool:
            self.hide_data()
        else:
            self.decoded_message=self.extract_data()
   
    def hide_data(self)->None: # Evoke encode method and create a new image instance with data encoded. 

       
        self.data_len=len(self.data_ip)

        if self.data_len*3 > self.pixel_count:
            raise Exception("Data to be encrypted is too big.")
        elif self.data_len==0:
            raise Exception("Data length is 0.")
       
        self.encode()
        
        l=self.img_path.split('/')
        self.img_path='/'.join(l[:-1])
        self.img_path+="/Output.png"
        
        cv.imwrite(self.img_path,self.img)
        print("Data encoded successfully!")
    
    def extract_data(self)->str: # Evoke decode method and print the hidden data.
        bin_decode=self.decode()
        print(bin_decode)
        hidden_data=""
        for value in bin_decode:
            ord_value=int(value,2)
            hidden_data+=chr(ord_value)
        print("Data decoded.")
        print(f"Hidden data is:{hidden_data}")
        return hidden_data   

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
