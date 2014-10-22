#!/usr/bin/env python
import itertools
from subprocess import call

class Region(object):
  def __init__(self, coords, op, result):
    self.squares = coords
    self.operation = op
    self.result = result

  def constraint(self):
    zs = map(lambda x: 'Z'+str(x[0])+str(x[1]), self.squares)
    if self.operation == '-' or self.operation == '/':
      perms = itertools.permutations(zs)
      ops = []
      for perm in perms:
        ops.append(self.operation.join(perm)+'#='+str(self.result))
      line = ' #\\/ '.join(ops)
    else:
      line = self.operation.join(zs)+'#='+str(self.result)
    return line

  def __str__(self):
    return self.operation.join(map(str, self.squares)) + ' = ' + str(self.result)

class Kenken(object):
  def __init__(self, size):
    self.size = size
    self.regions = []

  def add_region(self, coords, op, result):
    self.regions.append(Region(coords, op, result))

  def constraints(self):
    return self.global_constraints()+map(lambda x: x.constraint(), self.regions)

  def global_constraints(self):
    constraints = []
    zs = self.vars()
    all_vars = itertools.chain.from_iterable(zs)
    constraints.append(self.array(all_vars)+' ins 1..'+str(self.size))

    for row in zs:
      constraints.append('all_different('+self.array(row)+')')

    for column in zip(*zs):
      constraints.append('all_different('+self.array(column)+')')

    return constraints

  def array(self, vars):
    return '['+','.join(vars)+']'

  def vars(self, columns=None, rows=None):
    if columns is None:
      columns = range(self.size)

    if rows is None:
      rows = range(self.size)

    zs = []
    for x in rows:
      row = []
      for y in columns:
        row.append('Z'+str(x)+str(y))
      zs.append(row)

    return zs

  def to_prolog(self):
    txt = self.header()+\
    'puzzle(%s):-' % self.array(itertools.chain.from_iterable(self.vars()))+'\n'+\
    ',\n'.join(self.constraints())+'.\n\n'+\
    self.footer()
    return txt

  def header(self):
    return '#!/usr/bin/env swipl\n:-use_module(library(clpfd)).\n:-initialization main.\n\n'

  def footer(self):
    return "main :- puzzle(L), label(L), format('~w~n', [L]), halt."

  def solve(self):
    #Generate prolog code
    fpl = file('puzzle.pl', 'w')
    fpl.write(self.to_prolog())
    fpl.close()

    #Write result
    fpout = file('result.txt', 'w')
    call("./puzzle.pl", stdout=fpout)
    fpout.close()
    fpout = file('result.txt', 'r')

    self.result = eval(fpout.read())

  def __str__(self):
    return '\n'.join(map(str, self.regions))

if __name__ == '__main__':
  puzzle = Kenken(6)
  puzzle.add_region([(0,0), (1,0)], '+', 11)
  puzzle.add_region([(0,1), (0,2)], '/', 2)
  puzzle.add_region([(1,1), (1,2)], '-', 3)
  puzzle.add_region([(0,3), (1,3)], '*', 20)
  puzzle.add_region([(0,4), (0,5), (1,5), (2,5)], '*', 6)
  puzzle.add_region([(1,4), (2,4)], '/', 3)
  puzzle.add_region([(2,0), (2,1), (3,0), (3,1)], '*', 240)
  puzzle.add_region([(2,2), (2,3)], '*', 6)
  puzzle.add_region([(4,0), (4,1)], '*', 6)
  puzzle.add_region([(3,2), (4,2)], '*', 6)
  puzzle.add_region([(3,3), (4,3), (4,4)], '+', 7)
  puzzle.add_region([(3,4), (3,5)], '*', 30)
  puzzle.add_region([(5,0), (5,1), (5,2)], '+', 8)
  puzzle.add_region([(5,3), (5,4)], '/', 2)
  puzzle.add_region([(4,5), (5,5)], '+', 9)

  print puzzle
  puzzle.solve()
