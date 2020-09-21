# SLHAtools
Python module for reading/writing SLHA files.

## Module functions

**ReadSLHA(SLHAfile)**:
    *Read an SLHA file and return SLHAdata instance.*

**GetPID(particle)**:
    *Get particle ID from name.*

## Class: SLHAdata
*Class to store SLHA data and provide get/set functionality.*

**Blocks(self)**:
		*Returns a list of block names.*

**Decays(self)**:
		*Returns a list of particle IDs that have decay information.*

**FindBlock(self, blockname)**:
		*Finds first block that matches blockname.*
    
**GetBlock(self, blockname)**:
		*Returns a block as an OrderedDict.*

**GetBlockString(self, blockname)**:
		*Returns a block as a string.*

**GetValue(self, block, id)**:
		*Returns the value of an entry in a block.*

**SetValue(self, block, id, value)**:
		*Sets the value of an entry in a block.*

**GetDecay(self, particle)**:
		*Returns decay information for particle as an OrderedDict.*

**GetDecayString(self, particle)**:
		*Returns decay information for particle as a string.*

**GetWidth(self, particle)**:
		*Returns decay width of particle.*

**GetBR(self, particle, daughters)**:
		*Returns branching ratio for a given decay process.*

**Write(self, SLHAfile=sys.stdout)**:
		*Write SLHA data.*
		*SLHAfile can be a filename, sys.stdout (default), or sys.stderr.*
