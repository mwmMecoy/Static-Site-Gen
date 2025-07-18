from textnode import TextNode, TextType

def main():
    test = TextNode("This is a test", TextType.LINK, "http://example.com")
    print(test)

main()