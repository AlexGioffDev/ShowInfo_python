import requests
import tkinter as tk
import keys
params = {
    "api_key": keys.api_key,
    "language": "en-US",
    "include_adult": "false"
}
# Functions


def reset():
    root.update()
    c.config(scrollregion=c.bbox("all"))


def get_all_shows(page, shows_dict):
    query = query_entry.get()
    if query:
        params["query"] = query
        params["page"] = page
        response = requests.get(url='https://api.themoviedb.org/3/search/multi?', params=params)
        response.raise_for_status()
        data = response.json()['results']

        for element in data:
            if element['media_type'] == 'movie' or element['media_type'] == 'tv' and len(element['overview']) > 0:
                title = ''
                try:
                    title = element['title']
                except KeyError:
                    title = element['name']
                shows_dict[title] = {
                    "overview": element['overview'],
                    "media_type": element['media_type']
                }


def get_total_pages():
    query = query_entry.get()
    params["query"] = query
    params["page"] = 1
    response = requests.get(url='https://api.themoviedb.org/3/search/multi?', params=params)
    total_pages = response.json()['total_pages']
    return total_pages


def search_query():
    reset()
    shows = {}
    i = 1
    pages = get_total_pages()
    while i <= pages:
        get_all_shows(i, shows)
        i += 1
        if len(shows) > 50:
            break
    text = ""
    for key in shows.keys():
        if len(shows[key]['overview']) > 0:
            text += f"{key}({shows[key]['media_type']})\n--------------------------------------------\noverview: {shows[key]['overview']}\n\n"
    c.itemconfig(all_shows, text=text)
    reset()


# UI
root = tk.Tk()
root.title("SHOWS DB")
root.config(padx=20, pady=20, bg="#495464")
vscrollbar = tk.Scrollbar(root)

# Entry
query_entry = tk.Entry()
query_entry.grid(pady=10, row=0, column=1)

# Buttons
search_button = tk.Button(text="Search", command=search_query)
search_button.grid(row=0, column=2, padx=10)

# Canvas
c = tk.Canvas(root, background="white", yscrollcommand=vscrollbar.set)

vscrollbar.config(command=c.yview)
vscrollbar.grid(row=1, column=0, sticky="nse")

f = tk.Frame(c)  # Create the frame which will hold the widgets

c.grid(row=1, column=1, sticky="nsew", columnspan=2)

# Updated the window creation
c.create_window(0, 0, window=f, anchor='nw')
all_shows = c.create_text(120, 100, text='', font=("Arial", 10, "normal"), width=350)


# Updated the screen before calculating the scrollregion
root.update()
c.config(scrollregion=c.bbox("all"))

root.mainloop()

