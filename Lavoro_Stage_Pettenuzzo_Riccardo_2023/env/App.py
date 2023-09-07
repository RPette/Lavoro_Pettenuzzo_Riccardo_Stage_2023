import customtkinter#Lib used for creating UIs
import cv2
from PIL import Image

#TODO make button Take Photo and then processo the photo with run program

def Run_Program():
    import Main#this impor needs to be changed in a call, cause when it's imported it can only execute once
    results = Main.Get_Results()
    lbl_firs_method_res_width_ave.configure(text=str(results[1]))
    lbl_firs_method_res_delta_width.configure(text=str(results[2]))
    lbl_firs_method_res_std_dev.configure(text=str(results[3]))
    lbl_second_method_res_width_ave.configure(text=str(results[5]))
    lbl_second_method_res_delta_width.configure(text=str(results[6]))
    lbl_second_method_res_std_dev.configure(text=str(results[7]))
    btn_image_first_method = customtkinter.CTkImage(light_image=Image.fromarray(cv2.imread("imgs/first.jpg").astype('uint8'), 'RGB'), size=(300, 450))
    btn_image_second_method = customtkinter.CTkImage(light_image=Image.fromarray(cv2.imread("imgs/second.jpg").astype('uint8'), 'RGB'), size=(300, 450))
    btn_picture_result_first_method.configure(image=btn_image_first_method)
    btn_picture_result_second_method.configure(image=btn_image_second_method)

window = customtkinter.CTk()#create the ui
window.geometry("1280x720")#assing resolution to the window
window.title("Breton - Calcola Spessore Sfrido")#assing title to the window

#Defining objects of the window
btn_StartProgram = customtkinter.CTkButton(window, text="Run Program",command=Run_Program, corner_radius=10, fg_color="red", text_color="white", border_spacing=4, hover_color="dark red", height=45)
lbl_StartProgram = customtkinter.CTkLabel(window, text="This program calculate the Difference of Width in a cut made on a slab of variable materials")

#labels results 1° method
lbl_first_method_results = customtkinter.CTkLabel(window, text="1° METHOD RESULTS", fg_color="red", text_color="white", corner_radius=8)
lbl_firs_method_res_width_ave = customtkinter.CTkLabel(window, text="...")
lbl_firs_method_res_delta_width = customtkinter.CTkLabel(window, text="...")
lbl_firs_method_res_std_dev = customtkinter.CTkLabel(window, text="...")

#labels results 2° method
lbl_second_method_results = customtkinter.CTkLabel(window, text="2° METHOD RESULTS", fg_color="red", text_color="white", corner_radius=8)
lbl_second_method_res_width_ave = customtkinter.CTkLabel(window, text="...")
lbl_second_method_res_delta_width = customtkinter.CTkLabel(window, text="...")
lbl_second_method_res_std_dev = customtkinter.CTkLabel(window, text="...")

image1 = customtkinter.CTkImage(light_image=Image.open("C:\\Users\\stage.upe4\\Desktop\\Stefano\\Capture.png", mode="r"), size=(300, 450))
image2 = customtkinter.CTkImage(light_image=Image.open("C:\\Users\\stage.upe4\\Desktop\\Stefano\\Capture.png", mode="r"), size=(300, 450))

btn_picture_result_first_method = customtkinter.CTkButton(window, image=image1, text="", width=300, height=450, hover=False, fg_color="black")
btn_picture_result_second_method = customtkinter.CTkButton(window, image=image1, text="", width=300, height=450, hover=False, fg_color="black")


#Placing defined objects in the window
btn_StartProgram.grid(row=1, column=0, padx=40, pady=10)
lbl_StartProgram.grid(row=0, column=0, padx=40, pady=40)

#labels position results 1° method
lbl_first_method_results.grid(row=0, column=1, padx=30, pady=5)
lbl_firs_method_res_width_ave.grid(row=1, column=1, padx=30, pady=2)
lbl_firs_method_res_delta_width.grid(row=2, column=1, padx=30, pady=2)
lbl_firs_method_res_std_dev.grid(row=3, column=1, padx=30, pady=2)
btn_picture_result_first_method.grid(row=4, column=1, padx=10, pady=0)

#labels position results 2° method
lbl_second_method_results.grid(row=0, column=2, padx=30, pady=5)
lbl_second_method_res_width_ave.grid(row=1, column=2, padx=30, pady=2)
lbl_second_method_res_delta_width.grid(row=2, column=2, padx=30, pady=2)
lbl_second_method_res_std_dev.grid(row=3, column=2, padx=30, pady=2)
btn_picture_result_second_method.grid(row=4, column=2, padx=10, pady=0)


window.mainloop()#loop the window until closed