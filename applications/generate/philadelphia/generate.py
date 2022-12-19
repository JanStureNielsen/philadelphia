#
# Copyright 2015 Philadelphia authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os.path
import sys

from . import model
from . import orchestra
from . import quickfix
from . import repository
from . import source


USAGE = '''\
Usage: philadelphia-generate <command> <configuration-file> <input-path>

Commands:
  enumerations  Generate enumerations
  msg-types     Generate message types
  tags          Generate tags
'''


def enumerations(dialect: model.Dialect, source: source.Source, path: str) -> None:
    enumerations = source.read_enumerations(path)
    print(model.format_enumerations(enumerations, dialect))


def msg_types(dialect: model.Dialect, source: source.Source, path: str) -> None:
    messages = source.read_messages(path)
    print(model.format_msg_types(messages, dialect))


def tags(dialect: model.Dialect, source: source.Source, path: str) -> None:
    fields = source.read_fields(path)
    print(model.format_tags(fields, dialect))


def find_source(path: str) -> source.Source:
    if os.path.isdir(path):
        return repository
    if 'fixr:repository' in read(path):
        return orchestra
    return quickfix


def read(path: str) -> str:
    with open(path, 'r') as infile:
        return infile.read()


COMMANDS = {
    'enumerations': enumerations,
    'msg-types': msg_types,
    'tags': tags,
}


def main():
    if len(sys.argv) != 4:
        sys.exit(USAGE)

    command = COMMANDS.get(sys.argv[1])
    if not command:
        sys.exit('error: {}: Unknown command'.format(sys.argv[1]))

    config = sys.argv[2]
    path = sys.argv[3]

    dialect = model.read_dialect(config)
    source = find_source(path)

    command(dialect, source, path)


if __name__ == '__main__':
    main()
