	.data
numberstr:
	.asciiz "65539"
	.text
	.import "../../src/util.s"
	.import "../../src/moduloStr.s"
	.globl main
main:
	la	a0 numberstr
	li	a1 5
	li	a2 8
	jal	modulo_str
	mv	a1 a0
	li	a0 1
	ecall
	li	a0 10
	ecall
