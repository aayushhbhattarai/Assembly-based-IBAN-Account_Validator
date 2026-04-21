	.data
	.globl main
numberstr:
	.asciiz "1337"
numberstr_end:
	.text
.import "../../src/util.s"
.import "../../src/moduloStr.s"
main:
	la a0 numberstr
	la a1 numberstr_end
	sub a1 a1 a0
	addi a1 a1 -1
	li a2 42
	jal modulo_str
	mv a1 a0
	li a0 1
	ecall
	li a0 10
	ecall
