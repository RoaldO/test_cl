"""
code generator that generates test that test if modules can be imported.
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

from pathlib import Path

from test_cl.generators.packages import PackagesGenerator
from .. import interface, helpers
from ... import simple_types as t


class ImportTestGenerator(interface.TestGenerator):
    """
    Generates test cases that will simply import source files to see if problems
    arise.
    This alone should provide a significant boost in reliability.
    """
    def __init__(self, *, project_root: "Path"):
        """ performs basic initialization of the component """
        super().__init__(project_root=project_root)
        self._template = helpers.TemplatedFileGenerator(
            project_root=project_root,
            namespace="import_test",
            name="test_file.jinja2",
        )

    def run(self, source_file: "t.SourceFile") -> None:
        """ performs the code generation """
        if self.is_applicable(source_file):

            source_root = source_file.project_root / "tests"

            test_source_path = self._get_test_source_path(
                source_file=source_file,
                source_root=source_root
            )

            PackagesGenerator(
                project_root=source_file.project_root
            ).run(
                source_file=t.SourceFile(
                    project_root=source_file.project_root,
                    source_root=source_root,
                    path=test_source_path.parent,
                )
            )

            test_source = t.SourceFile(
                project_root=source_file.project_root,
                source_root=source_root,
                path=test_source_path
            )

            self._template.write(
                test_source,
                data={
                    "source_file": source_file,
                },
            )

    @staticmethod
    def is_applicable(source_file: "t.SourceFile") -> bool:
        """
        checks the filename to see if we actually need to generate a test for
        this file
        """
        return all((
            source_file.path.is_file(),
            source_file.path.suffix == '.py',
            not str(source_file.path).endswith("/__main__.py"),
        ))

    @staticmethod
    def _get_test_source_path(
            *,
            source_file: "t.SourceFile",
            source_root: "Path",
    ) -> "Path":
        *mod_parent_parts, mod_self = source_file.identifier.parts
        module = ".".join([
            "imports",
            *mod_parent_parts,
            f"test_{mod_self}"
        ])
        return helpers.module_to_path(t.Module(module), root=source_root)
