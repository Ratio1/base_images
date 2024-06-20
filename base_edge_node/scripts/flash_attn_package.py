"""
The purpose of this script is to look at the latest flash_attn release
binaries and to print the URL to a .whl binary which is compatible with
the current platform.

The flash attention github repo is at https://github.com/Dao-AILab/flash-attention
and we will get the .whl binary its github releases.
"""

import torch as th
import sys
import requests
import platform

def get_versions_from_name(name):
  """
  Parses the package name of a given flash_attn release and gives
  us a dict of the build configurations:
    - flash_attn_version - version of the flash_attn release
    - cuda_version - what cuda version the wheel was build for
    - torch_version - what pytorch version the used
    - cxx11abi_version - if the CXX 11 ABI was used for the wheel build
       ('TRUE' or 'FALSE')
    - python_version0 - minumum python version
    - python_version1 - maximum python version
    - architecture - the architecture used for he build (e.g. x86_64)

  Parameters
  ----------
    name - the name of the wheel binary

  Returns
  -------
    dict, a dict of configurations -> values
  """
  import re
  # Parse the whl name. This assumes something about the naming, but
  # this is a standard thing for wheels so it should be fairly consistent.
  pattern = r"flash_attn-(?P<flash_attn_version>[^+]+)\+cu(?P<cuda_version>[^t]+)torch(?P<torch_version>[^c]+)cxx11abi(?P<cxx11abi_version>[^-]+)-cp(?P<python_version0>[^-]+)-cp(?P<python_version1>[^-]+)-linux_(?P<architecture>.+)\.whl"

  match = re.match(pattern, name)
  if match:
    versions = match.groupdict()
  else:
    raise ValueError('could not parse versions')
  return versions

def get_cuda_major_ver(cuda_ver):
  last_dot_position = cuda_ver.rfind('.')
  return cuda_ver[:last_dot_position].replace('.', '')

if __name__ == '__main__':
  # Interrogate the github API endpoint to get the data on the latest release.
  url = "https://api.github.com/repos/Dao-AILab/flash-attention/releases/latest"
  response = requests.get(url)
  data = response.json()
  assets = data['assets']

  cpver = f"{sys.version_info[0]}{sys.version_info[1]}"

  # Get the cuda major version and ignore the minor version.
  ccver = get_cuda_major_ver(th.version.cuda)

  for asset in assets:
    versions = get_versions_from_name(asset['name'])
    cxxabi = 'FALSE' if '-D_GLIBCXX_USE_CXX11_ABI=0' in th.__config__.show() else 'TRUE'
    if versions['cxx11abi_version'] != cxxabi:
      continue
    cuda_ver = get_cuda_major_ver(versions['cuda_version'])

    th_ver = versions['torch_version']
    p_ver = versions['python_version0']
    arch = versions['architecture']
    if p_ver != cpver:
      continue
    if not th.__version__.startswith(th_ver):
      continue
    if cuda_ver != ccver:
      continue
    if arch != platform.machine():
      continue
    print(asset['browser_download_url'])
    exit(0)
