import requests
import tkinter as tk
from PIL import ImageTk, Image
from io import BytesIO
from tkinter import font

import keys
params = {
    "api_key": keys.api_key,
    "language": "en-US",
    "include_adult": "false"
}

primary_color = "#D8C9E3"
secondary_color = "#8D7796"


result_search = []
index_result = 0



def load_image(url):
    response = requests.get(url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    return image

def get_all_shows(page,result_search):
    query = query_entry.get()
    if query:
        params["query"] = query
        params["page"] = page
        response = requests.get(url='https://api.themoviedb.org/3/search/multi?', params=params)
        response.raise_for_status()
        data = response.json()['results']
        for element in data:
            if (element['media_type'] == 'movie' or element['media_type'] == 'tv') and len(element['overview']) > 0 and element['poster_path'] != None:
                title = ''
                try:
                    title = element['title']
                except KeyError:
                    title = element['name']
               
                result_search.append({
                    "title": title,
                    "overview": element['overview'],
                    "media_type": element['media_type'],
                    "poster_path": element['poster_path']
                })
            


def get_total_pages():
    query = query_entry.get()
    params["query"] = query
    params["page"] = 1
    response = requests.get(url='https://api.themoviedb.org/3/search/multi?', params=params)
    total_pages = response.json()['total_pages']
    return total_pages


def search_query():
    root.update()
    prev_button.config(state=tk.ACTIVE)
    next_button.config(state=tk.ACTIVE)
    global result_search
    result_search = []
    index_result = 0
    i = 1
    pages = get_total_pages()
    while i <= pages:
        get_all_shows(i,result_search)
        i += 1
        if len(result_search) > 50:
            break

    first_movie = result_search[index_result]
    text_container.delete("1.0", "end")
    if len(first_movie['overview']) > 0:
        image_url = "https://image.tmdb.org/t/p/w500" + first_movie['poster_path']
        poster_image = load_image(image_url)
        poster_image = poster_image.resize((int(740 * 0.30), int(400 * 0.85)))
        poster_img_tk = ImageTk.PhotoImage(poster_image)
        image_label.config(image=poster_img_tk)
        image_label.image = poster_img_tk

        text_container.insert("1.0", "Overview:\n\n")
        text_container.insert("2.0",f"\n{first_movie['overview']}")
        text_container.tag_add('Overview','1.0','1.end')
        text_container.tag_config('Overview', font='arial 20 bold')
        text_container.tag_add("text", '2.0', '2.end')
        text_container.tag_config('text', font="arial 14 normal", justify="left")


def next_movie():
    text_container.delete("1.0", "end")
    text_container.delete("2.0", "end")
    global index_result
    index_result += 1
    if index_result > len(result_search) - 1:
        index_result = 0
    movie = result_search[index_result]
    image_url = "https://image.tmdb.org/t/p/w500" + movie['poster_path']
    poster_image = load_image(image_url)
    poster_image = poster_image.resize((int(740 * 0.30), int(400 * 0.85)))
    poster_img_tk = ImageTk.PhotoImage(poster_image)
    image_label.config(image=poster_img_tk)
    image_label.image = poster_img_tk

    text_container.insert("1.0", "Overview:\n\n")
    text_container.insert("2.0",f"\n{movie['overview']}")
    text_container.tag_add('Overview','1.0','1.end')
    text_container.tag_config('Overview', font='arial 20 bold')
    text_container.tag_add("text", '2.0', '2.end')
    text_container.tag_config('text', font="arial 18 normal", justify="left")

def prev_movie():
    text_container.delete("1.0", "end")
    text_container.delete("2.0", "end")
    global index_result
    index_result -= 1
    if index_result < 0:
        index_result = len(result_search) - 1
    movie = result_search[index_result]
    image_url = "https://image.tmdb.org/t/p/w500" + movie['poster_path']
    poster_image = load_image(image_url)
    poster_image = poster_image.resize((int(740 * 0.30), int(400 * 0.85)))
    poster_img_tk = ImageTk.PhotoImage(poster_image)
    image_label.config(image=poster_img_tk)
    image_label.image = poster_img_tk

    text_container.insert("1.0", "Overview:\n\n")
    text_container.insert("2.0",f"\n{movie['overview']}")
    text_container.tag_add('Overview','1.0','1.end')
    text_container.tag_config('Overview', font='arial 20 bold')
    text_container.tag_add("text", '2.0', '2.end')
    text_container.tag_config('text', font="arial 18 normal", justify="left")


def check_entry_value():
    current_value = query_entry.get()
    global previous_value
    if current_value != previous_value:
        if current_value:
            button.config(state=tk.ACTIVE)
        else:
            button.config(state=tk.DISABLED)
    if len(current_value) <= 0:
        button.config(state=tk.DISABLED)
    previous_value = current_value
    root.after(100, check_entry_value)

# UI - Settings
root = tk.Tk()
root.title("SHOWS DB")
root.config(padx=20, pady=20,bg=primary_color)
root.minsize(800, 530)
root.maxsize(800, 530)

# Center the App 
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width/2) - (800/2))
y_coordinate = int((screen_height/2)-(530/2))
root.geometry("{}x{}+{}+{}".format(800, 530, x_coordinate, y_coordinate))
vscrollbar = tk.Scrollbar(root)

