from JackTokenaizer import JackTokenaizer


def main():
    tokenaizer = JackTokenaizer("Square.jack")

    tokenaizer.advance()
    print("check")
    print(tokenaizer.current_token)


if __name__ == '__main__':
    main()
