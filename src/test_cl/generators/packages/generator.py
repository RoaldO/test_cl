"""
code generator that places __init__.py files in folders to transform them into
packages.
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

from .. import interface, helpers
from ... import simple_types as t


class PackagesGenerator(interface.TestGenerator):
    def __init__(self, *, project_root: "Path"):
        """ performs basic initialization of the component """
        super().__init__(project_root=project_root)
        self._template = helpers.TemplatedFileGenerator(
            project_root=project_root,
            namespace="packages",
            name="init.jinja2",
        )

    def run(self, source_file: "t.SourceFile") -> None:
        """ performs the code generation """
        if source_file.path.parent != source_file.source_root:
            self.run(source_file=t.SourceFile(
                project_root=source_file.project_root,
                source_root=source_file.source_root,
                path=source_file.path.parent
            ))
        self._template.write(
            output_file=t.SourceFile(
                project_root=source_file.project_root,
                source_root=source_file.source_root,
                path=source_file.path / "__init__.py"
            ),
            data={
                "source_file": source_file,
            },
        )
