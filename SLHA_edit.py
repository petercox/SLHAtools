from SLHAtools import ReadSLHA

def main():

	# Read an SLHA file
	slha = ReadSLHA('test.slha')

	# Get List of blocks
	print slha.Blocks()

	# Get and set parameters
	print slha.GetValue('MINPAR', 3)
	slha.SetValue('MINPAR', 3, 10)
	print slha.GetValue('MINPAR', 3)

	# Get and set matrix parameters
	print slha.GetValue('NMIX', (1,3) )
	slha.SetValue('NMIX', (1,3), 0.5)
	print slha.GetValue('NMIX', (1,3) )

	# Get entire block
	slha.GetBlock('SMINPUTS')
	print slha.GetBlockString('SMINPUTS')

	# Get decay width
	print slha.GetWidth(1000021)
	print slha.GetWidth('~g')

	# Get BR
	print slha.GetBR(1000021, (-5,1000005))

	# Get all decay modes
	slha.GetDecay(1000021)
	print slha.GetDecayString(1000021)

	# Write modified slha file
	slha.Write('new.slha')


if __name__ == '__main__':
	main()
