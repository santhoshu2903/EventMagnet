from tkinter import *
from tkinter import ttk
import sv_ttk

root = Tk()
#background color
color='#21252b'
root.configure(background = color)
root.resizable(False, False)
#Notebook color
sky_color = "sky blue"
gold_color = "gold"
color_tab = "#ccdee0"
#style
style = ttk.Style()
style.theme_create( "beautiful", parent = "alt", settings ={
        "TNotebook": {
            "configure": {"tabmargins": [10, 10, 20, 10], "background":sky_color }},
        "TNotebook.Tab": {
            "configure": {"padding": [30, 15], "background": sky_color, "font":('consolas italic', 14), "borderwidth":[0]},
            "map":       {"background": [("selected", gold_color), ('!active', sky_color), ('active', color_tab)],
                          "expand": [("selected", [1, 1, 1, 0])]}}})
# style.theme_use("beautiful")
style.layout("Tab",
                    [('Notebook.tab', {'sticky': 'nswe', 'children':
                        [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                            #[('Notebook.focus', {'side': 'top', 'sticky': 'nswe', 'children':
                                [('Notebook.label', {'side': 'top', 'sticky': ''})],
                            #})],
                        })],
                    })]
                 )
style.configure('TLabel', background = color , foreground = 'white')
style.configure('TFrame', background = color)
#frame
frame_main_notebook = ttk.Frame(root, width = 400, height = 100)
frame_main_notebook.pack()
#note book
main_notebook = ttk.Notebook(frame_main_notebook, width = 200, height = 100)
main_notebook.pack(side = TOP, expand = 1, fill = 'both')
#first tab
frame_one = ttk.Frame(main_notebook, width = 200, height = 100)
frame_one.pack(side = TOP)
main_notebook.add(frame_one, text = '    tab one    ')
ttk.Label(frame_one, text = "this is inside of tab one").pack()
#second tab
frame_two = ttk.Frame(main_notebook, width = 200, height = 100)
frame_two.pack(side = TOP)
ttk.Label(frame_two, text = "this is inside of tab two").pack()
main_notebook.add(frame_two, text = '    tab two    ')
    
sv_ttk.set_theme('light')

root.mainloop()