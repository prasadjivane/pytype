"""Tests for arg_parser."""

import argparse
import types

from pytype import config as pytype_config
from pytype import datatypes
from pytype.tools import arg_parser

import unittest


class TestConvertString(unittest.TestCase):
  """Test arg_parser.convert_string."""

  def test_int(self):
    self.assertEqual(arg_parser.convert_string('3'), 3)

  def test_bool(self):
    self.assertIs(arg_parser.convert_string('True'), True)
    self.assertIs(arg_parser.convert_string('False'), False)

  def test_whitespace(self):
    self.assertEqual(arg_parser.convert_string('err1,\nerr2'), 'err1,err2')


def make_parser():
  """Construct a parser to run tests against."""

  parser = argparse.ArgumentParser()
  parser.add_argument(
      '-v', '--verbosity', dest='verbosity', type=int, action='store',
      default=1)
  parser.add_argument(
      '--config', dest='config', type=str, action='store', default='')

  # Add options from pytype-single.
  wrapper = datatypes.ParserWrapper(parser)
  pytype_config.add_basic_options(wrapper)
  return arg_parser.Parser(parser, wrapper.actions)


class TestParser(unittest.TestCase):
  """Test arg_parser.Parser."""

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.parser = make_parser()

  def test_verbosity(self):
    self.assertEqual(self.parser.parse_args(['--verbosity', '0']).verbosity, 0)
    self.assertEqual(self.parser.parse_args(['-v1']).verbosity, 1)

  def test_config(self):
    args = self.parser.parse_args(['--config=test.cfg'])
    self.assertEqual(args.config, 'test.cfg')

  def test_pytype_single_args(self):
    args = self.parser.parse_args(['--disable=import-error'])
    self.assertSequenceEqual(args.disable, ['import-error'])

  def test_postprocess(self):
    args = types.SimpleNamespace(disable='import-error')
    self.parser.postprocess(args)
    self.assertSequenceEqual(args.disable, ['import-error'])

  def test_postprocess_from_strings(self):
    args = types.SimpleNamespace(report_errors='False', protocols='True')
    self.parser.postprocess(args, from_strings=True)
    self.assertFalse(args.report_errors)
    self.assertTrue(args.protocols)


if __name__ == '__main__':
  unittest.main()
