#! /usr/bin/env python
# vim:fenc=utf-8
#
# Copyright © 2024 fred <github-fred@hidzz.com>
#
# Distributed under terms of the BSD 3-Clause license.

import re
from pathlib import Path

# Pre-compiled regexes (moved outside class for reuse)
TAG_PATTERN = re.compile(r'<([^:>]+):(\d+)>([^<]*)')
EOH_PATTERN = re.compile(r'<eoh>', re.IGNORECASE)
EOR_PATTERN = re.compile(r'<eor>', re.IGNORECASE)
WHITESPACE_PATTERN = re.compile(r'\s+')

# Set for O(1) lookups instead of tuple checks
NON_FLOAT_TAGS = frozenset(['BAND', 'QSO_DATE', 'TIME_ON', 'QSO_DATE_OFF', 'TIME_OFF'])


class ParseADIF:
  def __init__(self, filename: Path | str) -> None:
    if isinstance(filename, str):
      filename = Path(filename)

    with filename.open('r', encoding='utf8') as fdi:
      text = fdi.read()
      self.parse_adif(text)

  def __iter__(self):
    yield self.adif_data

  def adif(self):
    return self.adif_data

  def parse_adif(self, adif_data):
    # Normalize whitespace in one pass
    adif_data = WHITESPACE_PATTERN.sub(' ', adif_data.strip())

    # Split on <eoh>
    parts = EOH_PATTERN.split(adif_data, maxsplit=1)

    if len(parts) == 2:
      self.header = ParseADIF.parse_lines(parts[0])
      self.adif_data = ParseADIF.parse_lines(parts[1])
    else:
      self.header = {}
      self.adif_data = ParseADIF.parse_lines(parts[0])

  @staticmethod
  def parse_lines(data: str) -> list:
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
        if tag_name not in NON_FLOAT_TAGS:
          try:
            value = float(value)
          except ValueError:
            pass  # Keep as string if conversion fails

        record[tag_name] = value

      if record:
        records.append(record)

    return records
