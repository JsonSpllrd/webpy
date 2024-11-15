from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import re

# Define token categories inline
KEYWORDS = {"False", "await", "else", "import", "pass", "None", "break", "except", "in", "raise",
            "True", "class", "finally", "is", "return", "and", "continue", "for", "lambda", "try",
            "as", "def", "from", "nonlocal", "while", "assert", "del", "global", "not", "with",
            "async", "elif", "if", "or", "yield"}

OPERATORS = {'+': 'plus_op', '-': 'minus_op', '*': 'multiply_op', '/': 'divide_op',
             '%': 'modulus_op', '>': 'greater_than', '<': 'less_than', '=': 'equal_sign',
             '&': 'and_bitwise_op', '|': 'or_bitwise_op', '^': 'xor_bitwise_op', '~': 'not_bitwise_op'}

DELIMITERS = {',': 'comma', ';': 'semicolon', '(': 'open_parenthesis', ')': 'close_parenthesis',
              '[': 'open_bracket', ']': 'close_bracket', '{': 'open_brace', '}': 'close_brace', ':': 'colon'}

def get_token_type_and_name(char_or_word):
    if char_or_word in KEYWORDS:
        return "keyword"
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
    # Updated pattern to include floats explicitly
    pattern = r'"[^"]*"|\'[^\']*\'|["\']|\d+\.\d+|\w+|[+\-*/%<>=&|^~{},;()\[\]{}:]'
    for match in re.findall(pattern, input_text):
        if match.startswith('"') and match.endswith('"') and len(match) > 1:
            tokens.append((match, "string_literal"))
        elif match.startswith("'") and match.endswith("'") and len(match) == 3:
            tokens.append((match, "char_literal"))
        elif match in {'"', "'"}:
            tokens.append((match, "quotation_mark"))
        elif re.match(r'^[0-9]*\.[0-9]+$', match):  # Check for float literals
            tokens.append((match, "float_literal"))
        else:
            tokens.append((match, get_token_type_and_name(match)))
    return tokens


def generate_pdf(tokens, input_text, output_filename="lexical_analysis.pdf"):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter
    y = height - 30

    # Add report title
    c.drawString(30, y, "Lexical Analysis Report")
    y -= 20
    c.drawString(30, y, "=====================================")
    y -= 30
    c.drawString(30, y, f"Input Expression: {input_text}")
    y -= 20
    c.drawString(30, y, "=====================================")
    y -= 30

    # Add lexemes and tokens
    c.drawString(30, y, "Lexemes")
    c.drawString(200, y, "Tokens")
    y -= 20
    c.drawString(30, y, "=====================================")
    y -= 30

    for lexeme, token in tokens:
        c.drawString(30, y, lexeme)
        c.drawString(200, y, token)
        y -= 20
        if y < 40:  # Create a new page if running out of space
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
