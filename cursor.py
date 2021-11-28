class cursor:
    def  __init__(self, input_list):
        # print(list_tokens)
        self.input_list = input_list
        self.pointer = 0

    def getToken(self):
        return str(self.input_list[self.pointer].token)

    def getScope(self):
        return str(self.input_list[self.pointer].scope)

    def getValue(self):
        return str(self.input_list[self.pointer].valor)
    def getLine(self):
        return str(self.input_list[self.pointer].linea)
    def getObjectToken(self):
        return self.input_list[self.pointer]
    def getPos(self):
        return str(self.input_list[self.pointer].pos)
    def getLastObject(self):
        return self.input_list[self.pointer-1]
    def getTokenIfErrorExistsParam(self):
        return str(self.input_list[self.pointer].linea), str(self.input_list[self.pointer].pos),str(self.input_list[self.pointer].scope)
    def getBlock(self):
        return str(self.input_list[self.pointer].block)
    def move(self):
        self.pointer+=1


if __name__ == "__main__":
  from lexer import Lexer
  import sys
  from sintactico import sintactico
  
  content = open(sys.argv[1], 'r').read()
  lexer = Lexer(content)
  lexer = lexer.tokenizar()
  for lex in lexer:
      # print(f"{lex.valor}  \t {lex.token} ")
      pass

  pointer = cursor(lexer)
  ejemplo = sintactico(pointer)
  ejemplo.run()


  # print(pointer.getValue())
  # print(pointer.getTokenPosition())
