	.data
	.globl  validate_checksum
	.text

# -- validate_checksum --
# Arguments:
# a0 : Address of a string containing a german IBAN (22 characters)
# Return:
# a0 : the checksum of the IBAN
validate_checksum:
# TODO
	jr      ra
