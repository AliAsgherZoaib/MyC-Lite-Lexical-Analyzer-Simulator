class LexicalError:
    def __init__(self, error_type, line, message, suggested_fix):
        self.error_type = error_type
        self.line = line
        self.message = message
        self.suggested_fix = suggested_fix

    def to_dict(self):
        return {
            "error_type": self.error_type,
            "line": self.line,
            "message": self.message,
            "suggested_fix": self.suggested_fix
        }

class LexicalWarning:
    def __init__(self, line, message, lexeme):
        self.line = line
        self.message = message
        self.lexeme = lexeme

    def to_dict(self):
        return {
            "line": self.line,
            "message": self.message,
            "lexeme": self.lexeme
        }