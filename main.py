# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, MULTIPLY, DIVISON, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVISON', 'EOF',


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', '-', '*', '/' or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]

        # if statement to identify and skip over whitespaces
        while self.pos < len(text) and current_char.isspace():
            self.pos += 1
            current_char = text[self.pos]

        # Calculate integers with multiple digits 
        # if the character is a digit then convert it to integer, then increment self.pos
        # store it in variable result
        # while self.pos is less than text and is a digit, keep converting character if it is a digit
        # then return the INTEGER token
        if current_char.isdigit():
            result = ''
            while self.pos < len(text) and text[self.pos].isdigit():
                result += text[self.pos]
                self.pos += 1     
            return Token(INTEGER, int(result))
                
        # if statement to handle plus sign        
        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        # if statement to handle minus sign
        if current_char == '-':
            self.pos += 1
            return Token(MINUS, current_char)

        # if statement to handle multiplication sign
        if current_char == '*':
            self.pos += 1
            return Token(MULTIPLY, current_char)

        # if statement to handle division sign
        if current_char == '/':
            self.pos += 1
            return Token(DIVISON, current_char)


        self.error()

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be a single-digit integer
        left = self.current_token
        self.eat(INTEGER)
        result = left.value

        while op.type in (PLUS, MINUS, MULTIPLY, DIVISON):
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
                right = self.current_token
                self.eat(INTEGER)
                result = result + right.value
            elif op.type == MINUS:
                self.eat(MINUS)
                right = self.current_token
                self.eat(INTEGER)
                result = result - right.value
            elif op.type == MULTIPLY:
                self.eat(MULTIPLY)
                right = self.current_token
                self.eat(INTEGER)
                result = result * right.value
            elif op.type == DIVISON:
                self.eat(DIVISON)
                right = self.current_token
                self.eat(INTEGER)
                result = result // right.value

        return result
        


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()