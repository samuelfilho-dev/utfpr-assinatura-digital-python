import tkinter as tk
from criar_assinatura_view import criar_assinatura_view
from verificar_assinatura_view import verificar_assinatura_view

root = tk.Tk()
root.title("Coloque seu PDF")
root.geometry("300x200")

criar_assinatura_view(root)
verificar_assinatura_view(root)

root.mainloop()
