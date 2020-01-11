.MODEL	TINY
;8259宏定义
I08259_0	EQU	0250H
I08259_1	EQU	0251H
;8255宏定义
COM_8255	EQU	0273H
PA_ADD	EQU	0270H
PB_ADD	EQU	0271H
PC_ADD  EQU     0272H
;8253宏定义
COM_ADDR EQU    0263H
T0_ADDR EQU     0260H
T1_ADDR EQU     0261H
	.STACK	100
	.DATA
;led灯的查询表
LED_DATA	DB	11111111B
		DB	01111111B
		DB	00111111B
		DB	00011111B
		DB	00001111B
		DB	00000111B
		DB	00000011B
Counter	DB	?	;用于计数
Counter_1	DB ?
ReDisplayFlag	DB	0	;标志位，用来判定是否产生中断
	.CODE
START:	MOV	AX,@DATA	;初始化
	MOV	DS,AX
	MOV	ES,AX
	NOP
	CALL	Init8259
	CALL	Init8255
	CALL	WriIntver
	MOV	Counter,0
	MOV Counter_1,0
	STI
START1:		nop				;执行过程
	CMP		ReDisplayFlag,0	;若有中断产生，则标志位会置为1，则不会跳转到START1，继续执行下列步骤
	JZ		START1
	CALL	DLY5S			;5s延时，程序实现，有5s的时间拨动开关，Counter会记录拨动次数
	MOV		ReDisplayFlag,0
	mov		al,Counter
	mov		Counter_1,al
	MOV		Counter,0
	CALL	LED				;led显示，若Counter大于等于6，则闪烁，否则进行查表显示，并执行后续步骤
	CALL	DLY_WT			;根据奇数和偶数延迟1秒或2秒
	CALL	MOVEMENT		;Counter小于6时，则会进入此步骤，进而进行灯的移动
	
	JMP		START1
Init8255	PROC	NEAR	;8255初始化程序
	MOV		AX,@DATA
	NOP
	MOV		DX,COM_8255
	MOV		AL,81H
	OUT		DX,AL		;A口输出控制字81H=10000001
	MOV		DX,PA_ADD
	MOV		AL,0FFH
	OUT		DX,AL		;通过A端口让灯全灭
	MOV		DX,PC_ADD
	MOV		AL,00H
	OUT		DX,AL		;把C端口全部置成低电平
	RET
Init8255	ENDP
Init8259	PROC	NEAR	;8259初始化
	MOV	DX,I08259_0
	MOV	AL,13H		;设置icw1，边沿触发
	OUT	DX,AL
	MOV	DX,I08259_1
	MOV	AL,08H		;设置icw2
	OUT	DX,AL
	MOV	AL,19H		;设置icw4，特殊全嵌套，非自动结束
	OUT	DX,AL
	MOV	AL,0FBH		;设置ocw1，IR2中断，所以要把IR2的中断打开，FB=11111011，0表示打开
	OUT	DX,AL
	RET
Init8259	ENDP
WriIntver	PROC	NEAR	;写中断
	PUSH	ES
	MOV		AX,0
	MOV		ES,AX
	MOV		DI,28H		;根据icw2得来的，08H-0FH分别对应，IR0-IR7号中断，IR2，0AH=00001010,左移两位得到，00101000=28H
	LEA		AX,INT_0
	STOSW
	MOV		AX,CS
	STOSW
	POP		ES
	RET
WriIntver	ENDP
LED	PROC	NEAR
	PUSH	DX
	PUSH	AX
	PUSH	BX
	PUSH	CX
	MOV		DX,PA_ADD
	MOV		AL,0FFH
	OUT		DX,AL
	MOV		CX,6		;闪六次
	MOV		AL,Counter_1
	CMP		AL,6		;判断次数大于等于6还是小于6
	JA		FLASH
	LEA		BX,LED_DATA
	XLAT
	OUT		DX,AL
	JMP		LAST
FLASH: MOV	AL,00000000B
	OUT		DX,AL
	CALL	DLY500MS
	MOV		AL,11111111B
	OUT		DX,AL
	CALL	DLY500MS		;闪烁没要求要用硬件延时，这里用的是软件延时，也可改成call delay
	LOOP	FLASH
	JMP		START;次数大于6闪烁完之后全部重置
