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
	addi   sp sp -16
	sw     s0 12(sp)
	sw     s1 8(sp)
	sw     s2 4(sp)
	sw     ra 0(sp)

	li     s0 0          #remainder
	li     t3 10         #rem*10
	mv     t4 a2         #mod97

	mv     s1 a0         #pointer moved to blz
	li     t0 0          #counter
	mv     t1 a1         #total
	li     t2 48         #converter


convert:
	lbu    t5 0(s1)      #loading the first number unsigned
	addi   s1 s1 1       #pointer mve to 2nd number

	sub    t5 t5 t2      #convert the ascii number

	mul    s2 s0 t3      #mod math
	add    t5 t5 s2
	rem    s0 t5 t4

	addi   t0 t0 1       #increase counter
	blt    t0 t1 convert #loop back until done and go to finish

finish:
	mv     a0 s0         #moving at last to a0

	lw     ra 0(sp)
	lw     s2 4(sp)
	lw     s1 8(sp)
	lw     s0 12(sp)
	addi   sp sp 16

	jr     ra
