from os import truncate
import string
import sys
import re
from enum import Enum
from copy import copy
def puntero_caracter ( pos, st ) :
    string_final = st + '\n'
    for i in range(len(st)) :
        string_final += '^' if i == pos.pos else ' '
    if pos.pos >= len(st) :
        string_final += '^'
    return string_final


#scope
lineaActual= 1;
Scope= 1;
#LISTO
key_words = [
    'and',  'else', 'or', 'break',
    'false', 'return', 'dec', 'if', 'true', 'do', 'inc',
    'var', 'elif', 'not','while'
]
extra_key_words = [ 'printi', 'printc', 'prints''println','ready', 'reads', 'new', 'size', 'add', 'get', 'set' ]

class TOKEN ( Enum ) :
    # Delimitadores (LISTOS) 
    DELIMITADOR      = 'DELIMITADOR'  #( ) { } [ ] ' '
    # Escapes
    ESCAPE           = 'ESCAPE' # \n \a \f \b \r \t \V \' \" \\ \ooo \x hh \x hhhh \?
    # Números (NOLISTOS) checar punto decimal o float   funciona make numbers linea463
    NUMERO            = 'NUMERO' # 0x[0-9a-fA-F]+ 0[0-7]+ 0b[0-1]+ [0-9]+ [0-9]+\.[0-9]+ [0-9]+\.[0-9]+f
    #CHAR linea 533 
    FLOAT   = 'FLOAT'
    HEXADECIMAL       = 'HEXADECIMAL'         # 0x[0-9a-fA-F]+
    OCTAL             = 'OCTAL'               # 0[0-7]+
    BINARIO           = 'BINARIO'             # 0b[0-1]+
    ENTERO            = 'ENTERO'              # [0-9]+
    REAL              = 'REAL'                # [0-9]+\.[0-9]+

    CHAR              = 'CHAR'
    STRING            = 'STRING'
    INCLUDE           = 'INCLUDE'
    DEFINE            = 'DEFINE'
    PRAGMA            = 'PRAGMA' #literal pragma 
    UNDEF             = 'UNDEF'
    LINE              = 'LINE'
    OPERADOR           = 'OPERADOR'   # + += ++ - -= -- * / *= /= % %= ! != ? < < <= >= << >> <<= >>= ^ ^=  ||  || |=  &  &=  
    IDENTIFICADOR       = 'IDENTIFICADOR'        # Identificador
    KEYWORD             = 'KEYWORD'      # Keyword
    ENDOFFILE           = 'ENDOFFILE'          # Necesario??


#Agregar operadores especiales
OPERADORES_ESPECIALES = {
    '=' : TOKEN.OPERADOR,
    '<' : TOKEN.OPERADOR,
    '>' : TOKEN.OPERADOR,
    '+' : TOKEN.OPERADOR,
    '-' : TOKEN.OPERADOR,
    '*' : TOKEN.OPERADOR,
    '/' : TOKEN.OPERADOR,
    '%' : TOKEN.OPERADOR
}


separadores = {
    '{'  : TOKEN.DELIMITADOR,
    '}'  : TOKEN.DELIMITADOR,
    '('  : TOKEN.DELIMITADOR,
    ')'  : TOKEN.DELIMITADOR,
    '['  : TOKEN.DELIMITADOR,
    ']'  : TOKEN.DELIMITADOR,
    ','  : TOKEN.DELIMITADOR,
    ';'  : TOKEN.DELIMITADOR,
}


escapes = {
  '\n' : TOKEN.ESCAPE,
  '\r' : TOKEN.ESCAPE,
  '\t' : TOKEN.ESCAPE,
  '\\' : TOKEN.ESCAPE,   
  "\\'" : TOKEN.ESCAPE,
  '\"' : TOKEN.ESCAPE,
  '∖u' : TOKEN.ESCAPE
}


#Nuestro Alfabeto
alfabeto            = string.ascii_letters
digitos             = '0123456789'
#digitos_bin         = digitos[:2]
#digitos_hexa        = digitos + alfabeto[:6] + alfabeto[:6].upper()
#digitos_oct         = digitos[:8]
alfanum             = alfabeto + digitos
alfanumu            = alfanum + '_'
alfabeto_completo   = alfanum + "!\"#%&'()*+,-./:;<=>?[\\]^_{|}~"

#Nuestros token
class Token () :
    def __init__ (self, tipo, valor = None, token ="", pos=-1, linea=-1, scope=-1, block = -1) :
        self.tipo = tipo
        self.valor = valor
        self.token = token
        self.pos = pos
        self.linea = linea
        self.scope = scope
        self.block = block
    #Salida de tokens
    def __repr__ ( self ) :
      # return f'{ self.tipo }' + ( f': { self.valor }' if self.valor != None else '' )
      # return f'{ self.tipo }'
      return f'{ self.valor, self.token }'

