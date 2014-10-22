#!/usr/bin/env python

import Tkinter as tk
import tkSimpleDialog
import kenken

class Kengui(object):

  def __init__(self, master, size):
    self.master = master
    self.kenken = kenken.Kenken(size)
    self.labels = [tk.Label(self.master, highlightbackground='black', highlightthickness=1,\
        text=str(i)) for i in range(size**2)]
    self.selected = []

    master.bind("<Escape>", self.clear_selection)
    master.bind("<Return>", self.create_region)
    master.bind("<F1>", self.solve)

    for i, label in enumerate(self.labels):
      label.grid(row=i/size, column=i%size)
      label.bind("<Button-1>", self.add_selection)

  def add_selection(self, event):
    index = -1
    for i, label in enumerate(self.labels):
      if label == event.widget:
        index = i
        break

    self.selected.append(index)
    print self.selected

  def clear_selection(self, event):
    self.selected = []
    print "Cleared selection"

  def create_region(self, event):
    if not self.selected:
      return

    op = tkSimpleDialog.askstring("Operation", "Please enter one of +-/*")
    value = tkSimpleDialog.askinteger("Total", "Please enter desired result")
    self.kenken.add_region([(i/6, i%6) for i in self.selected], op, value)
    self.clear_selection(None)

  def solve(self, event):
    self.kenken.solve()
    for res, label in zip(self.kenken.result, self.labels):
      label['text'] = str(res)

if __name__ == '__main__':
  root = tk.Tk()
  gui = Kengui(root, 2)
  root.mainloop()
