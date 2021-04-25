import tkinter as tk
from functools import partial

chosen_options = []
button_identities = []


# Ściąga nazwe przycisku który kliknęliśmy = równoważność opcji
def event_button(n, opt=chosen_options):
    print(n)
    bname = (button_identities[n])
    opt.append(bname["text"])
    list_opt = check_if_exist(opt)
    print(list_opt)


# Nie potrzebujemy jednej opcji więcej niż raz = konwersja na dict usuwa duplikaty
def check_if_exist(option_list):
    return list(dict.fromkeys(option_list))


class settingsWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Snake game options")
        self.rowconfigure([0, 1, 2], minsize=50)
        self.columnconfigure([0, 1, 2], minsize=50)
        self.list_options = ["Speed up", "Grid", "Static obstacles", "Dynamic obstacles"]
        self.button_speedup = tk.Button(self, text=self.list_options[0], width=15, height=5,
                                        command=partial(event_button, 0))
        button_identities.append(self.button_speedup)
        self.button_speedup.grid(row=0, column=0)

        self.button_grid = tk.Button(self, text=self.list_options[1], width=15, height=5,
                                     command=partial(event_button, 1))
        button_identities.append(self.button_grid)
        self.button_grid.grid(row=0, column=1)

        self.button_obstacle_static = tk.Button(self, text=self.list_options[2], width=15, height=5,
                                                command=partial(event_button, 2))
        button_identities.append(self.button_obstacle_static)
        self.button_obstacle_static.grid(row=2, column=0)

        self.button_obstacle_dynamic = tk.Button(self, text=self.list_options[3], width=15, height=5,
                                                 command=partial(event_button, 3))
        button_identities.append(self.button_obstacle_dynamic)
        self.button_obstacle_dynamic.grid(row=2, column=1)

        self.button_accept = tk.Button(self, text="Zapisz zakres", width=10, height=2, command=self.print_result)
        self.button_accept.grid(row=2, column=2, sticky="n")

        self.number_obstacle_label = tk.Label(self, text="Liczba przeszkód statycznych(max zakres): ")
        self.number_obstacle_label.grid(row=0, column=2, sticky="s")

        self.number_obstacle = tk.Entry(self)
        self.number_obstacle.grid(row=1, column=2)

    def print_result(self):
        if self.number_obstacle.get().isnumeric():
            print(self.number_obstacle.get())
            chosen_options.append(int(self.number_obstacle.get()))
        else:
            print("Bad range was given!")


myApp = settingsWindow()
myApp.mainloop()
