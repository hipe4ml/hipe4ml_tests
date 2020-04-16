"""
Module used to generate the reference data for the tests
"""

import pickle
import sys
from pathlib import Path

from hipe4ml.tree_handler import TreeHandler

print("Generating the references for the tests ...")

# define paths for directories
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR.joinpath('Dplus7TeV')
REFERENCE_DIR = BASE_DIR.joinpath('references')

# define paths for files
DATA_FILE_PATH = DATA_DIR.joinpath('Bkg_Dpluspp7TeV_pT_1_50.root')
PROMPT_FILE_PATH = DATA_DIR.joinpath('Prompt_Dpluspp7TeV_pT_1_50.root')

# define dictionary for storing reference for the tests
INFO_DICT = {}

# preliminar check
if not REFERENCE_DIR.is_dir():
    sys.exit("No 'references' dir was found, so no reference data were produced!")

# instantiate tree handler objects
DATA_HDLR = TreeHandler(DATA_FILE_PATH, 'treeMLDplus')
PROMPT_HDLR = TreeHandler(PROMPT_FILE_PATH, 'treeMLDplus')

# store number of candidates in the original data sample
INFO_DICT['n_data'] = DATA_HDLR.get_n_cand()
INFO_DICT['n_prompt'] = PROMPT_HDLR.get_n_cand()

# store original variable list
INFO_DICT['data_var_list'] = PROMPT_HDLR.get_var_names()
INFO_DICT['prompt_var_list'] = PROMPT_HDLR.get_var_names()

# apply preselections
PRESEL_DATA = '(pt_cand > 1.30 and pt_cand < 42.00) and (inv_mass > 1.6690 and inv_mass < 2.0690)'
PRESEL_PROMPT = '(pt_cand > 1.00 and pt_cand < 25.60) and (inv_mass > 1.8320 and inv_mass < 1.8940)'

DATA_HDLR.apply_preselections(PRESEL_DATA)
PROMPT_HDLR.apply_preselections(PRESEL_PROMPT)

# store number of selcted data
INFO_DICT['n_data_preselected'] = DATA_HDLR.get_n_cand()
INFO_DICT['n_prompt_preselected'] = PROMPT_HDLR.get_n_cand()

# store preselections
INFO_DICT['data_preselections'] = DATA_HDLR.get_preselections()
INFO_DICT['prompt_preselections'] = PROMPT_HDLR.get_preselections()

# apply dummy eval() on the underlying data frame
DATA_HDLR.eval_data_frame('d_len_z = sqrt(d_len**2 - d_len_xy**2)')
PROMPT_HDLR.eval_data_frame('d_len_z = sqrt(d_len**2 - d_len_xy**2)')

# store new variable list
INFO_DICT['data_new_var_list'] = PROMPT_HDLR.get_var_names()
INFO_DICT['prompt_new_var_list'] = PROMPT_HDLR.get_var_names()

# get a random subset of the original data
DATA_HDLR = DATA_HDLR.get_subset(size=3000, rndm_state=42)
PROMPT_HDLR = PROMPT_HDLR.get_subset(size=55, rndm_state=42)

# slice both data and prompt data frame respect to the pT
BINS = [[0, 2], [2, 10], [10, 25]]

DATA_HDLR.slice_data_frame('pt_cand', BINS)
PROMPT_HDLR.slice_data_frame('pt_cand', BINS)

# store projection variable and binning
INFO_DICT['data_proj_variable'] = DATA_HDLR.get_projection_variable()
INFO_DICT['prompt_proj_variable'] = PROMPT_HDLR.get_projection_variable()

INFO_DICT['data_binning'] = DATA_HDLR.get_projection_binning()
INFO_DICT['prompt_binning'] = PROMPT_HDLR.get_projection_binning()

# get info from a single data slice
DATA_SLICE = DATA_HDLR.get_slice(2)
PROMPT_SLICE = PROMPT_HDLR.get_slice(2)

INFO_DICT['n_data_slice'] = len(DATA_SLICE)
INFO_DICT['n_prompt_slice'] = len(PROMPT_SLICE)

# save data slice DataFrame as pickle file
DATA_SLICE_PATH = REFERENCE_DIR.joinpath('data_slice.pickle')
DATA_SLICE.to_pickle(DATA_SLICE_PATH)

print(f"data_slice saved in '{DATA_SLICE_PATH}'")

# save prompt slice DataFrame as pickle file
PROMPT_SLICE_PATH = REFERENCE_DIR.joinpath('prompt_slice.pickle')
PROMPT_SLICE.to_pickle(PROMPT_SLICE_PATH)

print(f"data_slice saved in '{PROMPT_SLICE_PATH}'")

# save info dictionary as pickle file
INFO_DICT_PATH = f'{REFERENCE_DIR}/reference_dict.pickle'
with open(INFO_DICT_PATH, 'wb') as handle:
    pickle.dump(INFO_DICT, handle, protocol=pickle.HIGHEST_PROTOCOL)

print(f"info_dict saved in '{INFO_DICT_PATH}'")

print("References for the tests generated successfully!")
