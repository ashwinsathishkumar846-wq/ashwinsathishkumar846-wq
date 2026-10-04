/* Temperature Monitoring System using LPC2148 (ADC0 channel 1, LM35 on P0.28)
   Display : 16x2 LCD (4-bit)  D4-D7 = P1.16-P1.19, RS = P0.10, EN = P0.11
   Outputs : FAN relay = P0.8, BUZZER = P0.7, ALARM LED = P0.9
   Serial  : UART0 9600 baud, 8N1 (P0.0 = TXD0, P0.1 = RXD0)
   Clock   : Fosc = 12 MHz, CCLK = 60 MHz, PCLK = 15 MHz                       */

#include <lpc214x.h>
#include <stdio.h>

#define LCD_DATA     (0x0Fu << 16)          /* P1.16 - P1.19  -> D4 - D7        */
#define LCD_RS       (1u << 10)             /* P0.10                            */
#define LCD_EN       (1u << 11)             /* P0.11                            */
#define BUZZER       (1u << 7)              /* P0.7                             */
#define FAN          (1u << 8)              /* P0.8                             */
#define ALARM_LED    (1u << 9)              /* P0.9                             */

#define TEMP_LIMIT   40.0f                  /* fan ON at or above 40 deg C      */
#define HYSTERESIS    2.0f                  /* fan OFF at or below 38 deg C     */
#define SAMPLES       8                     /* conversions averaged per reading */

/* ---------------- delay ---------------- */
void delay_ms(unsigned int ms)
{
    unsigned int i, j;
    for (i = 0; i < ms; i++)
        for (j = 0; j < 6000; j++);         /* about 1 ms at CCLK = 60 MHz      */
}

/* ---------------- PLL : 12 MHz -> 60 MHz ---------------- */
void pll_init(void)
{
    PLL0CFG = 0x24;                         /* M = 5, P = 2                     */
    PLL0CON = 0x01;  PLL0FEED = 0xAA;  PLL0FEED = 0x55;
    while (!(PLL0STAT & (1 << 10)));        /* wait for PLL lock                */
    PLL0CON = 0x03;  PLL0FEED = 0xAA;  PLL0FEED = 0x55;     /* enable + connect */
    VPBDIV = 0x00;                          /* PCLK = CCLK / 4 = 15 MHz         */
}

/* ---------------- UART0 : 9600 baud ---------------- */
void uart0_init(void)
{
    PINSEL0 |= 0x00000005;                  /* P0.0 = TXD0, P0.1 = RXD0         */
    U0LCR = 0x83;                           /* 8 bits, no parity, 1 stop, DLAB=1*/
    U0DLL = 98;  U0DLM = 0;                 /* 15 MHz / (16 x 9600) = 97.6      */
    U0LCR = 0x03;                           /* DLAB = 0                         */
}

void uart0_puts(const char *s)
{
    while (*s) {
        while (!(U0LSR & 0x20));            /* wait until THR is empty          */
        U0THR = *s++;
    }
}

/* ---------------- 16x2 LCD (4-bit mode) ---------------- */
void lcd_write_nibble(unsigned char n)
{
    IO1CLR = LCD_DATA;
    IO1SET = ((unsigned int)n & 0x0F) << 16;
    IO0SET = LCD_EN;  delay_ms(1);  IO0CLR = LCD_EN;
}

void lcd_cmd(unsigned char c)
{
    IO0CLR = LCD_RS;
    lcd_write_nibble(c >> 4);  lcd_write_nibble(c);
    delay_ms(2);
}

void lcd_data(unsigned char d)
{
    IO0SET = LCD_RS;
    lcd_write_nibble(d >> 4);  lcd_write_nibble(d);
    delay_ms(2);
}

void lcd_puts(const char *s)  { while (*s) lcd_data(*s++); }

void lcd_init(void)
{
    IO0DIR |= LCD_RS | LCD_EN;
    IO1DIR |= LCD_DATA;
    delay_ms(20);
    lcd_cmd(0x02);                          /* 4-bit mode                       */
    lcd_cmd(0x28);                          /* 2 lines, 5x7 font                */
    lcd_cmd(0x0C);                          /* display ON, cursor OFF           */
    lcd_cmd(0x06);                          /* auto increment                   */
    lcd_cmd(0x01);                          /* clear display                    */
}

/* ---------------- ADC0 channel 1 (AD0.1 on P0.28) ---------------- */
void adc_init(void)
{
    PINSEL1 |= (1u << 24);                  /* P0.28 -> AD0.1 (bits 25:24 = 01) */
}

unsigned int adc_read(void)
{
    unsigned int val;
    /* SEL = channel 1, CLKDIV = 3 (15 MHz / 4 = 3.75 MHz), PDN = 1, START = 001 */
    AD0CR = (1u << 1) | (3u << 8) | (1u << 21) | (1u << 24);
    do { val = AD0DR1; } while (!(val & (1u << 31)));      /* wait for DONE bit */
    AD0CR &= ~(7u << 24);                   /* stop conversion                  */
    return (val >> 6) & 0x3FF;              /* 10-bit result in bits 15:6       */
}

unsigned int adc_average(void)
{
    unsigned int i, sum = 0;
    for (i = 0; i < SAMPLES; i++)  sum += adc_read();
    return sum / SAMPLES;
}

/* ---------------- main ---------------- */
int main(void)
{
    unsigned int adc;
    float temp;
    char line[32];
    unsigned char fan_on = 0;

    pll_init();
    IO0DIR |= BUZZER | FAN | ALARM_LED;
    IO0CLR  = BUZZER | FAN | ALARM_LED;
    uart0_init();
    lcd_init();
    adc_init();

    lcd_puts("LPC2148 TEMP MON");
    uart0_puts("\r\nLPC2148 Temperature Monitoring System\r\n");
    delay_ms(1500);

    while (1)
    {
        adc  = adc_average();
        temp = (adc * 330.0f) / 1023.0f;    /* 3.3 V x 100 deg C per volt       */

        if (temp >= TEMP_LIMIT)                 fan_on = 1;
        else if (temp <= TEMP_LIMIT - HYSTERESIS) fan_on = 0;

        if (fan_on)  IO0SET = FAN | BUZZER | ALARM_LED;
        else         IO0CLR = FAN | BUZZER | ALARM_LED;

        lcd_cmd(0x80);                      /* line 1                           */
        sprintf(line, "Temp: %4.1f %cC   ", temp, 0xDF);
        lcd_puts(line);
        lcd_cmd(0xC0);                      /* line 2                           */
        if (fan_on) lcd_puts("ALERT! FAN ON   ");
        else { sprintf(line, "ADC:%03X FAN:OFF ", adc);  lcd_puts(line); }

        sprintf(line, "Temp: %4.1f C | ADC: 0x%03X | FAN %s\r\n", temp, adc, fan_on ? "ON" : "OFF");
        uart0_puts(line);

        delay_ms(500);
    }
}
