from bs4 import BeautifulSoup
import requests


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

def enter_data() -> tuple[str, str, str]:
    print('Hello, welcome to the translator. Translator supports:')
    for num, language in languages.items():
        print(f'{num}. {language}')

    src = choose_language('Type the number of your language:\n', languages)
    dst = choose_language(
        "Type the number of a language you want to translate to or '0' to translate to all languages:\n",
        {'0': 'all', **languages})
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
    examples = [_.text.strip() for _ in soup.select('#examples-content .example .text')]

    return terms, examples


def output_content(word: str, dst: str, terms: list[str], examples: list[str]) -> None:
    file_name: str = word + '.txt'

    print(f'\n{dst} Translations:')
    print(terms[0])
    print(f'\n{dst} Examples:')
    print(examples[0])
    print(examples[1])
    # print()

    with open(file_name, 'a', encoding='utf-8') as f:
        print(f'\n{dst} Translations:', file=f)
        print(terms[0], file=f)
        print(f'\n{dst} Examples:', file=f)
        print(examples[0], file=f)
        print(examples[1], file=f)
        # print('', file=f)


def get_page(url: str) -> requests.Response:
    headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'}
    while True:
        page = requests.get(url, headers=headers)
        if page.status_code == requests.codes.ok:
            break
    return page


def main():
    src, dst, word = enter_data()
    if dst == 'all':
        for dst in languages.values():
            if src == dst:
                continue
            url = generate_url(src, dst, word)
            page = get_page(url)
            terms, examples = get_content(page)
            output_content(word, dst, terms, examples)

    else:
        url = generate_url(src, dst, word)
        page = get_page(url)
        terms, examples = get_content(page)
        output_content(word, dst, terms, examples)


if __name__ == '__main__':
    main()
