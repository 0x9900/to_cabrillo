#! /usr/bin/env python
# vim:fenc=utf-8
#
# Copyright © 2024 fred <github-fred@hidzz.com>
#
# Distributed under terms of the BSD 3-Clause license.
import argparse
import sys
from contextlib import ExitStack
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import (Any, Callable, ClassVar, Dict, Optional, ParamSpec, Set,
                    TextIO, TypeVar)

import jinja2
import toml
from adif_parser import AData, ParseADIF

P = ParamSpec('P')
R = TypeVar('R')
type FilterArg = str | int | float

config = None           # pylint: disable=invalid-name
jinja = jinja2.Environment()


def register(name: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
  """Register new filters for jinja"""
  def decorator(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
      return func(*args, **kwargs)
    jinja.filters[name] = wrapper
    return wrapper
  return decorator


@register('lpad')
def lpad_filter(value: FilterArg, width: int, fillchar: str = ' ') -> str:
  return str(value).rjust(width, fillchar)


@register('rpad')
def rpad_filter(value: FilterArg, width: int, fillchar: str = ' ') -> str:
  return str(value).ljust(width, fillchar)


@register('date')
def date_filter(value: str) -> str:
  return datetime.strptime(value, '%Y%m%d').date().strftime('%Y-%m-%d')


class Config:
  _instance: ClassVar[Optional['Config']] = None
  _config_keys: ClassVar[Set[str]] = set(['header', 'footer', 'line'])
  _config: ClassVar[Dict[str, Any]]
  variables: ClassVar[Dict[str, Any]]
  templates: ClassVar[Dict[str, str]]

  def __new__(cls, filename: Path) -> 'Config':
    if cls._instance:
      return cls._instance

    with filename.open('r') as fd:
      cls._config = toml.load(fd)
      cls.variables = cls._config['variables']
      cls.templates = {}
      for key, val in cls._config['templates'].items():
        cls.templates[key] = val
      if cls._config_keys & set(cls.templates.keys()) != cls._config_keys:
        raise SystemError('Missing variables in the configuration file')

    obj = super().__new__(cls)
    cls._instance = obj
    return cls._instance

  def __repr__(self) -> str:
    return str(self._config)


def process_lines(data: AData, file: TextIO) -> None:
  assert config is not None
  line = config.templates['line'].split('\n')
  line = ' '.join(line)
  template = jinja.from_string(line)

  for row in data:
    start_date = datetime.strptime(row["QSO_DATE"] + ' ' + row["TIME_ON"], '%Y%m%d %H%M%S')
    row['DATE_TIME'] = start_date.strftime('%Y-%m-%d %H%M')
    line = template.render(**row)
    print(line, file=file)


def make_header(file: TextIO) -> None:
  assert config is not None
  template = jinja.from_string(config.templates['header'])
  header = template.render(**config.variables)
  print(header, file=file, end='\n\n')


def make_footer(file: TextIO) -> None:
  assert config is not None
  print(config.templates['footer'], file=file)


def gen_cabrillo(cab_file: Path, adif: AData) -> None:
  with ExitStack() as stack:
    if cab_file == Path('-'):
      fdout = sys.stdout
    else:
      outfile = cab_file.expanduser().absolute()
      print(f'Write {outfile}')
      fdout = stack.enter_context(outfile.open('w', encoding='UTF-8'))

    make_header(fdout)
    process_lines(adif, fdout)
    make_footer(fdout)


def main() -> None:
  global config      # pylint: disable=global-statement

  parser = argparse.ArgumentParser(description="ADIF to Cabrillo")
  parser.add_argument('--config', type=Path, default='config.toml',
                      help='Configuration file (default: %(default)s)')
  parser.add_argument('-a', '--adif-file', type=Path, required=True,
                      help='Adif filename')
  parser.add_argument('-c', '--cabrillo-file', type=Path, required=True,
                      help='Cabrillo filename (output)')
  opts = parser.parse_args()

  config = Config(opts.config)
  try:
    with opts.adif_file.open('r') as fdi:
      adif = ParseADIF(fdi)
      if adif.contacts is None:
        raise SystemExit('No Contacts to process')
  except FileNotFoundError as err:
    print(err, file=sys.stderr)
    raise SystemExit('File not found')

  gen_cabrillo(opts.cabrillo_file, adif.contacts)


if __name__ == "__main__":
  main()
