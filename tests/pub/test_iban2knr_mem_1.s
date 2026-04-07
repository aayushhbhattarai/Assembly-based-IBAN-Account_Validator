	.data
ibanstr:
	.asciiz "DE00111111112222222222"
redzone:
	.byte -1 -1 -1 -1
knrbuf:
	.space 10
blzbuf:
	.space 8
	.text
	.import "../../src/util.s"
	.import "../../src/iban2knr.s"
	.globl main
main:
	la	a0 ibanstr
	la	a1 blzbuf
	la	a2 knrbuf
	jal	iban2knr
verify_redzone:
	la	a0 redzone
	lw	t0 0(a0)
	li	a1 0
	li	t1 -1
	bne	t0 t1 rz_fail
	li	a1 1
rz_fail:
	li	a0 1
	ecall
	li	a0 10
	ecall
