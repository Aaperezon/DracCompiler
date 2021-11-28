from anytree import Node, RenderTree
class sintactico:
  def __init__(self, pointer):
    self.pointer = pointer
    self.tabla = []
  def run(self):
    return self.aumentada()
    #return False
  def toReturn(self, return1, return2):
    if return1 == return2:
      return return1 
    if return2 is None:    
        return return1
    if return1 is None:            
        return return2
    elif return1 == 'lit-int':
      if return2 == 'lit-bool' or return2=='lit-char':
        return 'lit-int'
      elif return2 == 'lit-str':
        return return2
    elif return1== 'lit-char':
      if return2=='lit-int' or return2=='lit-str':
        return return2
      elif return2 == 'lit-bool':
        return return1
    elif return1=='lit-bool':
      if return2=='lit-int' or return2=='lit-str':
        return return2
      elif return2 == 'lit-char':
        return return1
    elif return1=='lit-str':
      return return1
    
    


  def assignType(self,to_assign,assign):
    # print(f"Want to assign '{to_assign}' the value of {assign}")
    for index,row in enumerate(self.tabla):
      for index2,aux in enumerate(self.tabla):
        if index != index2:
          if row['name'] == aux['name'] and row['scope'] == aux['scope'] and row['param'] == aux['param'] and row['tipo'] != 'fun' and aux['param'] != True:
            print(f"ERROR: Can not reassign variable: '{aux['name']}'  in line: {aux['line']}")
            exit()
      if row["tipoDato"] == None and row["name"] == to_assign and row['param'] == False:
        self.tabla[index]["tipoDato"] = assign
        
        
  def assignBlock(self, to_assign, assign):
    for index,row in enumerate(self.tabla):
      if row['name'] == to_assign and (row['param'] == True or row['tipo'] == 'fun'):
        self.tabla[index]['block'] = assign
        
  def modifyBlockParameters(self):
    for index,row in enumerate(self.tabla):
      for index2,aux in enumerate(self.tabla):
        if index != index2:
          if row['line'] == aux['line'] and row['tipo'] == 'fun' and aux['param'] == True:
            self.tabla[index2]['block']=row['block']

  def assignNumParam(self, to_assign, assign):
    # print(f"Want to assign '{to_assign}' the value of {assign}")
    for index,attribute in enumerate(self.tabla):
      if attribute["cantParam"] == None and attribute["name"] == to_assign and attribute["tipo"] == 'fun':
        self.tabla[index]["cantParam"] = assign


  def assignIfParam(self, to_assign, assign):
    for index,attribute in enumerate(self.tabla):
      if attribute["param"] == False and attribute["name"] == to_assign:
        self.tabla[index]["param"] = assign
        
  def checkCantParam(self,to_check, cant):
    for index,attribute in enumerate(self.tabla):
      if attribute["name"] == to_check.valor and attribute["tipo"] == 'fun':
        if attribute["cantParam"] != cant and  attribute['cantParam'] != None:
          print(f"ERROR: invalid number of parameters for '{attribute['name']}' in line {self.pointer.getLine()} ")
          exit()

  def checkIfVarExists(self,to_check):
    exists = False
    for index,attribute in enumerate(self.tabla):
      if attribute["name"] == to_check:
        exists = True
    if exists == False:
      print(f"ERROR: variable '{to_check}' not declared in line {self.pointer.getLine()}")
      exit()
  def error(self, esperados, linea, pos, scope):
    if linea != '-1':
      print("ERROR linea", linea, "pos: ", pos,"scope: ",scope, "se esperaba:")
      for token in esperados:
        print(token,end="|")
        pass
      print()
      exit()

  def consume2(self,token,parent):
    if(token==self.pointer.getToken()):
      parent = Node(str(token), parent=parent)
      self.pointer.move()
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["ERROR: "],linea,pos,scope)

  def addToTable(self,tipo,name,scope, param=False, line=0, tipo_dato = "lit-int"):
    tokencito = None
    if tipo == "fun":
      if scope == 0:
        tokencito = {'name':name,'tipo':tipo, 'scope':scope,'cantParam':None,'tipoDato':tipo_dato,  'param': param, 'line':line, 'block':self.pointer.getBlock() }
      else:
        tokencito = {'name':name,'tipo':tipo, 'scope':scope,'cantParam':None,'tipoDato':tipo_dato, 'param': param, 'line':line, 'block':self.pointer.getBlock()}
    else:
      if scope == 0:
        tokencito = {'name':name,'tipo':tipo, 'scope':scope,'cantParam':None,'tipoDato':None,  'param': param, 'line':line, 'block':self.pointer.getBlock()}
      else: 
        tokencito = {'name':name,'tipo':tipo, 'scope':scope,'cantParam':None,'tipoDato':None,  'param':param, 'line':line, 'block':self.pointer.getBlock()}
    self.tabla.append(tokencito)
  
  def buscarId(self, token, tipo):
    for id in self.tabla:
      if id['token'] == token and id['tipo'] == tipo:
        return id

  def aumentada(self):
    aumentada = Node("Aumentada")
    #print("Aumentada()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    self.pointer.getToken()
    if self.pointer.getToken() == '$' or  self.pointer.getToken() == 'var' or  self.pointer.getToken() == 'id':
      self.program(aumentada)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["aumentada ->","id","var","$"],linea,pos,scope)
    self.modifyBlockParameters()
    return False, aumentada, self.tabla

  def program(self,parent):
    parent = Node("Program", parent=parent)
    #print("program()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())    
    if self.pointer.getToken() == '$' or self.pointer.getToken() == 'var' or self.pointer.getToken() == 'id':
      self.def_list(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["program ->","id","var","$"],linea,pos,scope)
    
    

  def def_list(self,parent):    
    parent = Node("Def_list", parent=parent)
    #print("def_list()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == '$' or  self.pointer.getToken() == 'var' or  self.pointer.getToken() == 'id':
      self.def_list_p(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["def_list ->","id","var","$"],linea,pos,scope) ##COMO ESTA
    


  def def_list_p(self,parent):
    parent = Node("Def_list_p", parent=parent) 
    #print("def_list_p()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == '$':
      return
    elif self.pointer.getToken() == 'var' or self.pointer.getToken() == 'id':
      self.def_drac(parent)
      self.def_list_p(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["def_list_p ->","id","var","$"],linea,pos,scope)
    

    
  def def_drac(self,parent):
    parent = Node("Def_drac", parent=parent)
    #print("def_drac()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == 'var':
      self.var_def(parent)
    elif self.pointer.getToken() == 'id':
     self.fun_def(parent)
    else:
      #Antes habia una funcion return false
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["def_drac ->","id","var"],linea,pos,scope)

    
  def var_def(self,parent):
    parent = Node("Var_def", parent=parent)
    #print("var_def()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == 'var':
      self.consume2("var",parent)
      self.var_list(parent)
      self.consume2(";",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["var_def ->","var"],linea,pos,scope)

  def var_list(self,parent):
    parent = Node("Var_list", parent=parent)
    #print("var_list()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == 'id':
      self.id_list(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["var_list ->","id"],linea,pos,scope)
    
  def id_list(self,parent, counter=0):
    parent = Node("Id_list", parent=parent)
    #print("id_list()\t\t\t\t", self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == 'id':
      if self.pointer.getLastObject().token == "(":
        self.addToTable(name=self.pointer.getValue(), tipo='id',scope=self.pointer.getScope(),param=True,line=self.pointer.getLine())
      else:
        self.addToTable(name=self.pointer.getValue(), tipo='id',scope=self.pointer.getScope(),line=self.pointer.getLine())
      # tokencito = {'token':self.pointer.getValue(), 'tipo':'id', 'scope':self.pointer.getScope(),'cantParam':'', 'tipoDato': ''  }
      # self.tabla.append(tokencito)
      counter += 1
      self.consume2("id",parent)
      counter = self.id_list_cont(parent, counter) 
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["id_list ->","id"],linea,pos,scope)
    return counter


  def id_list_cont(self,parent, counter=0):
    parent = Node("Id_list_cont", parent=parent)
    #print("id_lis_cont()\t\t\t\t",self.pointer.getValue(), self.pointer.getToken())
    if self.pointer.getToken() == ';' or  self.pointer.getToken() == ')':
      return counter
    elif self.pointer.getToken() == ',':
      self.consume2(",",parent)
      self.addToTable(name=self.pointer.getValue(), tipo='id', scope=self.pointer.getScope(), param = True,line=self.pointer.getLine())
      # tokencito = {'token':self.pointer.getValue(), 'tipo':'id', 'scope':self.pointer.getScope() ,'cantParam':'', 'tipoDato': '' }
      # self.tabla.append(tokencito)
      counter += 1
      self.consume2("id",parent)
      counter = self.id_list_cont(parent,counter)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["id_list_cont -> ",";",",","id",")"],linea,pos,scope)
    return counter

  def fun_def(self,parent):
    parent = Node("Fun_def()", parent=parent)  
    #print("fun_def()")
    if self.pointer.getToken() == 'id':
      id = self.pointer.getObjectToken()
      self.consume2("id",parent)
      self.consume2("(",parent)
      self.addToTable(name= id.valor, tipo='fun', scope=self.pointer.getScope(),line=self.pointer.getLine())
      numparam = self.param_list(parent)
      self.assignNumParam(id.valor, numparam)
      self.consume2(")",parent)
      self.consume2("{",parent)
      self.assignBlock(id.valor, self.pointer.getBlock())
      self.var_def_list(parent)
      self.stmt_list(parent)
      # tokencito = {'token':id.valor, 'tipo':'fun', 'scope':self.pointer.getScope() ,'cantParam':'', 'tipoDato': ''}
      # self.tabla.append(tokencito)
      self.consume2("}",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["fun_def ->" ,"id","(",")","{","}"],linea,pos,scope)
    
  def param_list(self,parent ):
    parent = Node("Param_list", parent=parent) 
    #print("param_list()\t\t\t\t",self.pointer.getToken())
    if self.pointer.getToken() == 'id':
      return self.id_list(parent, 0)
    elif self.pointer.getToken() == ')':
      return
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["param_list ->","id",")"],linea,pos,scope)

  def var_def_list(self,parent):
    parent = Node("Var_def_list", parent=parent)  
    #print("var_def_list()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == 'var' or self.pointer.getToken() == ';' or self.pointer.getToken() == 'id' or self.pointer.getToken() == '}' or self.pointer.getToken() == 'inc' or self.pointer.getToken() == 'dec' or self.pointer.getToken() == 'if' or self.pointer.getToken() == 'while' or self.pointer.getToken() == 'do' or self.pointer.getToken() == 'break' or self.pointer.getToken() == 'return':
      self.var_def_list_p(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["var_def_list ->","id","var",";","}","inc","dec","if","while","do","break","return"],linea,pos,scope)
    return True

  def var_def_list_p(self,parent):
    parent = Node("Var_def_list_p", parent=parent)    
    #print("var_def_list_p()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == 'var':
      self.var_def(parent)
      self.var_def_list_p(parent)
    elif self.pointer.getToken() == ';' or self.pointer.getToken() == 'id' or self.pointer.getToken() == '}' or self.pointer.getToken() == 'inc' or self.pointer.getToken() == 'dec' or self.pointer.getToken() == 'if' or self.pointer.getToken() == 'while' or self.pointer.getToken() == 'do' or self.pointer.getToken() == 'break' or self.pointer.getToken() == 'return':
      return
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["var_def_list_p ->","var",";","id","}","inc","dec","if","while","do","break","return"],linea,pos,scope)

  def stmt_list(self,parent,breakValid=False):
    parent = Node("Stmt_list", parent=parent)  
    #print("stmt_list()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == ';' or self.pointer.getToken() == 'id' or self.pointer.getToken() == '}' or self.pointer.getToken() == 'inc' or self.pointer.getToken() == 'dec' or self.pointer.getToken() == 'if' or self.pointer.getToken() == 'while' or self.pointer.getToken() == 'do' or self.pointer.getToken() == 'break' or self.pointer.getToken() == 'return':
      self.stmt_list_p(parent, breakValid)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["stmt_list ->",";","id","}","inc","dec","if","while","do","break","return"],linea,pos,scope)

  def stmt_list_p(self,parent,breakValid=False):
    parent = Node("Stmt_list_p", parent=parent)  
    #print("stmt_list_p()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == ';' or self.pointer.getToken() == 'id' or self.pointer.getToken() == 'inc' or self.pointer.getToken() == 'dec' or self.pointer.getToken() == 'if' or self.pointer.getToken() == 'while' or self.pointer.getToken() == 'do' or self.pointer.getToken() == 'break' or self.pointer.getToken() == 'return':
      self.stmt(parent,breakValid)
      self.stmt_list_p(parent,breakValid)
    elif self.pointer.getToken() == '}':
      return
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["stmt_list_p ->","id","var",";","}","inc","dec","if","while","do","break","return"],linea,pos,scope)
    
  def stmt(self,parent,breakValid=False):
    parent = Node("Stmt", parent=parent)  
    #print("stmt()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == ';':
      self.consume2(self.pointer.getToken(),parent)
      self.stmt_empty(parent)
    elif self.pointer.getToken() == 'id':
      id = self.pointer.getObjectToken()
      if self.pointer.getValue() == "printi":
        self.addToTable(name=self.pointer.getValue(), tipo='fun',scope=self.pointer.getScope(),line=self.pointer.getLine() )
        self.assignNumParam(to_assign = self.pointer.getValue(), assign = 1)
      elif self.pointer.getValue() == "printc":
        self.addToTable(name=self.pointer.getValue(), tipo='fun',scope=self.pointer.getScope(),line=self.pointer.getLine() )
        self.assignNumParam(to_assign = self.pointer.getValue(), assign = 1)
      elif self.pointer.getValue() == "prints":
        self.addToTable(name=self.pointer.getValue(), tipo='fun',scope=self.pointer.getScope(),line=self.pointer.getLine() )
        self.assignNumParam(to_assign = self.pointer.getValue(), assign = 1)
      elif self.pointer.getValue() == "println":
        self.addToTable(name=self.pointer.getValue(), tipo='fun',scope=self.pointer.getScope(),line=self.pointer.getLine() )
        self.assignNumParam(to_assign = self.pointer.getValue(), assign = 0)
      elif self.pointer.getValue() == "readi":
        self.addToTable(name=self.pointer.getValue(), tipo='fun',scope=self.pointer.getScope(),line=self.pointer.getLine() )
        self.assignNumParam(to_assign = self.pointer.getValue(), assign = 0)
      elif self.pointer.getValue() == "reads":
        self.addToTable(name=self.pointer.getValue(), tipo='fun',scope=self.pointer.getScope(),line=self.pointer.getLine() )
        self.assignNumParam(to_assign = self.pointer.getValue(), assign = 0)
      elif self.pointer.getValue() == "new":
        self.addToTable(name=self.pointer.getValue(), tipo='fun',scope=self.pointer.getScope(),line=self.pointer.getLine() )
        self.assignNumParam(to_assign = self.pointer.getValue(), assign = 1)
      elif self.pointer.getValue() == "size":
        self.addToTable(name=self.pointer.getValue(), tipo='fun',scope=self.pointer.getScope(),line=self.pointer.getLine() )
        self.assignNumParam(to_assign = self.pointer.getValue(), assign = 1)
      elif self.pointer.getValue() == "add":
        self.addToTable(name=self.pointer.getValue(), tipo='fun',scope=self.pointer.getScope(),line=self.pointer.getLine() )
        self.assignNumParam(to_assign = self.pointer.getValue(), assign = 2)
      elif self.pointer.getValue() == "get":
        self.addToTable(name=self.pointer.getValue(), tipo='fun',scope=self.pointer.getScope(),line=self.pointer.getLine() )
        self.assignNumParam(to_assign = self.pointer.getValue(), assign = 2)
      elif self.pointer.getValue() == "set":
        self.addToTable(name=self.pointer.getValue(), tipo='fun',scope=self.pointer.getScope(),line=self.pointer.getLine() )
        self.assignNumParam(to_assign = self.pointer.getValue(), assign = 3)
      self.consume2("id",parent)
      counter = self.stmt_p(parent, id, counter = 0)
      if counter==None:
        self.checkCantParam(id, 0)
      elif counter != -1:
        self.checkCantParam(id, counter)
      elif counter==-1:
        self.checkIfVarExists(id.valor)
    elif self.pointer.getToken() == 'inc':
      self.stmt_incr(parent)
    elif self.pointer.getToken() == 'dec':
      self.stmt_decr(parent)
    elif self.pointer.getToken() == 'if':
      self.stmt_if(parent,breakValid)
    elif self.pointer.getToken() == 'while':
      self.stmt_while(parent)
    elif self.pointer.getToken() == 'do':
      self.stmt_do_while(parent)
    elif self.pointer.getToken() == 'break':
      self.stmt_break(parent,breakValid)
    elif self.pointer.getToken() == 'return':
      self.stmt_return(parent)
    else: 
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["stmt ->","id",";","}","inc","dec","if","while","do","break","return"],linea,pos,scope)

  def stmt_p(self,parent, id = None, counter=-1):
    parent = Node("Stmt_p", parent=parent)  
    #print("stmt_p()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == '(':
      self.consume2("(",parent)
      if counter == -1:
        counter = self.expr_list(parent)
      else:
        counter = self.expr_list(parent,counter)
      self.consume2(")",parent)
      self.consume2(";",parent)
    elif self.pointer.getToken() == '=': 
      self.consume2("=",parent)
      #id = self.pointer.getObjectToken()
      counter = -1
      tipo = self.expr(parent)
      if self.pointer.getValue() == "readi":
        self.addToTable(name=self.pointer.getValue(), tipo='fun',scope=self.pointer.getScope(),line=self.pointer.getLine())
        self.assignNumParam(to_assign = self.pointer.getValue(), assign = 0)
      elif self.pointer.getValue() == "reads":
        self.addToTable(name=self.pointer.getValue(), tipo='fun',scope=self.pointer.getScope(),line=self.pointer.getLine(), tipo_dato="lit-str" )
        self.assignNumParam(to_assign = self.pointer.getValue(), assign = 0)
      elif self.pointer.getValue() == "get":
        self.addToTable(name=self.pointer.getValue(), tipo='fun',scope=self.pointer.getScope(),line=self.pointer.getLine())
        self.assignNumParam(to_assign = self.pointer.getValue(), assign = 2)
      elif self.pointer.getValue() == "size":
        self.addToTable(name=self.pointer.getValue(), tipo='fun',scope=self.pointer.getScope(),line=self.pointer.getLine() )
        self.assignNumParam(to_assign = self.pointer.getValue(), assign = 1)
      elif self.pointer.getValue() == "new":
        self.addToTable(name=self.pointer.getValue(), tipo='fun',scope=self.pointer.getScope(),line=self.pointer.getLine() )
        self.assignNumParam(to_assign = self.pointer.getValue(), assign = 1)
      self.assignType(id.valor, tipo)
      self.consume2(";",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["Stmt_p ->","(",")","=",";"],linea,pos,scope)
    return counter



  def stmt_incr(self,parent):
    parent = Node("Stmt_incr", parent=parent)  
    #print("stmt_incr()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == 'inc':
      self.consume2("inc",parent)
      self.consume2("id",parent)
      self.consume2(";",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["stmt_incr ->","inc","id",";"],linea,pos,scope)

  def stmt_decr(self,parent):
    #print("stmt_decr()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    parent = Node("Stmt_decr", parent=parent)
    if self.pointer.getToken() == 'dec':
      self.consume2("dec",parent)
      self.consume2("id",parent)
      self.consume2(";",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["stmt_incr ->","dec","id",";"],linea,pos,scope)
    
  def expr_list(self,parent,counter = -1):
    parent = Node("Expr_list()", parent=parent)
    #print("exor_list()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    to_return = None
    if self.pointer.getToken() == ')' or self.pointer.getToken() == ']':
      return
    elif self.pointer.getToken() == 'id' or self.pointer.getToken() == '(' or self.pointer.getToken() == '+' or self.pointer.getToken() == '-' or self.pointer.getToken() == 'not' or self.pointer.getToken() == '[' or self.pointer.getToken() == 'lit-bool' or self.pointer.getToken() == 'lit-int' or self.pointer.getToken() == 'lit-char' or self.pointer.getToken() == 'lit-str':
      if counter == -1:
        to_return = self.expr(parent)
        counter = self.expr_list_cont(parent)
      else:
        self.expr(parent)
        counter = self.expr_list_cont(parent, counter+1)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["expr_list ->","id","(","+","-","not","[","lit-bool","lit-int","lit-char","lit-str"],linea,pos,scope)
    return to_return if counter==-1 else counter


  def expr_list_cont(self,parent,counter = -1):
    parent = Node("Expr_list_cont", parent=parent)
    #print("expr_list_cont()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == ',':
      self.consume2(",",parent)
      counter += 1
      self.expr(parent)
      counter = self.expr_list_cont(parent,counter)
    elif self.pointer.getToken() == ')' or self.pointer.getToken() == ']': 
      return counter
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["expr_list_cont -> ",",","]",")"],linea,pos,scope)
    return counter


  def stmt_if(self,parent,breakValid=False):
    parent = Node("Stmt_if", parent=parent)
    #print("stmt_if()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == 'if':
      self.consume2("if",parent)
      self.consume2("(",parent)
      self.expr(parent)
      self.consume2(")",parent)
      self.consume2("{",parent)
      self.stmt_list(parent,breakValid)
      self.consume2("}",parent)
      self.else_if_list(parent,breakValid)
      self.elseT(parent,breakValid)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["stmt_if ->","if","(","{","}"],linea,pos,scope)

  def else_if_list(self,parent,breakValid=False):
    parent = Node("Else_if_list", parent=parent)
    #print("else_if_list()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == ';' or self.pointer.getToken() == 'id' or self.pointer.getToken() == '}' or self.pointer.getToken() == 'inc' or self.pointer.getToken() == 'dec' or self.pointer.getToken() == 'if' or self.pointer.getToken() == 'elif' or self.pointer.getToken() == 'else' or self.pointer.getToken() == 'while' or self.pointer.getToken() == 'do' or self.pointer.getToken() == 'break' or self.pointer.getToken() == 'return':
      self.else_if_list_p(parent,breakValid)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["else_if_list ->","id",";","}","inc","dec","if","elif","else","while","do","break","return"],linea,pos,scope)
    
  def else_if_list_p(self,parent,breakValid=False):
    parent = Node("Else_if_list_p", parent=parent)
    #print("else_if_list_p()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == ';' or self.pointer.getToken() == 'id' or self.pointer.getToken() == '}' or self.pointer.getToken() == 'inc' or self.pointer.getToken() == 'dec' or self.pointer.getToken() == 'if' or self.pointer.getToken() == 'else' or self.pointer.getToken() == 'while' or self.pointer.getToken() == 'do' or self.pointer.getToken() == 'break' or self.pointer.getToken() == 'return':
      return
    elif self.pointer.getToken() == 'elif':
      self.consume2("elif",parent)
      self.consume2("(",parent)
      self.expr(parent)
      self.consume2(")",parent)
      self.consume2("{",parent)
      self.stmt_list(parent,breakValid)
      self.consume2("}",parent)
      self.else_if_list_p(parent,breakValid)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["Else_if_list_p ->","elif","(",")","{","}","if","while","do","break","return"],linea,pos,scope)
    
  def elseT(self,parent,breakValid=False):
    parent = Node("ElseT", parent=parent)
    #print("elseT()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == ';' or self.pointer.getToken() == 'id' or self.pointer.getToken() == '}' or self.pointer.getToken() == 'inc' or self.pointer.getToken() == 'dec' or self.pointer.getToken() == 'if' or self.pointer.getToken() == 'while' or self.pointer.getToken() == 'do' or self.pointer.getToken() == 'break' or self.pointer.getToken() == 'return':
      return
    elif self.pointer.getToken() == 'else':
      self.consume2("else",parent)
      self.consume2("{",parent)
      self.stmt_list(parent,breakValid)
      self.consume2("}",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["elseT ->","else","{","id",";","}","inc","dec","if","while","do","break","return"],linea,pos,scope)
    
  def stmt_while(self,parent):
    parent = Node("Stmt_while", parent=parent)
    #print("stmt_while()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == 'while':
      self.consume2("while",parent)
      self.consume2("(",parent)
      self.expr(parent)
      self.consume2(")",parent)
      self.consume2("{",parent)
      self.stmt_list(parent, breakValid=True)
      self.consume2("}",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["stmt_while ->","while","(",")","{","}"],linea,pos,scope)
 
  def stmt_do_while(self,parent):
    parent = Node("Stmt_do_while", parent=parent)
    #print("stmt_do_while()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == 'do':
      self.consume2("do",parent)
      self.consume2("{",parent)
      self.stmt_list(parent, breakValid=True)
      self.consume2("}",parent)
      self.consume2("while",parent)
      self.consume2("(",parent)
      self.expr(parent)
      self.consume2(")",parent)
      self.consume2(";",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["stmt_do_while ->","do","{","}","while","(",")",";"],linea,pos,scope)
    
  def stmt_break(self,parent,valid =False):
    parent = Node("Stmt_break", parent=parent)
    if self.pointer.getToken() == 'break':
      if not valid:
        linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
        self.error(["ERROR: break can only be inside","while or do-while"],linea,pos,scope)
      self.consume2("break",parent)
      self.consume2(";",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["stmt_break ->","break",";"],linea,pos,scope)

  def stmt_return(self,parent):
    parent = Node("Stmt_return", parent=parent)
    #print("stmt_return()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == 'return':
      self.consume2("return",parent)
      self.expr(parent)
      self.consume2(";",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["stmt_return ->",";","return"],linea,pos,scope)
    return True

  def stmt_empty(self,parent):
    parent = Node("Stmt_empty", parent=parent)
    #print("stmt_empty()\t\t\t\t",self.pointer.getValue(), self.pointer.getToken() )
    if self.pointer.getToken() == ';':
      self.consume2(";",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["stmt_empty ->",";"],linea,pos,scope)
    
  def expr(self,parent):
    parent = Node("Expr", parent=parent)
    #print("expr()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    to_return = None
    if self.pointer.getToken() == 'id' or self.pointer.getToken() == '(' or self.pointer.getToken() == '+' or self.pointer.getToken() == '-' or self.pointer.getToken() == 'not' or self.pointer.getToken() == '[' or self.pointer.getToken() == 'lit-bool' or self.pointer.getToken() == 'lit-int' or self.pointer.getToken() == 'lit-char' or self.pointer.getToken() == 'lit-str':
      to_return = self.expr_or(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["expr ->","id","(","+","-","not","[","lit-bool","lit-int","lit-char","lit-str"],linea,pos,scope)
    return to_return


  def expr_or(self,parent):
    parent = Node("expr_or", parent=parent)
    #print("expr_or()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    to_return = None
    if self.pointer.getToken() == 'id' or self.pointer.getToken() == '(' or self.pointer.getToken() == '+' or self.pointer.getToken() == '-' or self.pointer.getToken() == 'not' or self.pointer.getToken() == '[' or self.pointer.getToken() == 'lit-bool' or self.pointer.getToken() == 'lit-int' or self.pointer.getToken() == 'lit-char' or self.pointer.getToken() == 'lit-str':
      to_return = self.expr_and(parent)
      self.expr_or_p(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["expr_or ->","id","(","+","-","not","[","lit-bool","lit-int","lit-char","lit-str"],linea,pos,scope)
    return to_return

  def expr_or_p(self,parent):
    parent = Node("Expr_or_p", parent=parent)
    #print("expr_or_p()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == ';' or self.pointer.getToken() == ',' or  self.pointer.getToken() == ']' or self.pointer.getToken() == ')':
      return
    elif self.pointer.getToken() == 'or':
      self.consume2("or",parent)
      self.expr_and(parent)
      self.expr_or_p(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["or"],linea,pos,scope)


  def expr_and(self,parent):
    parent = Node("Expr_and", parent=parent)
    #print("expr_and()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    to_return = None
    if self.pointer.getToken() == 'id' or self.pointer.getToken() == '(' or self.pointer.getToken() == '+' or self.pointer.getToken() == '-' or self.pointer.getToken() == 'not' or self.pointer.getToken() == '[' or self.pointer.getToken() == 'lit-bool' or self.pointer.getToken() == 'lit-int' or self.pointer.getToken() == 'lit-char' or self.pointer.getToken() == 'lit-str':
      to_return = self.expr_comp(parent)
      self.expr_and_p(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["expr_and ->","id","(","+","-","not","[","lit-bool","lit-int","lit-char","lit-str"],linea,pos,scope)
    return to_return

  def expr_and_p(self,parent):
    parent = Node("Expr_and_p", parent=parent)
    #print("expr_and_p()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == ';' or self.pointer.getToken() == ',' or self.pointer.getToken() == ')' or self.pointer.getToken() == 'or' or self.pointer.getToken() == ']':
      return
    elif self.pointer.getToken() == 'and':
      self.consume2("and",parent)
      self.expr_comp(parent)
      self.expr_and_p(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["expr_and_p ->",";",",",")","or","]","[","and"],linea,pos,scope)

    
  def expr_comp(self,parent):
    parent = Node("Expr_comp", parent=parent)
    #print("expr_comp()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    to_return = None
    if self.pointer.getToken() == 'id' or self.pointer.getToken() == '(' or self.pointer.getToken() == '+' or self.pointer.getToken() == '-' or self.pointer.getToken() == 'not' or self.pointer.getToken() == '[' or self.pointer.getToken() == 'lit-bool' or self.pointer.getToken() == 'lit-int' or self.pointer.getToken() == 'lit-char' or self.pointer.getToken() == 'lit-str':
      to_return = self.expr_rel(parent)
      self.expr_comp_p(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["expr_comp ->","id","(","+","-","not","[","lit-bool","lit-int","lit-char","lit-str"],linea,pos,scope)
    return to_return

  def expr_comp_p(self,parent):
    parent = Node("Expr_comp_p", parent=parent)
    #print("expr_comp_p()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == ';' or self.pointer.getToken() == ',' or self.pointer.getToken() == ')' or self.pointer.getToken() == 'or' or self.pointer.getToken() == 'and' or self.pointer.getToken() == ']':
      return
    elif self.pointer.getToken() == '==' or self.pointer.getToken() == '<>':
      self.op_comp(parent)
      self.expr_rel(parent)
      self.expr_comp_p(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["Expr_comp_p ->",";",",",")","or","and","]","==","<>"],linea,pos,scope)
    return True

  def op_comp(self,parent):
    parent = Node("Op_comp", parent=parent)
    #print("op_comp()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == '==':
      self.consume2("==",parent)
    elif self.pointer.getToken() == '<>':
      self.consume2("<>",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["op_comp ->","==","<>"],linea,pos,scope)
    return True

  def expr_rel(self,parent):
    #print("expr_rel()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    to_return = to_return2 = None
    if self.pointer.getToken() == 'id' or self.pointer.getToken() == '(' or self.pointer.getToken() == '+' or self.pointer.getToken() == '-' or self.pointer.getToken() == 'not' or self.pointer.getToken() == '[' or self.pointer.getToken() == 'lit-bool' or self.pointer.getToken() == 'lit-int' or self.pointer.getToken() == 'lit-char' or self.pointer.getToken() == 'lit-str':
      to_return = self.expr_add(parent)
      to_return2 = self.expr_rel_p(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["expr_rel ->","id","(","+","-","not","[","lit-bool","lit-int","lit-char","lit-str"],linea,pos,scope)
    return self.toReturn(to_return, to_return2)


  def expr_rel_p(self,parent):
    parent = Node("Expr_rel_p", parent=parent)
    #print("expr_rel_p()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    to_return = to_return2 = None
    if self.pointer.getToken() == ';' or self.pointer.getToken() == ',' or self.pointer.getToken() == ')' or self.pointer.getToken() == 'or' or self.pointer.getToken() == 'and' or self.pointer.getToken() == '==' or self.pointer.getToken() == '<>' or self.pointer.getToken() == ']':
      return
    elif self.pointer.getToken() == '<' or self.pointer.getToken() == '<=' or self.pointer.getToken() == '>' or self.pointer.getToken() == '>=':
      self.op_rel(parent)
      to_return = self.expr_add(parent)
      to_return2 = self.expr_rel_p(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["expr_rel_p ->",";",",",")","or","and","==","<>","]","<","<=",">="],linea,pos,scope)
    return self.toReturn(to_return,to_return2)


  def op_rel(self,parent):
    #print("op_rel()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == '<':
      self.consume2("<",parent)
    elif self.pointer.getToken() == '<=':
      self.consume2("<=",parent)
    elif self.pointer.getToken() == '>':
      self.consume2(">",parent)
    elif self.pointer.getToken() == '>=':
      self.consume2(">=",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["op_rel ->","<","<=",">",">="],linea,pos,scope)


  def expr_add(self,parent):
    #print("expr_add()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    to_return = to_return2 = None
    if self.pointer.getToken() == 'id' or self.pointer.getToken() == '(' or self.pointer.getToken() == '+' or self.pointer.getToken() == '-' or self.pointer.getToken() == 'not' or self.pointer.getToken() == '[' or self.pointer.getToken() == 'lit-bool' or self.pointer.getToken() == 'lit-int' or self.pointer.getToken() == 'lit-char' or self.pointer.getToken() == 'lit-str':
      to_return = self.expr_mul(parent)
      to_return2 = self.expr_add_p(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["expr_add ->","id","(","+","-","not","[","lit-bool","lit-int","lit-char","lit-str"],linea,pos,scope)
    return self.toReturn(to_return,to_return2)


  def expr_add_p(self,parent):
    parent = Node("Expr_add_p", parent=parent)
    #print("expr_add_p()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    to_return = None
    to_return2 = None
    if self.pointer.getToken() == ';' or self.pointer.getToken() == ',' or self.pointer.getToken() == ')' or self.pointer.getToken() == 'or' or self.pointer.getToken() == 'and' or self.pointer.getToken() == '==' or self.pointer.getToken() == '<>' or self.pointer.getToken() == '<' or self.pointer.getToken() == '<=' or self.pointer.getToken() == '>' or self.pointer.getToken() == '>=' or self.pointer.getToken() == ']':
      return
    elif self.pointer.getToken() == '+' or self.pointer.getToken() == '-':
      self.op_add(parent)
      to_return = self.expr_mul(parent)
      to_return2  =self.expr_add_p(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["expr_add_p->",";",",",")","or","and","==","<>","]","<","<=",">=","+","-"],linea,pos,scope)
    return self.toReturn(to_return, to_return2)
    
  
            
  def op_add(self,parent):
    parent = Node("Op_add", parent=parent)
    #print("op_add()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == '+':
      self.consume2("+",parent)
    elif self.pointer.getToken() == '-':
      self.consume2("-",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["+","-"],linea,pos,scope)


  def expr_mul(self,parent):
    parent = Node("Expr_mul", parent=parent)
    to_return = to_return2 = None
    #print("expr_mul()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == 'id' or self.pointer.getToken() == '(' or self.pointer.getToken() == '+' or self.pointer.getToken() == '-' or self.pointer.getToken() == 'not' or self.pointer.getToken() == '[' or self.pointer.getToken() == 'lit-bool' or self.pointer.getToken() == 'lit-int' or self.pointer.getToken() == 'lit-char' or self.pointer.getToken() == 'lit-str':
      to_return = self.expr_unary(parent)
      to_return2 = self.expr_mul_p(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["expr_mul ->","id","(","+","-","not","[","lit-bool","lit-int","lit-char","lit-str"],linea,pos,scope)
    return self.toReturn(to_return, to_return2)
    

  def expr_mul_p(self,parent):
    parent = Node("Expr_mul_p", parent=parent)
    to_return = to_return2 = None
    #print("expr_mul_p()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == ';' or self.pointer.getToken() == ',' or self.pointer.getToken() == ')' or self.pointer.getToken() == 'or' or self.pointer.getToken() == 'and' or self.pointer.getToken() == '==' or self.pointer.getToken() == '<>' or self.pointer.getToken() == '<' or self.pointer.getToken() == '<=' or self.pointer.getToken() == '>' or self.pointer.getToken() == '>=' or self.pointer.getToken() == '+' or self.pointer.getToken() == '-' or self.pointer.getToken() == ']':
      return 
    elif self.pointer.getToken() == '*' or self.pointer.getToken() == '/' or self.pointer.getToken() == '%':
      self.op_mul(parent)
      if self.pointer.getToken() == '/' and self.pointer.getValue() == '0':
        linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
        self.error(["Can not divide by 0"],linea,pos,scope)
      to_return = self.expr_unary(parent)
      to_return2 = self.expr_mul_p(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["expr_mul_p -> ",";",",",")","or","and","==","<>","]","<","<=",">=","*","/","%"],linea,pos,scope)
    return self.toReturn(to_return,to_return2)


  def op_mul(self,parent):
    parent = Node("Op_mul", parent=parent)
    #print("op_mul()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == '*':
      self.consume2("*",parent)
    elif self.pointer.getToken() == '/':
      self.consume2("/",parent)
    elif self.pointer.getToken() == '%':
      self.consume2("%",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["op_mul ->","*","/","%"],linea,pos,scope)



  def expr_unary(self,parent):
    parent = Node("expr_unary", parent=parent)
    #print("expr_unary()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    to_return = None
    if self.pointer.getToken() == 'id' or self.pointer.getToken() == 'lit-int' or self.pointer.getToken() == 'lit-char' or self.pointer.getToken() == 'lit-str' or self.pointer.getToken() == 'lit-bool' or self.pointer.getToken() == '[' or self.pointer.getToken() == '(':
      to_return = self.expr_primary(parent)
    elif self.pointer.getToken() == '+' or self.pointer.getToken() == '-' or self.pointer.getToken() == 'not':
      self.op_unary(parent)
      self.expr_unary(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["expr_unary ->","id","[","(","+","-","not","[","lit-bool","lit-int","lit-char","lit-str"],linea,pos,scope)
    return to_return

  def op_unary(self,parent):
    #print("op_unary()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    parent = Node("Stmt_p", parent=parent)
    if self.pointer.getToken() == '+':
      self.consume2("+",parent)
    elif self.pointer.getToken() == '-':
      self.consume2("-",parent)
    elif self.pointer.getToken() == 'not':
      self.consume2("not",parent)
    else: 
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["+","-","not"],linea,pos,scope)

      
  def expr_primary(self,parent):
    parent = Node("Expr_primary", parent=parent)
    #print("expr_primary()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    to_return = None
    if self.pointer.getToken() == 'id':
      self.consume2("id",parent)
      self.expr_primary_p(parent)
    elif self.pointer.getToken() == '(':
      self.consume2("(",parent)
      self.expr(parent)
      self.consume2(")",parent)
    elif self.pointer.getToken() == '[':
      to_return = self.array(parent)
    elif self.pointer.getToken() == 'lit-bool' or self.pointer.getToken() == 'lit-int' or self.pointer.getToken() == 'lit-char' or self.pointer.getToken() == 'lit-str':
      to_return = self.pointer.getToken()
      self.lit(parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["expr_primary ->","id","(",")","[","not","[","lit-bool","lit-int","lit-char","lit-str"],linea,pos,scope)
    return to_return

  def expr_primary_p(self,parent):
    parent = Node("Expr_primary", parent=parent)
    #print("expr_primary_p()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    if self.pointer.getToken() == ';' or self.pointer.getToken() == ',' or self.pointer.getToken() == ')' or self.pointer.getToken() == 'or' or self.pointer.getToken() == 'and' or self.pointer.getToken() == '==' or self.pointer.getToken() == '<>' or self.pointer.getToken() == '<' or self.pointer.getToken() == '<=' or self.pointer.getToken() == '>' or self.pointer.getToken() == '>=' or self.pointer.getToken() == '+' or self.pointer.getToken() == '-' or self.pointer.getToken() == '*' or self.pointer.getToken() == '/' or self.pointer.getToken() == '%' or self.pointer.getToken() == ']':
      return
    elif self.pointer.getToken() == '(':
      self.consume2("(",parent)
      self.expr_list(parent)
      self.consume2(")",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["expr_primary_p ->",";",",","(",")","or","and","==","<>","<","<=",">=","+","-","*","/","%","]"],linea,pos,scope)


  def array(self,parent):
    parent = Node("Self", parent=parent) 
    #print("array()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    to_return = None
    if self.pointer.getToken() == '[':
      self.consume2("[",parent)
      self.expr_list(parent)
      self.consume2("]",parent)
      to_return = "array"
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["array ->","[","]"],linea,pos,scope)
    return to_return

  def lit(self,parent):
    #print("lit()\t\t\t\t",self.pointer.getValue(),self.pointer.getToken())
    to_return = None
    if self.pointer.getToken() == 'lit-bool':
      to_return = "lit-bool"
      self.consume2("lit-bool",parent)
    elif self.pointer.getToken() == 'lit-int':
      to_return = "lit-int"
      if int(self.pointer.getValue()) <= 2147483647 and int(self.pointer.getValue()) >= -2147483648 :
        self.consume2("lit-int",parent)
      else:
        print(f"ERROR: Number must be 32-bit")
        exit()
    elif self.pointer.getToken() == 'lit-char':
      to_return = "lit-char"
      self.consume2("lit-char",parent)
    elif self.pointer.getToken() == 'lit-str':
      to_return = "lit-str"
      self.consume2("lit-str",parent)
    else:
      linea,pos,scope=self.pointer.getTokenIfErrorExistsParam()
      self.error(["lit ->","lit-bool","lit-int","lit-char","lit-str"],linea,pos,scope)
    return to_return

    
if __name__ == "__main__":
  from sintactico import sintactico
  from cursor import cursor
        
  ex = ["id", "(",  ")", "{", "var",  "id", ",", "id",  ";", "if", "(", "id", ">", "lit-int", ")", "{", "id", "=", "litInt", ";", "}", "}" ]
  #print(ex)
  pointer = cursor(ex)
  ejemplo = sintactico(ex,pointer)
  ejemplo_run,aumentada = ejemplo.Run() 
  # #print(ejemplo_run)
  # #print(type(ejemplo_run))
  #ARBOL AROBOL
  for pre, fill, node in RenderTree(aumentada):
    print("%s%s" % (pre, node.name))