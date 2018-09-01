import requests
from typing import Dict, List

from consts import API_URL_BASE, INVALID_LANG


headers: Dict[str, str] = requests.utils.default_headers()
headers.update({
	'User-Agent': 'curl'
})


def get_cht(cmd: List[str]) -> str:
	'''
	Gets the output from the cht.sh server.
	:param cmd: input for the server
	'''
	if '--shell' in cmd:
		return 'Shell mode is not available.'

	# get a response for cmd
	response = requests.get(f"{API_URL_BASE}{cmd[0]}/{'+'.join(cmd[1:])}", headers=headers)
	if response.status_code != 200 and response.status_code != 500:
		return 'Cannot acsess cheat.sh server at the moment'
	elif response.status_code == 500:  # internal server error
		return 'Somthing is wrong with the cheat servers'
	return response.text


def check_lang(lang: str) -> str:
	'''
	Finds the language in the language list to make sure it is valid.
	:return: an empty string if valid, or an error message.
	'''
	lines = get_cht([':list']).splitlines()
	if len(lines) == 1:  # error
		return lines[0]
	
	langs = set()
	for line in lines:
		ind = line.find('/')
		if ind != -1:
			if lang == line[:ind]:
				return ''
			langs.add(line[:ind])
	return INVALID_LANG.format(lang, '\t'.join(langs))