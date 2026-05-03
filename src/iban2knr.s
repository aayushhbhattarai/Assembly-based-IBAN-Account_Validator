	.data
	.globl iban2knr
	.text
# -- iban2knr
# Arguments:
# a0: IBAN buffer (22 bytes)
# a1: BLZ buffer (8 bytes)
# a2: KNR buffer (10 bytes)
iban2knr:
	addi   sp sp -16
	sw     s0 12(sp)
	sw     s1 8(sp)
	sw     s2 4(sp)
	sw     ra 0(sp)

	addi   s0 a0 4
	mv     s1 a1

	li     t0 0
	li     t1 8

blzloop:
	lb     t2 0(s0)
	sb     t2 0(s1)

	addi   s0 s0 1
	addi   s1 s1 1

	addi   t0 t0 1
	blt    t0 t1 loop

	mv     s2 a2
	li     t0 0
	li     t3 10

knrloop:
	lb     t4 0(s0)
	sb     t4 0(s2)

	addi   s0 s0 1
	addi   s2 s2 1

	addi   t0 t0 1
	blt    t0 t3 knrloop


	lw     ra 0(sp)
	lw     s2 4(sp)
	lw     s1 8(sp)
	lw     s0 12(sp)
	addi   sp sp 16



	jr     ra
