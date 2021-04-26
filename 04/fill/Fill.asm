// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


(INIT)

	// Set Default color as white aka 00...00

	@color

	M=0

	// Get the screen address

	@SCREEN

	D=A
	
	// copying that address which is a pointer to the first pixel
 
	@pxl

	M=D

	// check for a keyboard input

	@KBD	

	D=M

	@DRAW

	// if there is none jump to the drawing block

	D;JEQ

	// Otherwise set color as black aka 11...11 = -1 and draw the black block

	@color

	M=-1


(DRAW)

	// Checks the color of the pixel

	@color

	D=M

	// Load the first or next pixel

	@pxl

	A=M

	M=D

	// Increment the next pixel

	@pxl

	M=M+1

	// Check how far the pixel address is from the keyboard 
	// (remember that the screen ends at address 24575 and 
	//		keyboard starts at address 24576 )

	@KBD

	D=A

	@pxl

	D=D-M

	// If it is not done it continues on drawing

	@DRAW

	D;JGT


	// Otherwise it goes back to the initial state

	@INIT

	0;JMP



	