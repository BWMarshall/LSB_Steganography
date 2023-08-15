##Libraries
import tkinter as tk
from tkinter import PhotoImage, filedialog
from PIL import Image, ImageTk
import LSBsteg as steg
import huffman as huff


##Global Variables
image_path = ''
text_path = ''
binary = ''
compressed_binary = ''
compression_toggle = True


def decode():
    decode_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
    if decode_path:
        decode_image = Image.open(decode_path)
        binary = steg.retireve_bin_image_lsb(decode_image)
        if binary[0] == "1":
            result = huff.decompress_all(binary[1:])
        else:
            result = huff.binary_to_string(binary[1:])
        save_path = decode_path.rsplit("/",1)[0] + "output.txt"
        with open(save_path,"w") as file:
            file.write(result)
        

##Methodsv
def update():
    ##Define Global Variables
    global image_path,text_path,compression_toggle,compressed_binary,binary
    max_msg_length = 0
    text = ''


    ##get image
    if image_path:
        ##Process Image
        image = Image.open(image_path)
        image = image.convert("RGBA")
        width,height = image.size
        max_msg_length = width * height * 4

        ##Update GUI and Labels
        img_resized = image.resize((round(height * 0.25),round(width * 0.25)))
        img_tkinter = ImageTk.PhotoImage(img_resized)
        image_preview.config(image=img_tkinter)
        image_preview.image = img_tkinter
        image_info_label.config(text = "Info:\n" + image_path + "\n" + str(steg.get_image_size(image)) + " Bits \nPreview:")


    ##get text
    if text_path:

        #Process text
        with open(text_path, 'r') as text_file:
            text = text_file.read()

        #binary and compress binary
        text = huff.ensure_ascii(text)
        binary = huff.string_to_binary(text)
        compressed_binary = huff.compress_alldata(text)

    ##Check Size
    msg_length = len(binary) + 1
    if compression_toggle == True:
        msg_length = len(compressed_binary) + 1

    ##Update Text GUI and Labels
    text_info_label.config(text="Info:\n" + text_path + "\n" + str(msg_length) + " Bits\nPreview:" )
    text_preview_label.config(text = text[:100] + "\n...")

    
    if msg_length > max_msg_length:
        ##Disabled Button 
        ##Display warning message
        print("Message Too Long")
        process_warning_label.config(text= "Process:\nMessage is too long for Image")
        process_encode_button.config(state=tk.DISABLED)
        return True
    else:
        print("Message Fits")
        process_warning_label.config(text= "Process:\nMessage fits Image")
        process_encode_button.config(state=tk.NORMAL)
        return False

    

    print("Updated")

def encode():
    if update():
        ##Prepare Message
        payload = "0" + binary
        if compression_toggle == True:
            payload = "1" + compressed_binary

        ##Encode Message and Save Image
        steg.hide_bin_image_lsb(image_path,payload)
        print("done!")

def select_image_filepath():
    ##get image path
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    update()

def select_text_filepath():
    ##get text file path
    global text_path
    text_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    update()

def toggle_compression():
    ##get compression status
    global compression_toggle
    compression_toggle = compression_checkbox_value.get()
    update()




##Tkinter-------------------------------------

# Tkinter Root & Frames
root = tk.Tk()
root.title("Steganography Tool")

image_frame = tk.Frame(root)
image_frame.grid(row = 0, column = 0, rowspan = 2)

text_frame = tk.Frame(root)
text_frame.grid(row = 0, column = 1, rowspan= 2)


process_frame = tk.Frame(root)
process_frame.grid(row = 0, column = 2, rowspan = 2)


##Image
image_title_label = tk.Label(image_frame, text= "Image")
image_title_label.pack()
image_select_button = tk.Button(image_frame, text="Select Image", command=select_image_filepath)
image_select_button.pack()
image_info_label = tk.Label(image_frame, text= "Info:\n\nPreview:")
image_info_label.pack()
image_preview = tk.Label(image_frame)
image_preview.pack()

##Text
text_title_label = tk.Label(text_frame, text= "Text")
text_title_label.pack()
text_select_button = tk.Button(text_frame, text="Select Text", command=select_text_filepath)
text_select_button.pack()
compression_checkbox_value = tk.BooleanVar(value=True)
compression_checkbox = tk.Checkbutton(text_frame, text= "Enable Compression", variable= compression_checkbox_value , command=toggle_compression)
compression_checkbox.pack()
text_info_label = tk.Label(text_frame, text= "Info:\n\nPreview:")
text_info_label.pack()
text_preview_label = tk.Label(text_frame)
text_preview_label.pack()


##Process
process_warning_label = tk.Label(process_frame, text="Process")
process_warning_label.pack()
process_encode_label = tk.Label(process_frame, text = "Encode Text to Image")
process_encode_label.pack()
process_encode_button = tk.Button(process_frame, text = "Encode", state=tk.DISABLED, command=encode)
process_encode_button.pack()
process_decode_label = tk.Label(process_frame, text="Decode Text from Image")
process_decode_label.pack()
process_decode_button = tk.Button(process_frame, text= "Decode", command=decode)
process_decode_button.pack()


##Undo

root.mainloop()