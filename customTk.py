import tkinter as tk
from tkinter.font import Font
COLORS = {  # discord palette : https://discordapp.com/branding
            "Not quite black":     "#23272A",
            "Dark, but not black": "#2C2F33",
            "Greyple":             "#99AAB5",
            "Blurple":             "#7289DA",
            # custom
            "Lighter Dark": '#323b42',
            "Darker Blurple": "#465791",
            "Brown": '#B5A499',
            "Placeholder": '#9AAAB5'
}     


class darkButton(tk.Button):

    def __init__(self, root,  text, command, font, **options):
        tk.Button.__init__(self, root, command=command, text=text)
        self.config(bg=COLORS["Dark, but not black"], fg=COLORS["Greyple"], bd=0,
                    highlightthickness=0, font=font)
        self.bind("<Enter>", func=lambda evt: evt.widget.configure(
            background=COLORS['Lighter Dark'], fg=COLORS['Blurple']))  # on mouse enter, change color
        self.bind("<Leave>", func=lambda evt: evt.widget.configure(
            background=COLORS["Dark, but not black"], fg=COLORS["Greyple"]))  # on mouse exit, change color
        self.configure(**options)

class darkText(tk.Label):

    def __init__(self, root,text, font='', **options):
        tk.Label.__init__(self, root, text=text)
        self.configure(bg=COLORS["Dark, but not black"],
                       foreground=COLORS["Greyple"])
        self.configure(**options)
        if font:
            self.configure(font=font)
    
class darkCheckbutton(tk.Checkbutton):
    
    def __init__(self, root, text, **options):
        tk.Checkbutton.__init__(self, root, text=text, **options)
        self.configure(bg=COLORS["Dark, but not black"],
                       foreground=COLORS["Greyple"], activebackground=COLORS["Dark, but not black"], selectcolor=COLORS["Dark, but not black"])
    
    def changeText(self, text):
        self.configure(text=text)
        

class darkEntry(tk.Entry):

    def __init__(self, root, font='', placeholder='', imgVar='', **options):
        tk.Entry.__init__(self, root)
        self.imgVar = imgVar
        self.configure(bg=COLORS["Dark, but not black"],
                       foreground=COLORS["Brown"])
        self.placeholder = placeholder

        if placeholder:
            self.configure(fg=COLORS["Placeholder"])
            self.insert(0, placeholder)

        self.bind('<FocusIn>', func = self.placeHolderText)
        self.bind('<FocusOut>', func = self.placeHolderText)

        if font:
            self.configure(font=font)
    
    def placeHolderText(self, evt):
        event = str(evt)
        focusedInText = "FocusIn event" in event
        focusedOutOfText = "FocusOut event" in event

        if focusedInText:
            if self.cget('fg') == COLORS["Placeholder"]:
                if self.imgVar:
                    self.imgVar.set(0)
                self.delete(0, tk.END)
                self.configure(fg=COLORS["Brown"])

        if focusedOutOfText:
            if self.get() == '':
                if self.imgVar:
                    self.imgVar.set(1)
                self.configure(fg=COLORS["Placeholder"])
                self.insert(0, self.placeholder)



class darkList(tk.Listbox):

    def __init__(self, root, font, browsemode, **options):
        tk.Listbox.__init__(self, root, font=font)
        self.configure(selectmode=browsemode, foreground=COLORS["Greyple"],
                       background=COLORS["Dark, but not black"], highlightthickness=0, bd=0, font=font)