from JackTokenaizer import JackTokenaizer

class JackAnalyzer:

    def main():
        tokenaizer = JackTokenaizer(input_file)

        tokenaizer.advance()
        print("check")
        print(tokenaizer.current_token)