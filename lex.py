import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Define token categories
KEYWORDS = {
    "False", "await", "else", "import", "pass", "None", "break", "except", "in", "raise",
    "True", "class", "finally", "is", "return", "and", "continue", "for", "lambda", "try",
    "as", "def", "from", "nonlocal", "while", "assert", "del", "global", "not", "with",
    "async", "elif", "if", "or", "yield", "do"
}

DATA_TYPES = {
    "int", "float", "complex", "str", "bool", "list", "tuple", "dict", "set", "frozenset",
    "bytes", "bytearray", "memoryview", "range", "None"
}

OPERATORS = {'+': 'plus_op', '-': 'minus_op', '*': 'multiply_op', '**': 'expo_op', '/': 'divide_op',
             '//': 'floor_divide_op', '%': 'modulus_op', '==': 'comp_equal_op', '!=': 'not_equal_op',
             '>': 'greater_than', '<': 'less_than', '>=': 'greater_equal', '<=': 'less_equal',
             '=': 'equal_op', '+=': 'plus_equal_op', '-=': 'minus_equal_op', '*=': 'multiply_equal_op',
             '/=': 'divide_equal_op', '//=': 'floor_divide_equal_op', '%=': 'modulus_equal_op',
             '**=': 'expo_equal_op', '++': 'increment_op', '--': 'decrement_op',
             '&=': 'and_equal', '^=': 'xor_equal', '|=': 'or_equal', '>>=': 'shift_right_equal',
             '<<=': 'shift_left_equal', ':=': 'colon_equal', '&': 'bitwise_and', '|': 'bitwise_or',
             '^': 'bitwise_xor', '~': 'bitwise_not', '<<': 'shift_left', '>>': 'shift_right'
             }

DELIMITERS = {
    ',': 'comma', ';': 'semicolon', '(': 'open_parenthesis', ')': 'close_parenthesis',
    '[': 'open_bracket', ']': 'close_bracket', '{': 'open_brace', '}': 'close_brace',
    ':': 'colon', '.': 'dot', '@': 'at_symbol', '#': 'hash'
}

def get_token_type_and_name(char_or_word):
    if char_or_word in KEYWORDS:
        return "keyword"
    if char_or_word in DATA_TYPES:
        return "data_type"
    if char_or_word in OPERATORS:
        return OPERATORS[char_or_word]
    if char_or_word in DELIMITERS:
        return DELIMITERS[char_or_word]
    if char_or_word.isdigit():
        return "int_literal"
    if re.match(r'^[0-9]*\.[0-9]+$', char_or_word):
        return "float_literal"
    if re.match(r'^[^\d\W]\w*\Z', char_or_word):
        return "identifier"
    return "unidentified"

def lexical_analyzer(input_text):
    tokens = []

    pattern = r'\+\+|--|\+=|-=|\*=|/=|%|==|!=|>=|<=|\*\*|<<|>>|&=|\^=|\|=|:=|[\+\-\*\/\%\&\^\|\=\~<>!]=?|\d+\.\d+|\d+[a-zA-Z_]\w*|\d+|\"[^\"]*\"|\'[^\']*\'|[a-zA-Z_]\w*|[{},;()\[\]{}:#@.]|[^a-zA-Z0-9\s]'

    for match in re.findall(pattern, input_text):
        if match.startswith('"') and match.endswith('"'):
            tokens.append((match, "string_literal"))
        elif match.startswith("'") and match.endswith("'"):
            if len(match) == 3:
                tokens.append((match, "char_literal"))
            else:
                tokens.append((match, "unidentified"))
        elif re.match(r'^[0-9]*\.[0-9]+$', match):
            tokens.append((match, "float_literal"))
        elif match.isdigit():
            tokens.append((match, "int_literal"))
        elif match in KEYWORDS:
            tokens.append((match, "keyword"))
        elif match in DATA_TYPES:
            tokens.append((match, "data_type"))
        elif match in OPERATORS:
            tokens.append((match, OPERATORS[match]))
        elif match in DELIMITERS:
            tokens.append((match, DELIMITERS[match]))
        elif re.match(r'^[^\d\W]\w*\Z', match):
            tokens.append((match, "identifier"))
        else:
            tokens.append((match, "unidentified"))
    return tokens

def generate_pdf(tokens, input_text, output_filename="lexical_analysis.pdf"):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter
    y = height - 30
    c.drawString(30, y, "Lexical Analysis Report")
    y -= 20
    c.drawString(30, y, "=====================================")
    y -= 30
    c.drawString(30, y, f"Input Expression: {input_text}")
    y -= 20
    c.drawString(30, y, "=====================================")
    y -= 30
    c.drawString(30, y, "Lexemes")
    c.drawString(200, y, "Tokens")
    y -= 20
    c.drawString(30, y, "=====================================")
    y -= 30

    for lexeme, token in tokens:
        c.drawString(30, y, lexeme)
        c.drawString(200, y, token)
        y -= 20
        if y < 40:
            c.showPage()
            y = height - 40
    c.save()
    print(f"PDF generated: {output_filename}")

def main():
    input_text = input("Enter an expression: ")
    tokens = lexical_analyzer(input_text)
    print("Lexical Analysis Results:")
    for lexeme, token in tokens:
        print(f"Lexeme: {lexeme}, Token: {token}")
    generate_pdf(tokens, input_text)

if __name__ == "__main__":
    main()
