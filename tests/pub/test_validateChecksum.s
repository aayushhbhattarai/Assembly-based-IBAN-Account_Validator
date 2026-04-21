	.data
ibanstr:
	.asciiz "DE42413746471724057190"
	.text
	.import "../../src/util.s"
	.import "../../src/moduloStr.s"
	.import "../../src/validateChecksum.s"
	.globl main
main:
	la	a0 ibanstr
	jal	validate_checksum
	mv	a1 a0
	li	a0 1
	ecall
	li	a0 10
	ecall
