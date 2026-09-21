import os
import sys
import glob
class Tokenizer:
    #this is the initializer to get the input and setting up where to put the output.
    def __init__(self, input_str):
        self.input = input_str
        self.tokens = []
        self.current = 0
        
        self.keywords = {"if", "let", "var", "true", "else", "int", "char", "boolean", "class", "constructor", "function", "method", "while", "void", "this", "do", "field", "static", "return", "null", "var", "false"}
        self.symbols = {'(', ')', '{', '}', ';', '=', '<', '>', '[', ']', '*', '&', '~', '.', '|', '-', '+', '/', ','}
    
    # the main tokenizer function that scans the input for each case and builds the tokens list
    def tokenizer(self):
        while self.current < len(self.input):
            char = self.input[self.current]
            
            if char.isspace():
                self.current += 1
                continue
            if char == '"':
                self.tokens.append(self.compileString())
                continue
            if char.isdigit():
                self.tokens.append(self.compileInteger())
                continue
            if char in self.symbols:
                value = self.compareSymbol(char)
                self.tokens.append(("symbol", value))
                self.current += 1
                continue
            if char.isalpha() or char == "_":
                self.tokens.append(self.compileWord())
                continue
            
            self.current += 1
            
    #this functions takes care of the string constants 
    def compileString(self):
        self.current += 1
        start = self.current
        
        #keeps going until the end of the string
        while self.current < len(self.input) and self.input[self.current] != '"':
            self.current += 1
    
        value = self.input[start: self.current]
        self.current += 1
        return("stringConstant", value)

    #this function takes care of the integer constants
    def compileInteger(self):
        start = self.current
        
        while self.current < len(self.input) and self.input[self.current].isdigit():
            self.current += 1
        value = self.input[start:self.current]
        return("integerConstant", value)

    #this function takes care of identifiers and keywords and seperates them
    def compileWord(self):
        start = self.current
        while (self.current < len(self.input) and (self.input[self.current].isalnum() or self.input[self.current] == "_")):
            self.current += 1
        
        word = self.input[start:self.current]
    
        if word in self.keywords:
            return ("keyword", word)
        else:
            return ("identifier", word)
    
    #converts symbols to the XML format
    def compareSymbol(self, symbol):
        # if symbol == '<':
        #     return "&lt;"
        # elif symbol == '>':
        #     return "&gt;"
        # elif symbol == '&':
        #     return "&amp;"
        
        return symbol
    
