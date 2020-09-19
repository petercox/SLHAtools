"""Module for reading/writing SLHA files.

Defines SLHAdata class for storing/manipulating SLHA data. 

Author: Peter Cox 
Last Update: 5 Sep 2018
"""

__version__ = 1.1
__author__ = "Peter Cox"

import sys
from collections import OrderedDict
from contextlib import contextmanager

###############################################

# Commonly used particle IDs for accessing decay information
SM_pid = {'d':1, 'u':2, 's':3, 'c':4, 'b':5, 't':6,
 		  'e':11, 've':12, 'mu':13, 'vm':14, 'tau':15, 'vt':16,
 		  'g':21, 'a':22, 'Z':23, 'W':24}

Higgs_pid = {'h': 25, 'H0': 35, 'A0':36, 'H+':37}

MSSM_pid = {'~dL':1000001, '~uL':1000002, '~sL':1000003, '~cL':1000004, '~b1':1000005,'~t1':1000006,
			'~eL':1000011, '~ve':1000012, '~muL':1000013, '~vmu':1000014, '~tau1':1000015, '~vt':1000016,
			'~dR':2000001, '~uR':2000002, '~sR':2000003, '~cR':2000004, '~b2':2000005,'~t2':2000006,
			'~eR':2000011, '~veR':2000012, '~muR':2000013, '~vmuR':2000014, '~tau2':2000015, '~vtR':2000016,
			'~g':1000021, '~N1':1000022, '~N2':1000023, '~C1':1000024, '~N3':1000025, '~N4':1000035, '~C2':1000037, '~G':1000039}

PIDs = {}
PIDs.update(SM_pid)
PIDs.update(Higgs_pid)
PIDs.update(MSSM_pid)

###############################################

class SLHAdata:
	"""Class to store SLHA data and provide get/set functionality."""

	def __init__(self, data=None):
		self.preamble = ''
		self.blocks = OrderedDict()
		self.decays = OrderedDict()

	def __str__(self):
		return '<SLHAdata: {} blocks, {} decays>'.format(len(self.blocks), len(self.decays))

	def Blocks(self):
		return self.blocks.keys()

	def Decays(self):
		return self.decays.keys()

	def FindBlock(self, blockname):
		"""Finds first block that matches blockname."""
		
		for block in self.blocks.keys():
			if block.startswith(blockname):
				return block

	def GetBlock(self, blockname):
		try:
			return self.blocks[blockname]['data']
		except KeyError:
			print "No block named '{}'!".format(blockname)
			return None

	def GetBlockString(self, blockname):
		try:
			return _BlockToString(self.blocks[blockname])
		except KeyError:
			print "No block named '{}'!".format(blockname)
			return ''

	def GetValue(self, block, id):
		try:
			return self.blocks[block]['data'][id]['value']
		except KeyError:
			print "No parameter '{}' in block '{}'!".format(id, block)
			return None

	def SetValue(self, block, id, value):
		try:
			self.blocks[block]['data'][id]['value'] = value
		except KeyError:
			print "No parameter '{}' in block '{}'!".format(id, block)
			return 1
		return 0

	def GetDecay(self, particle):
		pid = GetPID(particle)
		try:
			return self.decays[pid]['data']
		except KeyError:
			print "No decays for particle '{}'.".format(pid)
			return None

	def GetDecayString(self, particle):
		pid = GetPID(particle)
		try:
			return _DecayToString(self.decays[pid])
		except KeyError:
			print "No decays for particle '{}'.".format(pid)
			return ''

	def GetWidth(self, particle):
		pid = GetPID(particle)
		try:
			return self.decays[pid]['width']
		except KeyError:
			print "No decays for particle '{}'.".format(pid)
			return None

	def GetBR(self, particle, daughters):
		pid = GetPID(particle)
		try:
			return self.decays[pid]['data'][daughters]['BR']
		except KeyError:
			#print "Decay mode {} -> {} not found!".format(pid, daughters)
			return 0.


	def Write(self, SLHAfile=sys.stdout):
		"""Write SLHA data.

		SLHAfile can be a filename, sys.stdout (default), or sys.stderr.
		"""
		with _IOstream(SLHAfile) as fSLHA:

			# Write preamble
			fSLHA.write(self.preamble + '\n')
		
			# Write blocks
			for block in self.blocks.values():
				fSLHA.write(_BlockToString(block) + '\n')
				fSLHA.write(block['comments'] + '\n')

			# Write decays 
			for decay in self.decays.values():
				fSLHA.write(_DecayToString(decay) + '\n')
				fSLHA.write(decay['comments'] + '\n')

###############################################

