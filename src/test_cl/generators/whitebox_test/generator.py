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

from .. import interface, helpers
from ..packages import PackagesGenerator
from ... import simple_types as t
from ...helpers import AstWrapper


class WhiteboxTestGenerator(interface.TestGenerator):
    def __init__(self, *, project_root: "Path"):
        """ performs basic initialization of the component """
        super().__init__(project_root=project_root)
        self._method_template = helpers.TemplatedFileGenerator(
            project_root=project_root,
            namespace="whitebox_test",
            name="method.jinja2",
        )

    def run(self, source_file: "t.SourceFile") -> None:
        if self.is_applicable(source_file):
            source_root = self._get_tests_root(source_file.project_root)
            module = self._get_test_file_module(source_file)
            test_package_base = source_root / "/".join(module.split("."))

            ast_wrapper = AstWrapper(source_file)
            package_generator = PackagesGenerator(project_root=source_file.project_root)

            for class_def in ast_wrapper.iter_classes():
                test_source_package = test_package_base / class_def.identifier
                package_generator.run(
                    source_file=t.SourceFile(
                        project_root=source_file.project_root,
                        source_root=source_root,
                        path=test_source_package
                    ),
                )
                self._generate_method_tests(
                    ast_wrapper=ast_wrapper,
                    class_def=class_def,
                    source_file=source_file,
                    source_root=source_root,
                    test_source_package=test_source_package,
                )

    def _generate_method_tests(self, ast_wrapper, class_def, source_file, source_root, test_source_package):
        for function_def in ast_wrapper.iter_functions(class_def.ast_node):
            self._method_template.write(
                t.SourceFile(
                    project_root=source_file.project_root,
                    source_root=source_root,
                    path=test_source_package / f"test_{function_def.identifier}.py"
                ),
                data={
                    "source_file": source_file,
                    "class_def": class_def,
                    "function_def": function_def,
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
    def _get_tests_root(project_root: "Path") -> "Path":
        return project_root / "tests"

    @staticmethod
    def _get_test_file_module(source_file: "t.SourceFile") -> "t.Module":
        mod_parent, _, mod_self = source_file.identifier.rpartition(".")
        return t.Module(f"whitebox.{mod_parent}.test_{mod_self}")
