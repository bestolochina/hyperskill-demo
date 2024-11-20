from bs4 import BeautifulSoup
import requests


def enter_data() -> tuple[str, str, str]:
    while True:
        language = input('Type "en" if you want to translate from French into English, or "fr" if you want to translate'
                         ' from English into French:\n')
        if language == 'en':
            src, dst = 'french', 'english'
            break
        elif language == 'fr':
            src, dst = 'english', 'french'
            break

    word = input('Type the word you want to translate:\n')
    print(f'You chose "{language}" as the language to translate "{word}" to.')
    return src, dst, word


def generate_url(src: str, dst: str, word: str) -> str:
    return f'https://context.reverso.net/translation/{src}-{dst}/{word}'


def main():
    url = generate_url(*enter_data())
    headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'}
    while True:
        page = requests.get(url, headers=headers)
        if page.status_code == requests.codes.ok:
            print(page.status_code, 'OK')
            print('Translations')
            break

    # Parse the HTML content
    soup = BeautifulSoup(page.text, 'html.parser')

    # Find the spans with the class "display-term"
    terms = [_.text for _ in soup.find_all('span', class_='display-term')]

    print(terms)

    # Find the section containing the examples
    # examples_section = soup.find('section', id='examples-content')
    # Find all divs with class "example" within the examples section
    # examples = examples_section.find_all('div', class_='example')
    examples = soup.find_all('div', class_='example')

    # Extract and print the text from each pair of sentences
    # for example in examples:
    #     # Get the English (source) sentence
    #     src_sentence = example.find('div', class_='src').find('span', class_='text').get_text(strip=True)
    #     # Get the French (target) sentence
    #     trg_sentence = example.find('div', class_='trg').find('span', class_='text').get_text(strip=True)
    #     # Print the sentences
    #     print(f"English: {src_sentence}")
    #     print(f"French: {trg_sentence}")
    #     print("-" * 40)  # Separator for readability

    sentences_text = []
    for example in examples:
        # Get the raw sentences
        sentences = example.find_all('span', class_='text')

        # Get the pure sentences
        for sentence in sentences:
            sentences_text.append(sentence.get_text().strip())

    print(sentences_text)


if __name__ == '__main__':
    main()