def GetPID(particle):
	if isinstance(particle, str):
		try:
			return PIDs[particle]
		except KeyError:
			print "Particle '{}' is unknown.".format(particle)
			return None
	else:
		return particle

###############################################

def ReadSLHA(SLHAfile):
	"""Read an SLHA file and return SLHAdata instance."""

	with open(SLHAfile) as fSLHA:

		SLHA_data = SLHAdata()	
		data_type = None

		for line in fSLHA.readlines():
			line = line.strip()

			# Get comments
			if line.startswith('#'):
				if data_type == None:
					SLHA_data.preamble += (line + '\n')
				elif data_type == 'B':
					SLHA_data.blocks[block]['comments'] += (line + '\n')
				elif data_type == 'D':
					SLHA_data.decays[pid]['comments'] += (line + '\n')
				continue

			# Separate data and description
			data = line.split('#',1)[0]
			try:
				description = line.split('#',1)[1]
			except IndexError:
				description = ''

			# New block
			if line.lower().startswith('block'):
				data_type = 'B'
				block = data.split(None,1)[1].strip()
				try:
					SLHA_data.blocks[block]
					print "WARNING: multiple '{}' blocks. Only first will be kept!".format(block)
				except KeyError:
					SLHA_data.blocks[block] = {'name': block, 'description': description, 'comments': '', 'data': OrderedDict()}

			# New decay
			elif line.lower().startswith('decay'):
				data_type = 'D'
				data = data.split()
				pid = int(data[1])
				width = float(data[2])
				try:
					SLHA_data.decays[pid]
					print "WARNING: multiple decay tables for {}. Only first will be kept!".format(pid)
				except KeyError:
					SLHA_data.decays[pid] = {'pid': pid, 'width': width, 'description': description, 'comments': '', 'data': OrderedDict()}

			# Read block
			# For entries with more than 2 columns, key is a tuple of all columns except last
			# For more than three columns, tuple is kept as string
			elif data_type == 'B':
				data = data.split()
				columns = len(data)
				if columns == 0:
					continue
				if columns <= 2:
					try:
						keys = int(data[0])
					except ValueError:
						keys = data[0]
				elif columns == 3:
					try:
						keys = tuple([int(x) for x in data[:-1]])
					except ValueError:
						keys = tuple(data[:-1])
				else:
					keys = tuple(data[:-1])

				value = data[-1]

				try:
					SLHA_data.blocks[block]['data'][keys]
					print "WARNING: repeat entries in block {}. Only first will be kept!".format(block)
				except KeyError:
					SLHA_data.blocks[block]['data'][keys] = {'key': keys, 'value': value, 'description': description, 'columns': columns}

			# Read decay
			elif data_type == 'D':
				data = data.split()
				if len(data) < 4:
					continue

				BR = float(data[0])
				Nbody = int(data[1])
				daughters = [int(d) for d in data[2:]]

				try:
					SLHA_data.decays[pid]['data'][tuple(daughters)]
					print "WARNING: repeat entries in decay table for {}. Only first will be kept!".format(pid)
				except KeyError:
					SLHA_data.decays[pid]['data'][tuple(daughters)] = {'N-body': Nbody, 'daughters': tuple(daughters), 'BR': BR, 'description': description}

	return SLHA_data

###############################################

def _BlockToString(block):
	"""Convert block to string for printing/writing."""

	blockstring = 'BLOCK ' + block['name']
	if block['description'] != '':
		blockstring += '    # ' + block['description']

	for param in block['data'].values():
		blockstring += '\n  '

		if isinstance(param['key'], int) or isinstance(param['key'], basestring):
			blockstring += '{:<3}  '.format(param['key'])
		else:
			for k in param['key']:
				blockstring += '{:<2}  '.format(k)

		if param['columns'] > 1: 
			blockstring += '{:<16}'.format(param['value'])
		if param['description'] != '':
			blockstring += '    # ' + param['description']

	return blockstring

###############################################

def _DecayToString(decay):
	"""Convert decay to string for printing/writing."""

	decaystring = 'DECAY   {:<8}   {:<16}'.format(decay['pid'], decay['width'])
	if decay['description'] != '':
		decaystring += '    # ' + decay['description']

	for dmode in decay['data'].values():
		decaystring += '\n  {:<16}'.format(dmode['BR'])

		for d in dmode['daughters']:
			decaystring += '  {:>8}'.format(d)

		if dmode['description'] != '':
			decaystring += '    # ' + dmode['description']

	return decaystring

###############################################

@contextmanager
def _IOstream(file):
	if file == sys.stdout:
		yield sys.stdout
	elif file == sys.stderr:
		yield sys.stderr
	else:
		f = open(file, 'w')
		yield f
		f.close()

###############################################