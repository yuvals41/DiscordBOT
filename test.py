class Student:
  def __init__(self,name,year):
    self.name = name
    self.year = year
    self.grades = list()
  def add_grade(self, grade):
    if(type(grade)==type(Grade)):
      self.grade = grade
roger = Student("Roger van der Weyden", 10)
sandro = Student("Sandro Botticelli", 12)
pieter = Student("Pieter Bruegel the Elder", 8)
class Grade():
  minimum_passing = 65
  def __init__(self,score):
    self.score = score
print(type(Grade))