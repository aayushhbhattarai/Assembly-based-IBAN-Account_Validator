.data
temp_iban:
	.space 30           # 24 bytes needed; a little extra for safety

	.globl validate_checksum
	.text


validate_checksum:
	addi    sp sp -20
	sw      s0 16(sp)
	sw      s1 12(sp)
	sw      s2 8(sp)
	sw      s3 4(sp)
	sw      ra 0(sp)

	mv      s0 a0              
	la      s1 temp_iban       


	addi    s2 s0 4             # s2 = &IBAN[4]
	li      t0 0
	li      t1 18
vc_copy_blzknr:
	lbu     t2 0(s2)
	sb      t2 0(s1)
	addi    s2 s2 1
	addi    s1 s1 1
	addi    t0 t0 1
	blt     t0 t1 vc_copy_blzknr

	li      s3 55
	li      t3 10

	lbu     t0 0(s0)
	sub     t0 t0 s3
	div     t1 t0 t3
	rem     t2 t0 t3
	addi    t1 t1 '0'
	addi    t2 t2 '0'
	sb      t1 0(s1)
	sb      t2 1(s1)
	addi    s1 s1 2

	lbu     t0 1(s0)
	sub     t0 t0 s3
	div     t1 t0 t3
	rem     t2 t0 t3
	addi    t1 t1 '0'
	addi    t2 t2 '0'
	sb      t1 0(s1)
	sb      t2 1(s1)
	addi    s1 s1 2

	lbu     t0 2(s0)
	sb      t0 0(s1)
	lbu     t0 3(s0)
	sb      t0 1(s1)

	la      a0 temp_iban
	li      a1 24
	li      a2 97
	jal     ra modulo_str     

	lw      ra 0(sp)
	lw      s3 4(sp)
	lw      s2 8(sp)
	lw      s1 12(sp)
	lw      s0 16(sp)
	addi    sp sp 20

	jr      ra