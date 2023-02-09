""" file infor for the files read from the source folders """
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

from dataclasses import dataclass
from pathlib import Path
import ast
import typing as tg


@dataclass
class SourceFile:
    project_root: "Path"
    source_root: "Path"
    path: "Path"

    @property
    def identifier(self) -> "Module":
        if not self.path.is_file():
            raise ValueError(f"folder {self} has no valid module identifier")

        if str(self.path).startswith(str(self.source_root)):
            relative_file = str(self.path)[len(str(self.source_root)):]
            if relative_file.startswith('/'):
                relative_file = relative_file[1:]
            if relative_file.endswith("/__init__.py"):
                relative_file = relative_file[:-12]
            if relative_file.endswith(".py"):
                relative_file = relative_file[:-3]
            folder_parts = relative_file.split("/")
            identifier = ".".join(folder_parts)
            return Module(identifier)
        raise ValueError(f"{self} has no valid module identifier")


class Module(str):
    @property
    def parts(self):
        return self.split(".")


@dataclass()
class ClassDef:
    ast_node: tg.Any
    identifier: str

    @classmethod
    def from_ast(cls, ast_node: "ast.ClassDef") -> "ClassDef":
        return ClassDef(
            ast_node=ast_node,
            identifier=ast_node.name,
        )


@dataclass()
class Argument:
    identifier: tg.Optional[str]

    @classmethod
    def from_ast(cls, ast_node: "ast.ClassDef") -> "Argument":
        return Argument(
            identifier=getattr(ast_node, 'arg', None)
        )


@dataclass()
class FunctionDef:
    arguments: tg.List[Argument]
    ast_node: tg.Any
    identifier: str

    @classmethod
    def from_ast(cls, ast_node: "ast.ClassDef") -> "FunctionDef":
        return FunctionDef(
            arguments=[
                Argument.from_ast(arg)
                for arg in ast.iter_child_nodes(ast_node.args)
            ],
            ast_node=ast_node,
            identifier=ast_node.name,
        )
