import re
from error_handler import LexicalError, LexicalWarning
from symbol_table import SymbolTable

class MyCLiteLexer:
    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.length = len(source_code)
        self.tokens = []
        self.errors = []
        self.warnings = []
        self.trace = []
        self.symbol_table = SymbolTable()
        
        # Language Specifications
        self.keywords = {
            "if", "else", "while", "for", "int", "float", "char", "return", "void",
            "begin", "end", "display", "input", "repeat", "until"
        }
        self.operators = {'+', '-', '*', '/', '%', '=', '==', '!=', '<=', '>=', '<', '>', '&&', '||'}
        self.delimiters = {';', ',', ':', '.', '(', ')', '{', '}', '[', ']'}

    def add_trace(self, char, current_lexeme):
        escaped_char = repr(char).strip("'")
        self.trace.append(f"Reading character: '{escaped_char}' -> Building lexeme: '{current_lexeme}'")

    def analyze(self):
        while self.position < self.length:
            char = self.source[self.position]

            # Track Lines
            if char == '\n':
                self.line += 1
                self.position += 1
                continue

            # Skip common whitespace
            if char.isspace():
                self.position += 1
                continue

            # Multi-line / Single Line Comments
            if char == '/' and self.position + 1 < self.length:
                if self.source[self.position + 1] == '/':
                    self.position += 2
                    while self.position < self.length and self.source[self.position] != '\n':
                        self.position += 1
                    continue
                elif self.source[self.position + 1] == '*':
                    self.position += 2
                    closed = False
                    while self.position < self.length:
                        if self.source[self.position] == '*' and self.position + 1 < self.length and self.source[self.position + 1] == '/':
                            self.position += 2
                            closed = True
                            break
                        if self.source[self.position] == '\n':
                            self.line += 1
                        self.position += 1
                    if not closed:
                        self.errors.append(LexicalError("Unclosed Comment", self.line, "Unclosed comment block detected.", "Close the block comment using '*/'.").to_dict())
                    continue

            # String Literals
            if char == '"':
                start_line = self.line
                lexeme = '"'
                self.position += 1
                closed = False
                while self.position < self.length:
                    c = self.source[self.position]
                    lexeme += c
                    self.position += 1
                    if c == '"':
                        closed = True
                        break
                    if c == '\n':
                        self.line += 1
                if closed:
                    self.tokens.append({"lexeme": lexeme, "type": "STRING_LITERAL", "line": start_line})
                else:
                    self.errors.append(LexicalError("Unterminated String", start_line, "String literal must be terminated with closing double quotes.", "Append '\"' to close the string.").to_dict())
                continue

            # Invalid Base Character Check
            if char == '@' or char == '#':
                self.errors.append(LexicalError("Invalid Character", self.line, f"Character '{char}' is completely unrecognized in MyC-Lite language rules.", f"Remove '{char}' from your codebase.").to_dict())
                self.position += 1
                continue

            # Numeric Constants & Formats
            if char.isdigit() or (char == '.' and self.position + 1 < self.length and self.source[self.position + 1].isdigit()):
                lexeme = ""
                dot_count = 0
                while self.position < self.length:
                    c = self.source[self.position]
                    if c.isdigit() or c == '.':
                        if c == '.':
                            dot_count += 1
                        lexeme += c
                        self.add_trace(c, lexeme)
                        self.position += 1
                    else:
                        break
                
                if dot_count > 1:
                    self.errors.append(LexicalError("Invalid Number Format", self.line, f"Malformed float constant sequence '{lexeme}'. Found multiple points.", "Ensure floats contain a single radix fractional point.").to_dict())
                else:
                    self.tokens.append({"lexeme": lexeme, "type": "NUMERIC_CONSTANT", "line": self.line})
                continue

            # Identifiers & Keywords Process Core State Machine
            if char.isalpha() or char == '_':
                lexeme = ""
                while self.position < self.length:
                    c = self.source[self.position]
                    if c.isalnum() or c == '_':
                        lexeme += c
                        self.add_trace(c, lexeme)
                        self.position += 1
                    else:
                        break

                # Contextual keyword evaluation
                if lexeme in self.keywords:
                    self.tokens.append({"lexeme": lexeme, "type": "KEYWORD", "line": self.line})
                    self.trace.append(f"Token Generated: KEYWORD({lexeme})")
                    continue

                # Rule 9: Protection validation boundary
                if lexeme in ["v_", "fn_", "c_"]:
                    self.errors.append(LexicalError("Invalid Identifier", self.line, "Incomplete reserved identifier prefix.", f"Provide a proper suffix name after structural boundary '{lexeme}'.").to_dict())
                    continue

                # Rule 1: Validation processing rules
                if not (lexeme.startswith("v_") or lexeme.startswith("fn_") or lexeme.startswith("c_")):
                    self.errors.append(LexicalError("Invalid Identifier", self.line, "Identifier must start with v_, fn_, or c_.", f"Rename identifier to follow rules (e.g., v_{lexeme} or fn_{lexeme}).").to_dict())
                    continue

                # Rule 3: Max sequence checks
                if len(lexeme) > 20:
                    self.errors.append(LexicalError("Invalid Identifier", self.line, "Identifier exceeds maximum length of 20 characters.", f"Truncate identifier '{lexeme}' down underneath 20 characters maximum.").to_dict())
                    continue

                # Rule 5: User Readability warning conditions
                # Stripping standard core indicators when measuring naked payload length
                clean_payload = lexeme[2:] if lexeme.startswith("v_") else lexeme[3:]
                if len(clean_payload) < 3:
                    self.warnings.append(LexicalWarning(self.line, "Identifier name is too short and may reduce readability.", lexeme).to_dict())

                # Classification selection rules (Rule 6)
                token_type = "CONSTANT_IDENTIFIER" if lexeme.startswith("c_") else "IDENTIFIER"
                self.tokens.append({"lexeme": lexeme, "type": token_type, "line": self.line})
                self.trace.append(f"Token Generated: {token_type}({lexeme})")
                
                # Update table entry structure
                self.symbol_table.insert(lexeme, token_type, self.line)
                continue

            # Multi-character Operators evaluation check
            if char in self.operators or (char in ['=', '!', '<', '>', '&', '|']):
                lexeme = char
                self.position += 1
                if self.position < self.length:
                    next_char = self.source[self.position]
                    combined = lexeme + next_char
                    if combined in self.operators:
                        lexeme = combined
                        self.position += 1
                
                if lexeme in self.operators:
                    self.tokens.append({"lexeme": lexeme, "type": "OPERATOR", "line": self.line})
                else:
                    self.errors.append(LexicalError("Invalid Character", self.line, f"Broken symbol composition sequence '{lexeme}' unmatched.", "Fix matching compound assignments.").to_dict())
                continue

            # Delimiters fallback handling logic block
            if char in self.delimiters:
                self.tokens.append({"lexeme": char, "type": "DELIMITER", "line": self.line})
                self.position += 1
                continue

            # Final incremental catch fallback
            self.position += 1

        # Analytical metrics summary counts calculation (Rule 7)
        stats = {
            "keywords": sum(1 for t in self.tokens if t["type"] == "KEYWORD"),
            "identifiers": sum(1 for t in self.tokens if t["type"] in ["IDENTIFIER", "CONSTANT_IDENTIFIER"]),
            "operators": sum(1 for t in self.tokens if t["type"] == "OPERATOR"),
            "constants": sum(1 for t in self.tokens if t["type"] in ["NUMERIC_CONSTANT", "STRING_LITERAL"]),
            "delimiters": sum(1 for t in self.tokens if t["type"] == "DELIMITER"),
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "total_tokens": len(self.tokens)
        }

        return {
            "tokens": self.tokens,
            "errors": self.errors,
            "warnings": self.warnings,
            "symbol_table": self.symbol_table.get_all(),
            "stats": stats,
            "trace": self.trace
        }