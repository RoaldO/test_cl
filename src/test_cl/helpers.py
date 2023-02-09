""" various helper objects and function """
#   Copyright 2023 RoaldO
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import ast
import typing as tg
from pathlib import Path
from . import simple_types as t


def iter_files(top: "Path") -> tg.Generator["Path", None, None]:
    """ iterates all files, folders and symlinks in a recursive manner """
    for child in top.iterdir():
        yield child
        if child.is_dir():
            yield from iter_files(top=child)


class AstWrapper:
    def __init__(self, source_file: "t.SourceFile"):
        self.source_file = source_file

    def iter_classes(self, node: "ASTNode" = None):
        source_text = self.source_file.path.read_text()
        node = node or ast.parse(source_text, filename=self.source_file.path)
        for child_node in ast.iter_child_nodes(node):
            match child_node:
                case ast.ClassDef():
                    yield t.ClassDef.from_ast(child_node)
                case ast.FunctionDef():
                    pass  # no need to dive deeper because we can't address the children
                case _:
                    yield from self.iter_classes(node=child_node)

    def iter_functions(self, node: "ASTNode" = None):
        source_text = self.source_file.path.read_text()
        node = node or ast.parse(source_text, filename=self.source_file.path)
        for child_node in ast.iter_child_nodes(node):
            match child_node:
                case ast.FunctionDef():
                    yield t.FunctionDef.from_ast(child_node)
                case _:
                    pass  # no need to dive deeper because we can't address the children
