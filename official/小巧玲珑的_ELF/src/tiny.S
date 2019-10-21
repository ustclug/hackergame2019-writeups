	.file	"tinyELF.c"
	.text
	.section	.rodata
.LC0:
	.string	"please in put flag:"
.LC1:
	.string	"correct"
	.text
	.globl	_start
	.type	_start, @function
_start:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$112, %rsp
	movb	$102, -112(%rbp)
	movb	$110, -111(%rbp)
	movb	$101, -110(%rbp)
	movb	$107, -109(%rbp)
	movb	$-125, -108(%rbp)
	movb	$78, -107(%rbp)
	movb	$109, -106(%rbp)
	movb	$116, -105(%rbp)
	movb	$-123, -104(%rbp)
	movb	$122, -103(%rbp)
	movb	$111, -102(%rbp)
	movb	$87, -101(%rbp)
	movb	$-111, -100(%rbp)
	movb	$115, -99(%rbp)
	movb	$-112, -98(%rbp)
	movb	$79, -97(%rbp)
	movb	$-115, -96(%rbp)
	movb	$127, -95(%rbp)
	movb	$99, -94(%rbp)
	movb	$54, -93(%rbp)
	movb	$108, -92(%rbp)
	movb	$110, -91(%rbp)
	movb	$-121, -90(%rbp)
	movb	$105, -89(%rbp)
	movb	$-93, -88(%rbp)
	movb	$111, -87(%rbp)
	movb	$88, -86(%rbp)
	movb	$115, -85(%rbp)
	movb	$102, -84(%rbp)
	movb	$86, -83(%rbp)
	movb	$-109, -82(%rbp)
	movb	$-97, -81(%rbp)
	movb	$105, -80(%rbp)
	movb	$112, -79(%rbp)
	movb	$56, -78(%rbp)
	movb	$118, -77(%rbp)
	movb	$113, -76(%rbp)
	movb	$120, -75(%rbp)
	movb	$111, -74(%rbp)
	movb	$99, -73(%rbp)
	movb	$-60, -72(%rbp)
	movb	$-126, -71(%rbp)
	movb	$-124, -70(%rbp)
	movb	$-66, -69(%rbp)
	movb	$-69, -68(%rbp)
	movb	$-51, -67(%rbp)
	movl	$19, %ecx
	leaq	.LC0(%rip), %rdx
	movq	$1, %rdi
	movq    %rdx, %rsi
	movq	$19, %rdx
	movq	$1, %rax
	syscall
	leaq	-64(%rbp), %rax
	movq	$46, %rdx
	movq	%rax, %rsi
	movq	$0, %rdi
	movq	$0, %rax
	syscall
	movl	$0, -4(%rbp)
	jmp	.L2
.L3:
	movl	-4(%rbp), %eax
	cltq
	movzbl	-64(%rbp,%rax), %eax
	movl	%eax, %edx
	movl	-4(%rbp), %eax
	addl	%eax, %eax
	addl	%edx, %eax
	movl	%eax, %edx
	movl	-4(%rbp), %eax
	cltq
	movb	%dl, -64(%rbp,%rax)
	movl	-4(%rbp), %eax
	cltq
	movzbl	-64(%rbp,%rax), %eax
	movl	-4(%rbp), %edx
	xorl	%eax, %edx
	movl	-4(%rbp), %eax
	cltq
	movb	%dl, -64(%rbp,%rax)
	movl	-4(%rbp), %eax
	cltq
	movzbl	-64(%rbp,%rax), %eax
	movl	%eax, %edx
	movl	-4(%rbp), %eax
	subl	%eax, %edx
	movl	%edx, %eax
	movl	%eax, %edx
	movl	-4(%rbp), %eax
	cltq
	movb	%dl, -64(%rbp,%rax)
	addl	$1, -4(%rbp)
.L2:
	cmpl	$45, -4(%rbp)
	jle	.L3
	movl	$0, -8(%rbp)
	jmp	.L4
.L6:
	movl	-8(%rbp), %eax
	cltq
	movzbl	-64(%rbp,%rax), %edx
	movl	-8(%rbp), %eax
	cltq
	movzbl	-112(%rbp,%rax), %eax
	cmpb	%al, %dl
	je	.L5
	movq	$0, %rdi
	movq	$60, %rax
	syscall
.L5:
	addl	$1, -8(%rbp)
.L4:
	cmpl	$45, -8(%rbp)
	jle	.L6
	movq	$7, %rdx
	leaq	.LC1(%rip), %rsi
	movq	$1, %rax
	movq	$1, %rdi
	syscall
	movq	$0, %rdi
	movq	$60, %rax
	syscall
	.cfi_def_cfa 7, 8
	.cfi_endproc
.LFE0:
	.size	_start, .-_start
	.ident	"GCC: (Ubuntu 8.3.0-6ubuntu1~18.10.1) 8.3.0"
	.section	.note.GNU-stack,"",@progbits
