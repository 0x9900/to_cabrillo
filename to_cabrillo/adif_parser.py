#! /usr/bin/env python
# vim:fenc=utf-8
#
# Copyright © 2024 fred <github-fred@hidzz.com>
#
# Distributed under terms of the BSD 3-Clause license.

import re
from pathlib import Path
from typing import Any, Callable, Dict, List, TypeAlias, TypeVar

# Pre-compiled regexes (moved outside class for reuse)
TAG_PATTERN = re.compile(r'<([^:>]+):(\d+)>([^<]*)')
EOH_PATTERN = re.compile(r'<eoh>', re.IGNORECASE)
EOR_PATTERN = re.compile(r'<eor>', re.IGNORECASE)
WHITESPACE_PATTERN = re.compile(r'\s+')

# Set for O(1) lookups instead of tuple checks
FLOAT_TAGS = frozenset(['FREQ', 'FRED_RX', 'DXCC', 'MY_CQ_ZONE', 'MY_ITU_ZONE'])
NON_FLOAT_TAGS = frozenset(['BAND', 'QSO_DATE', 'TIME_ON', 'QSO_DATE_OFF', 'TIME_OFF'])

T = TypeVar('T')
AData: TypeAlias = List[Dict[Any, Any]]


def try_convert(val: Any, converter: Callable[[Any], T]) -> Any | T:
  try:
    return converter(val)
  except ValueError:
    return val


class ParseADIF:
  def __init__(self, filename: Path | str) -> None:
    if isinstance(filename, str):
      filename = Path(filename)

    self._header: AData | None
    self._data: AData | None

    with filename.open('r', encoding='utf8') as fdi:
      text = fdi.read()
      self.parse_adif(text)

  @property
  def header(self) -> AData | None:
    return self._header

  @property
  def contacts(self) -> AData | None:
    return self._data

  def parse_adif(self, text: str) -> None:
    # Normalize whitespace in one pass
    text = WHITESPACE_PATTERN.sub(' ', text.strip())

    # Split on <eoh>
    parts = EOH_PATTERN.split(text, maxsplit=1)

    if len(parts) == 2:
      self._header = ParseADIF.parse_lines(parts[0])
      self._data = ParseADIF.parse_lines(parts[1])
    else:
      self._data = ParseADIF.parse_lines(parts[0])

  @staticmethod
  def parse_lines(data: str) -> AData:
    records = []

    # Split records based on <eor>
    raw_records = EOR_PATTERN.split(data)

    for raw_record in raw_records:
      record = {}
      # Use finditer directly
      for match in TAG_PATTERN.finditer(raw_record):
        tag_name, _length, value = match.groups()
        # Strip only once and convert to upper
        value = value.strip()
        if not value:
          continue

        tag_name = tag_name.strip().upper()
        if tag_name in FLOAT_TAGS:
          value = try_convert(value, int)
        elif tag_name not in NON_FLOAT_TAGS:
          value = try_convert(value, float)

        record[tag_name] = value

      if record:
        records.append(record)

    return records
