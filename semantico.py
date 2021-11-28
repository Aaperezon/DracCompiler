class semantico:
    
  def __init__(self, tabla):
    self.tabla = tabla
    self.run()

  def run(self):
    self.checkRule2()
    self.checkRule5()
    self.checkRule6()
    self.checkRule11()
    
    
  def checkRule2(self):
    check = False
    for row in self.tabla:
      if row["name"] == "main":
        check = True
    if check == False:
      print(f"ERROR: No function 'main'")
      exit()

  def checkRule5(self):
    for index,row in enumerate(self.tabla):
      for index2,aux in enumerate(self.tabla):
        if index != index2:
          if row['scope'] == '0' and row['tipo'] == 'id': 
            if row['name'] == aux['name'] and row['param'] == aux['param'] and row['scope'] == aux['scope'] and row['param'] != True and row['tipo'] == aux['tipo']:
              print(f"ERROR: Two variables with the same name '{aux['name']}' in line {aux['line']}  ")
              exit()

  def checkRule6(self):
    for index,row in enumerate(self.tabla):
      for index2,aux in enumerate(self.tabla):
        if index != index2:
          if row['tipo'] == 'fun' and aux['tipo'] == 'fun' and row['name'] == aux['name'] and row['scope'] == '0' and aux['scope'] == '0':
            print(f"ERROR: Two functions with the same name '{aux['name']}' in line {aux['line']}  ")
            exit()

  
            
  def checkRule11(self):
    for index,row in enumerate(self.tabla):
      for index2,aux in enumerate(self.tabla):
        if index != index2:
          if row['name'] == aux['name'] and  row['param'] == True and row['block'] == aux['block']: 
            print(f"ERROR: Invalid declaration of variable, it exists as parameter '{aux['name']}' in line {aux['line']}  ")
            exit()


    