#Para leer 
class Position :
    def __init__ ( self, pos=-1, linea=0, columna=-1 ) :
        self.pos     = pos
        self.linea   = linea
        self.columna  = columna

    def avanzar ( self, fin_linea = False ) :
        self.pos     += 1
        self.columna  += 1
        if fin_linea:
            self.linea += 1 
            self.columna = 0
    
class Lexer : 
    def __init__ ( self, codigo : str,  ) :
        self.codigo = codigo
        self.linea_actual = ''
        self.contexto = self.linea_actual
        self.scope = 0
        self.block = 0
        sys.tracebacklimit = 0
        self.temp_block= 0
        if len(codigo) > 0 :
            self.Position = Position()
            self.caracter_actual = None
            self.remover_comentarios()
            self.avanzar()
        else:
            raise Exception("El codigo no puede estar vacio!")

    def lookahead ( self ) :
        auxPos = copy(self.Position)
        self.Position.avanzar(fin_linea=( self.caracter_actual == '\n' ))
        index = self.Position.pos
        self.Position = auxPos
        return self.codigo [ index ] if index < len(self.codigo) else None


    def avanzar_a ( self, chars ) :
        if chars != None :
            self.avanzar() # Mueve uno hacia adelante para no contar el actual
            while self.caracter_actual not in chars :
                self.avanzar()


    def avanzar ( self, qtd=1 ) :
        for _ in range ( qtd ) :
            if self.caracter_actual in [ '\n', None ] :
                self.linea_actual = ''
            else :
                self.linea_actual += self.caracter_actual
            self.contexto = puntero_caracter(self.Position, self.linea_actual)
            self.Position.avanzar( fin_linea=( self.caracter_actual == '\n' ) )
            self.caracter_actual = self.codigo[self.Position.pos] if self.Position.pos < len(self.codigo) else None
        


    def get_new_contexto ( self ) :
        new_contexto = puntero_caracter(Position(self.Position.pos + 1, self.Position.linea, self.Position.columna), self.linea_actual)
        return new_contexto


    def remover_comentarios ( self ) :
        # Bloques
        self.codigo =  re.sub(r"\s*\(\*\*?[^!][.\s\t\S\n\r]*?\*\)", "", self.codigo)
        # Una linea
        self.codigo = re.sub(r"(\-\-.+)", "", self.codigo)

    def tokenizar ( self ) :
        tokens = []
        while self.caracter_actual != None :
            if self.caracter_actual in '\n\r\t\\':
                self.avanzar()
            elif self.caracter_actual in digitos + '.':
                token = self.make_numbers()
                token.pos = self.Position.pos-len(token.token)
                token.linea=self.Position.linea
                token.scope = self.scope
                token.block = self.block
                tokens.append(token)
            elif self.caracter_actual in list(OPERADORES_ESPECIALES.keys()):
                token = self.make_operador ()
                if token != None:
                    token.pos = self.Position.pos-len(token.token)
                    token.linea=self.Position.linea
                    token.scope = self.scope
                    token.block = self.block
                    tokens.append(token)
                self.avanzar()
            elif self.caracter_actual in alfabeto + '_' :
                token = self.parse_word ()
                token.pos = self.Position.pos-len(token.token)
                # print("token",token.token, self.Position.pos-len(token.token))
                token.linea=self.Position.linea
                token.scope = self.scope
                token.block = self.block
                tokens.append(token)
            elif self.caracter_actual == '"':
                self.avanzar()
                token = self.parse_string()
                token.pos = self.Position.pos-len(token.token)
                token.linea=self.Position.linea
                token.scope = self.scope
                token.block = self.block
                tokens.append(token)
            elif self.caracter_actual == "'":
                self.avanzar()
                token = self.parse_char()
                token.pos = self.Position.pos-len(token.token)
                token.linea=self.Position.linea
                token.scope = self.scope
                token.block = self.block
                tokens.append(token)
            elif self.caracter_actual in list(separadores.keys()) :
                token = self.make_separador()
                if self.caracter_actual == "{":
                    self.scope += 1
                    if self.scope == 1:
                        self.temp_block += 1
                        self.block += self.temp_block 
                    token.block = self.block 
                elif self.caracter_actual == "}":
                    self.scope -= 1
                    if self.scope == 0:
                        self.block = 0
                    token.block = self.block 
                else:
                    token.block = self.block 
                token.pos = self.Position.pos-len(token.token)
                token.linea=self.Position.linea
                token.scope = self.scope                
                tokens.append(token)
                self.avanzar()
            elif self.caracter_actual not in alfabeto_completo :
                message = 'Caracter no reconocido ' + str(self.Position)
                self.avanzar()
                message += '\nlinea:\n\n' + self.contexto
                # raise Exception(message)            
            else :
                message = 'Error durante analisis: "' +  self.caracter_actual + '" Caracter no identificado.\n\nposicion: ' + str(self.Position)
                self.avanzar()
                message += '\nlinea:\n\n' + self.contexto
                #raise Exception(message)       
        tokens.append(Token(TOKEN.ENDOFFILE))
        return tokens


    def make_separador ( self ) :
        return Token(separadores[self.caracter_actual], token=self.caracter_actual, valor=self.caracter_actual )


    def make_operador ( self ) :
        if self.caracter_actual == '>' :
            if self.lookahead() == '=' :
                ret = Token(TOKEN.OPERADOR, token=self.caracter_actual+self.lookahead(),valor=self.caracter_actual+self.lookahead())
                self.avanzar()
                return ret
            return Token(TOKEN.OPERADOR, token=self.caracter_actual,valor=self.caracter_actual)
        if self.caracter_actual == '<' :
            if self.lookahead() == '>' :
                ret = Token(TOKEN.OPERADOR, token=self.caracter_actual+self.lookahead(),valor=self.caracter_actual+self.lookahead())
                self.avanzar()
                return ret
            elif self.lookahead() == '=' :
                ret = Token(TOKEN.OPERADOR, token=self.caracter_actual+self.lookahead(),valor=self.caracter_actual+self.lookahead())
                self.avanzar()
                return ret
            return Token(TOKEN.OPERADOR, token=self.caracter_actual,valor=self.caracter_actual)
        if self.caracter_actual == '=' :
            if self.lookahead() == '=' :
                ret = Token(TOKEN.OPERADOR, token=self.caracter_actual+self.lookahead(),valor=self.caracter_actual+self.lookahead())
                self.avanzar()
                return ret
            return Token(TOKEN.OPERADOR, token=self.caracter_actual,valor=self.caracter_actual)

        return Token(TOKEN.OPERADOR, token=self.caracter_actual,valor=self.caracter_actual)


    def make_numbers ( self ) :
        numero_final = ''
        while (self.caracter_actual != None and self.caracter_actual not in alfabeto+'_') and (self.caracter_actual in digitos or self.caracter_actual == '.'):
            numero_final += self.caracter_actual
            self.avanzar()
        try:      
          if self.caracter_actual in alfabeto+'_':
              raise Exception("Variable not valid")
        except:
              # raise Exception("Variable not valid")
              pass
        return Token(TOKEN.NUMERO, token="lit-int", valor=numero_final)


    def parse_word ( self ) :
        STRING = ''
        while self.caracter_actual != None and self.caracter_actual in alfanumu :
            STRING += self.caracter_actual
            self.avanzar()
        if STRING in key_words :
            if STRING == "true" or STRING == "false":
              return Token(TOKEN.KEYWORD, valor=STRING, token="lit-bool")
            else:
              return Token(TOKEN.KEYWORD, valor=STRING, token=STRING)
        else :
            return Token(TOKEN.IDENTIFICADOR, valor=STRING, token ="id")


    def parse_string ( self ) :
        STRING = ''
        while self.caracter_actual not in ( None, '"', "'" ) :
            if self.caracter_actual == '\\':
              STRING += self.caracter_actual
              self.avanzar()
              STRING += self.caracter_actual
              self.avanzar()
            else:
              STRING += self.caracter_actual
              self.avanzar()

        if self.caracter_actual == '"' :
            self.avanzar()
        return Token(TOKEN.STRING, valor=STRING, token="lit-str")

    def parse_char ( self ) :
        STRING = ''
        while self.caracter_actual not in ( None, "'" ) :
          if self.caracter_actual == '\\':
              STRING += self.caracter_actual
              self.avanzar()
              STRING += self.caracter_actual
              self.avanzar()
          else:
              STRING += self.caracter_actual
              self.avanzar()

        if self.caracter_actual == "'" :
            self.avanzar()
        return Token(TOKEN.CHAR, valor=STRING, token="lit-char")





if __name__ == "__main__":
  if len(sys.argv) == 2:
    content = open(sys.argv[1], 'r').read()
    lexer = Lexer(content)
    tokens = lexer.tokenizar()
    print("{:<10} {:<10}  {:<10}  {:<10}  {:<10}".format("token.valor","token.linea", "token.token", "token.scope", "token,block"))
    for token in tokens:
      print("{:<15} {:<15}  {:<15}  {:<15}  {:<15}".format(token.valor,token.linea, token.token, token.scope, token.block))


  else:
    while True :
      comando = input('> ')
      lexer = Lexer(comando)
      tokens = lexer.tokenizar()






