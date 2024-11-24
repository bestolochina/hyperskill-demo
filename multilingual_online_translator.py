from bs4 import BeautifulSoup
import requests


def enter_data() -> tuple[str, str, str]:
    languages: dict[str, str] = {
        '1': 'Arabic',
        '2': 'German',
        '3': 'English',
        '4': 'Spanish',
        '5': 'French',
        '6': 'Hebrew',
        '7': 'Japanese',
        '8': 'Dutch',
        '9': 'Polish',
        '10': 'Portuguese',
        '11': 'Romanian',
        '12': 'Russian',
        '13': 'Turkish',
    }
    print('Hello, welcome to the translator. Translator supports:')
    for num, language in languages.items():
        print(f'{num}. {language}')

    src = choose_language('Type the number of your language:\n', languages)
    dst = choose_language('Type the number of language you want to translate to:\n', languages)
    word = input('Type the word you want to translate:\n')
    return src, dst, word


def choose_language(prompt: str, languages: dict[str, str]) -> str:
    while (num := input(prompt)) not in languages:
        continue
    return languages[num]


def generate_url(src: str, dst: str, word: str) -> str:
    return f'https://context.reverso.net/translation/{src.lower()}-{dst.lower()}/{word.lower()}'


def get_content(page: requests.Response) -> tuple[list[str], list[str]]:
    # Parse the HTML content
    soup = BeautifulSoup(page.text, 'html.parser')

    # Find the terms with the class "display-term"
    # terms = [_.text.strip() for _ in soup.find_all('span', class_='display-term')]
    terms = [_.text.strip() for _ in soup.select('#translations-content .display-term')]

    # Extract the text of sentences
    # examples = [_.text.strip() for _ in soup.find_all('div', class_='ltr')]
    examples = [_.text.strip() for _ in soup.select('#examples-content .example .ltr')]

    return terms, examples


def output_content(dst: str, terms: list[str], examples: list[str]) -> None:
    print(f'\n{dst} Translations:')
    [print(term) for term in terms]

    print(f'\n{dst} Examples:')
    for i in range(0, len(examples), 2):
        print(examples[i])
        print(examples[i + 1])
        print()


def main():
    src, dst, word = enter_data()
    url = generate_url(src, dst, word)
    headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'}
    while True:
        page = requests.get(url, headers=headers)
        if page.status_code == requests.codes.ok:
            # print(page.status_code, 'OK')
            break

    terms, examples = get_content(page)

    output_content(dst, terms, examples)


if __name__ == '__main__':
    main()