LAST:	NOP
	POP	CX
	POP	BX
	POP	AX
	POP	DX
	ret
LED	ENDP
DLY500MS	PROC	NEAR		;500ms延时子程序（软件实现）
	PUSH	CX
	MOV		CX,60000
DL500MS1:	LOOP	DL500MS1
	POP	CX
	RET
DLY500MS	ENDP
DLY5S	PROC	NEAR		;5s延时子程序（软件实现）
	PUSH	CX
	MOV		CX,10
DLY5S1:	CALL	DLY500MS
	LOOP	DLY5S1
	POP		CX
	RET
DLY5S	ENDP

DELAY	PROC	NEAR		;1s延时子程序（硬件实现）
	PUSH	DX
	PUSH	AX
	MOV		DX,COM_ADDR
	MOV		AL,31H
	OUT		DX,AL		;计数器T0设置在模式0，BCD编码
	MOV		DX,T0_ADDR
	MOV		AL,53H
	OUT		DX,AL
	MOV		AL,19H
	OUT		DX,AL		;给计数器0写入初值1953，CLK0-1953HZ，记一个数需要1/1953s时间，则计1953个数需要1s时间
	XOR		AL,AL
	MOV		DX,PC_ADD	;开始初始化8255的子程序中已经把C口全部写为低电平，8253定时器的out0端口是接在8255的pc0上的
LP:	IN		AL,DX		;在给计数器0写初值时会使out0变为低电平，计数过程中也一直都是低电平，只有在计数结束了，out0才会变为高电平
	AND		AL,01H		;在这里读取C口最后一位，看是否为高电平，若为高电平则说明计数结束也就是过了1s
	JZ		LP
	POP		AX
	POP		DX
	RET
DELAY	ENDP

DLY_WT PROC NEAR
	MOV		AL,Counter_1
    AND		AL,01H
    JZ		EVEN11
	call 	DELAY
	jmp 	DONE
EVEN11:
	call DELAY
	call DELAY
DONE:
	ret
DLY_WT ENDP

MOVEMENT PROC  NEAR		;次数小于6时会进入此子程序
	 PUSH	DX
	 PUSH	AX
	 PUSH	BX
	 PUSH	CX
	 MOV	DX,PA_ADD
     MOV	AL,Counter_1
     AND	AL,01H;判断奇偶
     JZ		EVEN1
     MOV	AL,Counter_1
     LEA	BX,LED_DATA
     XLAT
ODD: 
	MOV 	AH,ReDisplayFlag
	CMP		AH,1
	JE		SHTDOWN
	ROR		AL,1;奇
	OUT		DX,AL
	CALL	DELAY
    TEST	AL,01H
    JZ		SHTDOWN
    JMP		ODD
EVEN1:   MOV	AL,Counter_1;偶
	 LEA	BX,LED_DATA
	 XLAT
	 XOR	CX,CX
	 MOV	CL,2
EVEN3:
	mov 	ah,ReDisplayFlag
	cmp		ah,1
	JE		SHTDOWN	
	ROR	AL,CL
	OUT	DX,AL
	CALL	DELAY
	CALL	DELAY
	TEST	AL,01H
	JZ	SHTDOWN
	JMP	EVEN3
SHTDOWN:     MOV	DX,PA_ADD;熄灭
	MOV	AL,0FFH
    OUT	DX,AL
    POP	CX
    POP	BX
    POP	AX
    POP	DX
    RET
MOVEMENT ENDP

INT_0:	PUSH	DX		;中断服务程序，只要拨动了开关，就进入到此程序
	PUSH	AX
	MOV		AL,Counter
	ADD		AL,1
	MOV		Counter,AL
	MOV		ReDisplayFlag,1
	MOV		DX,I08259_0;写入ocw2，普通eoi结束方式，允许同级中断进入
	MOV		AL,20H
	OUT		DX,AL
	POP		AX
	POP		DX
	IRET
	END		START

