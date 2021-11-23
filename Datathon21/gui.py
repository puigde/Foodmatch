from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
import beta_restaurant_atr as b
import matching_algorithm as m
import MGP
import time
import json

'''GUI made with tkinter to visualize our backend'''

def restaurants_search():
    f=open("test_reviews.json")
    json_data=json.load(f)

    restaurant = []
    for i in range(len(json_data)):
        reviews=json_data[i]["title"]
        restaurant.append(reviews)

    # Update the listbox
    def update(data):
        # Clear the listbox
        my_list.delete(0, END)

        for item in data:
            my_list.insert(END, item)



    # Update entry box with listbox clicked
    def fillout(e):
        changetext("")
        # Delete whatever is in the entry box
        my_entry.delete(0, END)

        # Add clicked list item to entry box
        my_entry.insert(0, my_list.get(ANCHOR))


    def changetext(word):
        Label_middle.config(text=word)

    # Creating function to check entry vs listbox
    def check(e):
        # Grab what was typed
        typed = my_entry.get()

        if typed == '':
            data = restaurant_list
        else:
            data = []
            for item in restaurant_list:
                if typed.lower() in item.lower():
                    data.append(item)

        # Updating our listbox with selected items
        update(data)

    # Positive reviews
    def printInput():
        word = my_entry.get()
        if word in restaurant_list:
            changetext("")
            b.process_mgp(word, 1)
        else:
            changetext("Not valid!")


    # Negative reviews
    def graph():
        word = my_entry.get()
        if word in restaurant_list:
            changetext("")
            b.process_mgp(word, 0)
        else:
            changetext("Not valid!")




    root = Tk()
    root.title('Title')
    root.geometry("500x300")

    # Create a list of all the restaurants
    restaurant_list = restaurant

    # Creating a label
    my_label = Label(root, text="Start Typing...",
        font=("Helvetica", 14), fg="grey")

    my_label.pack(pady=20)

    # Creating an entry box
    my_entry = Entry(root, font=("Helvetica", 20))
    my_entry.pack()



    positive = Button(root,text = "Good reviews", overrelief = "sunken", command = printInput)
    positive.pack()


    negative = Button(root, text= "Bad reviews", bd = 2, overrelief = "sunken", command= graph)
    negative.pack()


    # Creating a listbox
    my_list = Listbox(root, width=50)
    my_list.pack(pady=40)

    Label_middle = Label(root,
                            text ='')

    Label_middle.place(relx = 0.5,
                       rely = 0.6,
                       anchor = 'center')

    Button(root, text = " Label Text", command=changetext).pack()



    # Adding the restaurants
    update(restaurant_list)

    # Create a binding on the listbox onclick
    my_list.bind("<<ListboxSelect>>", fillout)

    # Create a binding on the entry box
    my_entry.bind("<KeyRelease>", check)



    root.mainloop()

def words_matching():
    def printInput():
        word = my_entry.get()
        print(word)
        list_function = m.matching(word)
        a = list_function[0]
        b = list_function[1]
        c = list_function[2]
        d = list_function[3]
        e = list_function[4]

        A = Label(root, text =a)
        A.place(relx = 0.5, rely = 0.5, anchor = 'center')
        B = Label(root, text =b)
        B.place(relx = 0.5, rely = 0.6, anchor = 'center')
        C = Label(root, text =c)
        C.place(relx = 0.5, rely = 0.7, anchor = 'center')
        D = Label(root, text =d)
        D.place(relx = 0.5, rely = 0.8, anchor = 'center')
        E = Label(root, text =e)
        E.place(relx = 0.5, rely = 0.9, anchor = 'center')





    # Starting the interface
    root = Tk()
    root.title('Auto Select/Search')
    root.geometry("500x300")


    # Create a label
    my_label = Label(root, text="Separate your preferences with commas.",
        font=("Helvetica", 14), fg="grey")

    my_label.pack(pady=20)

    my_label = Label(root, text="For example: meat, fish, tapas",
        font=("Helvetica", 14), fg="grey")

    my_label.pack(pady=20)

    # Create an entry box
    my_entry = Entry(root, font=("Helvetica", 20))
    my_entry.pack()


    enter = Button(root,text = "Enter", overrelief = "sunken", command = printInput)
    enter.pack()


    root.mainloop()

if __name__ == "__main__":
    option = int(input("Type 0 for mathcing, 1 for clustering: "))
    if option == 0:
        words_matching()
    elif option == 1:
        restaurants_search()
    else:
        print("Error. You must imput 0 or 1.")
