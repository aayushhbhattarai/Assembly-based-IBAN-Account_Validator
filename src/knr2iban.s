.data
temp_knr2iban:
	.space 24               # 22 bytes for the temp IBAN; 2 extra for safety

	.globl knr2iban
	.text


knr2iban:
	addi    sp sp -24
	sw      s0 20(sp)   
	sw      s1 16(sp)   
	sw      s2 12(sp)  
	sw      s3 8(sp)    
	sw      s4 4(sp)    
	sw      ra 0(sp)

	mv      s0 a0
	mv      s1 a1
	mv      s2 a2

	
	la      s3 temp_knr2iban
	li      t0 'D'
	sb      t0 0(s3)
	li      t0 'E'
	sb      t0 1(s3)
	li      t0 '0'
	sb      t0 2(s3)
	sb      t0 3(s3)

	# copy BLZ into temp[4..11]
	addi    t3 s3 4
	li      t0 0
	li      t1 8
k2i_blz:
	lbu     t2 0(s1)
	sb      t2 0(t3)
	addi    s1 s1 1
	addi    t3 t3 1
	addi    t0 t0 1
	blt     t0 t1 k2i_blz

	
	li      t0 0
	li      t1 10
k2i_knr:
	lbu     t2 0(s2)
	sb      t2 0(t3)
	addi    s2 s2 1
	addi    t3 t3 1
	addi    t0 t0 1
	blt     t0 t1 k2i_knr

	
	la      a0 temp_knr2iban
	jal     ra validate_checksum   # a0 = remainder


	li      t0 98
	sub     s4 t0 a0

	li      t0 'D'
	sb      t0 0(s0)
	li      t0 'E'
	sb      t0 1(s0)


	li      t0 10
	div     t1 s4 t0        # tens digit
	rem     t2 s4 t0        # ones digit
	addi    t1 t1 '0'
	addi    t2 t2 '0'
	sb      t1 2(s0)
	sb      t2 3(s0)

	
	la      t3 temp_knr2iban
	addi    t3 t3 4
	addi    t4 s0 4
	li      t0 0
	li      t1 18
k2i_final:
	lbu     t2 0(t3)
	sb      t2 0(t4)
	addi    t3 t3 1
	addi    t4 t4 1
	addi    t0 t0 1
	blt     t0 t1 k2i_final

	lw      ra 0(sp)
	lw      s4 4(sp)
	lw      s3 8(sp)
	lw      s2 12(sp)
	lw      s1 16(sp)
	lw      s0 20(sp)
	addi    sp sp 24

	jr      ra