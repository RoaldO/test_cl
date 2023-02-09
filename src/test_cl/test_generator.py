"""
facade definition
"""
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

import typing as tg
from pathlib import Path

from test_cl.generators.import_test import ImportTestGenerator
from test_cl.generators.whitebox_test import WhiteboxTestGenerator
from test_cl.helpers import iter_files
from test_cl.simple_types import SourceFile


class TestGenerator:
    """ The facade class that provides all public functionality """
    def __init__(self, project_root: "Path"):
        if not project_root.exists():
            raise FileNotFoundError(f'project root {project_root!r} not found')
        self._project_root = project_root
        self._source_roots = {
            "src",
            # "sources",
        }
        self._generators = {
            ImportTestGenerator(project_root=self._project_root),
            WhiteboxTestGenerator(project_root=self._project_root),
        }

    def run(self):
        """ runs the generation process """
        for source_file in self.get_source_files():
            self.generate_resources(source_file)

    def get_source_files(self) -> tg.Generator["SourceFile", None, None]:
        """ gets a generator that yields all the source files in the project for which the test creator is called """
        for source_root in self._source_roots:
            for path in iter_files(top=self._project_root / source_root):
                yield SourceFile(
                    project_root=self._project_root,
                    source_root=self._project_root / source_root,
                    path=path,
                )

    def generate_resources(self, source_file: "SourceFile") -> None:
        """ generates all test scripts and resources for the specified source file """
        for generator in self._generators:
            generator.run(source_file)
