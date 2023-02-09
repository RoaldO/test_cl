""" various helper objects to be used by the code generators """
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

import importlib.resources
import os
import typing as tg
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, BaseLoader, Template

import test_cl.simple_types as t


class TemplatedFileGenerator:
    """ template renderer """
    def __init__(
            self, *,
            project_root: "Path",
            namespace: str,
            name: str,
    ):
        self._template = self._get_template(
            project_root=project_root,
            namespace=namespace,
            name=name,
        )

    def write(self, output_file: "t.SourceFile", data: tg.Any):
        template_result = self._template.render(
            run={
                'now': datetime.now(),
                'login': os.getlogin(),
                # TODO add the lib version number as well
            },
            data=data,
        )
        output_file.path.parent.mkdir(parents=True, exist_ok=True)
        if not output_file.path.exists():
            with open(output_file.path, 'w+') as file:
                file.write(template_result)

    def _get_template(self, *, project_root, namespace, name) -> "Template":
        for policy in [
            self._find_template_from_env_var,
            self._find_template_from_config_value,
            self._find_template_from_project_folder,
            self._find_template_from_user_home_folder,
            self._find_template_from_library_resource,
        ]:
            template_string = policy(
                    project_root=project_root,
                    namespace=namespace,
                    name=name,
            )
            if template_string is not None:
                return Environment(loader=BaseLoader()).from_string(template_string)
        raise FileNotFoundError()

    def _find_template_from_env_var(self, *, project_root, namespace, name) -> str:
        pass

    def _find_template_from_config_value(self, *, project_root, namespace, name) -> str:
        pass

    def _find_template_from_project_folder(self, *, project_root, namespace, name) -> str:
        pass

    def _find_template_from_user_home_folder(self, *, project_root, namespace, name) -> str:
        pass

    @staticmethod
    def _find_template_from_library_resource(*, project_root, namespace, name) -> str:
        return importlib.resources.read_text(
            package=f"test_cl.generators.{namespace}",
            resource=name,
        )


def module_to_path(module: "t.Module", *, root: "Path") -> "Path":
    """
    converts a module notation and a source root to a file path.
    """
    result = root
    *path_parts, file_part = module.split(".")
    for path_part in path_parts:
        result = result / path_part
    return result / f"{file_part}.py"
