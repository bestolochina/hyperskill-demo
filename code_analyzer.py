from collections import defaultdict
import ast
import sys
import os.path
import re


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.local_vars: dict[int, list[str]] = defaultdict(list)
        self.current_function: str = ""
        self.function_names: dict[int, str] = {}
        self.function_arguments_names: dict[int, list[str]] = {}
        self.default_args_with_values: dict[int, list[tuple[str, any]]] = {}
        self.class_names: dict[int, list[str]] = {}

    def visit_FunctionDef(self, node) -> None:
        self.current_function = node.name

        self.function_names.update({node.lineno - 1: node.name})

        args = [arg.arg for arg in node.args.args]
        self.function_arguments_names[node.lineno - 1] = args

        default_args = [arg.arg for arg in node.args.args[len(node.args.args) - len(node.args.defaults):]]
        default_values = [ast.literal_eval(value) for value in node.args.defaults]
        self.default_args_with_values[node.lineno - 1] = list(zip(default_args, default_values))

        self.generic_visit(node)
        self.current_function = ""  # for local variables

    def visit_Assign(self, node) -> None:
        if self.current_function:  # look at def visit_FunctionDef
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.local_vars[node.lineno - 1].append(target.id)
        self.generic_visit(node)

    def visit_ClassDef(self, node) -> None:
        parent_classes = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                parent_classes.append(base.id)
            elif isinstance(base, ast.Attribute):
                parent_classes.append(base.attr)
        self.class_names.update({node.lineno - 1: [node.name, *parent_classes]})
        self.generic_visit(node)


