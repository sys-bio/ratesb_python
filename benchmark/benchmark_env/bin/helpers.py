""" Helpers for Tests. """

from SBMLKinetics.common import constants as cn

import os.path
import pandas as pd

DEBUG = False


def isValidDataFrame(df, expected_columns, min_rows=1,
    nan_columns=None, key=None,
    valid_dict=None):
  """
  Simple test of a data frame.
   a) Contains the expected columns
   b) Has a minimum number of rows
   c) Does not contain np.nan values
  :param pd.DataFrame df: DataFrame to validate
  :param list-of-str expected_columns:
  :param int min_rows:
  :param list-of-str nan_columns: columns where there may be nan
      values
  :param str or list-of-str key: Columns that is a key
  :param dict valid_dict: key=column name, value=function of value
  :return bool: True if passes tests
  """
  bads = [x for x in expected_columns if not x in df.columns.tolist()]
  if len(bads) > 0:
    if DEBUG:
      import pdb; pdb.set_trace()
    return False
  if len(df) < min_rows:
    if DEBUG:
      import pdb; pdb.set_trace()
    return False
  if (key is not None) and len(key) > 0:
    df_key = pd.DataFrame(df[key])
    if len(key) == 1:
      keys = df[key]
      if cn.NONE in keys:
        keys.remove(cn.NONE)
        df_key[key] = keys
    df_key = df_key.drop_duplicates()
    if len(df_key) != len(df.drop_duplicates()):
      if DEBUG:
        import pdb; pdb.set_trace()
      return False
  if valid_dict is not None:
    for col, func in valid_dict.items():
      trues = [func(x) for x in df[col]]
      if not all(trues):
        import pdb; pdb.set_trace()
        if DEBUG:
          import pdb; pdb.set_trace()
        return False
  return True
