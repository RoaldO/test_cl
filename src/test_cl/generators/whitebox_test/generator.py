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
            # FIXME de gegenereerde bestandsnamen kloppen nog niet
            source_root = source_file.project_root / "tests"

            mod_parent, _, mod_self = source_file.identifier.rpartition(".")
            module = t.Module(f"whitebox.{mod_parent}.test_{mod_self}")
            rel_path = "/".join(module.split("."))

            ast_wrapper = AstWrapper(source_file)

            for class_def in ast_wrapper.iter_classes():
                for function_def in ast_wrapper.iter_functions(class_def.ast_node):

                    test_source_path = source_root / \
                                       rel_path / \
                                       class_def.identifier / \
                                       f"test_{function_def.identifier}.py"

                    PackagesGenerator(
                        project_root=source_file.project_root
                    ).run(
                        source_file=t.SourceFile(
                            project_root=source_file.project_root,
                            source_root=source_root,
                            path=test_source_path.parent
                        ),
                    )

                    self._method_template.write(
                        t.SourceFile(
                            project_root=source_file.project_root,
                            source_root=source_root,
                            path=test_source_path
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
