# SLHAtools
Python module for reading/writing SLHA files.

## Module functions

**ReadSLHA(SLHAfile)**\
*Read an SLHA file and return an SLHAdata instance.*

**GetPID(particle)**\
*Get particle ID from name.*

## Class: SLHAdata
*Class to store SLHA data and provide get/set functionality.*

### Member functions

**Blocks()**\
*Returns a list of block names.*

**Decays()**\
*Returns a list of particle IDs that have decay information.*

**FindBlock(blockname)**\
*Finds first block that matches blockname.*
    
**GetBlock(blockname)**\
*Returns a block as an OrderedDict.*

**GetBlockString(blockname)**\
*Returns a block as a string.*

**GetValue(block, entry)**\
*Returns the value of an entry in a block.*

**SetValue(block, entry, value)**\
*Sets the value of an entry in a block.*

**GetDecay(particle)**\
*Returns decay information for particle as an OrderedDict.*

**GetDecayString(particle)**\
*Returns decay information for particle as a string.*

**GetWidth(particle)**\
*Returns decay width of particle.*

**GetBR(particle, daughters)**\
*Returns branching ratio for a given decay process.*

**Write(SLHAfile=sys.stdout)**\
*Write SLHA data.*
*SLHAfile can be a filename or sys.stdout (default).*
