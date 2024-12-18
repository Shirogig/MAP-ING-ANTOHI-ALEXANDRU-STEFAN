from tkinter import *
from tkinter import messagebox

# Inițializare fereastră principală
afisaj = Tk()
afisaj.title("X și 0 - Tic Tac Toe")
afisaj.configure(bg="black")  # Fundal negru

# Variabile globale
tabla = [[None for _ in range(3)] for _ in range(3)]
jucator_curent = "X"
scor = {"X": 0, "O": 0}
timer = None
timp_ramas = 5  # Timpul pentru fiecare mutare

# Funcție pentru actualizarea tabelei de scor
def actualizeaza_scor():
    label_scor.config(text=f"Scor - X: {scor['X']} | O: {scor['O']}")

# Funcție pentru resetarea jocului
def resetare_joc():
    global tabla, jucator_curent, timp_ramas, timer
    if timer:
        afisaj.after_cancel(timer)
    for i in range(3):
        for j in range(3):
            butoane[i][j].config(text="", state="normal", bg="gray20")
    tabla = [[None for _ in range(3)] for _ in range(3)]
    jucator_curent = "X"
    timp_ramas = 5
    actualizeaza_timer()
    label_tura.config(text=f"Tura jucătorului: {jucator_curent}")
    porneste_timer()

# Funcție pentru verificarea câștigătorului
def verifica_castigator():
    for i in range(3):
        if tabla[i][0] == tabla[i][1] == tabla[i][2]:
            return tabla[i][0]
        if tabla[0][i] == tabla[1][i] == tabla[2][i] and tabla[0][i] is not None:
            return tabla[0][i]
    if tabla[0][0] == tabla[1][1] == tabla[2][2] and tabla[0][0] is not None:
        return tabla[0][0]
    if tabla[0][2] == tabla[1][1] == tabla[2][0] and tabla[0][2] is not None:
        return tabla[0][2]
    return None

# Funcție pentru verificarea unei egalități
def tabla_plina():
    return all(tabla[i][j] is not None for i in range(3) for j in range(3))

# Funcție pentru timer
def actualizeaza_timer():
    label_timer.config(text=f"Timp rămas: {timp_ramas} secunde")

def porneste_timer():
    global timer, timp_ramas, jucator_curent
    if timp_ramas > 0:
        actualizeaza_timer()
        timer = afisaj.after(100000, porneste_timer)
        timp_ramas -= 1
    else:
        # Timer expirat - schimbă tura
        jucator_curent = "O" if jucator_curent == "X" else "X"
        label_tura.config(text=f"Tura jucătorului: {jucator_curent}")
        messagebox.showwarning("Timp expirat", f"Timpul a expirat! Revine tura jucătorului '{jucator_curent}'.")
        timp_ramas = 5
        actualizeaza_timer()
        porneste_timer()

# Funcție pentru gestionarea unei mutări
def mutare(linie, coloana):
    global jucator_curent, timp_ramas, timer
    if tabla[linie][coloana] is None:
        tabla[linie][coloana] = jucator_curent
        culoare_text = "white" if jucator_curent == "X" else "orange"
        butoane[linie][coloana].config(text=jucator_curent, fg=culoare_text, bg="gray30")
        
        castigator = verifica_castigator()
        if castigator:
            scor[castigator] += 1
            actualizeaza_scor()
            messagebox.showinfo("Câștigător!", f"Jucătorul '{castigator}' a câștigat!")
            resetare_joc()
            return
        elif tabla_plina():
            messagebox.showinfo("Egalitate", "Jocul s-a terminat cu egalitate!")
            resetare_joc()
            return

        # Schimbă tura și resetează timer-ul
        jucator_curent = "O" if jucator_curent == "X" else "X"
        label_tura.config(text=f"Tura jucătorului: {jucator_curent}")
        timp_ramas = 5
        actualizeaza_timer()
        if timer:
            afisaj.after_cancel(timer)
        porneste_timer()

# Crearea tabelei de joc
butoane = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        butoane[i][j] = Button(afisaj, text="", font=("Times New Roman", 24), height=2, width=5,
                               bg="gray20", fg="white",
                               command=lambda linie=i, coloana=j: mutare(linie, coloana))
        butoane[i][j].grid(row=i, column=j, padx=5, pady=5)

# Afișarea scorului și tura jucătorului
label_scor = Label(afisaj, text=f"Scor - X: {scor['X']} | O: {scor['O']}", font=("Times New Roman", 14),
                   bg="black", fg="white")
label_scor.grid(row=3, column=0, columnspan=3)

label_tura = Label(afisaj, text=f"Tura jucătorului: {jucator_curent}", font=("Times New Roman", 14),
                   bg="black", fg="white")
label_tura.grid(row=4, column=0, columnspan=3)

label_timer = Label(afisaj, text=f"Timp rămas: {timp_ramas} secunde", font=("Times New Roman", 14),
                    bg="black", fg="white")
label_timer.grid(row=5, column=0, columnspan=3)

btn_reset = Button(afisaj, text="Resetare Joc", font=("Times New Roman", 12), bg="gray20", fg="white",
                   command=resetare_joc)
btn_reset.grid(row=6, column=0, columnspan=3)

# Rulează interfața grafică și timer-ul inițial
porneste_timer()
afisaj.mainloop()