from ttkthemes import ThemedTk
from tkinter import ttk
from tkinter import messagebox, Label, Canvas, Text
from tkinter import filedialog, IntVar, Toplevel, Frame
import os
from datetime import datetime


def save_file():
    file_text = box_text.get("1.0", "end")
    today = datetime.today().strftime('%d-%m-%Y').split("-")
    # print(file_text)
    file = filedialog.asksaveasfilename(
        filetypes=[("txt file", ".txt")],
        defaultextension=".txt",
        initialfile=f"itau {today[0]} {today[1]} {today[2]}"
        )
    fob = open(file, 'w')
    fob.write(file_text)
    fob.close()
    # window.destroy()
    btn_save["state"] = "disabled"


def read_and_write(files):
    for file in files:
        with open(file) as original:
            for line in original:
                box_text.insert("end", f"{line}")
    btn_save["state"] = "normal"

    pop.destroy()


def choice(option, vars):
    if option == "Sim":
        box_text.delete("1.0", "end")
        selected = [pick for var, pick in vars if var.get() == 1]
        # for var, pick in vars:
        #     print('choice -> ', var.get(), pick)
        read_and_write(selected)
    elif option == "Mais":
        pop.destroy()
        last = []
        for _, pick in vars:
            last.append(pick)
        openFile(last)
    else:
        pop.destroy()
        return messagebox.showerror(
            title='Cancelamento',
            message="Nenhum arquivo selecionado"
        )


def clicker(res):
    global pop
    pop = Toplevel(window)
    ttk.Style(pop).theme_use("clam")
    logo = ".\\logo.ico"
    pop.iconbitmap(logo)
    pop.title("Arquivos selevionados")
    pop.geometry("600x400")
    pop_label = Label(
        pop,
        text="Deseja mesclar os arquivos abaixo?",
        font=("helvetica", 12)
        )
    pop_label.pack(pady=10)

    selected_files(res)


def selected_files(res):
    vars = []
    main_frame = Frame(pop)
    main_frame.pack(fill="both", expand=1)

    my_canvas = Canvas(main_frame)
    my_canvas.pack(side="left", fill="both", expand=1)

    my_scrollbar = ttk.Scrollbar(
        main_frame,
        orient="vertical",
        command=my_canvas.yview
        )
    my_scrollbar.pack(side="right", fill="y")

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind(
        '<Configure>',
        lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all"))
        )

    second_frame = Frame(my_canvas)
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    for pick in res:
        # print(pick)
        var = IntVar()
        name = os.path.basename(pick)
        chk = ttk.Checkbutton(
            second_frame,
            text=name,
            variable=var,
            onvalue=1,
            offvalue=0,
            width=200,
            # anchor="w",
            # padx=20,
            )
        var.set(1)
        chk.pack()
        vars.append([var, pick])

    my_frame = Frame(pop, padx=80)
    my_frame.pack(pady=5)

    yes = ttk.Button(
        my_frame,
        text="Sim",
        width=10,
        command=lambda: choice("Sim", vars)
        )
    yes.grid(row=0, column=1, padx=5, pady=3)

    more = ttk.Button(
        my_frame,
        text="Mais",
        width=10,
        command=lambda: choice("Mais", vars)
        )
    more.grid(row=0, column=2, padx=5, pady=3)

    no = ttk.Button(
        my_frame,
        text="Não",
        width=10,
        command=lambda: choice("Não", [])
        )
    no.grid(row=0, column=3, padx=5, pady=3)
    return vars


def openFile(localStorage=[]):
    folder = filedialog.askopenfilenames(
        initialdir="C:\\FINNET\\O0055FINNET\\",
        title="Selecione os arquivos",
        filetypes=(("text files", "*.txt"),
                   ("all files", "*.*"))
                   )

    if len(folder) == 0:
        return messagebox.showinfo(
            title='Arquivos selecionados:',
            message="Nenhum arquivo selecionado"
        )

    if (len(localStorage) != 0):
        for d in folder:
            if (d not in localStorage):
                localStorage.append(d)
        increment = localStorage
    else:
        increment = folder

    clicker(increment)

    return


if __name__ == '__main__':
    window = ThemedTk(theme="arc")
    ttk.Style(window).theme_use("clam")
    window.title("Merge text")
    logo = ".\\logo.ico"
    window.iconbitmap(logo)
    window.config(padx=10, pady=10)
    window.resizable(False, False)
    # button open
    btn = ttk.Button(window, text="Abrir", command=openFile, width=20)
    btn.grid(row=0, column=0, pady=10)
    # button save
    btn_save = ttk.Button(window, text="Salvar", command=save_file, width=20)
    btn_save.grid(row=0, column=1, pady=10)
    btn_save["state"] = "disabled"
    # Text Box
    box_text = Text(window, width=60, height=20, font="Helvetica")
    box_text.grid(row=1, column=0, columnspan=2)

    # website_label.pack()
    # btn.pack()
    window.mainloop()
