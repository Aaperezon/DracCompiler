from lexer import Lexer
from sintactico import sintactico
from cursor import cursor
from anytree import Node, RenderTree
from semantico import semantico
import sys

# sys.stdout  = open("randomfile.txt", "w")
try: 
  if len(sys.argv) == 2:
    content = open(sys.argv[1], 'r').read()
    lexer = Lexer(content)
    lexer = lexer.tokenizar()
    for lex in lexer:
        # print(f"| {lex.valor}  \t {lex.token}|")
        pass

    pointer = cursor(lexer)
    ejemplo = sintactico(pointer)
    ejemplo_run,aumentada,tabla = ejemplo.run() 
    # print(ejemplo_run)
    # print(aumentada)
    # print(tabla)
    # print("\n////TABLA DE SIMBOLOS")
    for id in tabla:
      print(f" {id} ")
      pass
    #ARBOL AROBOL
    # print("\n////ARBOL SINTACTICO")
    # for pre, fill, node in RenderTree(aumentada):
    #   print("%s%s" % (pre, node.name))
  
    semantico = semantico(tabla)
    print("COMPILATION SUCCESSFUL")
    
  else:
    while True :
      comando = input('> ')
      lexer = Lexer(comando)
      tokens = lexer.tokenizar()
      #for token in tokens:
          #print(token)
      pointer = cursor(lexer)
      ejemplo = sintactico(pointer)
      ejemplo_run,aumentada,tabla = ejemplo.run() 
      for id in tabla:
        # print(f" {id} ")
        pass
      semantico = semantico(tabla)
      print("COMPILATION SUCCESSFUL")

    
except KeyboardInterrupt :
  print('\b\Adios')

# sys.stdout.close()