# Top Frame 495464
top_frame = tk.Frame(root, width=740, height=60, background=primary_color)
top_frame.place(x=10, y=10)

# Element inside top frame (Entry - Button)
query_entry = tk.Entry(top_frame, highlightbackground=primary_color, bd=0,highlightcolor=primary_color, bg=secondary_color, fg="#FEFCFF")
query_entry.config()
query_entry.place(relx=0, rely=0, y=10, relwidth=0.70, relheight=40/60)

button_font = font.Font(weight="bold", size=14)
button = tk.Button(top_frame, text="SEARCH", font=button_font, bg="white", fg="black", highlightbackground=primary_color, bd=0, command=search_query)

previous_value = query_entry.get()
check_entry_value()



button.place(relx=0, rely=0, x=int(int(740*0.70) + 10 ) ,y=10, relwidth=0.30, relheight=40/60)
# Left Frame
left_frame = tk.Frame(root, width=int(740 * 0.60), height=400, background="#2c8194")
left_frame.place(x=10, y=int(10 + 60 + 10))

# Container text
text_container = tk.Text(left_frame, padx=5,pady=5, background=primary_color, bd=0, borderwidth=0, highlightbackground=primary_color, font=("Arial", 14))
text_container.place(relx=0, rely=0, relheight=1, relwidth=1)
text_container.insert(tk.INSERT, "Write a title...")




# Right Frame
right_frame = tk.Frame(root, width=int(740 * 0.30), height=400, background=primary_color)
right_frame.place(x=10 + int(740*0.65) + 37, y=int(10 + 60 + 10))
url_placeholder = "https://www.iconsdb.com/icons/preview/white/square-xxl.png"
image = load_image(url_placeholder)
image = image.resize((int(740 * 0.30), int(400 * 0.85)))


image_tk = ImageTk.PhotoImage(image)
image_label = tk.Label(right_frame, image=image_tk)
image_label.place(relx=0, rely=0, relwidth=1, relheight=0.85)
prev_button = tk.Button(right_frame, text="<", highlightbackground=primary_color, font=("Arial", 20, "bold"), command=prev_movie, state=tk.DISABLED)
prev_button.place(relx=0, rely=0, x=35, y=int(int(400 * 0.85) + 15), relwidth=0.3)
next_button = tk.Button(right_frame, text=">", highlightbackground=primary_color, font=("Arial", 20, "bold"), command=next_movie, state=tk.DISABLED)
next_button.place(relx=0, rely=0, x=120, y=int(int(400 * 0.85) + 15), relwidth=0.3)






root.mainloop()








# # Canvas
# c = tk.Canvas(root, background="white", yscrollcommand=vscrollbar.set)

# vscrollbar.config(command=c.yview)
# vscrollbar.grid(row=1, column=5, sticky="nse")


# # Updated the window creation
# c.create_window(0, 0, window=f, anchor='nw')
# all_shows = c.create_text(120, 100, text='', font=("Arial", 10, "normal"), width=350)