#class that is the parser
class CompilationEngine: 
    def __init__(self, tokens, outputfile):
        
        self.tokens = tokens
        self.current_index = 0
        self.output = outputfile
        self.vm = VMWriter(self.output)
        self.symbolTable = SymbolTable()
        self.isDefining = False
        self.className = ""
        
    #getter that for the current token
    def currentToken(self):
        return self.tokens[self.current_index]
    
    #going forward in the code
    def advance(self):
        self.current_index += 1
    
    # #writes the token in the outputfile 
    # def writeToken(self):
    #     token_type, token_value = self.currentToken()

    #     if token_type == "identifier":
    #         kind = self.symbolTable.kindOf(token_value)
    #         index = self.symbolTable.indexOf(token_value)

    #         if kind is None:
    #             category = "class/subroutine"
    #             index_str = ""
    #         else:
    #             category = kind
    #             index_str = f' index="{index}"'

    #         status = "defined" if self.isDefining else "used"

    #         self.writeLine(
    #             f'<identifier name="{token_value}" category="{category}"{index_str} status="{status}"/>'
    #         )
    #     else:
    #         self.writeLine(f"<{token_type}> {token_value} </{token_type}>")
        
    
    # def writeLine(self, line):
    #     self.output.write("  " * self.indent + line + "\n")
    
    # def writeOpen(self, tag):
    #     self.writeLine(f"<{tag}>")
    #     self.indent += 1
    
    # def writeClose(self, tag):
    #     self.indent -= 1
    #     self.writeLine(f"</{tag}>")
    
    #the function that takes in the tokenValue or type to write if it matches with the expected
    def eat(self, exp):
        tokenType, tokenValue = self.currentToken()
        
        if tokenType == exp or tokenValue == exp:
            self.advance()
        else: 
            raise Exception(f"Expected: {exp}, got {tokenValue}")
            
    #this section compiles the class function and determines what the token value is and compiles them based on what it is
    def compileClass(self):
        
        self.eat("class")
        self.className = self.currentToken()[1]
        self.eat("identifier")
        self.eat("{")
        
        while True: 
            tokenType, tokenValue = self.currentToken()
            if tokenValue in ("static", "field"):
                self.compileClassVarDec()
            else:
                break
            
        while True:
            tokenType, tokenValue = self.currentToken()
            if tokenValue in ("constructor", "function", "method"):
                self.compileSubroutine()
            else:
                break
            
        while self.currentToken()[1] == "var":
            self.compileVarDec()
            
        self.eat("}")
    
    #compiles the variable
    def compileVarDec(self):
        self.eat("var")
        
        type = self.currentToken()[1]
        
        if self.currentToken()[0] == "keyword":
            self.eat("keyword")
        else:
            self.eat("identifier")
            
        name = self.currentToken()[1]
        self.isDefining = True
        self.symbolTable.define(name, type, "var")
        self.eat("identifier")
        self.isDefining = False
            
        while self.currentToken()[1] == ',':
            self.eat(",")
            name = self.currentToken()[1]
            self.isDefining = True
            self.symbolTable.define(name, type, "var")
            self.eat("identifier")
            self.isDefining = False
            
        self.eat(";")
        
        
    def compileClassVarDec(self):

        kind = self.currentToken()[1]
        self.eat(kind)
        
        type = self.currentToken()[1]
    
        if self.currentToken()[0] == "keyword":
            self.eat("keyword")
        else:
            self.eat("identifier")

        name = self.currentToken()[1]
        self.isDefining = True
        self.symbolTable.define(name, type, kind)
        self.eat("identifier")
        self.isDefining = False
    
        while self.currentToken()[1] == ",":
            self.eat(",")
            name = self.currentToken()[1]
            self.isDefining = True
            self.symbolTable.define(name, type, kind)
            self.eat("identifier")
            self.isDefining = False
    
        self.eat(";")

    
    #compiles subroutine
    def compileSubroutine(self):
        self.symbolTable.startSubroutine() 

        self.subroutineType = self.currentToken()[1]
        subroutineType = self.subroutineType
        self.eat(subroutineType)
        
        if self.currentToken()[1] == "void":
            self.eat("void")
        elif self.currentToken()[0] == "keyword":
            self.eat("keyword")
        else:
            self.eat("identifier")
            

        self.currentFunction = self.currentToken()[1]
        self.eat("identifier")
        
        if self.subroutineType == "method":
            self.symbolTable.define("this", self.className, "argument")

        self.eat("(")
        self.compileParameterList()
        self.eat(")")
        self.compileSubBody()
        
    
    #compiles parameter list
    def compileParameterList(self):
        
        tokenType, tokenValue = self.currentToken()
        
        if tokenValue != ")":
            type = self.currentToken()[1]
            if self.currentToken()[0] == "keyword":
                self.eat("keyword")
            else: 
                self.eat("identifier")
            
            name = self.currentToken()[1]
            self.isDefining = True
            self.symbolTable.define(name, type, "argument")
            self.eat("identifier")
            self.isDefining = False
            
            
            tokenType, tokenValue = self.currentToken()
            
            while self.currentToken()[1] == ",":
                self.eat(",")
                type = self.currentToken()[1]
                if self.currentToken()[0] == "keyword":
                    self.eat("keyword")
                else: 
                    self.eat("identifier")
                    
                name = self.currentToken()[1]
                self.isDefining = True
                self.symbolTable.define(name, type, "argument")
                self.eat("identifier")
                self.isDefining = False
                
        
            
    #compiles the subbody
    def compileSubBody(self):
        
        self.eat("{")
        
        while self.currentToken()[1] == "var":
            self.compileVarDec()
        
        nLocals = self.symbolTable.varCount("var")
        self.vm.write(f"function {self.className}.{self.currentFunction} {nLocals}")
        
        if self.subroutineType == "constructor":
            nFields = self.symbolTable.varCount("field")
            self.vm.push("constant", nFields)
            self.vm.write("call Memory.alloc 1")
            self.vm.pop("pointer", 0)
        elif self.subroutineType == "method":
            self.vm.push("argument", 0)
            self.vm.pop("pointer", 0)
        
        self.compileStatements()
        
        self.eat("}")
        
       
        
    #compiles statements like let, if, while
    def compileStatements(self):
        
        while self.current_index < len(self.tokens):
            tokenType, tokenValue = self.currentToken()
            
            if tokenValue == "let":
                self.compileLet()
            elif tokenValue == "if":
                self.compileIf()
            elif tokenValue == "while":
                self.compileWhile()
            elif tokenValue == "do":
                self.compileDo()
            elif tokenValue == "return":
                self.compileReturn()
            else: 
                break
            
        
    
    #compiles let 
    def compileLet(self):
        
        self.eat("let")
        
        varName = self.currentToken()[1]
        
        kind = self.symbolTable.kindOf(varName)
        if kind is None:
            raise Exception(f"undefined variable: {varName}")
        
        index = self.symbolTable.indexOf(varName)
        segment = self.segment(kind)

        self.eat("identifier")
        
        isArray = False

        # self.eat("identifier")
        
        tokenType, tokenValue = self.currentToken()
        
        if self.currentToken()[1] == "[":
            isArray = True
            self.eat("[")
            self.vm.push(segment, index)
            self.compileExpression()
            self.eat("]")
            
            self.vm.write("add")
        
        self.eat("=")
        
        self.compileExpression()
        
        if isArray:
            self.vm.pop("temp", 0)
            self.vm.pop("pointer", 1)
            self.vm.push("temp", 0)
            self.vm.pop("that", 0)
        else :
        
            self.vm.pop(segment, index)

        self.eat(";")
        
        # self.compileExpression()
        
        # self.eat(";")
        
        # self.writeClose("letStatement")
    
    #compiles if
    def compileIf(self):
        labelTrue = f"IF_TRUE{self.current_index}"
        labelFalse = f"IF_FALSE{self.current_index}"
        labelEnd = f"IF_END{self.current_index}"
        
        self.eat("if")
        self.eat("(")
        self.compileExpression()
        self.eat(")")
        
        self.vm.write(f"if-goto {labelTrue}")
        self.vm.write(f"goto {labelFalse}")
        self.vm.write(f"label {labelTrue}")
        
        self.eat("{")
        self.compileStatements()
        self.eat("}")
        
        tokenType, tokenValue = self.currentToken()
        
        if tokenValue == "else":
            self.vm.write(f"goto {labelEnd}")
            self.vm.write(f"label {labelFalse}")
            
            self.eat("else")
            self.eat("{")
            self.compileStatements()
            self.eat("}")
            
            self.vm.write(f"label {labelEnd}")
        else:
            self.vm.write(f"label {labelFalse}")
        
    
    #compiles the while 
    def compileWhile(self):
        
        labelExp = f"WHILE_EXP{self.current_index}"
        labelEnd = f"WHILE_END{self.current_index}"
        
        self.vm.write(f"label {labelExp}")

        self.eat("while")
        self.eat("(")
        self.compileExpression()
        self.eat(")")
        
        self.vm.write("not")
        self.vm.write(f"if-goto {labelEnd}")
        
        self.eat("{")
        self.compileStatements()
        self.eat("}")
        
        self.vm.write(f"goto {labelExp}")
        self.vm.write(f"label {labelEnd}")
        
        
    #compiles the do  
    def compileDo(self):
        
        self.eat("do")
        self.compileSubroutineCall()
        self.eat(";")
        self.vm.pop("temp", 0)
        
        
    #compiles the return   
    def compileReturn(self):
        self.eat("return")
        
        if self.currentToken()[1] != ";":
            self.compileExpression()
        else: 
            self.vm.push("constant", 0)
            
        self.eat(";")
        self.vm.write("return")
      
       
    #compiles the expression 
    def compileExpression(self):
        self.compileTerm()

        ops = {
            "+" : "add",
            "-" : "sub",
            "&" : "and",
            "|" : "or",
            "<" : "lt",
            ">" : "gt",
            "=" : "eq",
            "*" : "call Math.multiply 2",
            "/" : "call Math.divide 2"
            
        }
        
        while self.currentToken()[1] in ops:
            op = self.currentToken()[1]
            self.eat(op)
            self.compileTerm()
            
            self.vm.arithmetic(ops[op])
        # ops = {"+", "-", "*", "/", "&", "|", "<", ">", "="}
       
        # while True: 
        #     tokenValue = self.currentToken()[1]
            
        #     if tokenValue in ("&lt;", "&gt;", "&amp;"):
        #         norm = self.normalizer(tokenValue)
        #     else:
        #         norm = tokenValue
        
        #     if norm in ops:
        #         self.eat(tokenValue)
        #         self.compileTerm()
        #     else:
        #         break

        # self.writeClose("expression")
        
    def normalizer(self, tokenValue):
        if tokenValue == "&lt;":
            return "<"
        elif tokenValue == "&gt;":
            return ">"
        elif tokenValue == "&amp;":
            return "&"

        return tokenValue
    
    
    #compiles the term and calls appropiate function
    def compileTerm(self):
        
        tokenType, tokenValue = self.currentToken()
        
        if tokenType == "integerConstant":
            value = int(tokenValue)
            self.vm.push("constant", value)
            self.eat("integerConstant")
        elif tokenType == "stringConstant":
            value = tokenValue
            self.vm.push("constant", len(value))
            self.vm.write("call String.new 1")
            
            for ch in value:
                self.vm.push("constant", ord(ch))
                self.vm.write("call String.appendChar 2")
                
            self.eat("stringConstant")
        elif tokenType == "keyword" and tokenValue in ("true", "false", "null", "this"):
            if tokenValue == "true":
                self.vm.push("constant", 0)
                self.vm.arithmetic("not")
            elif tokenValue in ("false", "null"):
                self.vm.push("constant", 0)
            elif tokenValue == "this":
                self.vm.push("pointer", 0)
                
            self.eat(tokenValue)
        elif tokenType == "identifier":
            
            name = tokenValue

            next_token = self.tokens[self.current_index + 1][1] if self.current_index + 1 < len(self.tokens) else None

            if next_token in ("(", "."):
                self.compileSubroutineCall()
                return
            
            if next_token == "[":
                kind = self.symbolTable.kindOf(name)
                if kind is None:
                    raise Exception(f"undefined variable: {name}")

                index = self.symbolTable.indexOf(name)
                segment = self.segment(kind)

                self.eat("identifier")
                self.eat("[")

                self.vm.push(segment, index)
                self.compileExpression()
                self.eat("]")

                self.vm.arithmetic("add")
                self.vm.pop("pointer", 1)
                self.vm.push("that", 0)
                return

            kind = self.symbolTable.kindOf(name)

            if kind is None:
                raise Exception(f"undefined variable: {name}")

            index = self.symbolTable.indexOf(name)
            segment = self.segment(kind)

            self.vm.push(segment, index)
            self.eat("identifier")

        elif tokenValue == "(":
            self.eat("(")
            self.compileExpression()
            self.eat(")")

        elif tokenValue in ("-", "~"):
            op = tokenValue
            self.eat(op)
            self.compileTerm()
            
            if op == "-":
                self.vm.write("neg")
            else:
                self.vm.write("not")
        
        # while self.currentToken()[1] in ("*", "/"):
        #     op = self.currentToken()[1]
        #     self.eat(op)
        #     self.compileTerm()
            
        #     if op == "*":
        #         self.vm.write("call Math.multiply 2")
        #     else:
        #         self.vm.write("call Math.divide 2")
        
    #compiles subroutine calls
    def compileSubroutineCall(self):
        name = self.currentToken()[1]
        self.eat("identifier")
        
        numArg = 0
        fullname = ""
        
        if self.currentToken()[1] == ".":
            self.eat(".")
            subname = self.currentToken()[1]
            self.eat("identifier")
            kind = self.symbolTable.kindOf(name)
            
            if kind is not None:
                segment = self.segment(kind)
                index = self.symbolTable.indexOf(name)
                typeName = self.symbolTable.typeOf(name)
                
                self.vm.push(segment, index)
                numArg += 1
                fullname = f"{typeName}.{subname}"
            else:
                fullname = f"{name}.{subname}"
            
        else:
            fullname = f"{self.className}.{name}"
            self.vm.push("pointer", 0)
            numArg += 1
            
        self.eat("(")
        numArg += self.compileExpressionList()
        self.eat(")")
        
        self.vm.write(f"call {fullname} {numArg}")
    
    #compiles expression lists    
    def compileExpressionList(self):
        count = 0
        
        if self.currentToken()[1] != ")":
            self.compileExpression()
            count += 1
            
            while self.currentToken()[1] == ",":
                self.eat(",")
                self.compileExpression()
                count += 1
        
        return count
        
        
    def segment(self, kind):
        if kind == "var":
            return "local"
        if kind == "argument":
            return "argument"
        if kind == "field":
            return "this"
        if kind == "static":
            return "static"
        
        raise Exception(f"Invalid:  {kind}")
        