class StaticCodeAnalyzer:
    def __init__(self, path: str) -> None:
        self.visitor = Visitor()
        self.path: str = path
        self.files: list[str] = self.read_files()
        self.file: str = ''
        self.code: list[str] = []
        self.errors: list[dict[str, str | callable]] = \
            [{'code': 'S001', 'message': 'The line is too long', 'function': self.s001},
             {'code': 'S002', 'message': 'Indentation is not a multiple of four', 'function': self.s002},
             {'code': 'S003', 'message': 'Unnecessary semicolon after a statement', 'function': self.s003},
             {'code': 'S004', 'message': 'Less than two spaces before inline comments', 'function': self.s004},
             {'code': 'S005', 'message': 'TODO found', 'function': self.s005},
             {'code': 'S006', 'message': 'More than two blank lines preceding a code line', 'function': self.s006},
             {'code': 'S007', 'message': 'Too many spaces after construction_name (def or class)',
              'function': self.s007},
             {'code': 'S008', 'message': 'Class name class_name should be written in CamelCase', 'function': self.s008},
             {'code': 'S009', 'message': 'Function name function_name should be written in snake_case',
              'function': self.s009},
             {'code': 'S010', 'message': 'Argument name arg_name should be written in snake_case',
              'function': self.s010},
             {'code': 'S011', 'message': 'Variable var_name should be written in snake_case', 'function': self.s011},
             {'code': 'S012', 'message': 'The default argument value is mutable', 'function': self.s012}]
        self.line: str = ''
        self.line_number: int = 0
        self.char: str = ''
        self.char_index: int = 0

    def read_files(self) -> list[str]:
        if os.path.isfile(self.path):
            return [self.path]
        else:
            files_list = []
            for (root, dirs, files) in os.walk(self.path):
                for name in files:
                    path = str(os.path.join(root, name))
                    if path.endswith('.py'):
                        files_list.append(path)
            return files_list

    def close_quote(self) -> bool:
        while True:
            try:
                next_quot_index = self.line.find(self.char, self.char_index + 1)
            except IndexError:
                return False
            if next_quot_index == -1:
                return False
            if self.line[next_quot_index - 1] == '\\':
                self.char_index = next_quot_index
                continue
            self.char_index = next_quot_index
            return True

    def s001(self) -> bool:  # line length
        return len(self.line) > 80

    def s002(self) -> bool:  # indentation
        spaces: re.Match[str] = re.match(pattern=r'^( *)\w', string=self.line)
        return spaces and len(spaces.group(1)) % 4 != 0

    def s003(self) -> bool:  # semicolon in line
        self.char_index = 0
        while True:
            if self.char_index >= len(self.line):
                return False
            self.char = self.line[self.char_index]

            if self.char == '#':
                return False
            elif self.char in {"'", '"'} and not self.close_quote():
                return False
            elif self.char == ';':
                return True
            self.char_index += 1

    def s004(self) -> bool:  # two spaces before inline comments
        self.char_index = 0
        while True:
            if self.char_index >= len(self.line):
                return False
            self.char = self.line[self.char_index]

            if self.char in {"'", '"'} and not self.close_quote():
                return False
            elif self.char == '#':
                if self.char_index == 0:
                    return False
                elif (self.char_index > 2
                      and self.line[self.char_index - 2:self.char_index] == '  '
                      and self.line[self.char_index - 3] != ' '):
                    return False
                return True
            self.char_index += 1

    def s005(self) -> bool:  # TODO found (in comments only and case-insensitive)
        self.char_index = 0
        while True:
            if self.char_index >= len(self.line):
                return False

            self.char = self.line[self.char_index]
            if self.char in {"'", '"'} and not self.close_quote():
                return False
            elif self.char == '#' and re.search(pattern=r'todo', string=self.line[self.char_index:], flags=re.I):
                return True
            self.char_index += 1

    def s006(self) -> bool:  # More than two blank lines preceding a code line
        if not self.line.strip() or self.line_number < 3:
            return False
        elif not ''.join(self.code[self.line_number - 3:self.line_number]).strip():
            return True
        return False

    def s007(self) -> bool:  # Too many spaces after construction_name (def or class)
        return (('def' in self.line or 'class' in self.line)
                and re.search(pattern=r'(?:def |class )(?:\s)', string=self.line))

    def s008(self) -> bool:  # Class name class_name should be written in CamelCase
        return ((names := self.visitor.class_names.get(self.line_number))
                and not all(map(lambda x: re.fullmatch(pattern=r'(?:[A-Z][A-Za-z\d_]+)', string=x), names)))

    def s009(self) -> bool:  # Function name function_name should be written in snake_case
        return ((name := self.visitor.function_names.get(self.line_number))
                and not re.fullmatch(pattern=r'(?:[a-z_])(?:[a-z\d_]*)', string=name))

    def s010(self) -> bool:  # Argument name arg_name should be written in snake_case
        return ((arguments := self.visitor.function_arguments_names.get(self.line_number))
                and not all(map(lambda x: re.fullmatch(pattern=r'[a-z_][a-z\d_]*', string=x), arguments)))

    def s011(self) -> bool:  # Variable var_name should be written in snake_case
        return ((names := self.visitor.local_vars.get(self.line_number))
                and not all(map(lambda x: re.fullmatch(pattern=r'(?:[a-z_])(?:[a-z\d_]*)', string=x), names)))

    def s012(self) -> bool:  # The default argument value is mutable
        if args_values := self.visitor.default_args_with_values.get(self.line_number):
            for arg, value in args_values:
                if isinstance(value, (list, set, dict)):
                    return True

    def check(self) -> None:
        for self.line_number, self.line in enumerate(self.code):
            for error in self.errors:
                if error['function']():
                    print(f'{self.file}: Line {self.line_number + 1}: {error['code']} {error['message']}')

    def start(self) -> None:
        for self.file in self.files:
            with open(self.file) as file:
                self.code = file.readlines()
            with open(self.file) as file:
                tree = ast.parse(file.read())
            self.visitor = Visitor()
            self.visitor.visit(tree)

            self.check()


def main() -> None:
    assert len(sys.argv) == 2
    path = sys.argv[1]
    if os.path.exists(path=path):
        analyzer = StaticCodeAnalyzer(path=path)
        analyzer.start()
    else:
        print(f"{path} doesn't exist.")


if __name__ == '__main__':
    main()
