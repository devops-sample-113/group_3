
Whiteday0804 D1158429 王定偉

whoami13579 褚翊喨 D1158787

youchen7 陳宗佑 D1158801

weber 馮柏瑋 D1158459

meikung 莊智凱 D1158623

c8763
hello chu
test
c8763
==123456789==
:joy:

`

#include <stdio.h>
#include "NUC100Series.h"
#include "MCU_init.h"
#include "SYS_init.h"
#include "LCD.h"
#include "Scankey.h"

void Buzz(int number)
{
    int i;
    for (i=0; i<number; i++) {
        PB11=0; // PB11 = 0 to turn on Buzzer
        CLK_SysTickDelay(100000);     // Delay 
        PB11=1; // PB11 = 1 to turn off Buzzer    
        CLK_SysTickDelay(100000);     // Delay 
    }
}

unsigned char rect_hor[16] = {
    0xFF,0x81,0x81,0x81,0x81,0x81,0x81,0x81,0x81,0x81,0x81,0x81,0x81,0x81,0x81,0xFF
};

unsigned char rect_ver[16] = {
    0xFF,0x01,0x01,0x01,0x01,0x01,0x01,0xFF,
    0xFF,0x80,0x80,0x80,0x80,0x80,0x80,0xFF,
};

int main(void)
{
    int8_t x = 0,y = 0;
    int8_t keyin = 0;
    int8_t movX = 2, dirX = 0;
    int8_t movY = 2, dirY = 0;
    int flag = 0;

    SYS_Init();
    init_LCD();
    clear_LCD();
    OpenKeyPad();
    GPIO_SetMode(PB, BIT11, GPIO_MODE_OUTPUT);
    
  x = 64; y = 32;
    draw_Bmp16x8(x,y,FG_COLOR,BG_COLOR,rect_hor);
    
    while(keyin==0) keyin=ScanKey(); // wait till key is pressed

    clear_LCD();
    
    while(1) {
        if(flag % 2 == 0){
            draw_Bmp16x8(x,y,FG_COLOR,BG_COLOR,rect_hor);
            CLK_SysTickDelay(100000);
            draw_Bmp16x8(x,y,BG_COLOR,BG_COLOR,rect_hor);
        }else{
            draw_Bmp8x16(x,y,FG_COLOR,BG_COLOR,rect_ver);
            CLK_SysTickDelay(100000);
            draw_Bmp8x16(x,y,BG_COLOR,BG_COLOR,rect_ver);
        }
        
    keyin = ScanKey(); // Scan 3x3 keypad
    switch(keyin){   // input 2,4,5,6,8 to chang (x,y) direction
            case 2: //up
                {
                    dirX=0;  dirY=-1; 
                    break;
                }
            case 4:    //left
                {
                    dirX=-1; dirY=0;  
                    break; 
                }
            case 5: //spin
                {
                    flag++;
                    break; 
                }
            case 6: //right
                {
                    dirX=+1; dirY=0;  
                    break; 
                }
            case 8: //down
                {
                    dirX=0;  dirY=+1; 
                    break; 
                }
            default: break;
        }
        
        x = x + dirX * movX; // increment/decrement X
        y = y + dirY * movY; // increment/decrement Y
        
        if(flag % 2 == 0) // horizontal
        {
            if (x<=0)           {Buzz(1); dirX*=-1; x = 2;} // check X boundary Min
            if (x>=LCD_Xmax-16) {Buzz(1); dirX*=-1; x = LCD_Xmax-16-2;}           // check X boundary Max
            if (y<=0)           {Buzz(1); dirY*=-1; y = 2;} // check Y boundary Min
            if (y>=LCD_Ymax-8)  {Buzz(1); dirY*=-1; y = LCD_Ymax-8-2;}               // check Y boundary Max
        }
        if(flag % 2 == 1) // vertical
        {
            if (x<=0)           {Buzz(1); dirX*=-1; x = 2;} // check X boundary Min
            if (x>=LCD_Xmax-8)  {Buzz(1); dirX*=-1; x = LCD_Xmax-16-2;}           // check X boundary Max
            if (y<=0)           {Buzz(1); dirY*=-1; y = 2;} // check Y boundary Min
            if (y>=LCD_Ymax-16) {Buzz(1); dirY*=-1; y = LCD_Ymax-16-2;}               // check Y boundary Max
        }
    }
}

`

- 阿偉