class SymbolTable:
    def __init__(self):
        self.class_scope = {}
        self.subroutine_scope = {}
        self.counts = {
            "static": 0,
            "field" : 0,
            "argument" : 0,
            "var": 0 }
        
    def startSubroutine(self):
        self.subroutine_scope = {}
        self.counts["argument"] = 0
        self.counts["var"] = 0
        
    def define(self, name, type, kind):
        index = self.counts[kind]
        entry = (type, kind, index)
        
        if kind in ("static", "field"):
            self.class_scope[name] = entry
        else: 
            self.subroutine_scope[name] = entry
        
        self.counts[kind] += 1
        
    def varCount(self, kind):
        return self.counts[kind]
    
    def kindOf(self, name):
        if name in self.subroutine_scope:
            return self.subroutine_scope[name][1]
        
        if name in self.class_scope:
            return self.class_scope[name][1]
        
        return None
    
    def typeOf(self, name):
        if name in self.subroutine_scope:
            return self.subroutine_scope[name][0]
        if name in self.class_scope:
            return self.class_scope[name][0]
        
        return None
    
    def indexOf(self, name):
        if name in self.subroutine_scope:
            return self.subroutine_scope[name][2]
        
        if name in self.class_scope:
            return self.class_scope[name][2]
        
        return None
    
        
