	.data
	.globl modulo_str
	.text

# --- modulo_str ---
# Arguments:
# a0: start address of the buffer
# a1: number of bytes in the buffer
# a2: divisor
# Return:
# a0: the decimal number (encoded using ASCII digits '0' to '9') in the buffer [a0 to a0 + a1 - 1] modulo a2
modulo_str:
# TODO
	jr     ra
