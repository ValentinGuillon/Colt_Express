from tkinter import *
from typing import Literal


def destroyWidgets(widgets:list[Widget]):
    for widget in widgets:
        widget.destroy()





def configWidgets(window, widgetType:Literal['Button', 'Label', 'Entry'], widgets:list[Widget]):
    if widgetType == 'Button':
        for btn in widgets:
            btn.config(highlightthickness=0, border=2, bg=window.WIDGET_COLORS['train'], fg=window.WIDGET_COLORS['road'], activebackground=window.WIDGET_COLORS['road'], activeforeground=window.WIDGET_COLORS['train'], disabledforeground=window.WIDGET_COLORS['moutainShadow'])

    elif widgetType == 'Label':
        for label in widgets:
            label.config(bg=window.WIDGET_COLORS['road'], fg=window.WIDGET_COLORS['train'])

    elif widgetType == 'Entry':
        for entry in widgets:
            entry.config(border=1, highlightthickness=0, justify='right', width=5, bg=window.WIDGET_COLORS['road'], fg=window.WIDGET_COLORS['train'])
    
    else:
        print(f'ERROR: in configWidgets:\n    "{widgetType}" doesnt exist (allowed: "Button", "Label", "Entry")')
        exit()







def configActionButton(window, phase:Literal['preparation', 'action']):
    if phase == 'preparation':
        window.btnAction.config(state='disabled', border=0, bg=window.WIDGET_COLORS['redLight'], disabledforeground=window.WIDGET_COLORS['road'])
    elif phase == 'action':
        window.btnAction.config(state='normal', border=2, bg=window.WIDGET_COLORS['train'], disabledforeground=window.WIDGET_COLORS['moutainShadow'], fg=window.WIDGET_COLORS['road'], activebackground=window.WIDGET_COLORS['road'], activeforeground=window.WIDGET_COLORS['train'])
    else:
        print(f'ERROR: in configActionButton:\n   "{phase}" doesnt exist (allowed: "preparation", "action")')
        exit()


