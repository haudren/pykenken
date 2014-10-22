#!/usr/bin/env python

import Tkinter as tk
import tkSimpleDialog
import kenken

class Kengui(object):

  def __init__(self, master, size):
    self.master = master
    self.kenken = kenken.Kenken(size)
    self.labels = [tk.Label(self.master, highlightbackground='black', highlightthickness=1,\
        height=2, width=3, text=" ") for i in range(size**2)]
    self.selected = []
    self.color_index = 0
    self.colors = ['#e8e2d5', '#fbda7e', '#e2e2e2', '#9ee7ff', '#99accb', '#afaba2', '#c0a96b', '#d7d7d7', '#00b4ff', '#cdd8ea', '#b5aa94', '#cba81a', '#00ddff', '#97d5ff', '#a7abb4', '#e1d0aa', '#ffd91c', '#00c7ff', '#7daeec']

    self.default_bg = root.cget('bg')

    master.bind("<Escape>", self.clear_selection)
    master.bind("<Return>", self.create_region)
    master.bind("<F1>", self.solve)

    for i, label in enumerate(self.labels):
      label.grid_propagate(0)
      label.grid(row=i/size, column=i%size)
      label.bind("<Button-1>", self.add_selection)

  def add_selection(self, event):
    index = -1
    for i, label in enumerate(self.labels):
      if label == event.widget:
        label['background'] = 'white'
        index = i
        break

    self.selected.append(index)
    print self.selected

  def clear_selection(self, event):
    for index in self.selected:
      self.clear_label_format(index)
    self.selected = []
    print "Cleared selection"

  def clear_label_format(self, index):
    if self.labels[index]['background'] == 'white':
      self.labels[index]['background'] = self.default_bg

  def create_region(self, event):
    if not self.selected:
      return

    op = tkSimpleDialog.askstring("Operation", "Please enter one of +-/*")
    value = tkSimpleDialog.askinteger("Total", "Please enter desired result")
    self.kenken.add_region([(i/6, i%6) for i in self.selected], op, value)

    for index in self.selected:
      self.labels[index]['background'] = self.colors[self.color_index]

    self.color_index += 1
    self.color_index %= len(self.colors)

    self.clear_selection(None)

  def solve(self, event):
    self.kenken.solve()
    for res, label in zip(self.kenken.result, self.labels):
      label['text'] = str(res)

if __name__ == '__main__':
  root = tk.Tk()
  gui = Kengui(root, 6)
  root.mainloop()
