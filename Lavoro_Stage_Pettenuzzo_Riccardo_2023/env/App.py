from PIL import Image#lib for creating images from CTkImage
import customtkinter#Lib used for creating UIs
import cv2#lib for reading images from main

image_submit = None

#after running the program this function write and shows all the results
def Run_Program():
    import Main
    results = Main.Get_Results()
    lbl_firs_method_res_width_ave.configure(text=str(results[1]) + " px")
    lbl_firs_method_res_delta_width.configure(text=str(results[2])+ " px")
    lbl_firs_method_res_std_dev.configure(text=str(results[3])+ " px")
    lbl_second_method_res_width_ave.configure(text=str(results[5])+ " px")
    lbl_second_method_res_delta_width.configure(text=str(results[6])+ " px")
    lbl_second_method_res_std_dev.configure(text=str(results[7])+ " px")
    btn_image_first_method = customtkinter.CTkImage(light_image=Image.fromarray(cv2.imread("imgs/first.jpg").astype('uint8'), 'RGB'), size=(300, 450))
    btn_image_second_method = customtkinter.CTkImage(light_image=Image.fromarray(cv2.imread("imgs/second.jpg").astype('uint8'), 'RGB'), size=(300, 450))
    btn_picture_result_first_method.configure(image=btn_image_first_method)
    btn_picture_result_second_method.configure(image=btn_image_second_method)

def Take_Photo():
    #define the camera that would be used using an index 
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    #define variable for the codec
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3856)#widht of the image
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2764)#heigth of the image
    cap.set(cv2.CAP_PROP_FORMAT, -1)#format of the video/photo
    cap.set(cv2.CAP_PROP_FPS, 7)#fps of the camera 
    cap.set(cv2.CAP_PROP_CONVERT_RGB, 1)#if something needs to be converted to rgb
    cap.set(cv2.CAP_PROP_FOURCC, fourcc)#define the codec

    result, image = cap.read()#read a frame from the camera
    image_submit = image
    
    cap.release()#after reading a frame it releases the camera
    
    cv2.imwrite("imgs/photo.jpg", image)
    photo = customtkinter.CTkImage(light_image=Image.open("imgs\\photo.jpg", mode="r"), size=(300, 450))
    btn_photo = customtkinter.CTkButton(window, hover=False, image=photo, fg_color="#9b0037", corner_radius=10, text="", width=300, height=200)
    btn_photo.grid(row=5, column=4, padx=250, pady=10)
    
def Submit_Photo():
    cv2.imwrite("imgs/photo.jpg")


window = customtkinter.CTk()#create the UI
window.geometry("1920x1080")#assing resolution to the window
window.title("Breton - Calculate Width Sfrido")#assing title to the window
window.configure(fg_color='white')


#Defining objects of the window
btn_StartProgram = customtkinter.CTkButton(window, text="RUN PROGRAM",command=Run_Program, corner_radius=10, fg_color="#9b0037", text_color="white", border_spacing=4, hover_color="#9b0037", height=45)
lbl_StartProgram = customtkinter.CTkLabel(window, text="This program calculate the Difference of Width in a cut made on a slab of variable materials \n by taking a photo of the cutted slab")
btn_TakePhoto = customtkinter.CTkButton(window, text="TAKE PHOTO", hover=False, command=Take_Photo, text_color="white", fg_color="#9b0037", corner_radius=10, border_spacing=4, height=45)
btn_SubmitPhoto = customtkinter.CTkButton(window, text="SUBMIT PHOTO", hover=False, command=Submit_Photo, text_color="white", fg_color="#9b0037", corner_radius=10, border_spacing=4, height=45)

#labels results 1° method
lbl_first_method_results = customtkinter.CTkLabel(window, text="1° METHOD RESULTS", fg_color="#9b0037", text_color="white", corner_radius=8)
lbl_firs_method_res_width_ave = customtkinter.CTkLabel(window, text="...")
lbl_firs_method_res_delta_width = customtkinter.CTkLabel(window, text="...")
lbl_firs_method_res_std_dev = customtkinter.CTkLabel(window, text="...")

#labels results 2° method
lbl_second_method_results = customtkinter.CTkLabel(window, text="2° METHOD RESULTS", fg_color="#9b0037", text_color="white", corner_radius=8)
lbl_second_method_res_width_ave = customtkinter.CTkLabel(window, text="...")
lbl_second_method_res_delta_width = customtkinter.CTkLabel(window, text="...")
lbl_second_method_res_std_dev = customtkinter.CTkLabel(window, text="...")

#Createing the first images for the buttons that will store the results photos
temp = customtkinter.CTkImage(light_image=Image.open("logos\\loghettino.jpg", mode="r"), size=(200, 200))
logo = customtkinter.CTkImage(light_image=Image.open("logos\\logo.png", mode="r"), size=(300, 200))

#Creating the buttons for results images
btn_picture_result_first_method = customtkinter.CTkButton(window, image=temp, text="", width=300, height=450, hover=False, fg_color="#9b0037", corner_radius=10)
btn_picture_result_second_method = customtkinter.CTkButton(window, image=temp, text="", width=300, height=450, hover=False, fg_color="#9b0037", corner_radius=10)
btn_logo = customtkinter.CTkButton(window, image=logo, hover=False, fg_color="#9b0037", corner_radius=10, text="", width=300, height=200)


#Placing defined objects in the window
btn_logo.grid(row=0, column=1, padx=20, pady=20, columnspan=2)
btn_StartProgram.grid(row=4, column=0, padx=40, pady=10)
lbl_StartProgram.grid(row=3, column=0, padx=40, pady=40)
btn_TakePhoto.grid(row=3, column=3, padx=250, pady=10, columnspan=10)
btn_SubmitPhoto.grid(row=4, column=3, padx=250, pady=10, columnspan=10)

#labels and buttons position results 1° method
lbl_first_method_results.grid(row=1, column=1, padx=30, pady=20)
lbl_firs_method_res_width_ave.grid(row=2, column=1, padx=30, pady=2)
lbl_firs_method_res_delta_width.grid(row=3, column=1, padx=30, pady=2)
lbl_firs_method_res_std_dev.grid(row=4, column=1, padx=30, pady=2)
btn_picture_result_first_method.grid(row=5, column=1, padx=10, pady=10)

#labels and buttons position results 2° method
lbl_second_method_results.grid(row=1, column=2, padx=30, pady=20)
lbl_second_method_res_width_ave.grid(row=2, column=2, padx=30, pady=2)
lbl_second_method_res_delta_width.grid(row=3, column=2, padx=30, pady=2)
lbl_second_method_res_std_dev.grid(row=4, column=2, padx=30, pady=2)
btn_picture_result_second_method.grid(row=5, column=2, padx=10, pady=10)

window.mainloop()#loop the window until closed