	.section	__TEXT,__text,regular,pure_instructions
	.macosx_version_min 10, 13
	.globl	_main
	.p2align	4, 0x90
_main:                                  ## @main
	.cfi_startproc
## BB#0:
	pushq	%rbp
Lcfi0:
	.cfi_def_cfa_offset 16
Lcfi1:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Lcfi2:
	.cfi_def_cfa_register %rbp
	subq	$48, %rsp
	movl	$0, -4(%rbp)
	movl	%edi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	cmpl	$1, -8(%rbp)
	jne	LBB0_2
## BB#1:
	movl	$0, -20(%rbp)
	jmp	LBB0_3
LBB0_2:
	movq	-16(%rbp), %rax
	movq	8(%rax), %rdi
	callq	_atoi
	movl	%eax, -20(%rbp)
LBB0_3:
	movl	-20(%rbp), %eax
	testl	%eax, %eax
	movl	%eax, -36(%rbp)         ## 4-byte Spill
	je	LBB0_4
	jmp	LBB0_9
LBB0_9:
	movl	-36(%rbp), %eax         ## 4-byte Reload
	subl	$1, %eax
	movl	%eax, -40(%rbp)         ## 4-byte Spill
	je	LBB0_5
	jmp	LBB0_10
LBB0_10:
	movl	-36(%rbp), %eax         ## 4-byte Reload
	subl	$2, %eax
	movl	%eax, -44(%rbp)         ## 4-byte Spill
	je	LBB0_6
	jmp	LBB0_7
LBB0_4:
	leaq	L_.str(%rip), %rax
	movq	%rax, -32(%rbp)
	jmp	LBB0_8
LBB0_5:
	leaq	L_.str.1(%rip), %rax
	movq	%rax, -32(%rbp)
	jmp	LBB0_8
LBB0_6:
	leaq	L_.str.2(%rip), %rax
	movq	%rax, -32(%rbp)
	jmp	LBB0_8
LBB0_7:
	leaq	L_.str.3(%rip), %rax
	movq	%rax, -32(%rbp)
LBB0_8:
	leaq	L_.str.4(%rip), %rdi
	movl	-20(%rbp), %esi
	movq	-32(%rbp), %rdx
	movb	$0, %al
	callq	_printf
	xorl	%esi, %esi
	movl	%eax, -48(%rbp)         ## 4-byte Spill
	movl	%esi, %eax
	addq	$48, %rsp
	popq	%rbp
	retq
	.cfi_endproc

	.section	__TEXT,__cstring,cstring_literals
L_.str:                                 ## @.str
	.asciz	"zero"

L_.str.1:                               ## @.str.1
	.asciz	"one"

L_.str.2:                               ## @.str.2
	.asciz	"two"

L_.str.3:                               ## @.str.3
	.asciz	"unknow"

L_.str.4:                               ## @.str.4
	.asciz	"%d's string is %s.\n"


.subsections_via_symbols
