	.data
	.globl validate_checksum
	.text

# -- validate_checksum --
# Arguments:
# a0 : Address of a string containing a german IBAN (22 characters)
# Return:
# a0 : the checksum of the IBAN
validate_checksum:
	addi   sp sp -16
	sw     s0 12(sp)
	sw     s1 8(sp)
	sw     ra 4(sp)

	mv     s0 a0

	addi   s0 s0 4
	li     t0 0
	li     t1 18


blzknrcopy:
	lbu    t2 0(s0)
	sb     t2 0(s1)

	addi   s0 s0 1
	addi   s1 s1 1

	addi   t0 t0 1
	blt    t0 t1 blzknrcopy

	li     t2 49
	sb     t2 19(s1)
	li     t2 51
	sb     t2 20(s1)
	li     t2 49
	sb     t2 21(s1)
	li     t2 52
	sb     t2 22(s1)

	lbu    t2 -2(s0)
	sb     t2 23(s1)
	lbu    t2 -3(s0)
	sb     t2 24(s1)

	la     a0 temp_iban
	li     a1 24
	li     a2 97
	jal    ra, modulo_str


	lw     ra, 4(sp)
	lw     s1, 8(sp)
	lw     s0, 12(sp)
	addi   sp, sp, 16

	jr     ra
