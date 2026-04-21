	.data
testblz:
	.asciiz "12345678"
testknr:
	.asciiz "1234567890"
ibanbuf:
	.space 23
	.text
	.import "../../src/util.s"
	.import "../../src/moduloStr.s"
	.import "../../src/validateChecksum.s"
	.import "../../src/knr2iban.s"
	.globl main
main:
	la	a0 ibanbuf
	la	a1 testblz
	la	a2 testknr
	jal	knr2iban
	li	a0 10
	la	a0 ibanbuf
	li	a1 22
	jal	println_range
	ecall
	li	a0 10
	ecall
