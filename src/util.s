	.data
	.globl  memcpy
	.globl  int_to_buf
	.globl  println
	.globl  print
	.globl  readbuf
	.globl  end
	.globl  error
	.globl  println_range

newlinestr:
	.asciiz "\n"
	.text

# -- memcpy --
# Arguments:
# a0: target address
# a1: source address
# a2: number of bytes
# Return: none
# Semantics:
# Copies the memory area [a1 to a1 + a2 - 1] to [a0 to a0 + a2 - 1]
memcpy:
	mv      t0 a0         # current target
	mv      t1 a1         # current source
	add     t2 a1 a2      # last source

mc_loop:
# copy over 1 byte from source to target
	lbu     t4 0(t1)
	sb      t4 0(t0)
	addi    t0 t0 1
	addi    t1 t1 1
	bltu    t1 t2 mc_loop # while current source != last

mv_return:
	jr      ra

# -- int_to_buf --
# Arguments:
# a0: positive integer
# a1: target address
# a2: number of digits (counted from the from right)
# Return: none
# Semantics:
# Writes the last a2 digits of the positive integer in a0 as a decimal string to the memory area [a1 to a1 + a2 - 1]
int_to_buf:
	mv      t2 a1         # start to write to
	add     t3 a1 a2
	addi    t1 t3 -1      # end to write to (position of last char)
	mv      t0 a0         # keep number
	li      t5 10         # number base

# move from back to front
ib_loop:
# t0 = remainder
	mv      t3 t0
	div     t0 t0 t5
	mul     t4 t0 t5
# t3 = t3 - ((t3/10)*10)
# (extract last digit)
	sub     t3 t3 t4

	addi    t3 t3 '0'
	sb      t3 0(t1)

	addi    t1 t1 -1
	bgeu    t1 t2 ib_loop

ib_return:
	jr      ra

# a0 : String
# a1 : number of characters
println_range:
	add     t1 a0 a1
	mv      t0 a0
pr_loop:
	bgeu    t0 t1 pr_exit
	lbu     a1 0(t0)
	li      a0 11
	ecall
	addi    t0 t0 1
	j       pr_loop

pr_exit:
	li      a1 10
	li      a0 11
	ecall
	jr      ra

# Print the string at a0
print:
	mv      a1 a0
	li      a0 4
	ecall
	jr      ra

# -- println --
# Arguments:
# a0: address of the string
# Return: none
# Semantics:
# Writes the string at a0 to the console and appends a newline character
println:
	mv      a1 a0
	li      a0 4
	ecall
	la      a1 newlinestr
	li      a0 4
	ecall
	jr      ra

# -- readbuf --
# Arguments:
# a0: target address
# a1: number of characters
# Return: none
# Semantics:
# Reads a string of at most a1 characters from the console and stores it in the memory area [a0 to a0 + a1 - 1]
readbuf:
	mv      a2 a1
	addi    a2 a2 1
	mv      a1 a0
	li      a0 8
	ecall
	la      a1 newlinestr
	li      a0 4
	ecall
	jr      ra

# -- end --
# Arguments: none
# Return: none
# Semantics: Terminates the program
end:
	li      a0 10
	ecall

# -- error --
# Arguments:
# a0: error message (null-terminated string)
# Return: none
# Semantics: Prints the error message and terminates the program
error:
	mv      a1 a0
	li      a0 4
	ecall
	li      a1 1
	li      a0 17
	ecall