class VMWriter:
    def __init__(self, output):
        self.out = output
        
    def write(self, cmd):
        self.out.write(cmd + "\n")
    
    def push(self, segment, index):
        self.write(f"push {segment} {index}")
        
    def pop(self, segment, index):
        self.write(f"pop {segment} {index}")
        
    def arithmetic(self, cmd):
        self.write(cmd)
        
                
#changes the extension of the file
def changeExtension(filename, newExtension):
    base, _ = os.path.splitext(filename)
    return base + newExtension

#the main function that reads the file and takes in multiple files
def main(inputpath):
    if os.path.isfile(inputpath) and inputpath.endswith(".jack"):
        processFile(inputpath)
    elif os.path.isdir(inputpath):
        jack_files = glob.glob(os.path.join(inputpath, "*.jack"))
        for filepath in jack_files:
            processFile(filepath)

#processes one jack file and writes the tokens
def processFile(filename):
    outputFileName = changeExtension(filename, ".vm")
    with open(filename, "r") as infile:
        input_text = infile.read()
    input_text = remove_comments(input_text)
    tokenizer = Tokenizer(input_text)
    tokenizer.tokenizer()
    with open(outputFileName, "w") as outfile:
        # outfile.write("<tokens>\n")
        # for type, value in tokenizer.tokens:
        #     outfile.write(f"<{type}> {value} </{type}>\n")
        
        engine = CompilationEngine(tokenizer.tokens, outfile)
        engine.compileClass()
        #outfile.write("</tokens>\n")

#removes the comments from the files so they do not get processed
def remove_comments(input_text):
    import re
    no_single = re.sub(r'//.*', '', input_text)
    no_multi = re.sub(r'/\*.*?\*/', '', no_single, flags=re.DOTALL)
    return no_multi
        
        
if __name__ == "__main__":
    main(sys.argv[1]) 