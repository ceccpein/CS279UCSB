# Version: 1.0

import os
import sys
import json
import jsonpickle
import base64
import argparse
import requests
from pandas import DataFrame

# Change the following appropriately before running the script
JEOPARDY_SERVER = '10.0.10.10'
JEOPARDY_PORT = 0xDEAD
TIMEOUT = 5

# The API end-point
API_ENDPOINT = 'http://' + JEOPARDY_SERVER + ':' + str(JEOPARDY_PORT)

class Challenge:
    def __init__(self, challenge, ip, port, weight, hint, files):
        self.challenge = challenge
        self.ip = ip
        self.port = port
        self.weight = weight
        self.hint = hint
        self.files = files

def list_challenges():
	try:
		req = requests.get(API_ENDPOINT, timeout=TIMEOUT)
		challenges = jsonpickle.decode(req.text)
		df_challenges = DataFrame(challenges[1:], columns=challenges[0])
		df_challenges.index += 1
		print df_challenges
	except requests.exceptions.ConnectionError, ce:
		print '[x]: %s' % ce.message

def get_challenge(challenge_name):
	try:
		req = requests.get(API_ENDPOINT + '/challenge/%s' % challenge_name, timeout=TIMEOUT)
		challenge_info = json.loads(req.text)
		challenge_name = challenge_info['challenge']
		challenge_ip = challenge_info['ip']
		challenge_port = challenge_info['port']
		challenge_weight = challenge_info['weight']
		challenge_hint = challenge_info['hint']
		challenge_files = challenge_info['files']
		challenge = Challenge(challenge_name, challenge_ip, challenge_port, challenge_weight, challenge_hint, challenge_files)

		# Save the challenge archive
		archive_name = challenge_name + '.tar.gz'
		archive_data = base64.b64decode(challenge_info['archive'])
		with open(archive_name, 'w') as challenge_archive:
			challenge_archive.write(archive_data)
		print json.dumps(challenge.__dict__, indent=4)
	except requests.exceptions.ConnectionError, ce:
		print '[x]: %s' % ce.message
	except KeyError, ke:
		print "[x]: The challenge %s doesn't exist" % challenge_name

def submit_flag(handle, challenge_name, flag):
	try:
		req = requests.get(API_ENDPOINT + '/submit/%s/%s/%s' % (handle, challenge_name, flag), timeout=TIMEOUT)
		print req.text
	except requests.exceptions.ConnectionError, ce:
		print '[x]: %s' % ce.message

def get_leaderboard():
	try:
		req = requests.get(API_ENDPOINT + '/leaders', timeout=TIMEOUT)
		leaders = jsonpickle.decode(req.text)
		df_leaders = DataFrame(leaders[1:], columns=leaders[0])
		df_leaders.index += 1
		print df_leaders
	except requests.exceptions.ConnectionError, ce:
		print '[x]: %s' % ce.message

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Fetch challenges, submit the flags')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-l', '--list', action='store_true', help='List available challenges')
	group.add_argument('-c', '--challenge', nargs=1, help='Fetch the challenge from the server')
	group.add_argument('-e', '--leaders', action='store_true', help='Show the leaderboard')
	group.add_argument('-s', '--submit', nargs=3, help='Submit a flag', metavar=('HANDLE', 'CHALLENGE', 'FLAG'))
	if len(sys.argv) == 1:
	    parser.print_help(sys.stderr)
	    sys.exit(1)

	args = parser.parse_args()

	if args.list:
		list_challenges()
	elif args.challenge:
		challenge_name = args.challenge[0]
		get_challenge(challenge_name)
	elif args.leaders:
		get_leaderboard()
	elif args.submit:
		handle = args.submit[0]
		challenge_name = args.submit[1]
		flag = args.submit[2]
		submit_flag(handle, challenge_name, flag)
	else:
		print '[x]: Argument unknown'
