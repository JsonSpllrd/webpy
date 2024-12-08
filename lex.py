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

def is_identifier(word):
    # Check if the word starts with a valid character
    if word[0].isalpha() or word[0] == "_":
        # Check each character in the word
        for char in word:
            # If the character is in delimiters or operators, return False
            if char in DELIMITERS or char in ''.join(OPERATORS.keys()):
                return False
            # If the character is not alphanumeric or an underscore, return False
            if not (char.isalnum() or char == "_"):
                return False
        return True
    return False


def tokenize(input_text):
    tokens = []
    i = 0
    n = len(input_text)

    while i < n:
        char = input_text[i]

        # Skip whitespace
        if char.isspace():
            i += 1
            continue

        # Match operators
        for op in sorted(OPERATORS.keys(), key=len, reverse=True):  # Match longest operators first
            if input_text.startswith(op, i):
                tokens.append((op, OPERATORS[op]))
                i += len(op)
                break
        else:
            # Match delimiters
            if char in DELIMITERS:
                tokens.append((char, DELIMITERS[char]))
                i += 1
                continue

            # Match string literals
            if char in {'"', "'"}:
                quote_type = char
                end_idx = i + 1
                while end_idx < n and input_text[end_idx] != quote_type:
                    end_idx += 1
                if end_idx < n:
                    tokens.append((input_text[i:end_idx + 1], "string_literal"))
                    i = end_idx + 1
                else:
                    tokens.append((input_text[i:], "unidentified"))
                    break
                continue

            # Match identifiers or invalid identifiers
            if char.isalpha() or char == "_":
                word_start = i
                while i < n and (input_text[i].isalnum() or input_text[i] in DELIMITERS or input_text[i] in ''.join(OPERATORS.keys()) or input_text[i] == "_"):
                    i += 1
                word = input_text[word_start:i]

                # If the word contains invalid characters, mark it as "unidentified"
                if any(delimiter in word for delimiter in DELIMITERS) or \
                   any(op in word for op in OPERATORS):
                    tokens.append((word, "unidentified"))
                elif word in KEYWORDS:
                    tokens.append((word, "keyword"))
                elif word in DATA_TYPES:
                    tokens.append((word, "data_type"))
                elif is_identifier(word):
                    tokens.append((word, "identifier"))
                else:
                    tokens.append((word, "unidentified"))
                continue

            # Match numeric literals
            if char.isdigit():
                num_start = i
                has_dot = False
                while i < n and (input_text[i].isdigit() or (input_text[i] == '.' and not has_dot)):
                    if input_text[i] == '.':
                        has_dot = True
                    i += 1
                num_str = input_text[num_start:i]
                tokens.append((num_str, "float_literal" if '.' in num_str else "int_literal"))
                continue

            # Unidentified characters
            tokens.append((char, "unidentified"))
            i += 1

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
    tokens = tokenize(input_text)
    print("Lexical Analysis Results:")
    for lexeme, token in tokens:
        print(f"Lexeme: {lexeme}, Token: {token}")
    generate_pdf(tokens, input_text)

if __name__ == "__main__":
    main()
