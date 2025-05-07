import tkinter as tk

from main_controller import selecionar_pdf

root = tk.Tk()
root.title("Coloque seu PDF")
root.geometry("300x200")


botao_upload = tk.Button(root, text="Selecionar PDF", command=selecionar_pdf)
botao_upload.pack(pady=20)

root.mainloop()